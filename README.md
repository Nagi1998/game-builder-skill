# Youth Game Builder Skill

Youth Game Builder 是为小学、初中阶段学习者准备的 Codex Skill。它用适合孩子理解的中文，把学习者自己的游戏点子逐步整理成可开发的设计，并在设计获得批准后协助完成和验证 Web 游戏，同时保护学习者对创意的决定权。

## 触发示例

以下请求应触发本 Skill，其中最典型的表达是 `我想创作一个游戏`：

- 我想创作一个游戏，请一步一步问我。
- 我有一个网页游戏点子，但不知道怎样整理规则。
- 能陪我从零构思一个适合手机和电脑玩的小游戏吗？

寻找现成游戏、询问玩法、修复已有游戏代码、翻译现成 GDD，或只要一个代码示例而明确不要设计访谈时，不应触发这套创作流程。

## 工作流程

1. 进行对孩子友好的关联式访谈：一次只问一个主要问题；触发消息已经提供设计信息时，首个和后续设计问题都要连接这些信息，只有完全没有设计信息时才用首问引出初始创意愿景。
2. 正常访谈大致保持 18–22 轮有效回答：第 18 轮后信息足够就结束，只有关键缺口才继续，第 22 轮后绝不再问。
3. 学习者发送“停止”或“停止提问”时，立即结束问答，用安全、主流、轻量的默认方案补齐全部剩余设计，并清楚标出哪些是系统默认。
4. 根据学习者决定和必要的已标注默认项整理完整 GDD。
5. 请学习者审阅当前 GDD 版本；“停止”不代表批准，只有收到对该版本的明确批准，才可进入开发。
6. 依据已批准的 GDD 开发 Web 游戏，并完成自动化测试、浏览器检查、操作说明和试玩记录。

时间紧张或“直接做”不会提前写代码；它们仍按 18–22 轮规则推进。明确“停止”会自动生成待批准 GDD，但模糊同意仍不会跳过 GDD 批准门禁。

## Web 游戏技术范围

- 最终只生成浏览器可运行的静态 Web 游戏，入口为 `game/index.html`，可直接双击离线运行。
- 默认采用原生 HTML5、CSS、JavaScript、DOM 或 Canvas 2D，无需玩家安装 Node.js 或其他开发工具。
- 保留轻量 3D：当创意或已批准 GDD 确实需要时，可使用低负载 WebGL 和随项目本地交付的 Three.js 类轻量库。
- 不默认使用 Unity、Unreal、Godot、WebGPU、复杂物理、实时阴影、全屏后处理、npm 构建链、后端、CDN 或联网服务。
- 面向多数 Windows 10/11 与 macOS 主流浏览器，不要求独立显卡；首版资源控制在 10 MB 内。

## 安全与隐私

- 不询问或记录学习者的真实姓名、学校、班级、地址、联系方式、账号、照片或精确位置。
- 不要求登录、公开发布或分享个人资料来完成设计流程。
- 始终使用适合小学、初中生理解的中文，并根据学习者选择的年龄段调整表达难度。
- 不展开可操作的现实危险、自残、仇恨式针对、性内容、赌博或真钱随机机制、战利品箱操纵、暗黑模式或剥削性变现；把安全的创作目标改写为虚构、非血腥、非性化、不歧视且不使用真钱的玩法。
- 如果学习者表示马上要伤害自己或他人，停止游戏设计访谈，并鼓励其立即向可信任的成年人或当地急救服务求助。

## 仓库结构

```text
.
├── README.md
├── SKILL.md
├── evals
│   ├── baseline-findings.md
│   ├── evals.json
│   └── trigger-evals.json
├── integrations
│   ├── agents/AGENTS.md
│   ├── claude/CLAUDE.md
│   ├── copilot/copilot-instructions.md
│   ├── cursor/game-builder-interview.mdc
│   ├── gemini/GEMINI.md
│   └── shared/interview-contract.md
├── references
│   ├── gdd-template.md
│   ├── interview-protocol.md
│   └── web-game-development.md
├── scripts
│   ├── install_integration.py
│   ├── preview_game.py
│   └── validate_skill.py
└── tests
    ├── __init__.py
    ├── test_platform_integrations.py
    ├── test_skill_content.py
    └── test_validator.py
```

## 安装

先克隆仓库：

```bash
git clone https://github.com/Nagi1998/game-builder-skill.git
```

然后找到你的 Codex 配置所使用的 Skills 目录，把整个仓库复制或移动到该目录，并将目标文件夹命名为 `youth-game-builder`。不同安装方式的 Skills 目录可能不同，因此这里不假定固定的 `CODEX_HOME`：

```bash
cp -R game-builder-skill "<你的 Codex Skills 目录>/youth-game-builder"
```

重新启动或刷新 Codex 后，可用“我想创作一个游戏”开始一次新项目。

## 跨工具安装（推荐）

`SKILL.md` 是 Codex 的 Skill 格式；其他 coding 工具不会因为仓库中有这个文件而自动启用问答。因此要把对应的规则文件安装到**准备创作游戏的目标项目根目录**，再在该项目中新开对话并输入“我想创作一个游戏”。规则会要求首条回复用中文提出恰好一个设计问题，不会直接写代码。

从本仓库根目录运行下面的命令；把 `<目标游戏项目>` 换成你要创建游戏的项目文件夹。安装器会同时放入规则文件和 `.game-builder/preview_game.py` 预览助手；它不会覆盖已有文件，遇到同名文件会安全停止。

| 使用工具 | 命令 |
| --- | --- |
| Cursor | `python3 scripts/install_integration.py --tool cursor --target "<目标游戏项目>"` |
| GitHub Copilot | `python3 scripts/install_integration.py --tool copilot --target "<目标游戏项目>"` |
| Gemini CLI | `python3 scripts/install_integration.py --tool gemini --target "<目标游戏项目>"` |
| Claude Code | `python3 scripts/install_integration.py --tool claude --target "<目标游戏项目>"` |
| 支持 AGENTS.md 的工具 | `python3 scripts/install_integration.py --tool agents --target "<目标游戏项目>"` |

如果安装器提示目标位置已有规则，请保留原文件，并把相应 `integrations/` 文件中的“青少年游戏创作问答”章节合并到原有规则中。不要直接覆盖它。Cursor 可关闭并重新打开目标项目；Gemini CLI 可在目标项目中执行 `/memory reload` 后再开始对话。

## 验证

在仓库根目录依次运行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
python3 -m unittest tests.test_platform_integrations -v
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool evals/trigger-evals.json >/dev/null
```

## GitHub

项目仓库：[Nagi1998/game-builder-skill](https://github.com/Nagi1998/game-builder-skill)
