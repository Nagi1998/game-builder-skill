# Youth Game Builder Skill

Youth Game Builder 是为小学、初中阶段学习者准备的 Codex Skill。它用适合孩子理解的中文，把学习者自己的游戏点子逐步整理成可开发的设计，并在设计获得批准后协助完成和验证网页游戏，同时保护学习者对创意的决定权。

## 触发示例

以下请求应触发本 Skill，其中最典型的表达是 `我想创作一个游戏`：

- 我想创作一个游戏，请一步一步问我。
- 我有一个网页游戏点子，但不知道怎样整理规则。
- 能陪我从零构思一个适合手机和电脑玩的小游戏吗？

寻找现成游戏、询问玩法、修复已有游戏代码、翻译现成 GDD，或只要一个代码示例而明确不要设计访谈时，不应触发这套创作流程。

## 工作流程

1. 进行对孩子友好的关联式访谈：一次只问一个主要问题；触发消息已经提供设计信息时，首个和后续设计问题都要连接这些信息，只有完全没有设计信息时才用首问引出初始创意愿景。
2. 收集不少于 20 轮有效回答，同时覆盖愿景、玩家目标、核心玩法、世界与内容、系统与体验、范围六个主题，并解决关键冲突。
3. 根据学习者已经确认的决定整理 GDD，不替学习者发明重大决定。
4. 请学习者审阅当前 GDD 版本；只有收到对该版本的明确批准，才可进入开发。
5. 依据已批准的 GDD 开发网页游戏，并完成自动化测试、浏览器检查、操作说明和试玩记录。

时间紧张、“直接做”或模糊同意都不会跳过访谈、GDD 和批准门禁；此时应把下一问变得更容易，而不是提前写代码。

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
├── references
│   ├── gdd-template.md
│   ├── interview-protocol.md
│   └── web-game-development.md
├── scripts
│   └── validate_skill.py
└── tests
    ├── __init__.py
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

## 验证

在仓库根目录依次运行：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
python3 -m json.tool evals/evals.json >/dev/null
python3 -m json.tool evals/trigger-evals.json >/dev/null
```

## GitHub

项目仓库：[Nagi1998/game-builder-skill](https://github.com/Nagi1998/game-builder-skill)
