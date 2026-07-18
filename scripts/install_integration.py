#!/usr/bin/env python3
"""Install a self-contained game-interview instruction file into a project."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
INTEGRATIONS = {
    "cursor": (
        "integrations/cursor/game-builder-interview.mdc",
        ".cursor/rules/game-builder-interview.mdc",
    ),
    "copilot": (
        "integrations/copilot/copilot-instructions.md",
        ".github/copilot-instructions.md",
    ),
    "gemini": ("integrations/gemini/GEMINI.md", "GEMINI.md"),
    "claude": ("integrations/claude/CLAUDE.md", "CLAUDE.md"),
    "agents": ("integrations/agents/AGENTS.md", "AGENTS.md"),
}
PREVIEW_HELPER = ("scripts/preview_game.py", ".game-builder/preview_game.py")


def destination_for(tool: str, target: Path) -> Path:
    """Return the target-project location for a supported tool."""
    try:
        _, destination = INTEGRATIONS[tool]
    except KeyError as exc:
        raise ValueError(f"unsupported tool: {tool}") from exc
    return target / destination


def install(tool: str, target: Path) -> Path:
    """Copy the adapter and preview helper without replacing user files."""
    try:
        source_relative, _ = INTEGRATIONS[tool]
    except KeyError as exc:
        raise ValueError(f"unsupported tool: {tool}") from exc

    if not target.is_dir():
        raise ValueError(f"target project directory does not exist: {target}")

    destination = destination_for(tool, target)
    helper_destination = target / PREVIEW_HELPER[1]
    existing_files = [
        path
        for path in (destination, helper_destination)
        if path.exists() or path.is_symlink()
    ]
    if existing_files:
        raise FileExistsError(
            f"refusing to overwrite existing file: {existing_files[0]}"
        )

    source = REPOSITORY_ROOT / source_relative
    helper_source = REPOSITORY_ROOT / PREVIEW_HELPER[0]
    destination.parent.mkdir(parents=True, exist_ok=True)
    helper_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    shutil.copyfile(helper_source, helper_destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the youth game-builder interview rule into a project."
    )
    parser.add_argument("--tool", choices=sorted(INTEGRATIONS))
    parser.add_argument("--target", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        destination = install(arguments.tool, arguments.target)
    except (FileExistsError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Installed {arguments.tool} interview rule at {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
