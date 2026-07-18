import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_PATHS = {
    "cursor": "integrations/cursor/game-builder-interview.mdc",
    "copilot": "integrations/copilot/copilot-instructions.md",
    "gemini": "integrations/gemini/GEMINI.md",
    "claude": "integrations/claude/CLAUDE.md",
    "agents": "integrations/agents/AGENTS.md",
}


def load_installer():
    path = ROOT / "scripts/install_integration.py"
    spec = importlib.util.spec_from_file_location("install_integration", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_preview_server():
    path = ROOT / "scripts/preview_game.py"
    spec = importlib.util.spec_from_file_location("preview_game", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PlatformIntegrationTests(unittest.TestCase):
    def test_every_adapter_requires_one_chinese_design_question(self) -> None:
        for relative_path in ADAPTER_PATHS.values():
            text = (ROOT / relative_path).read_text(encoding="utf-8")
            for phrase in (
                "我想创作一个游戏",
                "中文",
                "恰好一个",
                "设计问题",
                "不得直接生成代码",
                "18–22",
                "停止",
            ):
                self.assertIn(phrase, text, relative_path)

    def test_cursor_adapter_is_always_loaded_but_conditional(self) -> None:
        text = (ROOT / ADAPTER_PATHS["cursor"]).read_text(encoding="utf-8")
        self.assertIn("alwaysApply: true", text)
        self.assertIn("仅当", text)

    def test_installer_writes_self_contained_adapter_at_tool_location(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            destination = installer.install("cursor", target)
            self.assertEqual(
                destination,
                target / ".cursor/rules/game-builder-interview.mdc",
            )
            self.assertTrue(destination.is_file())
            self.assertIn("恰好一个", destination.read_text(encoding="utf-8"))
            helper = target / ".game-builder/preview_game.py"
            self.assertTrue(helper.is_file())
            self.assertIn("Port conflict detected", helper.read_text(encoding="utf-8"))

    def test_installer_never_overwrites_existing_instruction_file(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            destination = target / ".github/copilot-instructions.md"
            destination.parent.mkdir()
            destination.write_text("用户已有规则", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                installer.install("copilot", target)
            self.assertEqual(destination.read_text(encoding="utf-8"), "用户已有规则")

    def test_installer_never_overwrites_existing_preview_helper(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            helper = target / ".game-builder/preview_game.py"
            helper.parent.mkdir()
            helper.write_text("用户已有预览脚本", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                installer.install("cursor", target)
            self.assertEqual(helper.read_text(encoding="utf-8"), "用户已有预览脚本")

    def test_installer_rejects_a_dangling_instruction_symlink(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary_directory:
            target = Path(temporary_directory)
            destination = target / ".cursor/rules/game-builder-interview.mdc"
            destination.parent.mkdir(parents=True)
            destination.symlink_to(target / "missing-user-rule.mdc")
            with self.assertRaises(FileExistsError):
                installer.install("cursor", target)
            self.assertTrue(destination.is_symlink())

    def test_installer_rejects_unknown_tool(self) -> None:
        installer = load_installer()
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaises(ValueError):
                installer.install("unknown", Path(temporary_directory))

    def test_preview_server_skips_a_busy_port(self) -> None:
        import socket

        preview = load_preview_server()
        with tempfile.TemporaryDirectory() as temporary_directory:
            project = Path(temporary_directory)
            (project / "index.html").write_text("<!doctype html>", encoding="utf-8")
            occupied = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            occupied.bind(("127.0.0.1", 0))
            busy_port = occupied.getsockname()[1]
            occupied.listen()
            try:
                server, skipped_ports = preview.start_preview_server(
                    project,
                    preferred_ports=(busy_port,),
                )
                try:
                    self.assertIn(busy_port, skipped_ports)
                    self.assertNotEqual(server.server_port, busy_port)
                finally:
                    server.server_close()
            finally:
                occupied.close()

    def test_preview_server_requires_a_game_entry_point(self) -> None:
        preview = load_preview_server()
        with tempfile.TemporaryDirectory() as temporary_directory:
            with self.assertRaises(FileNotFoundError):
                preview.start_preview_server(Path(temporary_directory))

    def test_preview_opens_the_default_browser(self) -> None:
        preview = load_preview_server()
        with patch.object(preview.webbrowser, "open", return_value=True) as open_browser:
            self.assertTrue(preview.open_default_browser("http://127.0.0.1:5173/"))
        open_browser.assert_called_once_with(
            "http://127.0.0.1:5173/",
            new=2,
            autoraise=True,
        )
