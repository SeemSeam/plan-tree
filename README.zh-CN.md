# Plan Tree

[English](README.md)

![Plan Tree](assets/plan-tree.jpg)

> 把短期 plans 变成一棵长期稳定、结构化的树。

`plan-tree` 是一个通用的 AI planning skill，用于长期保存项目规划状态。它把临时 provider plans、讨论、决策、开放问题、交接状态和验证证据沉淀成一棵 Markdown 规划树，让项目跨会话、跨 agent 推进时不漂移。

## 核心思想

Provider 自带的 `plan` 通常是短期的、会话内的、任务级的。它能安排“下一步做什么”，但很难长期保存“为什么这么做、哪些方案被排除、哪些问题未决、当前进度到哪里、下一次应该从哪里继续”。结果是：计划用后即丢，项目越推进越容易漂移。

AI 让这个问题更明显。过去很多项目接近 `10% 规划 + 90% 实施`：实现本身很慢，开发者有足够长的反馈周期边做边修正方向。AI 时代实现速度被大幅压缩，复杂项目更接近 `90% 规划 + 10% 实施`。这个比例不是精确工时，而是工作重心变化：质量越来越取决于前置方案是否充分、边界是否稳定、验收是否清楚、状态源是否统一。

因此工作流也必须改变：不要继续“小规划 + 小推进 + 边落盘边想”。`plan-tree` 推荐大循环模式：先充分讨论、澄清、形成可落地方案图谱，再让 AI 批量执行；执行完成后，再把进度、证据和剩余问题回写到规划树。

## Plan Tree 的意义

结构化 plans 比结构化代码更好维护，是因为 plan 的结构主要约束表达和协作；代码结构还必须承载可执行行为、历史兼容、性能、依赖、失败和变化。Roadmap、Status、Decision、Open Questions、Risks、History 这些 plan 节点是稳定的语义槽位，新信息通常可以归类进去，不必改变树的结构。代码里的模块、类、函数、接口则是可执行边界；部分校验、用户配置、失败恢复、多租户、后台重试、老数据、第三方失败和性能压力都会穿透原来的边界。

从这个角度看，`plan-tree` 是代码演化的意图空间和控制平面。代码库是实现空间；规划树是意图、约束、评价和投影空间。比如“parser 与 storage 必须解耦”不是代码，但它是作用在代码状态上的观察和约束。大部分实现变化都应该能投影回 plan：`Done`、`Blocked`、`Risk reduced`、`Decision changed` 或 `Question opened`。长期没有投影回 plan 的变化，就会变成不可见的漂移。

Plan 的漂移更容易看见：`Next` 里全是已完成事项，`Open Questions` 里有已决问题，roadmap 和 status 对不上，两个文件重复表达同一个决策。代码漂移更隐蔽：程序还能跑、测试还能过，但模块职责变宽，抽象不再贴合现实，公共工具变成杂物间，层与层之间互相知道太多。

设计和维护原则：

- 保持节点类型稳定且语义化：roadmap、status、decisions、open questions、topics、history、ideas。
- 分离意图、决策、当前状态、未解决问题、执行证据和历史细节。
- 实现中发现新事实时，先更新 plan，避免它沉淀成无记录的架构变化。
- 用链接关联文件，不要在多个地方重复同一条规则。
- 保持梗概短小，把细节拆到可检索的 capsule、detail shards、evidence 和 history。
- 把旧证据归档，让活跃 roadmap 和 handoff 保持短小。
- 只有当 artifact、decision 或 verification 存在时，才把事项标为 done。
- Open questions 只放未解决问题，不要当任务列表使用。

## Plan Tree 保存什么

一棵成熟的 planning tree 通常保存这些长期状态：

- 规划入口和阅读路径：从哪里读、哪个文件说了算。
- Roadmap 和当前进度：什么完成了、什么正在做、下一步是什么。
- Decisions：稳定决策、上下文和后果。
- Open questions：仍未解决的问题，而不是隐藏任务。
- Topics：topic capsule 和 detail shards，包括业务流程、架构边界、验收标准、风险和执行门禁。
- Implementation status：当前交接、活跃 TODO、blockers、最近验证。
- Evidence / History：验证记录、旧验证、检查点和过期证据，避免污染活跃状态。

默认结构可以是：

```text
docs/plantree/
  README.md
  baseline/
  plans/001-<plan-name>/
    README.md
    roadmap.md
    implementation-status.md
    open-questions.md
    indexes/
    topics/
      README.md
      <topic>.md
      <topic>/
        contracts.md
        alternatives.md
        edge-cases.md
    decisions/
    evidence/
    history/
  ideas/inbox.md
```

对于没有既有命名约定的新规划树，Plan root 使用项目级轻量编号，例如 `P001`，对应平铺目录 `plans/001-authentication/`。编号是稳定的创建引用，不是优先级位置：允许空号，已经分配的编号不得复用或重排。

Roadmap 中的 `T001` 等任务标签是可选的，并且只在所属 Plan 内有效。使用任务编号时，roadmap 仍是任务身份、状态和顺序的唯一活跃权威，不再建立平行的任务分配账本。受影响的代码或产品模块使用 `Affected Modules: authentication, storage` 这样的 Plan 元数据记录，其中的稳定 key 来自 `baseline/module-map.md`，不增加物理模块目录层。每次修改同时更新权威文件和必要的入口摘要，然后检查编号、模块 key、状态和链接。

已有成熟规划树不必强行迁移到 `docs/plantree/`。可以先注册、桥接，再逐步整理。
已有巨石文件也可以原地 normalize：先创建或更新 migration map，再保留短梗概，把稳定细节拆到 detail shards，把验证记录移到 evidence，把旧推理保存在 history 或 archive-only source notes。

## 版本管理

`plan-tree` 使用语义化版本管理公开发布：

- `MAJOR`：skill 契约或默认树模型出现不兼容变化。
- `MINOR`：新增 work modes、文档角色、模板或 provider metadata，且保持兼容。
- `PATCH`：措辞修正、小型文档更新和兼容性安全的细节优化。

当前版本写在 `VERSION` 文件中。发布 tag 使用 `vX.Y.Z` 格式，例如 `v0.1.0`。

## 使用方式

installer 现在会默认注入一段精简的 Provider 持久指令，使后续会话能够在规划、需求澄清、进度维护和 plan-to-execution 协调时自动使用 `plan-tree`。如果需要团队共享的项目级规则或更完整的约束，可以继续把下面的英文规则加入项目 `AGENTS.md`、`CLAUDE.md`、团队 memory 或 agent memory。

```md
## Plan Tree Usage Rule

Any project planning, roadmap discussion, requirement clarification, scope negotiation, implementation strategy, progress tracking, handoff, decision recording, open-question management, or plan-to-execution coordination must use the `plan-tree` skill as the planning authority and state store.

When a request is related to planning or implementation direction, first inspect the relevant plan-tree entrypoint and current plan state when available. If no plan-tree exists and the task needs durable planning state, initialize or propose the minimal `docs/plantree/` structure according to the skill rules.

For new Plan roots without an established project convention, use stable project-wide IDs such as `P001` with flat directories such as `plans/001-authentication/`. Keep optional task IDs in the roadmap as their sole active authority. Treat affected modules as metadata rather than physical Plan-directory parents, and never renumber IDs to express priority or status.

Before the solution is mature enough to implement, stay in planning and clarification mode. Deeply elicit and expand the user's intent into a concrete solution map: goals, non-goals, constraints, options, tradeoffs, risks, dependencies, acceptance criteria, verification path, and rollout or rollback notes. Record durable clarification results, open questions, assumptions, and decisions in plan-tree files when useful.

Do not start formal implementation in the main project surface while the plan still contains unresolved core ambiguity. At most, create a small isolated prototype or sample only when it helps validate the direction, and keep it clearly separate from the production path.

A plan is implementation-ready only when the scope, chosen approach, expected behavior, affected surfaces, acceptance criteria, verification method, and remaining risks are explicit enough that execution should not rely on "figure it out while coding." Once implementation-ready, proceed autonomously with the project changes, then update plan-tree status, decisions, open questions, and handoff notes to reflect the result.

Maintain same-change consistency: update the authoritative Plan Tree file and any required entrypoint summary together, then check IDs, paths, affected module keys, roadmap state, and relative links. Prefer read-only drift detection over watchers, automatic renumbering, or ambiguous repair.

`plan-tree` governs planning documents and execution readiness. It does not by itself authorize commits, pushes, releases, destructive file operations, or broad unrelated refactors unless the user explicitly asks for them.
```

## 安装

先从 npm 安装轻量 installer，再用 installer 安装 skill：

```bash
npm install -g plan-tree
plan-tree install codex
```

常用命令：

```bash
plan-tree version
plan-tree install claude
plan-tree install opencode
plan-tree install codex
plan-tree install all
```

也可以从 PyPI 安装同一个 `plan-tree` 命令：

```bash
python -m pip install seemseam-plan-tree
plan-tree install claude
```

npm 包通过 `bin` 字段暴露 `plan-tree` 命令。想在任意 shell 里直接运行 `plan-tree`，需要全局安装。普通的 `npm install plan-tree` 只会把命令放到 npm 的本地 binary 路径里，需要用 `npx plan-tree ...`、`npm exec plan-tree -- ...` 或 `./node_modules/.bin/plan-tree ...` 调用。

支持的安装目标：

```bash
plan-tree install claude
plan-tree install opencode
plan-tree install codex
plan-tree install all
```

默认情况下，每次安装还会在 Provider 官方的用户级全局指令文件中创建或更新一个 Plan Tree managed block：

| Provider | 持久指令文件 |
| --- | --- |
| Claude Code | `~/.claude/CLAUDE.md` |
| OpenCode | `~/.config/opencode/AGENTS.md` |
| Codex | `$CODEX_HOME/AGENTS.md`，默认是 `~/.codex/AGENTS.md` |

installer 只管理 `<!-- plan-tree:instructions:start -->` 与 `<!-- plan-tree:instructions:end -->` 之间的内容。用户原有内容和文件权限会被保留，重复安装只更新该区块。这些文件属于每次会话加载的持久指令，不会替换 Provider 内置 system prompt，也不是安全策略。

使用 `--no-instructions` 可以只安装 skill；使用 `--dry-run` 可以查看 skill 和指令目标而不写入：

```bash
plan-tree install codex --no-instructions
plan-tree install all --dry-run
```

`--force` 会替换已有 skill 目录，但不会替换整个指令文件。如果 marker 缺失、重复或顺序异常，安装器会在替换已有 skill 前停止并要求手工修复。自定义 `--target` 只改变 skill 目录，持久指令仍写入该 Provider 的官方全局路径。

skill payload 包含 `SKILL.md`、`VERSION`、README 文件、`references/`、`prompts/`、`assets/`，以及安装到 Codex 时需要的 Codex/OpenAI metadata。它不会安装 `.ccb/`、git 状态、日志、生成物或项目运行态文件。Provider 路径遵循官方 [Claude Code memory](https://code.claude.com/docs/en/memory)、[OpenCode rules](https://opencode.ai/docs/rules/) 和 [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) 文档。

本地开发或离线安装时，可以显式指定当前仓库：

```bash
plan-tree install claude --source /path/to/plan-tree
```

也可以直接把仓库克隆到你的 skill 目录：

```bash
mkdir -p "$SKILLS_HOME"
git clone https://github.com/SeemSeam/plan-tree.git "$SKILLS_HOME/plan-tree"
```

将 `SKILLS_HOME` 设置为你的 provider 使用的 skill 根目录。也可以直接克隆到明确路径：

```bash
git clone https://github.com/SeemSeam/plan-tree.git /path/to/skills/plan-tree
```

直接 clone 只会安装 skill payload；如果还需要 managed 持久指令，请使用 installer。

## 仓库内容

```text
VERSION
SKILL.md
pyproject.toml
package.json
bin/plan-tree.js
agents/openai.yaml
prompts/claude.md
prompts/opencode.md
prompts/codex.md
references/maintenance-patterns.md
references/legacy-migration.md
docs/releases/v0.4.0.md
tests/test_plantree_contract.py
tests/test_installer_instructions.py
assets/plan-tree.jpg
README.md
README.zh-CN.md
```
