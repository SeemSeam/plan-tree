# Plan Tree

> 把短期 plans 变成一棵长期稳定、结构化的树。
> Turn short-lived plans into a long-term, stable, structured tree.

`plan-tree` is a Codex skill for keeping project planning durable. It turns temporary provider plans, discussions, decisions, open questions, handoff state, and verification evidence into a Markdown planning tree that can survive many sessions and many agents.

`plan-tree` 是一个用于长期保存项目规划状态的 Codex skill。它把临时 provider plans、讨论、决策、开放问题、交接状态和验证证据沉淀成一棵 Markdown 规划树，让项目跨会话、跨 agent 推进时不漂移。

## 中文

### 核心思想

Provider 自带的 `plan` 通常是短期的、会话内的、任务级的。它能安排“下一步做什么”，但很难长期保存“为什么这么做、哪些方案被排除、哪些问题未决、当前进度到哪里、下一次应该从哪里继续”。结果是：计划用后即丢，项目越推进越容易漂移。

AI 让这个问题更明显。过去很多项目接近 `10% 规划 + 90% 实施`：实现本身很慢，开发者有足够长的反馈周期边做边修正方向。AI 时代实现速度被大幅压缩，复杂项目更接近 `90% 规划 + 10% 实施`。这个比例不是精确工时，而是工作重心变化：质量越来越取决于前置方案是否充分、边界是否稳定、验收是否清楚、状态源是否统一。

因此工作流也必须改变：不要继续“小规划 + 小推进 + 边落盘边想”。`plan-tree` 推荐大循环模式：先充分讨论、澄清、形成可落地方案图谱，再让 AI 批量执行；执行完成后，再把进度、证据和剩余问题回写到规划树。

### Plan Tree 保存什么

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

### 使用方式

最重要的使用方式不是记命令，而是把下面规则写进项目记忆文件，例如 `AGENTS.md`、团队 memory 或 Codex memory。之后 provider 会在相关任务中自动使用 `plan-tree`。

```md
## Plan Tree 使用规则

任何和项目规划、路线图讨论、需求澄清、范围确认、实现策略、进度把握、交接、决策记录、开放问题管理、方案到执行的推进相关的任务，都必须使用 `plan-tree` skill 作为规划权威和状态存储。

当请求涉及规划或实现方向时，优先读取已有 plan-tree 入口和当前计划状态。如果项目尚无 plan-tree，且任务需要长期规划状态，则按照 skill 规则初始化或提出最小 `docs/plantree/` 结构。

在方案尚不完善、不明晰、不足以直接实现之前，只进行规划和澄清。需要深度启发用户基于真实意图完善方案图谱，包括目标、非目标、约束、方案选项、取舍、风险、依赖、验收标准、验证路径、发布或回滚说明。必要时将稳定的澄清结果、开放问题、假设和决策记录到 plan-tree 文件中。

当计划仍存在核心歧义时，不允许提前在正式项目实现面落盘推进。最多只能创建小型、隔离、可删除的小样或原型，用于验证方向，且不得混入生产路径。

只有当范围、选定方案、预期行为、影响面、验收标准、验证方法和剩余风险都足够明确，不需要边实现边补方案时，才视为方案可落地。方案成熟后，自动推进项目修改，并在完成后回写 plan-tree 的状态、决策、开放问题和交接记录。

`plan-tree` 管理规划文档和执行就绪状态。它不默认授权 commit、push、release、破坏性文件操作或大范围无关重构，除非用户明确要求。
```

## English

### Core Idea

Provider-native `plan` features are usually short-term, session-local task plans. They can answer "what should happen next", but they rarely preserve why a direction was chosen, what was rejected, which questions remain open, where progress stands, or where the next session should resume.

AI makes this failure mode sharper. Many older projects looked like `10% planning + 90% implementation`: implementation was slow enough that humans could keep correcting direction while coding. In AI-assisted work, implementation is compressed, and complex projects often move closer to `90% planning + 10% implementation`. The numbers are not exact accounting; they describe where quality is now won or lost.

That means the workflow must change. Do not keep doing small planning, small execution, and planning while mutating production files. `plan-tree` favors a larger loop: discuss and clarify first, shape an implementation-ready solution map, then let AI execute in larger batches. After execution, write progress, evidence, and remaining questions back into the planning tree.

### What It Stores

A mature planning tree keeps durable state such as:

- Entry point and reading path.
- Roadmap and current progress.
- Stable decisions.
- Open questions.
- Topic notes for solution maps, boundaries, risks, and acceptance criteria.
- Implementation status and handoff notes.
- Historical verification and checkpoint evidence.

Default shape:

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

Mature existing planning trees do not need to be forced into `docs/plantree/`. They can be registered, bridged, and migrated gradually.

### Usage

The main usage pattern is to add the memory rule above to `AGENTS.md`, team memory, or Codex memory. Providers can then invoke `plan-tree` automatically whenever planning, clarification, progress tracking, or plan-to-execution coordination is involved.

## Installation

Clone this repository into your Codex skills directory:

```bash
mkdir -p "$CODEX_HOME/skills"
git clone https://github.com/SeemSeam/plan-tree.git "$CODEX_HOME/skills/plan-tree"
```

If `CODEX_HOME` is not set, use your Codex skills root, for example:

```bash
git clone https://github.com/SeemSeam/plan-tree.git ~/.codex/skills/plan-tree
```

## Repository Contents

```text
SKILL.md
agents/openai.yaml
references/maintenance-patterns.md
references/legacy-migration.md
README.md
```
