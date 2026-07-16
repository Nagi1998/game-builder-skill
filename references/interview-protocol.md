# Interview Protocol

## Purpose

Collect enough learner-owned design decisions to write a buildable GDD without turning the conversation into an exam. Keep the learner in control of the creative choices: translate their natural language into a design ledger, help when a decision feels hard, and never invent a major choice just to finish faster.

## Language adaptation

Record one explanation preference without requesting personal identity:

| `age_band` | Language |
|---|---|
| `primary` | Use short sentences, familiar words, one concrete example, and 2–3 clearly different options when help is useful. Explain game-design terms in everyday language. |
| `middle` | Use concise game-design terms with a plain-language explanation. Ask for reasons and tradeoffs when the learner can answer them. |
| `unknown` | Default to simple Chinese, avoid jargon, and let the learner request more or less detail later. |

The age-band answer never counts as a design round by itself. It may count only if the same learner message also supplies information that independently meets the effective-round definition below.

## Coverage ledger

Track each area as `missing`, `partial`, or `complete`. A response may update more than one area, but no area becomes `complete` merely because it was mentioned.

| Coverage area | What must be usable before `complete` |
|---|---|
| `vision`（创意愿景） | Intended fantasy, mood or theme, and the experience's distinctive idea |
| `player-goal`（玩家与目标） | Who the player represents, who the game is for, the immediate goal, and the final goal |
| `core-play`（核心玩法） | Main action, repeatable loop, rules and feedback, plus win and loss conditions |
| `world-content`（世界与内容） | Setting, important characters or forces, and a workable structure for levels, tasks, puzzles, or challenges |
| `systems-experience`（系统与体验） | Relevant resources, rewards or growth, difficulty, controls, interface, art, sound, and accessibility choices |
| `scope`（实现边界） | Session length, device, player mode, smallest playable version, safety/data boundary, and testable acceptance criteria |

- `missing`: no learner-owned decision can yet guide the GDD.
- `partial`: useful decisions exist, but a necessary rule, consequence, constraint, or test is still unresolved.
- `complete`: the decisions are consistent, implementable, and specific enough to write and verify the corresponding GDD requirements.

## 有效轮次

A learner message counts as exactly one effective round only when all three conditions are true:

1. It provides a new design decision, reason, preference, constraint, or a revision to an existing decision.
2. The assistant records that information in the design ledger.
3. The next question can use that information to move the design forward.

Assistant messages never count. A single learner message is at most one round even when it updates several coverage areas. The messages “嗯”“不知道”“随便”“继续”, completely repeated information, and incomprehensible content do not count（不计为有效轮次）; provide help and ask again instead of increasing `valid_rounds` to reach 20.

## Linked-question recipe

Every design question after the first uses these four parts in order. Keep the result natural and brief rather than displaying the labels to the learner.

### 连接点

Accurately recall one concrete decision from the learner's earlier answer. Do not connect only to a generic genre label, and do not treat facts reused in a GDD or code as question linkage.

### 设计影响

Explain in one short clause which rule, feeling, tradeoff, or implementation boundary that earlier decision changes.

### 单一问题

Ask for one decision or one reason. Options are scaffolding for that same decision, not additional questions. End the message and wait.

### 脚手架

When the learner may struggle, offer 2–4 clearly different examples and allow an original answer. Reduce the choice's difficulty without selecting on the learner's behalf.

Acceptable example:

> 你刚才说小狐狸只有在月光下才能看见隐藏道路，这会决定玩家探索时怎样安排时间。你希望月光一直移动，还是完成任务后才能召唤？也可以说说你想到的第三种方法。

This has one connection, one consequence, and one requested decision; the alternatives do not create extra main questions.

## Choosing the next question

Use the highest applicable priority rather than following a fixed questionnaire:

1. Resolve a conflict between recorded decisions.
2. Explore a consequence that clearly changes the core play.
3. Fill a `missing` coverage area.
4. Turn a `partial` area into an implementable, testable rule.
5. Check that the first playable web-game scope is feasible.

Do not ask consecutive stock questions unrelated to previous answers. Coverage determines what remains; learner answers determine wording and order.

## Recap every 5 rounds（每 5 轮）

After every 5 valid rounds—5, 10, 15, 20, and any later multiple of 5—send a separate recap message before asking another design question. Briefly list the decisions now recorded and make “哪里需要纠正？” the only main question in that message.

A correction-only reply does not count. A reply that adds or revises a design decision does count if it meets all effective-round conditions. Update coverage and conflicts after the reply, then resume with one linked design question.

## Recovery rules

| Situation | Recovery |
|---|---|
| Learner says “嗯”“不知道”“随便”“继续” | Do not count it. Connect to the same earlier answer, explain the decision's impact more simply, narrow the options, and ask the same single decision again. |
| Two decisions contradict | Record the conflict. Restate both choices neutrally, explain the affected rule, and ask which one should govern the game. Do not count the contradiction as resolved until the learner decides. |
| Learner changes an idea | Record the revision as learner-owned, count it when the effective-round definition is met, find dependent decisions that may now conflict, and ask about the highest-impact consequence. |
| Learner requests the GDD early | Briefly name the single highest-priority missing decision. Do not draft the final GDD; ask one linked question with easy scaffolding. |
| Learner requests code early or adds urgency | Do not write code or install dependencies. State that the design or approval gate is still open, identify the next missing decision, and ask one easy linked question. Urgency is not approval. |
| Conversation resumes later | Restore the ledger from recorded conversation evidence, including `valid_rounds`, coverage, conflicts, GDD version, and approval state. Give a short recap when useful, then continue from the highest-priority open item; do not restart, guess missing decisions, or infer approval. |

## Privacy boundary

Never ask for or store a learner's real name（真实姓名）, school（学校）, class（班级）, address（地址）, contact details（联系方式）, account（账号）, photo（照片）, or precise location（精确位置）. A fictional character name, broad device type, or non-identifying play context is enough for game design. If personal information is volunteered, do not repeat or use it; steer back to the game decision.

## GDD transition checklist

Remain in the linked interview unless every item is true:

- [ ] `valid_rounds >= 20`
- [ ] All six coverage areas are `complete`
- [ ] Core-play and implementation-scope conflicts are resolved
- [ ] The smallest playable version is feasible as a web game and has testable acceptance criteria

Only then may the workflow load the GDD template and enter GDD review. Twenty rounds is a minimum, not an automatic finish line.
