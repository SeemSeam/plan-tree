# Plan Tree

`plan-tree` is a Codex skill for maintaining structured planning documentation in Markdown. It helps teams keep roadmaps, implementation handoffs, decisions, open questions, topic notes, migration notes, and idea inboxes discoverable and consistent over time.

`plan-tree` 是一个用于维护结构化 Markdown 规划文档的 Codex skill。它帮助团队长期管理 roadmap、实现交接、决策记录、开放问题、专题笔记、迁移记录和想法收集箱，并保持这些文档之间的可发现性与一致性。

## 中文介绍

### 这个 skill 做什么

`plan-tree` 面向那些需要长期维护项目规划、设计文档和执行状态的代码仓库。它不会替你做架构评分、代码审查或发布决策，而是专注于把规划材料组织成一棵稳定、可检索、可交接的文档树。

默认文档根目录是：

```text
docs/plantree/
```

推荐结构是：

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

这些文件不是强制模板，而是一组文档角色。skill 会优先尊重已有项目结构；只有在项目没有规划入口时，才会按 `docs/plantree/` 初始化轻量文档树。

### 适合使用的场景

- 初始化一个项目级规划入口，比如 `docs/plantree/README.md`。
- 为一个功能、重构、迁移或产品方向创建独立 plan root。
- 更新 `roadmap.md`、`implementation-status.md` 或 handoff TODO。
- 记录稳定决策，并把已解决的问题从 `open-questions.md` 移走。
- 把低承诺想法写入 `ideas/inbox.md`，后续再提升为 roadmap、topic、question 或 decision。
- 迁移已有的 `plans/`、`planning/`、设计文档或 ADR 到统一入口。
- 审计规划文档之间是否有状态冲突、断链、重复历史或过大的活跃文件。

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

### 使用方式

常见提示词示例：

```text
使用 $plan-tree 初始化这个项目的规划文档树。
```

```text
用 plan-tree 给当前重构创建一个 plan root，并记录 roadmap、open questions 和 implementation status。
```

```text
用 plan-tree 审计 docs/plantree，检查 roadmap、handoff、decisions 和 open questions 是否互相矛盾。
```

```text
用 plan-tree 把 docs/plans 里的旧规划迁移到 docs/plantree，先 bridge，不要删除旧文件。
```

```text
用 plan-tree 记录一个决策：新的计划入口使用 docs/plantree/README.md，旧 plans 目录先作为 legacy source 注册。
```

### 工作流概览

每次处理规划文档时，skill 会按以下顺序工作：

1. 识别 plantree root、目标 plan root 和用户意图。
2. 只读取必要的入口、roadmap、status、topic、decision、question、idea、history 或 baseline 文件。
3. 判断请求类型，例如 idea、promotion、status、question、decision、archive、audit、resume、migrate、restructure 或 consistency repair。
4. 保留已有入口、注册关系、目录命名、文档风格和权威顺序。
5. 让活跃 roadmap 和 handoff 文件保持短小，把历史证据移动到 history 或其他稳定位置。
6. 添加、移动、提升、归档或拆分文档后，更新索引和链接。
7. 最后检查入口、注册关系、相对链接、开放问题、决策和 roadmap 状态是否一致。

### 文档治理原则

- 一个项目应该有一个主要规划入口，默认是 `docs/plantree/README.md`。
- 项目级上下文放在 `docs/plantree/baseline/`。
- 具体工作流放在 `docs/plantree/plans/<plan-name>/`。
- 想法不是承诺；只有被提升后才进入 roadmap、topic、question 或 decision。
- `open-questions.md` 只保留未解决问题。
- `roadmap.md` 只记录 durable state，避免堆积流水账。
- `implementation-status.md` 面向会话恢复和交接，应该保持短、准、可执行。
- 历史日志、旧验证结果、已接受检查点和过期审查细节应进入 `history/`。

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

### What This Skill Does

`plan-tree` is for repositories that need long-lived planning, design, and implementation state in Markdown. It does not perform code review, architecture scoring, or release approval. Its job is to keep planning material organized as a stable, searchable, and handoff-friendly document tree.

The default planning root is:

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

This is a role model, not a mandatory template. The skill preserves mature local conventions. It only bootstraps `docs/plantree/` when no useful planning entrypoint already exists.

### When To Use It

- Bootstrap a project planning entrypoint such as `docs/plantree/README.md`.
- Create a plan root for a feature, refactor, migration, or product direction.
- Update `roadmap.md`, `implementation-status.md`, or handoff TODOs.
- Record stable decisions and remove resolved questions from `open-questions.md`.
- Capture low-commitment ideas in `ideas/inbox.md` and promote them later.
- Bridge or migrate older planning folders, design docs, or ADRs into a unified entrypoint.
- Audit planning docs for drift, broken links, duplicated history, stale handoff state, or contradictory status.

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
Use plan-tree to create a plan root for the current refactor, including roadmap, open questions, and implementation status.
```

```text
Use plan-tree to audit docs/plantree for contradictions between roadmap, handoff, decisions, and open questions.
```

```text
Use plan-tree to migrate old docs/plans material into docs/plantree. Bridge first, and do not delete old files.
```

```text
Use plan-tree to record a decision: the canonical planning entrypoint is docs/plantree/README.md, and the old plans folder remains registered as a legacy source.
```

### Workflow Summary

For each planning task, the skill:

1. Identifies the plantree root, target plan root, and user intent.
2. Reads only the relevant entrypoint, roadmap, status, topic, decision, question, idea, history, or baseline files.
3. Classifies the request as idea, promotion, status, question, decision, archive, audit, resume, migrate, restructure, or consistency repair.
4. Preserves existing entrypoints, registered roots, folder names, document style, and authority order.
5. Keeps active roadmap and handoff files small, moving historical evidence out of active state.
6. Updates indexes and links when adding, moving, promoting, archiving, or splitting documents.
7. Runs final checks for entrypoints, registered roots, relative links, open questions, decisions, and roadmap consistency.

### Governance Principles

- A project should have one main planning entrypoint, usually `docs/plantree/README.md`.
- Project-wide context belongs in `docs/plantree/baseline/`.
- Specific workstreams belong in `docs/plantree/plans/<plan-name>/`.
- Ideas are not commitments until promoted into roadmap, topic, question, or decision artifacts.
- `open-questions.md` should contain unresolved questions only.
- `roadmap.md` should hold durable state, not running logs.
- `implementation-status.md` should stay short and operational for session resume and handoff.
- Checkpoint logs, old verification outputs, accepted review records, and superseded evidence belong in `history/`.

### Repository Contents

```text
SKILL.md
agents/openai.yaml
references/maintenance-patterns.md
references/legacy-migration.md
README.md
```

`SKILL.md` contains the core behavior. The `references/` files provide deeper maintenance patterns and legacy migration guidance, and are intended to be read only when the task calls for them.
