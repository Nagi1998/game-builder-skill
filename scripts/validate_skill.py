#!/usr/bin/env python3
"""Validate the youth-game-builder Skill repository."""

import json
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
        (r"我想创作一个游戏", "missing exact game-creation trigger phrase"),
        (r"valid_rounds\s*>=\s*20", "missing 20-round GDD gate"),
        (r"gdd_approved:\s*true", "missing explicit GDD approval gate"),
        (r"一次只问一个主要问题", "missing one-question rule"),
        (
            r"账本已有任何学习者提供的设计信息[\s\S]*第一个以及之后的每个设计问题",
            "missing linkage when the ledger already has design information",
        ),
        (
            r"账本没有设计信息[\s\S]*第一个设计问题[\s\S]*初始创意愿景",
            "missing no-design-information first-question exception",
        ),
        (
            r"年龄段和解释偏好[\s\S]*不会消耗或抹去触发消息中的设计信息",
            "missing setup/design-information preservation rule",
        ),
        (
            r"现实危险[\s\S]*自残[\s\S]*仇恨[\s\S]*性内容[\s\S]*赌博[\s\S]*真钱[\s\S]*战利品箱[\s\S]*暗黑模式[\s\S]*剥削性变现",
            "missing child-content safety boundary",
        ),
        (
            r"虚构[\s\S]*非血腥[\s\S]*非性化[\s\S]*不歧视[\s\S]*不使用真钱",
            "missing safe creative transformation",
        ),
        (
            r"伤害自己或他人[\s\S]*可信任的成年人[\s\S]*当地急救服务",
            "missing immediate-harm response",
        ),
        (r"真实姓名|学校", "missing child privacy boundary"),
    ),
    "references/interview-protocol.md": (
        (r"有效轮", "missing valid-round definition"),
        (r"连接点", "missing linked-question recipe"),
        (r"不知道", "missing learner uncertainty recovery"),
        (
            r"账本已有任何学习者提供的设计信息[\s\S]*第一个以及之后的每个设计问题",
            "missing conditional first-question linkage rule",
        ),
        (
            r"现实危险[\s\S]*自残[\s\S]*可信任的成年人[\s\S]*当地急救服务",
            "missing child-content safety response",
        ),
    ),
    "references/gdd-template.md": (
        (
            r"valid_rounds\s*>=\s*20",
            "missing 20-round generation gate",
        ),
        (
            r"六个覆盖主题均为\s*`complete`",
            "missing six-coverage generation gate",
        ),
        (
            r"所有影响核心玩法或实现范围的冲突均已解决",
            "missing resolved-conflicts generation gate",
        ),
        (r"15\.\s*决策来源摘要", "missing decision traceability section"),
        (
            r"只有学生明确批准当前完整版本",
            "missing explicit current-version approval gate",
        ),
        (r"gdd_approved:\s*true", "missing approved GDD state"),
        (
            r"现实危险[\s\S]*自残[\s\S]*仇恨[\s\S]*性内容[\s\S]*赌博[\s\S]*真钱[\s\S]*战利品箱[\s\S]*暗黑模式[\s\S]*剥削性变现",
            "missing child-content safety boundary",
        ),
    ),
    "references/web-game-development.md": (
        (r"HTML", "missing default web technology"),
        (
            r"gdd_approved:\s*true",
            "missing gdd_approved: true entry gate",
        ),
        (
            r"输入是点名的已批准\s*`gdd_version`，页眉状态为\s*`已批准`",
            "missing approved GDD version input",
        ),
        (
            r"先写对应的自动化验收测试[\s\S]*预期失败",
            "missing test-first development loop",
        ),
        (
            r"桌面视口[\s\S]{0,120}手机视口",
            "missing desktop/mobile browser verification",
        ),
        (r"键盘", "missing keyboard accessibility"),
        (r"控制台错误", "missing browser error check"),
        (r"game/README\.md", "missing game README deliverable"),
        (r"game/tests/", "missing automated tests deliverable"),
        (r"PLAYTEST\.md", "missing playtest deliverable"),
        (
            r"现实危险[\s\S]*自残[\s\S]*仇恨[\s\S]*性内容[\s\S]*赌博[\s\S]*真钱[\s\S]*战利品箱[\s\S]*暗黑模式[\s\S]*剥削性变现",
            "missing child-content safety boundary",
        ),
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


def _load_json(path: Path, relative_path: str, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{relative_path}: invalid JSON: {exc.msg}")
        return None


def _validate_trigger_evals(path: Path, errors: list[str]) -> None:
    relative_path = "evals/trigger-evals.json"
    payload = _load_json(path, relative_path, errors)
    if payload is None:
        return
    if not isinstance(payload, list):
        errors.append(f"{relative_path}: must contain a JSON array")
        return

    if len(payload) != 20:
        errors.append(f"{relative_path}: must contain exactly 20 items")

    queries: set[str] = set()
    true_count = 0
    false_count = 0
    has_exact_positive = False
    for index, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            errors.append(f"{relative_path}: item {index} must be an object")
            continue

        query = item.get("query")
        normalized_query = query.strip() if isinstance(query, str) else ""
        if not normalized_query:
            errors.append(
                f"{relative_path}: item {index} query must be a non-empty string"
            )
        elif normalized_query in queries:
            errors.append(f"{relative_path}: queries must be unique")
        else:
            queries.add(normalized_query)

        should_trigger = item.get("should_trigger")
        if not isinstance(should_trigger, bool):
            errors.append(
                f"{relative_path}: item {index} should_trigger must be boolean"
            )
        elif should_trigger:
            true_count += 1
            if "我想创作一个游戏" in normalized_query:
                has_exact_positive = True
        else:
            false_count += 1

    if true_count != 10 or false_count != 10:
        errors.append(
            f"{relative_path}: trigger evals must contain exactly 10 true and 10 false should_trigger values"
        )
    if not has_exact_positive:
        errors.append(
            f"{relative_path}: a positive item must include the exact phrase 我想创作一个游戏"
        )


def _validate_evals(path: Path, errors: list[str]) -> None:
    relative_path = "evals/evals.json"
    payload = _load_json(path, relative_path, errors)
    if payload is None:
        return

    items = payload.get("evals") if isinstance(payload, dict) else None
    if not isinstance(items, list) or not items:
        errors.append(f"{relative_path}: must contain a non-empty evals array")
        return

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"{relative_path}: item {index} must be an object")
            continue
        if "id" not in item:
            errors.append(f"{relative_path}: item {index} must contain id")
        for field in ("prompt", "expected_output"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{relative_path}: item {index} {field} must be a non-empty string"
                )
        if not isinstance(item.get("files"), list):
            errors.append(f"{relative_path}: item {index} files must be a list")
        expectations = item.get("expectations")
        if (
            not isinstance(expectations, list)
            or not expectations
            or not all(
                isinstance(expectation, str) and expectation.strip()
                for expectation in expectations
            )
        ):
            errors.append(
                f"{relative_path}: item {index} expectations must be a non-empty list of non-empty strings"
            )


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

    trigger_evals_path = root / "evals/trigger-evals.json"
    if trigger_evals_path.is_file():
        _validate_trigger_evals(trigger_evals_path, errors)

    evals_path = root / "evals/evals.json"
    if evals_path.is_file():
        _validate_evals(evals_path, errors)

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
