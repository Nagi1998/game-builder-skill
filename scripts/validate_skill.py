#!/usr/bin/env python3
"""Validate the youth-game-builder Skill repository."""

from pathlib import Path
import re
import sys


REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "references/interview-protocol.md",
    "references/gdd-template.md",
    "references/web-game-development.md",
    "evals/evals.json",
    "evals/trigger-evals.json",
)

CONTENT_CONTRACTS = {
    "SKILL.md": (
        (r"valid_rounds\s*>=\s*20", "missing 20-round GDD gate"),
        (r"gdd_approved", "missing explicit GDD approval state"),
        (r"一次只问一个主要问题", "missing one-question rule"),
        (r"此前回答|之前回答", "missing prior-answer linkage"),
        (r"真实姓名|学校", "missing child privacy boundary"),
    ),
    "references/interview-protocol.md": (
        (r"有效轮", "missing valid-round definition"),
        (r"连接点", "missing linked-question recipe"),
        (r"不知道", "missing learner uncertainty recovery"),
    ),
    "references/gdd-template.md": (
        (r"15\.\s*决策来源摘要", "missing decision traceability section"),
        (r"明确批准", "missing version approval rule"),
    ),
    "references/web-game-development.md": (
        (r"HTML", "missing default web technology"),
        (r"键盘", "missing keyboard accessibility"),
        (r"控制台错误", "missing browser error check"),
        (r"PLAYTEST\.md", "missing playtest deliverable"),
    ),
}


def parse_frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must start with YAML frontmatter")

    result: dict[str, str] = {}
    for raw_line in match.group("body").splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")
        key, value = raw_line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def validate_repository(root: Path) -> list[str]:
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = skill_path.read_text(encoding="utf-8")
        try:
            metadata = parse_frontmatter(skill_text)
        except ValueError as exc:
            errors.append(str(exc))
        else:
            if metadata.get("name") != "youth-game-builder":
                errors.append("frontmatter name must be youth-game-builder")
            if not re.fullmatch(r"[a-z0-9-]+", metadata.get("name", "")):
                errors.append("frontmatter name must use lowercase letters, numbers, and hyphens")
            description = metadata.get("description", "")
            if not description.startswith("Use when"):
                errors.append("frontmatter description must start with 'Use when'")
            if not re.search(r"我想创作一个游戏|创作.*游戏|设计.*游戏|web game", description, re.I):
                errors.append("frontmatter description must cover the game-creation trigger")
        if len(skill_text.splitlines()) >= 500:
            errors.append("SKILL.md must remain under 500 lines")

    for relative_path, contracts in CONTENT_CONTRACTS.items():
        path = root / relative_path
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern, message in contracts:
            if not re.search(pattern, text, re.I | re.MULTILINE):
                errors.append(f"{relative_path}: {message}")

    return errors


def main(argv: list[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()
    errors = validate_repository(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
