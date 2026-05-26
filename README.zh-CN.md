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
- 把旧证据归档，让活跃 roadmap 和 handoff 保持短小。
- 只有当 artifact、decision 或 verification 存在时，才把事项标为 done。
- Open questions 只放未解决问题，不要当任务列表使用。

## Plan Tree 保存什么

一棵成熟的 planning tree 通常保存这些长期状态：

- 规划入口和阅读路径：从哪里读、哪个文件说了算。
- Roadmap 和当前进度：什么完成了、什么正在做、下一步是什么。
- Decisions：稳定决策、上下文和后果。
- Open questions：仍未解决的问题，而不是隐藏任务。
- Topics：方案图谱，包括业务流程、架构边界、验收标准、风险和执行门禁。
- Implementation status：当前交接、活跃 TODO、blockers、最近验证。
- History：旧验证、检查点和过期证据，避免污染活跃状态。

默认结构可以是：

```text
docs/plantree/
  README.md
  baseline/
  plans/<plan-name>/
    README.md
    roadmap.md
    implementation-status.md
    open-questions.md
    topics/
    decisions/
    history/
  ideas/inbox.md
```

已有成熟规划树不必强行迁移到 `docs/plantree/`。可以先注册、桥接，再逐步整理。

## 使用方式

最重要的使用方式不是记命令，而是把下面英文规则写进项目记忆文件，例如 `AGENTS.md`、团队 memory 或 agent memory。之后 provider 会在相关任务中自动使用 `plan-tree`。

```md
## Plan Tree Usage Rule

Any project planning, roadmap discussion, requirement clarification, scope negotiation, implementation strategy, progress tracking, handoff, decision recording, open-question management, or plan-to-execution coordination must use the `plan-tree` skill as the planning authority and state store.

When a request is related to planning or implementation direction, first inspect the relevant plan-tree entrypoint and current plan state when available. If no plan-tree exists and the task needs durable planning state, initialize or propose the minimal `docs/plantree/` structure according to the skill rules.

Before the solution is mature enough to implement, stay in planning and clarification mode. Deeply elicit and expand the user's intent into a concrete solution map: goals, non-goals, constraints, options, tradeoffs, risks, dependencies, acceptance criteria, verification path, and rollout or rollback notes. Record durable clarification results, open questions, assumptions, and decisions in plan-tree files when useful.

Do not start formal implementation in the main project surface while the plan still contains unresolved core ambiguity. At most, create a small isolated prototype or sample only when it helps validate the direction, and keep it clearly separate from the production path.

A plan is implementation-ready only when the scope, chosen approach, expected behavior, affected surfaces, acceptance criteria, verification method, and remaining risks are explicit enough that execution should not rely on "figure it out while coding." Once implementation-ready, proceed autonomously with the project changes, then update plan-tree status, decisions, open questions, and handoff notes to reflect the result.

`plan-tree` governs planning documents and execution readiness. It does not by itself authorize commits, pushes, releases, destructive file operations, or broad unrelated refactors unless the user explicitly asks for them.
```

## 安装

把仓库克隆到你的 skill 目录：

```bash
mkdir -p "$SKILLS_HOME"
git clone https://github.com/SeemSeam/plan-tree.git "$SKILLS_HOME/plan-tree"
```

将 `SKILLS_HOME` 设置为你的 provider 使用的 skill 根目录。也可以直接克隆到明确路径：

```bash
git clone https://github.com/SeemSeam/plan-tree.git /path/to/skills/plan-tree
```

## 仓库内容

```text
SKILL.md
agents/openai.yaml
references/maintenance-patterns.md
references/legacy-migration.md
assets/plan-tree.jpg
README.md
README.zh-CN.md
```
