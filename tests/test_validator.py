from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_skill.py"
SPEC = spec_from_file_location("validate_skill", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validate_skill = module_from_spec(SPEC)
SPEC.loader.exec_module(validate_skill)


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
    def test_missing_repository_files_are_reported(self) -> None:
        with TemporaryDirectory() as temp_dir:
            errors = validate_skill.validate_repository(Path(temp_dir))
        self.assertIn("missing required file: SKILL.md", errors)
        self.assertIn("missing required file: README.md", errors)
        self.assertIn(
            "missing required file: references/interview-protocol.md",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
