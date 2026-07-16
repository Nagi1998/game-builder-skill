from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class CoreSkillContractTests(unittest.TestCase):
    def test_core_files_exist(self) -> None:
        self.assertTrue((ROOT / "SKILL.md").is_file())
        self.assertTrue((ROOT / "references/interview-protocol.md").is_file())

    def test_core_state_and_gates_are_explicit(self) -> None:
        text = read("SKILL.md")
        self.assertIn("valid_rounds >= 20", text)
        self.assertIn("gdd_approved", text)
        self.assertIn("一次只问一个主要问题", text)
        self.assertRegex(text, r"此前回答|之前回答")
        self.assertIn("references/interview-protocol.md", text)
        self.assertIn("references/gdd-template.md", text)
        self.assertIn("references/web-game-development.md", text)

    def test_interview_protocol_defines_effective_rounds_and_linkage(self) -> None:
        text = read("references/interview-protocol.md")
        for phrase in ("有效轮次", "连接点", "设计影响", "单一问题", "脚手架"):
            self.assertIn(phrase, text)
        self.assertRegex(text, r"嗯.*不知道.*随便.*继续")
        self.assertIn("不计", text)
        self.assertIn("每 5 轮", text)

    def test_child_privacy_boundary_is_present(self) -> None:
        combined = read("SKILL.md") + read("references/interview-protocol.md")
        for phrase in ("真实姓名", "学校", "联系方式", "精确位置"):
            self.assertIn(phrase, combined)

    def test_child_content_safety_rule_is_operational(self) -> None:
        for relative_path in ("SKILL.md", "references/interview-protocol.md"):
            text = read(relative_path)
            for phrase in (
                "现实危险",
                "自残",
                "仇恨",
                "性内容",
                "赌博",
                "真钱",
                "战利品箱",
                "暗黑模式",
                "剥削性变现",
                "虚构",
                "非血腥",
                "非性化",
                "不歧视",
                "一个安全替代方案",
                "一个关联设计问题",
                "可信任的成年人",
                "当地急救服务",
            ):
                self.assertIn(phrase, text)

    def test_learner_facing_language_is_always_child_friendly_chinese(self) -> None:
        for relative_path in ("SKILL.md", "references/interview-protocol.md"):
            text = read(relative_path)
            self.assertIn(
                "所有面向学生的对话始终使用适合小学、初中生理解的中文",
                text,
            )
            self.assertIn("年龄段适配只调整中文表达的复杂度", text)

    def test_first_design_question_linkage_depends_on_ledger_content(self) -> None:
        for relative_path in ("SKILL.md", "references/interview-protocol.md"):
            text = read(relative_path)
            for phrase in (
                "账本已有任何学习者提供的设计信息",
                "第一个以及之后的每个设计问题",
                "账本没有设计信息",
                "初始创意愿景",
                "年龄段和解释偏好",
                "不会消耗或抹去触发消息中的设计信息",
            ):
                self.assertIn(phrase, text)

    def test_recap_confirmation_only_reply_does_not_count(self) -> None:
        text = read("references/interview-protocol.md")
        self.assertIn("A confirmation-only reply does not count.", text)
        self.assertNotIn("A correction-only reply does not count.", text)


class GDDContractTests(unittest.TestCase):
    def test_gdd_reference_exists(self) -> None:
        self.assertTrue((ROOT / "references/gdd-template.md").is_file())

    def test_gdd_template_has_all_numbered_sections(self) -> None:
        text = read("references/gdd-template.md")
        for number in range(1, 16):
            self.assertRegex(text, rf"(?m)^{number}\.\s")
        self.assertIn("15. 决策来源摘要", text)

    def test_gdd_gate_requires_rounds_coverage_conflicts_and_approval(self) -> None:
        text = read("references/gdd-template.md")
        for phrase in (
            "valid_rounds >= 20",
            "六个覆盖主题",
            "冲突",
            "明确批准",
            "gdd_approved",
        ):
            self.assertIn(phrase, text)

    def test_gdd_keeps_child_content_safety_boundaries(self) -> None:
        text = read("references/gdd-template.md")
        for phrase in (
            "现实危险",
            "自残",
            "仇恨",
            "性内容",
            "赌博",
            "战利品箱",
            "暗黑模式",
            "剥削性变现",
            "虚构",
            "非血腥",
            "非性化",
            "不歧视",
            "不使用真钱",
        ):
            self.assertIn(phrase, text)


class DevelopmentContractTests(unittest.TestCase):
    def test_development_reference_exists(self) -> None:
        self.assertTrue(
            (ROOT / "references/web-game-development.md").is_file()
        )

    def test_development_reference_has_required_deliverables(self) -> None:
        text = read("references/web-game-development.md")
        for phrase in (
            "game/README.md",
            "game/PLAYTEST.md",
            "键盘",
            "触控",
            "控制台错误",
            "验收标准",
        ):
            self.assertIn(phrase, text)

    def test_development_starts_only_from_approved_gdd(self) -> None:
        text = read("references/web-game-development.md")
        self.assertIn("gdd_approved: true", text)
        self.assertIn("HTML", text)
        self.assertRegex(text, r"Phaser|原生")

    def test_development_keeps_child_content_safety_boundaries(self) -> None:
        text = read("references/web-game-development.md")
        for phrase in (
            "现实危险",
            "自残",
            "仇恨",
            "性内容",
            "赌博",
            "战利品箱",
            "暗黑模式",
            "剥削性变现",
            "虚构",
            "非血腥",
            "非性化",
            "不歧视",
            "不使用真钱",
        ):
            self.assertIn(phrase, text)


class RepositoryCompletenessTests(unittest.TestCase):
    def test_readme_and_trigger_evals_exist(self) -> None:
        self.assertTrue((ROOT / "README.md").is_file())
        self.assertTrue((ROOT / "evals/trigger-evals.json").is_file())

    def test_trigger_eval_set_is_balanced(self) -> None:
        import json

        items = json.loads(read("evals/trigger-evals.json"))
        self.assertEqual(len(items), 20)
        self.assertEqual(sum(item["should_trigger"] for item in items), 10)
        self.assertEqual(sum(not item["should_trigger"] for item in items), 10)

    def test_readme_documents_the_exact_trigger_and_gates(self) -> None:
        text = read("README.md")
        for phrase in (
            "我想创作一个游戏",
            "不少于 20 轮",
            "GDD",
            "明确批准",
            "python3 scripts/validate_skill.py .",
        ):
            self.assertIn(phrase, text)

    def test_readme_summarizes_child_content_safety(self) -> None:
        text = read("README.md")
        for phrase in (
            "现实危险",
            "自残",
            "仇恨",
            "性内容",
            "赌博",
            "战利品箱",
            "暗黑模式",
            "剥削性变现",
            "虚构",
            "非血腥",
            "非性化",
            "不歧视",
            "不使用真钱",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
