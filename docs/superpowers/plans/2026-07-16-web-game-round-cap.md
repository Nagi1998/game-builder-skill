# Web Game Round Cap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:test-driven-development for implementation and superpowers:verification-before-completion before claiming success.

**Goal:** Update `youth-game-builder` so its interview normally ends after 18–22 effective learner answers, handles “停止” by defaulting all remaining design decisions, and develops only lightweight, offline-capable 2D Web games.

**Architecture:** Keep the existing three-gate workflow (interview → approved GDD → development) and extend its ledger with round-cap, stop, completion-reason, and default-source fields. Put detailed behavioral rules in the references, keep `SKILL.md` as the routing contract, and enforce critical invariants through repository tests and the standalone validator.

**Tech Stack:** Markdown Skill files, JSON evaluation fixtures, Python standard-library `unittest`, and the existing Python validator.

**Global Constraints:**

- Preserve all existing child privacy, content-safety, GDD approval, test-first, and browser-verification gates.
- Treat “停止” as interview completion, never as GDD approval or permission to develop.
- Never request a 23rd effective answer.
- Default game output is static 2D HTML/CSS/JavaScript that opens from `game/index.html` without player-installed tooling, network services, or high-end hardware.
- Make production changes only after the matching new tests fail for the expected reason.

---

### Task 1: Lock the new interview contract with failing content tests

**Files:**
- Modify: `tests/test_skill_content.py`
- Test: `tests/test_skill_content.py`

**Step 1: Add contract tests**

Add focused assertions that require:

- the adaptive `18 <= valid_rounds < 22` window and hard cap of 22;
- no design question after the cap;
- explicit “停止” handling, automatic default completion, and `gdd_approved: false`;
- defaulted decisions labelled `系统默认`;
- Web-only static 2D output and `game/index.html`;
- native HTML/CSS/JavaScript, Canvas 2D/DOM, offline double-click startup, Windows/macOS compatibility;
- default exclusions for WebGL/3D, heavy frameworks, npm build chains, backend services, CDN and runtime network requests;
- README and evaluation fixtures covering the revised workflow;
- removal of stale runtime statements that require at least 20 rounds.

**Step 2: Run the focused suite and confirm RED**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_skill_content -v`

Expected: FAIL because the current runtime Skill still requires at least 20 rounds and does not define the stop/default or lightweight Web-only contracts.

**Step 3: Commit the failing tests**

```bash
git add tests/test_skill_content.py
git commit -m "test: define adaptive interview and web game contracts"
```

### Task 2: Implement the adaptive interview and stop behavior

**Files:**
- Modify: `SKILL.md`
- Modify: `references/interview-protocol.md`
- Modify: `references/gdd-template.md`
- Modify: `README.md`
- Modify: `evals/evals.json`
- Test: `tests/test_skill_content.py`

**Step 1: Update the runtime state and routing contract**

Document `target_rounds: 18..22`, `hard_round_cap: 22`, `stop_requested`, `completion_reason`, and `defaulted_decisions`. Route normal interviews to GDD generation once coverage is complete from round 18 onward, force completion at round 22, and route a clear “停止” command directly to default completion without another question.

**Step 2: Update the interview protocol**

Specify exact stop-command detection, the adaptive end algorithm, no 23rd request, and safe handling of incomplete coverage or conflicts. Preserve one-question-at-a-time linkage before completion.

**Step 3: Update GDD provenance and gates**

Allow GDD generation through:

- coverage-complete at 18–22 effective rounds;
- round-cap at 22 with safe defaults;
- stop with safe defaults.

Require every defaulted field to be labelled `系统默认` with a short reason, keep the output `待批准`, and retain explicit version approval before development.

**Step 4: Update README and behavioral evaluations**

Explain the revised round window and stop command in plain Chinese. Update existing evaluation expectations and add focused cases for round 18, round 22, and early stop.

**Step 5: Run the focused content suite**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_skill_content -v`

Expected: interview/GDD/README tests pass; development-stack assertions may remain red until Task 3.

### Task 3: Implement the lightweight Web-game development contract

**Files:**
- Modify: `references/web-game-development.md`
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `evals/evals.json`
- Test: `tests/test_skill_content.py`

**Step 1: Define the output and default stack**

Require `game/index.html`, native HTML5/CSS/JavaScript, DOM or Canvas 2D, local assets, direct offline double-click startup, keyboard and touch parity, and current mainstream Windows/macOS browsers.

**Step 2: Define complexity and resource limits**

Default-exclude WebGL/3D/WASM/GPU compute, Phaser/React/Vue, npm build tooling, backends, databases, logins, cloud APIs, CDN/runtime network requests, and first-version assets over 10 MB. Permit at most one lightweight local dependency only through a newly approved GDD.

**Step 3: Extend verification**

Require offline-start verification, no runtime network dependence, desktop/mobile viewport checks, compatibility evidence, resource-size reporting, and playable performance without a dedicated GPU.

**Step 4: Run content tests**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_skill_content -v`

Expected: PASS.

**Step 5: Commit the runtime contract**

```bash
git add SKILL.md README.md references/interview-protocol.md references/gdd-template.md references/web-game-development.md evals/evals.json
git commit -m "feat: cap interviews and require lightweight web games"
```

### Task 4: Strengthen the standalone validator with mutation tests

**Files:**
- Modify: `tests/test_validator.py`
- Modify: `scripts/validate_skill.py`
- Test: `tests/test_validator.py`

**Step 1: Add validator mutation tests**

Create repository mutations that separately remove:

- the round-18 earliest completion gate;
- the round-22 hard cap;
- the “停止” no-more-questions rule;
- the `gdd_approved: false` stop outcome;
- default-decision provenance;
- the static 2D Web-only entry point;
- offline/direct-open and Windows/macOS compatibility;
- the prohibition on complex/high-resource defaults.

**Step 2: Run validator tests and confirm RED**

Run: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_validator -v`

Expected: new mutation tests FAIL because the validator does not yet enforce these phrases.

**Step 3: Implement validator checks**

Update the required-fragment checks and error messages so every mutation is detected independently. Replace the obsolete fixed 20-round validator rule with the adaptive-window and stop-completion rules.

**Step 4: Run validator and full tests**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_validator -v
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
```

Expected: all commands pass.

**Step 5: Commit validator coverage**

```bash
git add tests/test_validator.py scripts/validate_skill.py
git commit -m "test: enforce round cap stop and web stack invariants"
```

### Task 5: Compare behavior and obtain independent review

**Files:**
- Create outside repository: `../youth-game-builder-workspace/iteration-2/`
- Inspect: all changed repository files

**Step 1: Snapshot the pre-change Skill**

Archive commit `473efa6` as the baseline so old and new behavior can be evaluated against identical prompts.

**Step 2: Run matched scenarios**

Compare baseline and new Skill on:

1. complete design information at effective round 18;
2. incomplete design at round 22;
3. “停止” after a short interview;
4. development from an approved GDD that asks for a Web game.

Record whether each response asks another question, generates a pending GDD, exposes defaults, preserves approval, and stays within the lightweight Web stack.

**Step 3: Review the comparison**

Confirm the new Skill passes every acceptance criterion and does not regress safety or approval gates. Obtain an independent review of the branch diff, tests, and specification; fix any high-confidence issues and rerun affected checks.

### Task 6: Final verification, integration, packaging, and publication

**Files:**
- Verify: entire repository
- Package: clean committed repository snapshot

**Step 1: Run final verification**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
git diff --check
git status --short --branch
```

Expected: all tests and validation pass, no whitespace errors, and only intended state remains.

**Step 2: Merge the feature branch into `main`**

Use the repository’s isolated-worktree integration flow, then rerun the full verification on `main`.

**Step 3: Package from a clean committed snapshot**

Run the Skill packager against an archive of the verified `main` commit. Confirm the output package is created without including `.git`, worktree metadata, caches, or unrelated files.

**Step 4: Push and verify**

Push `main` to `Nagi1998/game-builder-skill`, then confirm local `main`, `origin/main`, and the packaged source commit are identical.

