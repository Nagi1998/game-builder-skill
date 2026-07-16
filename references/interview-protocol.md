# Interview Protocol

## Purpose

Collect enough learner-owned design decisions to write a buildable GDD without turning the conversation into an exam. Keep the learner in control of the creative choices: translate their natural language into a design ledger, help when a decision feels hard, and never invent a major choice just to finish faster.

## Language adaptation

所有面向学生的对话始终使用适合小学、初中生理解的中文。年龄段适配只调整中文表达的复杂度，不改变对话语言。

Record one explanation preference without requesting personal identity:

| `age_band` | Language |
|---|---|
| `primary` | Use short sentences, familiar words, one concrete example, and 2–3 clearly different options when help is useful. Explain game-design terms in everyday language. |
| `middle` | Use concise game-design terms with a plain-language explanation. Ask for reasons and tradeoffs when the learner can answer them. |
| `unknown` | Default to simple Chinese, avoid jargon, and let the learner request more or less detail later. |

The age-band answer never counts as a design round by itself. It may count only if the same learner message also supplies information that independently meets the effective-round definition below. 年龄段和解释偏好只是设置，不会消耗或抹去触发消息中的设计信息。

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

Assistant messages never count. A single learner message is at most one round even when it updates several coverage areas. The messages “嗯”“不知道”“随便”“继续”, completely repeated information, and incomprehensible content do not count（不计为有效轮次）; provide help and ask again without increasing `valid_rounds`.

## Linked-question recipe

当账本已有任何学习者提供的设计信息时，第一个以及之后的每个设计问题都使用下面四个部分，并明确连接账本中的一项具体信息，包括触发消息里的设计信息。只有当账本没有设计信息时，第一个设计问题才可省略连接，并应引出学习者的初始创意愿景；从下一问起使用完整结构。Keep the result natural and brief rather than displaying the labels to the learner.

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

After valid rounds 5, 10, and 15, send a separate recap message before asking another design question. At round 20, recap only if a critical gap means the interview will continue. Briefly list the decisions now recorded and make “哪里需要纠正？” the only main question in that message.

A confirmation-only reply does not count. A reply that adds or revises a design decision does count if it meets all effective-round conditions. Update coverage and conflicts after the reply, then resume with one linked design question.

## Adaptive completion（18–22 轮）

第 18 轮是最早正常结束点，第 22 轮是绝对上限。目标是大致保持 18–22 个有效回答，并在信息足够时尽早结束；只有关键缺口才延长。

1. When `valid_rounds < 18`, ask one linked design question and wait.
2. When `18 <= valid_rounds < 22`, stop questioning if all six coverage areas are complete, core-play and scope conflicts are resolved, and the smallest Web MVP is feasible. Set `completion_reason: coverage-complete` and load the GDD contract.
3. Otherwise ask only the highest-priority unresolved decision. Do not add optional polish questions just to approach 22.
4. When `valid_rounds == 22`, set `completion_reason: round-cap`, 不再提出任何设计问题, use the mainstream defaults below for gaps, choose the safest and simplest option for unresolved conflicts, and load the GDD contract.
5. 不得提出第 23 个设计问题，也不得把系统默认伪装成新的有效回答。

## Stop command（停止提问）

After trimming surrounding whitespace, treat “停止”, “停止提问”, or “结束问答” as a request to end this design interview. A phrase about the game, such as “角色停止移动” or “暂停游戏”, is not a stop command.

On a clear stop command:

1. Set `stop_requested: true` and `completion_reason: stop`; the command itself does not increase `valid_rounds`.
2. 不再提出任何设计问题。
3. Preserve every learner decision and use the mainstream defaults below for all remaining fields; 默认值不得覆盖已确认决定。
4. Load the GDD contract and generate a complete `待批准` GDD with `gdd_approved: false`.
5. Label every filled decision `系统默认` with a short reason.
6. Explain that “停止”只结束问答，不代表批准 GDD，也不授权开发。
7. 停止后只允许一个审批问题：展示完整 GDD 后，询问要修改当前版本还是明确批准。不得再问设计问题。

### Mainstream defaults

Use only for decisions the learner has not made:

| Gap | Default |
|---|---|
| 游戏名称 | Use a short provisional title based on the confirmed theme, or “[主角/主题]小冒险” when no theme exists |
| 世界、角色与动机 | A safe fictional setting; preserve any confirmed character, otherwise use a neutral explorer/helper whose motive is to complete the visible goal |
| Game form | Single-player lightweight 2D collect-or-challenge game; use low-load 3D only when an existing learner idea clearly needs space/depth |
| Session and content | 3–5 minutes per run, three short levels, gradual difficulty |
| Core loop | Move or click → collect/avoid → immediate feedback → reach the goal |
| Input | Arrow keys/WASD plus Space; equivalent on-screen touch controls |
| Outcome | Win by reaching or collecting the target; lose when a resource reaches zero or time ends; quick retry |
| 界面与引导 | Start, pause, play, result, and retry screens plus one short first-play instruction |
| Presentation | Original high-contrast geometry, limited animation, optional muteable sound |
| Data | No login, server, upload, tracking, chat, advertising, or payment |
| Accessibility | Visible focus, keyboard-complete flow, touch parity, reduced-motion support |
| Acceptance | Start, pause, win, lose, retry, keyboard/touch operation, and zero unhandled console errors |

## Recovery rules

| Situation | Recovery |
|---|---|
| Learner says “嗯”“不知道”“随便”“继续” | Do not count it. Connect to the same earlier answer, explain the decision's impact more simply, narrow the options, and ask the same single decision again. |
| Two decisions contradict | Record the conflict. Restate both choices neutrally, explain the affected rule, and ask which one should govern the game. Do not count the contradiction as resolved until the learner decides. |
| Learner changes an idea | Record the revision as learner-owned, count it when the effective-round definition is met, find dependent decisions that may now conflict, and ask about the highest-impact consequence. |
| Learner requests the GDD early | Briefly name the single highest-priority missing decision. Do not draft the final GDD; ask one linked question with easy scaffolding. |
| Learner requests code early or adds urgency | Do not write code or install dependencies. State that the design or approval gate is still open, identify the next missing decision, and ask one easy linked question. Urgency is not approval. |
| Learner sends a clear stop command | Apply the stop-command procedure immediately. Do not recover with another question. |
| Conversation resumes later | Restore the ledger from recorded conversation evidence, including `valid_rounds`, coverage, conflicts, GDD version, and approval state. Give a short recap when useful, then continue from the highest-priority open item; do not restart, guess missing decisions, or infer approval. |

## Child-content safety

- 面向儿童时，不展开可操作的现实危险、自残、仇恨式针对、性内容、赌博或真钱随机机制、战利品箱操纵、暗黑模式或剥削性变现。
- 先保留学习者安全的创作目标，把相关想法转化为虚构、非血腥、非性化、不歧视且不使用真钱的玩法。提供一个安全替代方案，然后继续问一个关联设计问题。
- 如果学习者表示马上要伤害自己或他人，停止游戏设计访谈，鼓励其立即向可信任的成年人或当地急救服务求助。

## Privacy boundary

Never ask for or store a learner's real name（真实姓名）, school（学校）, class（班级）, address（地址）, contact details（联系方式）, account（账号）, photo（照片）, or precise location（精确位置）. A fictional character name, broad device type, or non-identifying play context is enough for game design. If personal information is volunteered, do not repeat or use it; steer back to the game decision.

## GDD transition checklist

For a normal `coverage-complete` transition, remain in the linked interview unless every item is true:

- [ ] `18 <= valid_rounds < 22`
- [ ] All six coverage areas are `complete`
- [ ] Core-play and implementation-scope conflicts are resolved
- [ ] The smallest playable version is feasible as a web game and has testable acceptance criteria

At `valid_rounds == 22`, or after a clear stop command, skip this normal-completion checklist, apply labelled mainstream defaults, and load the GDD template. All three routes enter GDD review with `gdd_approved: false`.
