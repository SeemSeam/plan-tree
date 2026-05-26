# Plan Tree

`plan-tree` is a Codex skill for turning project planning into a durable Markdown knowledge tree. It keeps long-range intent, decisions, open questions, roadmap state, execution handoffs, and verification evidence connected so AI-assisted projects do not drift while moving quickly.

`plan-tree` 是一个用于把项目规划沉淀为长期 Markdown 知识树的 Codex skill。它把长期意图、决策、开放问题、路线图状态、执行交接和验证证据连接起来，避免 AI 高速落地时项目方向漂移。

## 中文介绍

### 为什么需要 Plan Tree

很多 provider 自带的 `plan` 能力本质上是短期、临时、会话内的任务拆解。它适合回答“接下来几步做什么”，但很难形成长期组织关系：上下文、决策、开放问题、执行状态、验证证据和历史取舍往往用后即丢。项目一旦跨越多个会话、多个 agent 或多个实现批次，规划就容易漂移。

更本质的原因是工作模式变了。

过去，方案落地本身承载了巨大的工作量和时间成本，所以“小规划 + 小推进”是合理常态。人类开发者在实现过程中有足够长的反馈周期来慢慢修正方向。

可以概括为：过去很多项目接近 `10% 规划 + 90% 实施`。规划提供方向，真正的复杂度、时间和风险大多沉在人工实现里。

AI 时代不是这样。AI 的落地速度远远超过人类，但它天然偏短期记忆。继续沿用“小规划 + 小推进”，就会出现一个反直觉问题：代码和文件变化很快，但全局方案、业务边界、决策理由和验收标准没有同步变得更清晰。使用者如果还按过去的逻辑边落盘边规划，项目很容易发生漂移、腐烂和局部补丁化。

在 AI 主导实现的工作流里，比例会反过来：更接近 `90% 规划 + 10% 实施`。这里的比例不是精确工时统计，而是工作重心变化。实施本身被 AI 大幅压缩后，真正决定质量的是前置方案是否充分、边界是否稳定、验收是否明确、执行是否有统一状态源。这必然要求工作流从“边想边做”转向“先澄清方案图谱，再批量落地”。

`plan-tree` 推荐并遵从“大循环”模式：充分讨论、澄清和冻结可落地方案，然后再进入正式实现。很多复杂项目里，方案规划和讨论会承担 90% 以上的人与 AI 迭代时间；真正落地应该是基于已经清晰的方案图谱推进，而不是一边写一边临时补方向。

### Plan Tree 能提供什么

`plan-tree` 提供的不是一个固定模板，而是一套规划治理方式。成熟的 planning tree 通常能提供这些能力：

- **长期规划入口**：用一个 README 或 root index 说明当前规划树的范围、权威顺序、阅读路径和活动计划。
- **权威顺序**：明确当 roadmap、topic、decision、handoff、历史记录互相冲突时，哪个文件说了算。
- **稳定决策记录**：把真正确定的选择写入 `decisions/`，保留上下文、决策和后果，而不是让决策散落在聊天记录里。
- **开放问题管理**：把未解决问题保留在 `open-questions.md`，并且只保留真正未解决的问题，避免把问题伪装成任务。
- **方案图谱**：用 `topics/` 承载业务流程、架构边界、数据模型、交互契约、迁移策略、验收矩阵、运行手册和风险说明。
- **路线图状态**：用 `roadmap.md` 表达 `Done`、`In Progress`、`Next`、`Deferred` 和 release gate，而不是堆积流水账。
- **执行交接**：用 `implementation-status.md` 记录当前阶段、活跃 TODO、blockers、下一个提交目标和最近验证结果，让新会话能快速恢复。
- **执行门禁**：用 start brief、package contract、execution checklist、acceptance matrix 等文件把“能不能开始实现”和“怎样算完成”讲清楚。
- **历史归档**：把旧验证输出、检查点、审查记录和过期状态移入 `history/`，让活跃文件保持短小。
- **AI 检索路径**：通过索引、阅读路径和 retrieval headers，减少 agent 随机扫文件或凭短期记忆猜上下文。
- **漂移控制**：当实现中发现新字段、新状态、新业务规则、新页面契约或新风险时，先更新规划，再继续实现。

例如，一个成熟的 `docs/rebuild-plan/` 树可以包含：

```text
docs/rebuild-plan/
  README.md
  CORE.md
  roadmap.md
  implementation-status.md
  open-questions.md
  decisions/
    README.md
    001-*.md
    002-*.md
  topics/
    README.md
    domain-boundaries.md
    implementation-control.md
    first-launch-implementation-runbook.md
    package-*-start-brief.md
    package-*-execution-checklist.md
    *-package-contract.md
    *-implementation-plan.md
  history/
    README.md
    implementation-status-verification-log.md
```

这种结构能把一个大重构从“聊天里的方向”变成可执行系统：`README.md` 告诉 agent 从哪里读，`CORE.md` 定义权威顺序和漂移控制，`decisions/` 固化不可随便改的选择，`topics/` 拆解业务和技术面，`implementation-status.md` 承接当前执行状态，`history/` 保留证据但不污染活跃 handoff。

### 推荐记忆规则

建议把下面规则加入项目的 `AGENTS.md`、团队记忆文件或 Codex memory 中：

```md
## Plan Tree 使用规则

任何和项目规划、路线图讨论、需求澄清、范围确认、实现策略、进度把握、交接、决策记录、开放问题管理、方案到执行的推进相关的任务，都必须使用 `plan-tree` skill 作为规划权威和状态存储。

当请求涉及规划或实现方向时，优先读取已有 plan-tree 入口和当前计划状态。如果项目尚无 plan-tree，且任务需要长期规划状态，则按照 skill 规则初始化或提出最小 `docs/plantree/` 结构。

在方案尚不完善、不明晰、不足以直接实现之前，只进行规划和澄清。需要深度启发用户基于真实意图完善方案图谱，包括目标、非目标、约束、方案选项、取舍、风险、依赖、验收标准、验证路径、发布或回滚说明。必要时将稳定的澄清结果、开放问题、假设和决策记录到 plan-tree 文件中。

当计划仍存在核心歧义时，不允许提前在正式项目实现面落盘推进。最多只能创建小型、隔离、可删除的小样或原型，用于验证方向，且不得混入生产路径。

只有当范围、选定方案、预期行为、影响面、验收标准、验证方法和剩余风险都足够明确，不需要边实现边补方案时，才视为方案可落地。方案成熟后，自动推进项目修改，并在完成后回写 plan-tree 的状态、决策、开放问题和交接记录。

`plan-tree` 管理规划文档和执行就绪状态。它不默认授权 commit、push、release、破坏性文件操作或大范围无关重构，除非用户明确要求。
```

这条规则的重点不是增加命令参数，而是建立默认工作方式：规划、讨论、澄清和进度把握都进入 plan-tree；方案不成熟时不提前污染正式实现；方案成熟后才自动执行，并把结果回写规划树。

### 默认文件系统

默认跨项目规划根目录是：

```text
docs/plantree/
```

推荐结构：

```text
docs/plantree/
  README.md
  baseline/
    README.md
    module-map.md
    runtime-flows.md
    storage-and-state.md
    test-and-release-gates.md
    risk-hotspots.md
  plans/
    <plan-name>/
      README.md
      roadmap.md
      implementation-status.md
      open-questions.md
      topics/
      decisions/
      history/
      ideas/
  ideas/
    inbox.md
```

这些文件不是强制模板，而是一组文档角色。已有成熟规划树不需要强行搬到 `docs/plantree/`；可以先桥接、注册、逐步迁移。

### 适合使用的场景

- 初始化一个项目级规划入口。
- 为功能、重构、迁移、产品方向或发布目标创建独立 plan root。
- 把讨论中的想法变成可检索的方案图谱。
- 在实现前澄清目标、非目标、约束、风险和验收标准。
- 更新 roadmap、implementation status、handoff TODO 和 verification evidence。
- 记录稳定决策，并把已解决的问题移出 `open-questions.md`。
- 审计规划文档之间是否存在状态冲突、断链、重复历史或过大的活跃文件。
- 迁移已有的 `plans/`、`planning/`、设计文档或 ADR 到统一入口。

### 安装方法

把这个仓库放到 Codex 的 skills 目录下，并确保目录名是 `plan-tree`：

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/SeemSeam/plan-tree.git "$CODEX_HOME/skills/plan-tree"
```

如果你的 Codex 环境没有设置 `CODEX_HOME`，请把仓库克隆到你的 Codex skills 根目录下，例如：

```bash
git clone https://github.com/SeemSeam/plan-tree.git ~/.codex/skills/plan-tree
```

安装后，在 Codex 会话里提到 `plan-tree` 或 `$plan-tree` 即可触发这个 skill。

### 使用示例

```text
使用 $plan-tree 初始化这个项目的规划文档树。
```

```text
使用 plan-tree，把当前产品方向讨论整理成方案图谱，先不要改项目代码。
```

```text
用 plan-tree 审计 docs/plantree，检查 roadmap、handoff、decisions 和 open questions 是否互相矛盾。
```

```text
用 plan-tree 给当前重构创建 plan root，包含 roadmap、open questions、topics 和 implementation status。
```

```text
用 plan-tree 把 docs/plans 里的旧规划桥接到 docs/plantree，先不要移动或删除旧文件。
```

```text
基于 plan-tree 当前方案继续推进实现，完成后回写 implementation-status、roadmap 和验证结果。
```

### 仓库内容

```text
SKILL.md
agents/openai.yaml
references/maintenance-patterns.md
references/legacy-migration.md
README.md
```

`SKILL.md` 是 skill 的核心规则。`references/` 里的文档提供更详细的维护模式和旧文档迁移流程，只有在相关任务需要时才读取。

## English Guide

### Why Plan Tree Exists

Provider-native planning tools are usually short-lived task plans inside a session. They are useful for the next few steps, but they rarely form a durable organizational structure. Context, decisions, open questions, roadmap state, verification evidence, and historical tradeoffs are often discarded after use. Once a project spans multiple sessions, multiple agents, or multiple implementation batches, planning starts to drift.

The deeper reason is that the work model has changed.

In the past, implementation itself carried most of the labor and time cost. Small planning plus small execution was a reasonable default because humans had long feedback loops while coding.

In short, many projects used to look like `10% planning + 90% implementation`. Planning set direction, while most complexity, time, and risk lived in manual implementation.

AI changes that balance. AI can land changes much faster than humans, but it also tends toward short-term memory. If a project keeps using small planning plus small execution, the files can change quickly while the global solution, business boundaries, decision rationale, and acceptance criteria remain underdeveloped. Planning while landing production changes is a poor fit for vibe-coding-era work.

In an AI-led implementation workflow, the ratio often flips closer to `90% planning + 10% implementation`. The numbers are not exact time accounting; they describe a shift in where quality is won or lost. Once implementation is compressed by AI, the deciding factors become upfront solution clarity, stable boundaries, explicit acceptance criteria, and a shared source of execution state. That forces the workflow to move from "think while coding" toward "clarify the solution map first, then execute in larger batches."

`plan-tree` recommends a larger loop: discuss, clarify, and freeze an implementation-ready solution before formal execution. In complex projects, planning and discussion may take more than 90% of the human-and-AI iteration time. Implementation should then follow a clear solution map instead of inventing direction while writing files.

### What Plan Tree Provides

`plan-tree` is not a rigid template. It is a planning governance model. A mature planning tree can provide:

- **Long-term entrypoint**: a README or root index that explains scope, authority order, reading path, and active plans.
- **Authority order**: a rule for resolving conflicts between roadmap, topics, decisions, handoff notes, and history.
- **Stable decision records**: `decisions/` files that preserve context, decision, and consequences instead of scattering decisions across chat history.
- **Open-question management**: `open-questions.md` contains unresolved questions only, not hidden tasks.
- **Solution map**: `topics/` holds workflows, architecture boundaries, data models, interaction contracts, migration strategy, acceptance matrices, runbooks, and risks.
- **Roadmap state**: `roadmap.md` tracks `Done`, `In Progress`, `Next`, `Deferred`, and release gates without becoming a running log.
- **Execution handoff**: `implementation-status.md` records current phase, active TODO, blockers, next commit target, and latest verification.
- **Execution gates**: start briefs, package contracts, execution checklists, and acceptance matrices make start and completion criteria explicit.
- **History archive**: `history/` stores old verification output, checkpoints, reviews, and superseded status so active handoff files stay small.
- **AI retrieval path**: indexes, reading paths, and retrieval headers reduce random file scans and short-term-memory guesses.
- **Drift control**: when implementation discovers new fields, states, business rules, page contracts, or risks, the plan is updated before continuing.

A mature tree such as `docs/rebuild-plan/` can look like this:

```text
docs/rebuild-plan/
  README.md
  CORE.md
  roadmap.md
  implementation-status.md
  open-questions.md
  decisions/
    README.md
    001-*.md
    002-*.md
  topics/
    README.md
    domain-boundaries.md
    implementation-control.md
    first-launch-implementation-runbook.md
    package-*-start-brief.md
    package-*-execution-checklist.md
    *-package-contract.md
    *-implementation-plan.md
  history/
    README.md
    implementation-status-verification-log.md
```

That structure turns a large rebuild from chat-based direction into an executable system. `README.md` tells agents what to read. `CORE.md` defines authority and drift control. `decisions/` freezes choices that should not casually change. `topics/` decomposes business and technical surfaces. `implementation-status.md` carries the current handoff. `history/` preserves evidence without bloating active state.

### Recommended Memory Rule

Add this to `AGENTS.md`, team memory, or Codex memory:

```md
## Plan Tree Usage Rule

Any project planning, roadmap discussion, requirement clarification, scope negotiation, implementation strategy, progress tracking, handoff, decision recording, open-question management, or plan-to-execution coordination must use the `plan-tree` skill as the planning authority and state store.

When a request is related to planning or implementation direction, first inspect the relevant plan-tree entrypoint and current plan state when available. If no plan-tree exists and the task needs durable planning state, initialize or propose the minimal `docs/plantree/` structure according to the skill rules.

Before the solution is mature enough to implement, stay in planning and clarification mode. Deeply elicit and expand the user's intent into a concrete solution map: goals, non-goals, constraints, options, tradeoffs, risks, dependencies, acceptance criteria, verification path, and rollout or rollback notes. Record durable clarification results, open questions, assumptions, and decisions in plan-tree files when useful.

Do not start formal implementation in the main project surface while the plan still contains unresolved core ambiguity. At most, create a small isolated prototype or sample only when it helps validate the direction, and keep it clearly separate from the production path.

A plan is implementation-ready only when the scope, chosen approach, expected behavior, affected surfaces, acceptance criteria, verification method, and remaining risks are explicit enough that execution should not rely on "figure it out while coding." Once implementation-ready, proceed autonomously with the project changes, then update plan-tree status, decisions, open questions, and handoff notes to reflect the result.

`plan-tree` governs planning documents and execution readiness. It does not by itself authorize commits, pushes, releases, destructive file operations, or broad unrelated refactors unless the user explicitly asks for them.
```

The rule is intentionally not a command-flag system. It sets the default working mode: planning, discussion, clarification, and progress tracking go through plan-tree; immature plans do not mutate the formal implementation surface; mature plans can be implemented autonomously and then written back into the planning tree.

### Default Filesystem

The default cross-project planning root is:

```text
docs/plantree/
```

Recommended shape:

```text
docs/plantree/
  README.md
  baseline/
    README.md
    module-map.md
    runtime-flows.md
    storage-and-state.md
    test-and-release-gates.md
    risk-hotspots.md
  plans/
    <plan-name>/
      README.md
      roadmap.md
      implementation-status.md
      open-questions.md
      topics/
      decisions/
      history/
      ideas/
  ideas/
    inbox.md
```

This is a set of document roles, not a mandatory directory template. Mature existing planning trees do not need to be forced into `docs/plantree/`; they can be bridged, registered, and migrated gradually.

### When To Use It

- Bootstrap a project planning entrypoint.
- Create a plan root for a feature, refactor, migration, product direction, or release goal.
- Turn a discussion into a searchable solution map.
- Clarify goals, non-goals, constraints, risks, and acceptance criteria before implementation.
- Update roadmap, implementation status, handoff TODOs, and verification evidence.
- Record stable decisions and remove resolved questions from `open-questions.md`.
- Audit planning docs for drift, broken links, duplicated history, stale handoff state, or contradictory status.
- Bridge or migrate older planning folders, design docs, or ADRs into a unified entrypoint.

### Installation

Clone this repository into your Codex skills directory. The directory name should be `plan-tree`:

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/SeemSeam/plan-tree.git "$CODEX_HOME/skills/plan-tree"
```

If your Codex environment does not define `CODEX_HOME`, clone it into your Codex skills root, for example:

```bash
git clone https://github.com/SeemSeam/plan-tree.git ~/.codex/skills/plan-tree
```

After installation, mention `plan-tree` or `$plan-tree` in a Codex session to invoke the skill.

### Usage Examples

```text
Use $plan-tree to initialize planning docs for this project.
```

```text
Use plan-tree to turn this product direction discussion into a solution map. Do not change project code yet.
```

```text
Use plan-tree to audit docs/plantree for contradictions between roadmap, handoff, decisions, and open questions.
```

```text
Use plan-tree to create a plan root for the current refactor, including roadmap, open questions, topics, and implementation status.
```

```text
Use plan-tree to bridge old docs/plans material into docs/plantree. Do not move or delete legacy files yet.
```

```text
Continue implementation from the current plan-tree state, then update implementation-status, roadmap, and verification notes.
```

### Repository Contents

```text
SKILL.md
agents/openai.yaml
references/maintenance-patterns.md
references/legacy-migration.md
README.md
```

`SKILL.md` contains the core behavior. The `references/` files provide deeper maintenance patterns and legacy migration guidance, and are intended to be read only when the task calls for them.
