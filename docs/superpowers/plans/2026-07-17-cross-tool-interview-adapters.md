# Cross-tool Interview Adapters Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the game-creation interview start reliably when this repository is installed into supported coding tools.

**Architecture:** Keep one concise, tool-neutral interview contract in `integrations/shared/`. Provide small adapter files at each tool's recognized project-instruction location, each delegating to that same contract. Provide an opt-in Python copier that writes an adapter into a target project only when it would not replace an existing user file.

**Tech Stack:** Markdown instruction files; Python 3 standard library; `unittest`.

## Global Constraints

- Trigger only for a user who wants to create or design their own game, not code-only fixes or recommendations.
- The first reply must be Chinese, welcoming, and ask exactly one game-design question; it must not generate code, a GDD, or a multi-question checklist.
- Preserve the existing 18–22-round interview, `停止` completion, GDD approval, child-safety, and lightweight web-game requirements.
- Never overwrite an existing target-project instruction file.
- Support Cursor, GitHub Copilot, Gemini CLI, Claude Code, and generic `AGENTS.md` consumers.

---

### Task 1: Lock the cross-tool contract with tests

**Files:**
- Create: `tests/test_platform_integrations.py`
- Modify: `scripts/validate_skill.py`

**Interfaces:**
- Consumes: repository root resolved as `Path(__file__).resolve().parents[1]`.
- Produces: tests requiring all adapter files, their single-question start contract, and deterministic installer behavior.

- [ ] **Step 1: Write the failing test**

```python
def test_every_adapter_requires_one_chinese_design_question():
    for path in ADAPTER_PATHS:
        text = read(path)
        self.assertIn("恰好一个", text)
        self.assertIn("设计问题", text)
        self.assertIn("不得直接", text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_platform_integrations -v`
Expected: FAIL because `integrations/` and the installer do not exist.

- [ ] **Step 3: Write minimal implementation**

Create the shared contract, the five adapter files, and `scripts/install_integration.py` with a `destination_for(tool, target)` function and a no-overwrite `install(tool, target)` function.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_platform_integrations -v`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add integrations scripts/install_integration.py tests/test_platform_integrations.py scripts/validate_skill.py
git commit -m "feat: add cross-tool interview adapters"
```

### Task 2: Document reliable installation and package the skill

**Files:**
- Modify: `README.md`
- Modify: `scripts/validate_skill.py`
- Test: `tests/test_skill_content.py`

**Interfaces:**
- Consumes: adapter names and installer command from Task 1.
- Produces: a short deployment table that explains copying an adapter into the *game project*, where the coding tool auto-loads it.

- [ ] **Step 1: Write the failing test**

```python
def test_readme_documents_cross_tool_installation():
    text = read("README.md")
    self.assertIn("跨工具", text)
    self.assertIn("install_integration.py", text)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_skill_content.RepositoryCompletenessTests.test_readme_documents_cross_tool_installation -v`
Expected: FAIL because the cross-tool installation section is absent.

- [ ] **Step 3: Write minimal implementation**

Add exact commands for each tool and explain that a repository upload alone does not install an active project rule. Extend the validator to require each adapter and the new README section.

- [ ] **Step 4: Run tests and package validation**

Run: `python3 -m unittest discover -s tests -v && python3 scripts/validate_skill.py`
Expected: all tests PASS and `Skill validation passed.`

- [ ] **Step 5: Commit and publish**

```bash
git add README.md scripts/validate_skill.py tests/test_skill_content.py
git commit -m "docs: explain cross-tool interview installation"
git push -u origin codex/cross-tool-interview
```
