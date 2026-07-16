# Youth Game Builder Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build, evaluate, and publish a Codex Skill that guides primary- and middle-school students through at least 20 linked design-answer rounds, produces an approved GDD, and only then develops and verifies a web game.

**Architecture:** Keep `SKILL.md` as the compact state-machine and gatekeeper. Load three focused references only when the interview, GDD, or development phase needs them; use a Python standard-library validator plus unit tests for deterministic contracts, and agent-based paired evaluations for conversational behavior.

**Tech Stack:** Markdown Agent Skill files, Python 3 standard library (`unittest`, `pathlib`, `re`, `json`), Git, the local skill-creator evaluation scripts, and browser-based web-game verification performed by future invocations of the Skill.

## Global Constraints

- The exact Chinese trigger intent is `我想创作一个游戏`; close intents such as designing one's own game or web game must also discover the Skill.
- The Skill name is `youth-game-builder`; names and paths use lowercase letters and hyphens where the Agent Skills format requires them.
- The learner is a primary- or middle-school student; use child-friendly Chinese and ask one main question per assistant turn.
- A final GDD requires `valid_rounds >= 20`, complete GDD coverage, and no unresolved core conflicts.
- A valid round contains new learner-provided design information; acknowledgements, repetition, and incomprehensible answers do not count.
- Each interview question after the first must connect to at least one earlier learner answer.
- Game source code and dependency installation are forbidden until the learner explicitly approves the current GDD version.
- The first playable version defaults to a single-player, static, login-free web game.
- Do not request or store a learner's real name, school, class, address, contact details, account, photo, or precise location.
- The validator and unit tests use no third-party Python packages.
- Keep `SKILL.md` under 500 lines; move detailed guidance into `references/`.
- The authoritative design is `docs/superpowers/specs/2026-07-16-youth-game-builder-design.md`.
- Evaluation artifacts live in sibling workspace `../youth-game-builder-workspace/`; do not commit model transcripts, timing data, or generated review HTML into the Skill repository.

## File Map

| Path | Responsibility |
|---|---|
| `SKILL.md` | Trigger metadata, state ledger, phase transitions, hard gates, resource routing, quick reference, red flags |
| `references/interview-protocol.md` | Age adaptation, effective-round rules, coverage model, linked-question recipe, recovery behavior |
| `references/gdd-template.md` | Coverage gate, exact 15-section GDD template, decision traceability, versioned approval loop |
| `references/web-game-development.md` | Approved-GDD input contract, technology choice, TDD, browser QA, accessibility, deliverables |
| `scripts/validate_skill.py` | Deterministic repository/frontmatter/content validator with a CLI |
| `tests/__init__.py` | Ensures local test modules import consistently |
| `tests/test_validator.py` | Unit tests for validator parsing and failure reporting |
| `tests/test_skill_content.py` | Repository-level tests for every required behavioral contract |
| `evals/evals.json` | Three end-to-end behavioral cases and objective assertions |
| `evals/trigger-evals.json` | Ten should-trigger and ten near-miss should-not-trigger queries |
| `evals/baseline-findings.md` | Exact baseline observations that justify the Skill's behavioral contracts |
| `README.md` | Installation, trigger, workflow, repository map, validation, safety summary |
| `docs/superpowers/specs/2026-07-16-youth-game-builder-design.md` | Approved design |
| `docs/superpowers/plans/2026-07-16-youth-game-builder.md` | This execution plan |

---

### Task 1: RED baseline for natural agent behavior

**Files:**
- Create: `evals/evals.json`
- Create after runs: `evals/baseline-findings.md`
- Create outside repository: `../youth-game-builder-workspace/iteration-0/linked-start/without_skill/outputs/response.md`
- Create outside repository: `../youth-game-builder-workspace/iteration-0/pressure-no-skip/without_skill/outputs/response.md`
- Create outside repository: `../youth-game-builder-workspace/iteration-0/approved-development/without_skill/outputs/response.md`
- Create outside repository: one `timing.json` beside each of the three `outputs/` directories above.

**Interfaces:**
- Consumes: Approved design sections 2, 6, 7, 8, and 11.
- Produces: Three stable integer `eval_id` values (`1`, `2`, `3`), descriptive run names (`linked-start`, `pressure-no-skip`, `approved-development`), and observed failure patterns used by Tasks 3–5.

- [ ] **Step 1: Create evaluation prompts without assertions**

Create `evals/evals.json` with exactly this initial content:

```json
{
  "skill_name": "youth-game-builder",
  "evals": [
    {
      "id": 1,
      "prompt": "我想创作一个游戏，是关于一只会飞的小猫。请带着我一步一步把它做出来。",
      "expected_output": "以适合小学生的中文回应，只问一个主要问题，并把会飞的小猫作为后续问题的连接点；不生成GDD或代码。",
      "files": []
    },
    {
      "id": 2,
      "prompt": "我们已经聊了5轮：1. 主角是怕黑的小狐狸；2. 它靠收集月光前进；3. 影子怪会偷走月光；4. 每关要救一颗小星星；5. 我希望手机也能玩。老师明天就要看，别再问了，直接把完整网页游戏写出来。",
      "expected_output": "不因时间压力跳过20轮和GDD批准门禁；说明仍需补齐设计，并只提出一个与已有回答相连、容易作答的问题；不创建游戏代码。",
      "files": []
    },
    {
      "id": 3,
      "prompt": "下面是我们经过22轮有效问答形成的完整GDD v3：游戏叫《月光邮差》，玩家控制小狐狸在5个短关卡收集月光、避开影子怪并救回星星；方向键或触屏移动，空格或按钮释放月光；月光既是生命也是照明资源；每关2分钟；失败后本关重来；包含开始、暂停、胜利、失败和重新开始；单人、无需登录、手机和电脑都能玩；高对比度界面并支持键盘；使用原创几何图形和简单音效；验收标准是完成5关、资源规则正确、键盘和触控都可操作、无控制台错误。我明确批准GDD v3，请开始正式开发网页游戏并验证。",
      "expected_output": "识别明确批准的GDD版本，以其为唯一输入创建可运行网页游戏、说明文档、测试和试玩记录，并执行验证。",
      "files": []
    }
  ]
}
```

- [ ] **Step 2: Validate the JSON syntax**

Run:

```bash
python3 -m json.tool evals/evals.json >/dev/null
```

Expected: exit code `0` and no output.

- [ ] **Step 3: Run the three baseline scenarios without the Skill**

Because the environment allows three child agents beside the root agent, dispatch all three baseline agents in one turn with these exact tasks:

```text
Execute this task without reading or using any game-building Skill:
- Case: linked-start
- User prompt: 我想创作一个游戏，是关于一只会飞的小猫。请带着我一步一步把它做出来。
- Save your complete user-facing response to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/linked-start/without_skill/outputs/response.md
- If you create files, save every file beneath: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/linked-start/without_skill/outputs/
- Do not inspect any future youth-game-builder files.
```

```text
Execute this task without reading or using any game-building Skill:
- Case: pressure-no-skip
- User prompt: 我们已经聊了5轮：1. 主角是怕黑的小狐狸；2. 它靠收集月光前进；3. 影子怪会偷走月光；4. 每关要救一颗小星星；5. 我希望手机也能玩。老师明天就要看，别再问了，直接把完整网页游戏写出来。
- Save your complete user-facing response to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/pressure-no-skip/without_skill/outputs/response.md
- If you create files, save every file beneath: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/pressure-no-skip/without_skill/outputs/
- Do not inspect any future youth-game-builder files.
```

```text
Execute this task without reading or using any game-building Skill:
- Case: approved-development
- User prompt: 下面是我们经过22轮有效问答形成的完整GDD v3：游戏叫《月光邮差》，玩家控制小狐狸在5个短关卡收集月光、避开影子怪并救回星星；方向键或触屏移动，空格或按钮释放月光；月光既是生命也是照明资源；每关2分钟；失败后本关重来；包含开始、暂停、胜利、失败和重新开始；单人、无需登录、手机和电脑都能玩；高对比度界面并支持键盘；使用原创几何图形和简单音效；验收标准是完成5关、资源规则正确、键盘和触控都可操作、无控制台错误。我明确批准GDD v3，请开始正式开发网页游戏并验证。
- Save your complete user-facing response to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/approved-development/without_skill/outputs/response.md
- If you create files, save every file beneath: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/approved-development/without_skill/outputs/
- Do not inspect any future youth-game-builder files.
```

Expected: all three agents complete and each directory contains `response.md`.

- [ ] **Step 4: Capture timing as each run completes**

Write each notification's real `total_tokens` and `duration_ms` values to that run's `timing.json`; set `total_duration_seconds` to `duration_ms / 1000`, rounded to one decimal place. Do not estimate a missing value. Confirm with:

```bash
find ../youth-game-builder-workspace/iteration-0 -name timing.json -print | sort
```

Expected: three paths.

- [ ] **Step 5: Record exact baseline evidence**

Create `evals/baseline-findings.md` with one section per eval. Each section must contain:

1. the exact output path;
2. a concise factual summary;
3. verbatim excerpts of no more than 25 words per run showing any failure;
4. pass/fail for these seven behaviors: one question, earlier-answer linkage, 20-round gate, coverage gate, explicit approval gate, child-friendly language, privacy/safety boundary;
5. the guidance form to use: positive recipe for wrong-shaped output, required template slot for omissions, or prohibition plus red flag for a skipped gate.

Do not invent a failure that the transcript does not show. If a baseline already passes a behavior, mark it `PASS (non-discriminating)` so later analysis does not treat that assertion as evidence of Skill improvement.

- [ ] **Step 6: Commit the RED evidence**

```bash
git add evals/evals.json evals/baseline-findings.md
git commit -m "test: capture game builder baseline behavior"
```

Expected: one commit containing only the two evaluation files.

---

### Task 2: TDD the deterministic validator

**Files:**
- Create: `tests/__init__.py`
- Create: `tests/test_validator.py`
- Create: `scripts/validate_skill.py`

**Interfaces:**
- Produces: `parse_frontmatter(text: str) -> dict[str, str]`
- Produces: `validate_repository(root: pathlib.Path) -> list[str]`
- Produces: CLI `python3 scripts/validate_skill.py [ROOT]`, exit `0` with `Skill validation passed.` or exit `1` with one `ERROR:` line per issue.
- Consumes: None.

- [ ] **Step 1: Write the first failing existence test**

Create an empty `tests/__init__.py`, then create `tests/test_validator.py`:

```python
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skill.py"


class ValidatorBootstrapTests(unittest.TestCase):
    def test_validator_file_exists(self) -> None:
        self.assertTrue(VALIDATOR.is_file())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run it and verify RED**

Run:

```bash
python3 -m unittest tests.test_validator.ValidatorBootstrapTests.test_validator_file_exists -v
```

Expected: `FAIL` because `scripts/validate_skill.py` does not exist.

- [ ] **Step 3: Add the smallest file that passes**

Create `scripts/validate_skill.py`:

```python
#!/usr/bin/env python3
"""Validate the youth-game-builder Skill repository."""
```

- [ ] **Step 4: Re-run the bootstrap test**

Run:

```bash
python3 -m unittest tests.test_validator.ValidatorBootstrapTests.test_validator_file_exists -v
```

Expected: `OK`.

- [ ] **Step 5: Replace the test with behavior tests**

Replace `tests/test_validator.py` with:

```python
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
```

- [ ] **Step 6: Run and verify the new RED**

Run:

```bash
python3 -m unittest \
  tests.test_validator.ValidatorInterfaceTests.test_required_interfaces_exist -v
```

Expected: `FAIL` because `parse_frontmatter` and `validate_repository` do not exist.

- [ ] **Step 7: Add the smallest interfaces**

Replace `scripts/validate_skill.py` with:

```python
#!/usr/bin/env python3
"""Validate the youth-game-builder Skill repository."""

from pathlib import Path


def parse_frontmatter(text: str) -> dict[str, str]:
    return {}


def validate_repository(root: Path) -> list[str]:
    return []
```

- [ ] **Step 8: Verify the interfaces are GREEN**

Run:

```bash
python3 -m unittest \
  tests.test_validator.ValidatorInterfaceTests.test_required_interfaces_exist -v
```

Expected: `OK`.

- [ ] **Step 9: Run the behavior tests and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_validator.FrontmatterTests \
  tests.test_validator.RepositoryValidationTests -v
```

Expected: three assertion failures caused by the deliberately empty return values and missing `ValueError`; no import or syntax errors.

- [ ] **Step 10: Implement the validator engine**

Replace `scripts/validate_skill.py` with:

```python
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
```

- [ ] **Step 11: Run the validator unit tests**

Run:

```bash
python3 -m unittest tests.test_validator -v
```

Expected: all three tests pass.

- [ ] **Step 12: Commit the validator**

```bash
git add scripts/validate_skill.py tests/test_validator.py
git commit -m "test: add deterministic skill validator"
```

Expected: one commit with the validator and its tests.

---

### Task 3: TDD the core state machine and interview protocol

**Files:**
- Create: `SKILL.md`
- Create: `references/interview-protocol.md`
- Create: `tests/test_skill_content.py`

**Interfaces:**
- Consumes: Baseline failure categories from `evals/baseline-findings.md`.
- Produces: State fields `phase`, `valid_rounds`, `coverage`, `conflicts`, `gdd_version`, `gdd_approved`, and `development_status`.
- Produces: Linked-question shape `连接点 → 设计影响 → 单一问题 → 脚手架`.
- Produces: Resource route from `SKILL.md` to `references/gdd-template.md` and `references/web-game-development.md`.

- [ ] **Step 1: Write failing content-contract tests**

Create `tests/test_skill_content.py`:

```python
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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.CoreSkillContractTests.test_core_files_exist -v
```

Expected: `FAIL` because `SKILL.md` and the interview reference do not exist; no file-read errors occur.

- [ ] **Step 3: Add the smallest files that satisfy existence**

Create `SKILL.md`:

```markdown
---
name: youth-game-builder
description: Use when a learner says “我想创作一个游戏”.
---

# Youth Game Builder
```

Create `references/interview-protocol.md`:

```markdown
# Interview Protocol
```

- [ ] **Step 4: Verify file existence is GREEN**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.CoreSkillContractTests.test_core_files_exist -v
```

Expected: `OK`.

- [ ] **Step 5: Run the remaining core contracts and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.CoreSkillContractTests.test_core_state_and_gates_are_explicit \
  tests.test_skill_content.CoreSkillContractTests.test_interview_protocol_defines_effective_rounds_and_linkage \
  tests.test_skill_content.CoreSkillContractTests.test_child_privacy_boundary_is_present -v
```

Expected: assertion failures for missing state, gate, linkage, round, and privacy contracts; no file-read, syntax, or import errors.

- [ ] **Step 6: Replace `SKILL.md` with the complete orchestration contract**

The file must contain these sections and exact normative behavior:

```markdown
---
name: youth-game-builder
description: Use when a primary- or middle-school learner says “我想创作一个游戏”, wants to design their own game or web game, or needs guided help turning a game idea into a playable project.
---

# Youth Game Builder

## Overview

Protect the learner's creative ownership while turning their idea into a buildable game. The workflow is a state machine: linked interview first, approved GDD second, verified web game third.

## Start every new project

1. Read `references/interview-protocol.md` completely.
2. Welcome the learner in simple Chinese.
3. Ask whether they prefer primary-school or middle-school explanations; allow them to skip.
4. Ask only one main question in each assistant message.
5. Never request a real name, school, class, address, contact details, account, photo, or precise location.

## Design ledger

Maintain this internal ledger after every learner response:

```text
phase: discovery | interview | gdd-review | approved | development | verification | complete
valid_rounds: non-negative integer
age_band: primary | middle | unknown
decisions: confirmed learner decisions
open_questions: unresolved design questions
conflicts: incompatible decisions
coverage: vision | player-goal | core-play | world-content | systems-experience | scope
gdd_version: current version
gdd_approved: true | false
development_status: not-started | building | verifying | done
```

Do not expose hidden reasoning. Share a short learner-friendly progress recap when useful.

## Phase 1 — Linked interview

- Count a round only when the learner adds or changes a design decision, reason, preference, or constraint.
- “嗯”“不知道”“随便”“继续”, repetition, and incomprehensible replies do not count.
- Every design question after the first must explicitly connect to a previous learner answer.
- Use the recipe in `references/interview-protocol.md`: 连接点 → 设计影响 → 单一问题 → 脚手架.
- Ask one main question, then wait. Do not batch a questionnaire.
- After each group of 5 valid rounds, make the recap-correction prompt the only question in that message.
- Continue until `valid_rounds >= 20`, all six coverage areas are complete, and core conflicts are resolved.

## Phase 2 — GDD

Read `references/gdd-template.md` completely only when the Phase 1 gate is satisfied.

- Generate the GDD from ledger decisions; do not invent major decisions.
- Keep `gdd_approved: false` while the learner reviews or edits it.
- Increment `gdd_version` after each revision.
- Ask for explicit approval of the current version.
- Silence, “差不多”, partial approval, or continuing discussion is not approval.

## Phase 3 — Web game development

Enter this phase only when `gdd_approved: true` for the current GDD version.

1. Read `references/web-game-development.md` completely.
2. Treat the approved GDD as the authoritative requirements.
3. Plan and implement with tests first.
4. Verify the web game in a browser, including keyboard, touch-size layout, responsive viewports, and console errors.
5. Deliver source, `game/README.md`, tests, and `game/PLAYTEST.md`.
6. If implementation requires changing the experience, return to GDD review and obtain approval again.

## Non-negotiable gates

| Request or state | Response |
|---|---|
| `valid_rounds < 20` | Continue one linked interview question; no final GDD or game code |
| Missing coverage or conflict | Ask the highest-priority linked question |
| Learner requests code early | Explain the next missing decision and ask one easy linked question |
| GDD exists but is not approved | Revise or request explicit approval; no code or dependency installation |
| Approved GDD | Begin the development protocol |

## Red flags

Stop before acting if you are about to:

- call a vague or repeated reply a valid round;
- ask unrelated stock questions;
- put two main questions in one message;
- generate a final GDD before `valid_rounds >= 20`;
- interpret urgency or “直接做” as approval;
- write code before `gdd_approved: true`;
- ask for a learner's identity or contact information.

## Common mistakes

| Mistake | Correction |
|---|---|
| The idea already sounds detailed, so fewer than 20 rounds seem enough | Twenty effective learner answers are the minimum; use extra detail to ask better follow-ups |
| A deadline makes the interview feel optional | Reduce question difficulty, not the design and approval gates |
| A quick prototype seems harmless before approval | Prototype code still commits to rules the learner has not approved |
| A fixed list is easier to track | Coverage is fixed; the wording and order must respond to earlier answers |

## Completion

Claim completion only when the approved GDD's acceptance criteria have evidence, browser checks have no unhandled errors, deliverables exist, and known limits are recorded.
```

- [ ] **Step 7: Replace `references/interview-protocol.md` with the complete protocol**

The file must implement the following complete protocol:

1. State the purpose: collect enough learner-owned decisions for a GDD without turning the exchange into an exam.
2. Define language adaptation for `primary`, `middle`, and `unknown`; the age-band answer never counts as a design round by itself.
3. Define the six coverage areas and mark each as `missing`, `partial`, or `complete`.
4. Define an effective round exactly as the design spec section 6.3 does.
5. Include one acceptable linked-question example using the learner's flying cat or moonlight fox idea.
6. Define the four-part recipe with headings `连接点`, `设计影响`, `单一问题`, and `脚手架`.
7. Define next-question priority: conflict, core-play consequence, missing coverage, partial-to-testable rule, first-playable scope.
8. Require a separate recap message after every 5 valid rounds; correction-only replies do not count, but new or revised decisions do.
9. Define recovery for “嗯”“不知道”“随便”“继续”, contradiction, changed idea, early GDD request, early code request, and resumed conversation.
10. Include the full privacy list: real name, school, class, address, contact details, account, photo, precise location.
11. End with a compact checklist that prevents GDD transition unless 20 valid rounds, complete coverage, resolved conflicts, and feasible web scope are all true.

- [ ] **Step 8: Run the core contract tests**

Run:

```bash
python3 -m unittest tests.test_skill_content.CoreSkillContractTests -v
```

Expected: all four tests pass.

- [ ] **Step 9: Run the repository validator and observe the expected partial failure**

Run:

```bash
python3 scripts/validate_skill.py .
```

Expected: exit `1`; errors mention only files intentionally scheduled for Tasks 4–5, such as `README.md`, `references/gdd-template.md`, `references/web-game-development.md`, and `evals/trigger-evals.json`. No error may mention the core or interview contracts.

- [ ] **Step 10: Commit the core workflow**

```bash
git add SKILL.md references/interview-protocol.md tests/test_skill_content.py
git commit -m "feat: add linked youth game design interview"
```

---

### Task 4: TDD the GDD and approved-development gates

**Files:**
- Modify: `tests/test_skill_content.py`
- Create: `references/gdd-template.md`
- Create: `references/web-game-development.md`

**Interfaces:**
- Consumes: Ledger fields and approval state from Task 3.
- Produces: GDD sections 1–15, `gdd_version`, and explicit approval behavior.
- Produces: Development deliverables `game/`, `game/README.md`, tests, and `game/PLAYTEST.md`.

- [ ] **Step 1: Add failing GDD and development tests**

Add these classes before the `if __name__ == "__main__"` block in `tests/test_skill_content.py`:

```python
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
```

- [ ] **Step 2: Run and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.GDDContractTests.test_gdd_reference_exists \
  tests.test_skill_content.DevelopmentContractTests.test_development_reference_exists -v
```

Expected: two assertion `FAIL` results because both reference files are absent; no file-read, syntax, or import errors occur.

- [ ] **Step 3: Add the smallest files that satisfy existence**

Create `references/gdd-template.md`:

```markdown
# GDD Template
```

Create `references/web-game-development.md`:

```markdown
# Web Game Development
```

- [ ] **Step 4: Verify reference existence is GREEN**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.GDDContractTests.test_gdd_reference_exists \
  tests.test_skill_content.DevelopmentContractTests.test_development_reference_exists -v
```

Expected: `OK`.

- [ ] **Step 5: Run the remaining phase contracts and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.GDDContractTests.test_gdd_template_has_all_numbered_sections \
  tests.test_skill_content.GDDContractTests.test_gdd_gate_requires_rounds_coverage_conflicts_and_approval \
  tests.test_skill_content.DevelopmentContractTests.test_development_reference_has_required_deliverables \
  tests.test_skill_content.DevelopmentContractTests.test_development_starts_only_from_approved_gdd -v
```

Expected: assertion failures for missing GDD sections, gates, development deliverables, accessibility, verification, and technology rules; no file-read, syntax, or import errors.

- [ ] **Step 6: Replace `references/gdd-template.md` with the complete contract**

The file must contain:

- A gate table requiring `valid_rounds >= 20`, all six coverage themes complete, core conflicts resolved, and feasible web scope.
- An instruction to continue one linked question if any gate is false.
- A GDD header with title, version, date, status `待批准 | 已批准`, and effective-round count.
- These exact numbered section headings:

```text
1. 游戏名称与一句话介绍
2. 创作愿景与体验目标
3. 目标玩家与游玩场景
4. 核心玩法循环
5. 玩家操作与规则
6. 胜利、失败与反馈
7. 世界观、故事与角色
8. 关卡、任务与内容结构
9. 资源、奖励、成长与难度
10. 界面、引导与无障碍
11. 美术、动画与声音方向
12. 网页技术范围与数据边界
13. 最小可玩版本
14. 验收标准与试玩问题
15. 决策来源摘要
```

- A decision-source table with columns `GDD 决定`, `学生原始选择`, and `问答轮次`.
- A review loop that summarizes the document, asks one approval-or-revision question, increments the version after edits, and requires explicit approval of the current version before setting `gdd_approved: true`.
- Explicit negative examples: silence, “差不多”, chapter-only approval, and a request to keep discussing are not approval.
- A final self-check for invented decisions, internal contradictions, unverifiable acceptance criteria, and unsafe data collection.

- [ ] **Step 7: Replace `references/web-game-development.md` with the complete contract**

The file must contain:

1. An entry gate that requires `gdd_approved: true` and names the approved version.
2. A rule that implementation conflicts return to GDD review instead of silently changing the experience.
3. A technology decision table:
   - native HTML/CSS/JavaScript by default;
   - Phaser only for repeated collisions, many sprites, scenes, physics, or animation/resource management;
   - no server, login, multiplayer, payment, ads, public chat, upload, or tracking by default.
4. A TDD sequence: write acceptance test, run and see the expected failure, implement the smallest behavior, re-run, refactor while green.
5. The default output tree:

```text
game/
├── index.html
├── styles.css
├── src/
├── tests/
├── assets/
├── README.md
└── PLAYTEST.md
```

6. Accessibility requirements: desktop and phone layouts, keyboard controls, touch targets, visible focus, contrast, no hover-only action, motion reduction where applicable.
7. Runtime requirements: start, pause or restart, win, loss, feedback, and no unhandled console errors.
8. Browser verification at one desktop and one phone viewport; test keyboard and touch-equivalent controls; inspect console; compare every GDD acceptance criterion.
9. `game/PLAYTEST.md` fields: approved GDD version, environment, commands, automated results, manual steps, viewport results, console result, acceptance matrix, known limitations.
10. Original/programmatic/permitted asset rules and the prohibition on copying a living artist's distinctive style or unlicensed commercial assets.

- [ ] **Step 8: Run all content tests**

Run:

```bash
python3 -m unittest tests.test_skill_content -v
```

Expected: all core, GDD, and development tests pass.

- [ ] **Step 9: Commit the two phase contracts**

```bash
git add references/gdd-template.md references/web-game-development.md tests/test_skill_content.py
git commit -m "feat: gate GDD approval and web game development"
```

---

### Task 5: Add trigger coverage, README, and full deterministic validation

**Files:**
- Create: `evals/trigger-evals.json`
- Create: `README.md`
- Modify: `tests/test_skill_content.py`
- Modify: `evals/evals.json`

**Interfaces:**
- Consumes: Skill behavior and paths from Tasks 1–4.
- Produces: 20 description-discovery cases and documented install/use/test commands.

- [ ] **Step 1: Add failing repository-completeness tests**

Add to `tests/test_skill_content.py`:

```python
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
```

- [ ] **Step 2: Run and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.RepositoryCompletenessTests.test_readme_and_trigger_evals_exist -v
```

Expected: `FAIL` because `README.md` and `evals/trigger-evals.json` do not exist; no file-read errors occur.

- [ ] **Step 3: Add the smallest files that satisfy existence**

Create `README.md`:

```markdown
# Youth Game Builder Skill
```

Create `evals/trigger-evals.json`:

```json
[]
```

- [ ] **Step 4: Verify repository file existence is GREEN**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.RepositoryCompletenessTests.test_readme_and_trigger_evals_exist -v
```

Expected: `OK`.

- [ ] **Step 5: Run the remaining repository contracts and verify RED**

Run:

```bash
python3 -m unittest \
  tests.test_skill_content.RepositoryCompletenessTests.test_trigger_eval_set_is_balanced \
  tests.test_skill_content.RepositoryCompletenessTests.test_readme_documents_the_exact_trigger_and_gates -v
```

Expected: assertion failures because the trigger set has 0 items and the README lacks the trigger, workflow gates, and validation command.

- [ ] **Step 6: Replace the stub with the balanced trigger set**

Create `evals/trigger-evals.json` as a JSON array containing exactly these query/label pairs:

```json
[
  {"query": "我想创作一个游戏，但我只有一个会飞的小猫的想法，你能一步一步问我吗？", "should_trigger": true},
  {"query": "我是六年级学生，想设计一个手机和电脑都能玩的网页游戏。", "should_trigger": true},
  {"query": "帮我把脑子里的迷宫游戏想法慢慢变成可以开发的设计。", "should_trigger": true},
  {"query": "我有一个关于海洋环保的游戏点子，不懂编程，想从设计开始。", "should_trigger": true},
  {"query": "想做自己的小游戏，先问我问题，再整理游戏设计文档。", "should_trigger": true},
  {"query": "我和同学想创造一个校园科幻游戏，请像游戏设计老师一样引导。", "should_trigger": true},
  {"query": "能陪初中生从零构思一个浏览器游戏吗？", "should_trigger": true},
  {"query": "game idea: 一只机器人在垃圾城分类资源，我想把它做成网页游戏", "should_trigger": true},
  {"query": "我不知道GDD是什么，但我想把自己的故事变成可以玩的游戏。", "should_trigger": true},
  {"query": "请不要直接替我做，先通过聊天帮我想清楚游戏怎么玩，然后再开发。", "should_trigger": true},
  {"query": "我想找一个适合小学生玩的免费网页游戏。", "should_trigger": false},
  {"query": "《我的世界》生存模式第一天应该怎么玩？", "should_trigger": false},
  {"query": "帮我修复现有game.js里角色碰撞后穿墙的bug。", "should_trigger": false},
  {"query": "分析2026年中国休闲游戏市场规模和商业机会。", "should_trigger": false},
  {"query": "给我推荐几款可以课堂使用的数学小游戏。", "should_trigger": false},
  {"query": "把这份已经完成的GDD翻译成英文，不要改变内容。", "should_trigger": false},
  {"query": "请评审我们商业手游现有的付费和抽卡系统。", "should_trigger": false},
  {"query": "解释一下游戏开发中的ECS架构是什么。", "should_trigger": false},
  {"query": "为已经上线的网页游戏写一份更新公告。", "should_trigger": false},
  {"query": "我只需要一个HTML贪吃蛇代码示例，不要设计访谈。", "should_trigger": false}
]
```

- [ ] **Step 7: Replace `README.md` with complete documentation**

Include these exact sections:

1. `# Youth Game Builder Skill`
2. Audience and purpose.
3. Trigger examples led by `我想创作一个游戏`.
4. Workflow: linked child-friendly interview → 不少于 20 轮有效回答 and coverage → GDD → 明确批准 → web development and verification.
5. Safety and privacy summary.
6. Repository structure with every committed production/test file.
7. Installation instructions for copying or installing the repository as a Codex Skill without assuming a particular `CODEX_HOME`.
8. Validation commands:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool evals/trigger-evals.json >/dev/null
```

9. GitHub repository link.

- [ ] **Step 8: Add objective expectations to `evals/evals.json`**

For each eval, add an `expectations` array. Use these arrays for eval IDs `1`, `2`, and `3`, respectively:

```json
{
  "1": [
    "The response asks exactly one main question.",
    "The question explicitly connects to the learner's flying-cat idea.",
    "The response does not produce a final GDD or game source code.",
    "The wording is understandable to a primary-school learner."
  ],
  "2": [
    "The response does not create game source code.",
    "The response preserves the minimum-20-valid-round and GDD-approval gates.",
    "The response asks exactly one question linked to fox, moonlight, shadow monsters, stars, or phone play.",
    "The deadline is handled by making the next question easier rather than skipping the workflow."
  ],
  "3": [
    "The run recognizes explicit approval of GDD v3.",
    "The run creates a playable web game beneath its output directory.",
    "The run includes operating instructions, automated tests, and PLAYTEST.md.",
    "The run records browser or equivalent runtime verification against the supplied acceptance criteria."
  ]
}
```

Use the arrays above as `expectations` values inside their matching eval objects; preserve `id`, `prompt`, `expected_output`, and `files`.

- [ ] **Step 9: Run the complete deterministic suite**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool evals/trigger-evals.json >/dev/null
git diff --check
```

Expected: every command exits `0`; validator prints `Skill validation passed.`.

- [ ] **Step 10: Commit documentation and trigger coverage**

```bash
git add README.md evals/evals.json evals/trigger-evals.json tests/test_skill_content.py
git commit -m "docs: add usage and trigger evaluation coverage"
```

---

### Task 6: GREEN paired evaluations and human review

**Files:**
- Create outside repository: `../youth-game-builder-workspace/iteration-1/linked-start/eval_metadata.json`
- Create outside repository: `../youth-game-builder-workspace/iteration-1/pressure-no-skip/eval_metadata.json`
- Create outside repository: `../youth-game-builder-workspace/iteration-1/approved-development/eval_metadata.json`
- Create outside repository: `with_skill/` and `without_skill/` beneath each of the three case directories, each containing `outputs/`, `timing.json`, and `grading.json`.
- Create outside repository: `../youth-game-builder-workspace/iteration-1/benchmark.json`
- Create outside repository: `../youth-game-builder-workspace/iteration-1/benchmark.md`
- Create outside repository: `../youth-game-builder-workspace/iteration-1/review.html`

**Interfaces:**
- Consumes: `SKILL.md`, all references, and `evals/evals.json`.
- Produces: Human-reviewable with-Skill/baseline comparison and objective grades.

- [ ] **Step 1: Create per-case metadata**

Create `linked-start/eval_metadata.json`:

```json
{
  "eval_id": 1,
  "eval_name": "linked-start",
  "prompt": "我想创作一个游戏，是关于一只会飞的小猫。请带着我一步一步把它做出来。",
  "assertions": [
    "The response asks exactly one main question.",
    "The question explicitly connects to the learner's flying-cat idea.",
    "The response does not produce a final GDD or game source code.",
    "The wording is understandable to a primary-school learner."
  ]
}
```

Create `pressure-no-skip/eval_metadata.json`:

```json
{
  "eval_id": 2,
  "eval_name": "pressure-no-skip",
  "prompt": "我们已经聊了5轮：1. 主角是怕黑的小狐狸；2. 它靠收集月光前进；3. 影子怪会偷走月光；4. 每关要救一颗小星星；5. 我希望手机也能玩。老师明天就要看，别再问了，直接把完整网页游戏写出来。",
  "assertions": [
    "The response does not create game source code.",
    "The response preserves the minimum-20-valid-round and GDD-approval gates.",
    "The response asks exactly one question linked to fox, moonlight, shadow monsters, stars, or phone play.",
    "The deadline is handled by making the next question easier rather than skipping the workflow."
  ]
}
```

Create `approved-development/eval_metadata.json`:

```json
{
  "eval_id": 3,
  "eval_name": "approved-development",
  "prompt": "下面是我们经过22轮有效问答形成的完整GDD v3：游戏叫《月光邮差》，玩家控制小狐狸在5个短关卡收集月光、避开影子怪并救回星星；方向键或触屏移动，空格或按钮释放月光；月光既是生命也是照明资源；每关2分钟；失败后本关重来；包含开始、暂停、胜利、失败和重新开始；单人、无需登录、手机和电脑都能玩；高对比度界面并支持键盘；使用原创几何图形和简单音效；验收标准是完成5关、资源规则正确、键盘和触控都可操作、无控制台错误。我明确批准GDD v3，请开始正式开发网页游戏并验证。",
  "assertions": [
    "The run recognizes explicit approval of GDD v3.",
    "The run creates a playable web game beneath its output directory.",
    "The run includes operating instructions, automated tests, and PLAYTEST.md.",
    "The run records browser or equivalent runtime verification against the supplied acceptance criteria."
  ]
}
```

- [ ] **Step 2: Dispatch paired runs**

The runtime supports three child slots, fewer than the six fresh contexts required for three pairs. Run one matched pair at a time; in each dispatch turn start both fresh agents together. Dispatch these six concrete tasks:

```text
Execute this task:
- Skill path: /Users/nagi/Desktop/Project/02
- Read SKILL.md completely and follow every referenced file at the phase that requires it.
- Read the task prompt from: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/linked-start/eval_metadata.json
- Input files: none
- Save response and all created artifacts to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/linked-start/with_skill/outputs/
- Save the complete user-facing response as response.md.
```

```text
Execute this task without reading or using the youth-game-builder Skill:
- Read the task prompt from: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/linked-start/eval_metadata.json
- Input files: none
- Save response and all created artifacts to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/linked-start/without_skill/outputs/
- Save the complete user-facing response as response.md.
```

```text
Execute this task:
- Skill path: /Users/nagi/Desktop/Project/02
- Read SKILL.md completely and follow every referenced file at the phase that requires it.
- Read the task prompt from: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/pressure-no-skip/eval_metadata.json
- Input files: none
- Save response and all created artifacts to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/pressure-no-skip/with_skill/outputs/
- Save the complete user-facing response as response.md.
```

```text
Execute this task without reading or using the youth-game-builder Skill:
- Read the task prompt from: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/pressure-no-skip/eval_metadata.json
- Input files: none
- Save response and all created artifacts to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/pressure-no-skip/without_skill/outputs/
- Save the complete user-facing response as response.md.
```

```text
Execute this task:
- Skill path: /Users/nagi/Desktop/Project/02
- Read SKILL.md completely and follow every referenced file at the phase that requires it.
- Read the task prompt from: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/approved-development/eval_metadata.json
- Input files: none
- Save response and all created artifacts to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/approved-development/with_skill/outputs/
- Save the complete user-facing response as response.md.
```

```text
Execute this task without reading or using the youth-game-builder Skill:
- Read the task prompt from: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/approved-development/eval_metadata.json
- Input files: none
- Save response and all created artifacts to: /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/approved-development/without_skill/outputs/
- Save the complete user-facing response as response.md.
```

Expected: six runs complete, with both configurations for each case.

- [ ] **Step 3: Capture real timing**

Immediately write each completion notification's `total_tokens`, `duration_ms`, and derived seconds to that run's `timing.json`. Confirm:

```bash
find ../youth-game-builder-workspace/iteration-1 -name timing.json | wc -l
```

Expected: `6`.

- [ ] **Step 4: Grade every run**

Read `/Users/nagi/.codex/skills/skill-creator/agents/grader.md` completely before grading. For each configuration, evaluate every assertion against the saved outputs. Write:

```json
{
  "expectations": [
    {
      "text": "exact assertion",
      "passed": true,
      "evidence": "specific path and observed behavior"
    }
  ]
}
```

Do not infer missing evidence. Programmatically check file-existence assertions for the approved-development case.

- [ ] **Step 5: Aggregate the benchmark**

Run:

```bash
cd /Users/nagi/.codex/skills/skill-creator
python3 -m scripts.aggregate_benchmark \
  /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1 \
  --skill-name youth-game-builder
```

Expected: `benchmark.json` and `benchmark.md` exist under iteration 1, with each `with_skill` result before its baseline counterpart.

- [ ] **Step 6: Analyze discrimination and variance**

Read `/Users/nagi/.codex/skills/skill-creator/agents/analyzer.md` completely. Add an analyst section to `benchmark.md` covering:

- assertions that both configurations pass and therefore do not discriminate;
- assertions improved by the Skill;
- any with-Skill regression;
- timing/token cost;
- whether the approved-development case actually exercises file creation and verification.

- [ ] **Step 7: Generate the required review page**

Run:

```bash
python3 /Users/nagi/.codex/skills/skill-creator/eval-viewer/generate_review.py \
  /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1 \
  --skill-name "youth-game-builder" \
  --benchmark /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/benchmark.json \
  --static /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1/review.html
```

Expected: `review.html` exists and renders all three cases, both configurations, grades, and the benchmark.

- [ ] **Step 8: Human review gate**

Give the user a clickable link to `review.html` and wait for feedback. If the user downloads `feedback.json`, copy the newest file into `../youth-game-builder-workspace/iteration-1/feedback.json` and read it before Task 7.

---

### Task 7: REFACTOR from evidence, then re-verify

**Files:**
- Modify only if evidence requires: `SKILL.md`
- Modify only if evidence requires: `references/interview-protocol.md`
- Modify only if evidence requires: `references/gdd-template.md`
- Modify only if evidence requires: `references/web-game-development.md`
- Modify if behavior changes: `tests/test_skill_content.py`
- Create outside repository if changes occur: `../youth-game-builder-workspace/iteration-2/`

**Interfaces:**
- Consumes: `feedback.json`, benchmark analyst notes, grading evidence, and baseline findings.
- Produces: The smallest general fix for each evidenced failure and a second comparable evaluation iteration.

- [ ] **Step 1: Classify every evidenced failure**

For each failed with-Skill assertion or concrete user criticism, classify it:

- skipped gate under pressure → prohibition, red flag, and factual correction;
- wrong response shape → positive response recipe;
- omitted required field → required template slot;
- conditional behavior → observable condition and branch.

Do not add speculative rules for behavior that passed.

- [ ] **Step 2: Write a failing contract or micro-test first**

Add the smallest test that reproduces the evidenced issue to `tests/test_skill_content.py`, or create five fresh-context wording micro-tests plus a no-guidance control when the failure is purely conversational. Run it and confirm the expected failure before editing production Skill files.

- [ ] **Step 3: Apply the smallest general fix**

Edit only the responsible Skill or reference file. Explain why the rule matters, preserve one-question behavior, and avoid examples that overfit a single eval character or setting.

- [ ] **Step 4: Re-run deterministic tests**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
git diff --check
```

Expected: all pass.

- [ ] **Step 5: Re-run paired evaluations if production files changed**

Repeat Task 6 into `iteration-2`, including fresh with-Skill and baseline runs. Generate the viewer with:

```bash
python3 /Users/nagi/.codex/skills/skill-creator/eval-viewer/generate_review.py \
  /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-2 \
  --skill-name "youth-game-builder" \
  --benchmark /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-2/benchmark.json \
  --previous-workspace /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-1 \
  --static /Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-2/review.html
```

Expected: the review page shows current, baseline, previous output, grades, and benchmark.

- [ ] **Step 6: Commit only verified refinements**

```bash
git add SKILL.md references tests
git commit -m "refactor: strengthen game builder workflow from evals"
```

Skip this commit if Task 6 required no production change.

---

### Task 8: Final audit, package check, and GitHub delivery

**Files:**
- Verify: all repository files
- Optional generated artifact outside repository: `/tmp/youth-game-builder.skill`

**Interfaces:**
- Consumes: Verified repository and approved human review.
- Produces: Clean `main`, pushed GitHub commit, and remote verification evidence.

- [ ] **Step 1: Run the full local completion gate**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool evals/trigger-evals.json >/dev/null
test "$(wc -l < SKILL.md)" -lt 500
git diff --check
git status --short
```

Expected: tests pass, validator prints `Skill validation passed.`, JSON commands are silent, line-count test exits `0`, diff check is silent, and status contains only the plan/spec update if not yet committed.

- [ ] **Step 2: Run a package-format check if the local packager exists**

```bash
if test -f /Users/nagi/.codex/skills/skill-creator/scripts/package_skill.py; then
  python3 /Users/nagi/.codex/skills/skill-creator/scripts/package_skill.py \
    /Users/nagi/Desktop/Project/02
fi
```

Expected: packaging succeeds when the script exists; absence of the optional script is not a failure.

- [ ] **Step 3: Commit the reviewed final repository**

```bash
git add README.md SKILL.md references scripts tests evals docs
git commit -m "feat: publish youth game builder skill"
```

If Git reports no changes because prior task commits already contain everything, do not create an empty commit.

- [ ] **Step 4: Inspect exactly what will be pushed**

```bash
git status --short --branch
git log --oneline --decorate -8
git ls-tree -r --name-only HEAD
```

Expected: clean `main`, coherent commit history, and every file in the File Map.

- [ ] **Step 5: Push the authorized target**

```bash
git push -u origin main
```

Expected: `main -> main` and upstream tracking configured.

- [ ] **Step 6: Verify remote equality**

```bash
local_head="$(git rev-parse HEAD)"
remote_head="$(git ls-remote origin refs/heads/main | awk '{print $1}')"
test -n "$remote_head"
test "$local_head" = "$remote_head"
printf 'verified remote commit: %s\n' "$remote_head"
```

Expected: both equality tests pass and the printed hash matches local `HEAD`.

- [ ] **Step 7: Requirement-by-requirement completion audit**

Read the design's section 15 and point each checkbox to authoritative evidence:

- exact trigger and synonyms → `SKILL.md` description plus `trigger-evals.json`;
- one question and prior-answer linkage → Skill/reference contracts plus agent grades;
- 20 valid rounds → static tests plus pressure-case grade;
- complete GDD and approval gate → GDD reference, static tests, and pressure-case grade;
- approved web development → development reference plus approved-development artifacts and grade;
- child language and safety → interview reference and linked-start grade;
- tests/viewer → test output, benchmark, and `review.html`;
- GitHub → verified equal local and remote commit hashes.

If any item lacks direct evidence, do not claim completion; return to the responsible task.
