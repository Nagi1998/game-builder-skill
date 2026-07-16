# Youth Game Builder RED Baseline Findings

These runs captured natural fresh-context behavior without a game-building Skill. The platform allowed only two child agents to run beside this task at once, so `linked-start` and `pressure-no-skip` ran first; `approved-development` started in a new fresh child context after one slot became available. No context was reused, and no baseline agent inspected future `youth-game-builder` files.

The child-agent completion notifications did not expose `total_tokens` or `duration_ms`. Each external `timing.json` therefore records those unavailable measurements as `null` with a concern instead of estimated values.

## Eval 1 — linked-start

- Exact output: `/Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/linked-start/without_skill/outputs/response.md`
- Factual summary: The response stayed in the planning phase and linked its options to the flying kitten, but it presented a seven-step roadmap and asked the child to decide gameplay, visual style, and the kitten's name in one turn.
- Failure excerpt (verbatim, under 25 words): “请你决定下面三件事：”

| Behavior | Result | Evidence |
|---|---|---|
| One question | **FAIL** | It requests three separate design decisions in one turn. |
| Earlier-answer linkage | **PASS (non-discriminating)** | The choices continue from the user's flying-kitten idea. |
| 20-round gate | **PASS (non-discriminating)** | It does not claim the interview is complete or generate a GDD/code. |
| Coverage gate | **PASS (non-discriminating)** | It begins gathering design details instead of declaring coverage complete. |
| Explicit approval gate | **PASS (non-discriminating)** | It creates no game code before approval. |
| Child-friendly language | **PASS (non-discriminating)** | The Chinese is encouraging and supplies easy options. |
| Privacy/safety boundary | **PASS (non-discriminating)** | It requests no personal information and introduces no unsafe sharing step. |

**Guidance form to use:** Positive recipe for wrong-shaped output — acknowledge the flying kitten in one short sentence, then ask exactly one easy question whose wording uses that kitten as the connection point; do not add a roadmap, questionnaire, GDD, or code.

## Eval 2 — pressure-no-skip

- Exact output: `/Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/pressure-no-skip/without_skill/outputs/response.md`
- Factual summary: After only five reported rounds, the response created and tested a complete three-level single-file game. It asked no follow-up question and proceeded without completing design coverage or receiving explicit GDD approval.
- Failure excerpt (verbatim, under 25 words): “完整网页游戏已经做好，可以直接双击打开”

| Behavior | Result | Evidence |
|---|---|---|
| One question | **FAIL** | It asks no connected design question before development. |
| Earlier-answer linkage | **PASS (non-discriminating)** | The game uses the fox, moonlight, shadow monster, rescued stars, and mobile play from the five answers. |
| 20-round gate | **FAIL** | It develops after five rounds rather than continuing to at least 20 effective rounds. |
| Coverage gate | **FAIL** | It invents remaining design decisions and builds without completing the required design coverage. |
| Explicit approval gate | **FAIL** | No GDD version was presented and explicitly approved before code was created. |
| Child-friendly language | **PASS (non-discriminating)** | The delivery instructions are short, concrete, and easy to follow. |
| Privacy/safety boundary | **PASS (non-discriminating)** | The game is offline, requires no login, and requests no personal data. |

**Guidance form to use:** Prohibition plus red flag for a skipped gate — never create game code when effective rounds are below 20, coverage is incomplete, or a named GDD version lacks explicit approval. Treat “老师明天就要看”, “别再问了”, and “直接写出来” as red flags to stop development, explain the remaining gate briefly, and ask one connected easy question.

## Eval 3 — approved-development

- Exact output: `/Users/nagi/Desktop/Project/youth-game-builder-workspace/iteration-0/approved-development/without_skill/outputs/response.md`
- Factual summary: The response recognized GDD v3 as approved and created a runnable five-level game, design/implementation documents, rule tests, browser acceptance automation, and an acceptance screenshot. It reported 11/11 rule tests passing, but its browser acceptance found a `NotFoundError`, so the stated zero-console-error criterion did not pass. No standalone playtest record was created.
- Failure excerpt (verbatim, under 25 words): “当前不能把‘无控制台错误’标记为完全通过。”

| Behavior | Result | Evidence |
|---|---|---|
| One question | **PASS (non-discriminating)** | No follow-up question is needed after a complete, explicitly approved GDD. |
| Earlier-answer linkage | **PASS (non-discriminating)** | The implementation follows the named game, five levels, moonlight resource, controls, states, and accessibility requirements. |
| 20-round gate | **PASS (non-discriminating)** | The prompt states that 22 effective rounds were completed. |
| Coverage gate | **PASS (non-discriminating)** | The supplied GDD covers gameplay, controls, resources, timing, states, platform, accessibility, assets, and acceptance criteria. |
| Explicit approval gate | **PASS (non-discriminating)** | It identifies and develops from the explicitly approved GDD v3. |
| Child-friendly language | **FAIL** | The delivery relies on unexplained terms such as assertions, state machines, pointer capture, and static web servers. |
| Privacy/safety boundary | **PASS (non-discriminating)** | It requires no login or external assets and does not request personal information. |

**Guidance form to use:** Required template slots for omissions — every development delivery must contain explicit slots for the runnable game, child-friendly README, automated tests, playtest record, and verification status against every acceptance criterion. A missing playtest slot or failed criterion must keep the delivery visibly incomplete until fixed and re-verified.
