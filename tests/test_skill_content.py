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

    def test_learner_facing_language_is_always_child_friendly_chinese(self) -> None:
        for relative_path in ("SKILL.md", "references/interview-protocol.md"):
            text = read(relative_path)
            self.assertIn(
                "所有面向学生的对话始终使用适合小学、初中生理解的中文",
                text,
            )
            self.assertIn("年龄段适配只调整中文表达的复杂度", text)

    def test_linkage_starts_after_the_first_design_question(self) -> None:
        text = read("SKILL.md")
        self.assertIn("第一个设计问题后的每一问", text)
        self.assertNotIn("第一个问题后的每一问", text)


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


if __name__ == "__main__":
    unittest.main()
