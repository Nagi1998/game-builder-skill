from contextlib import contextmanager
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_skill.py"
SPEC = spec_from_file_location("validate_skill", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validate_skill = module_from_spec(SPEC)
SPEC.loader.exec_module(validate_skill)


@contextmanager
def repository_copy():
    with TemporaryDirectory() as temp_dir:
        destination = Path(temp_dir) / "repository"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__"),
        )
        yield destination


class ValidatorInterfaceTests(unittest.TestCase):
    def test_required_interfaces_exist(self) -> None:
        self.assertTrue(hasattr(validate_skill, "parse_frontmatter"))
        self.assertTrue(hasattr(validate_skill, "validate_repository"))


class FrontmatterTests(unittest.TestCase):
    def test_parse_frontmatter_returns_simple_fields(self) -> None:
        text = (
            "---\n"
            "name: youth-game-builder\n"
            "description: Use when a learner wants to create a game\n"
            "---\n\n"
            "# Heading\n"
        )
        self.assertEqual(
            validate_skill.parse_frontmatter(text),
            {
                "name": "youth-game-builder",
                "description": "Use when a learner wants to create a game",
            },
        )

    def test_parse_frontmatter_rejects_missing_fence(self) -> None:
        with self.assertRaises(ValueError):
            validate_skill.parse_frontmatter("# No frontmatter")


class RepositoryValidationTests(unittest.TestCase):
    def assert_error_contains(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(
            any(fragment in error for error in errors),
            f"expected an error containing {fragment!r}, got {errors!r}",
        )

    def replace_once(
        self,
        repository: Path,
        relative_path: str,
        old: str,
        new: str,
    ) -> None:
        path = repository / relative_path
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def test_missing_repository_files_are_reported(self) -> None:
        with TemporaryDirectory() as temp_dir:
            errors = validate_skill.validate_repository(Path(temp_dir))
        self.assertIn("missing required file: SKILL.md", errors)
        self.assertIn("missing required file: README.md", errors)
        self.assertIn(
            "missing required file: references/interview-protocol.md",
            errors,
        )

    def test_invalid_trigger_json_is_reported(self) -> None:
        with repository_copy() as repository:
            (repository / "evals/trigger-evals.json").write_text(
                "{not valid json",
                encoding="utf-8",
            )
            errors = validate_skill.validate_repository(repository)

        self.assert_error_contains(
            errors,
            "evals/trigger-evals.json: invalid JSON",
        )

    def test_unbalanced_trigger_json_is_reported(self) -> None:
        with repository_copy() as repository:
            path = repository / "evals/trigger-evals.json"
            items = json.loads(path.read_text(encoding="utf-8"))
            items[0]["should_trigger"] = False
            path.write_text(
                json.dumps(items, ensure_ascii=False),
                encoding="utf-8",
            )
            errors = validate_skill.validate_repository(repository)

        self.assert_error_contains(
            errors,
            "trigger evals must contain exactly 10 true and 10 false",
        )

    def test_removed_gdd_round_gate_is_reported(self) -> None:
        with repository_copy() as repository:
            self.replace_once(
                repository,
                "references/gdd-template.md",
                "`valid_rounds >= 20`",
                "`valid_rounds recorded`",
            )
            errors = validate_skill.validate_repository(repository)

        self.assert_error_contains(
            errors,
            "references/gdd-template.md: missing 20-round generation gate",
        )

    def test_removed_gdd_coverage_or_conflict_gate_is_reported(self) -> None:
        mutations = (
            (
                "六个覆盖主题均为 `complete`",
                "覆盖主题已经记录",
                "missing six-coverage generation gate",
            ),
            (
                "所有影响核心玩法或实现范围的冲突均已解决",
                "设计已经过一致性检查",
                "missing resolved-conflicts generation gate",
            ),
        )
        for old, new, expected_error in mutations:
            with self.subTest(expected_error=expected_error):
                with repository_copy() as repository:
                    self.replace_once(
                        repository,
                        "references/gdd-template.md",
                        old,
                        new,
                    )
                    errors = validate_skill.validate_repository(repository)

                self.assert_error_contains(errors, expected_error)

    def test_removed_development_approval_state_is_reported(self) -> None:
        with repository_copy() as repository:
            self.replace_once(
                repository,
                "references/web-game-development.md",
                "`gdd_approved: true`",
                "`gdd_approved`",
            )
            errors = validate_skill.validate_repository(repository)

        self.assert_error_contains(
            errors,
            "references/web-game-development.md: missing gdd_approved: true entry gate",
        )

    def test_removed_approved_version_input_is_reported(self) -> None:
        with repository_copy() as repository:
            self.replace_once(
                repository,
                "references/web-game-development.md",
                "输入是点名的已批准 `gdd_version`，页眉状态为 `已批准`",
                "输入包含一个 GDD 版本",
            )
            errors = validate_skill.validate_repository(repository)

        self.assert_error_contains(
            errors,
            "references/web-game-development.md: missing approved GDD version input",
        )

    def test_malformed_eval_expectations_are_reported(self) -> None:
        with repository_copy() as repository:
            path = repository / "evals/evals.json"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["evals"][0]["expectations"] = [""]
            path.write_text(
                json.dumps(payload, ensure_ascii=False),
                encoding="utf-8",
            )
            errors = validate_skill.validate_repository(repository)

        self.assert_error_contains(
            errors,
            "evals/evals.json: item 1 expectations must be a non-empty list of non-empty strings",
        )


if __name__ == "__main__":
    unittest.main()
