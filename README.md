# Plan Tree

[中文说明](README.zh-CN.md)

![Plan Tree](assets/plan-tree.jpg)

> Turn short-lived plans into a long-term, stable, structured tree.

`plan-tree` is a portable AI planning skill for keeping project planning durable. It turns temporary provider plans, discussions, decisions, open questions, handoff state, and verification evidence into a Markdown planning tree that can survive many sessions and many agents.

## Core Idea

Provider-native `plan` features are usually short-term, session-local task plans. They can answer "what should happen next", but they rarely preserve why a direction was chosen, what was rejected, which questions remain open, where progress stands, or where the next session should resume.

AI makes this failure mode sharper. Many older projects looked like `10% planning + 90% implementation`: implementation was slow enough that humans could keep correcting direction while coding. In AI-assisted work, implementation is compressed, and complex projects often move closer to `90% planning + 10% implementation`. The numbers are not exact accounting; they describe where quality is now won or lost.

That means the workflow must change. Do not keep doing small planning, small execution, and planning while mutating production files. `plan-tree` favors a larger loop: discuss and clarify first, shape an implementation-ready solution map, then let AI execute in larger batches. After execution, write progress, evidence, and remaining questions back into the planning tree.

## Why It Matters

Structured plans are easier to maintain than structured code because they organize expression and collaboration. Structured code must also carry executable behavior, compatibility, performance, dependencies, failures, and change. Plan nodes such as roadmap, status, decisions, open questions, risks, and history are stable semantic slots: new information can usually be classified without changing the tree. Code modules, classes, functions, and interfaces are executable boundaries; real requirements such as partial validation, user configuration, recovery, multi-tenancy, retries, old data, third-party failures, and performance pressure can pierce those boundaries.

In that sense, `plan-tree` acts as an intent space or control plane for code evolution. The codebase is the implementation space; the planning tree is the space of intent, constraints, evaluation, and projection. A plan item such as "parser and storage must stay decoupled" is not code, but it is a useful observation and constraint over code. Most implementation changes can project back into plan state as `Done`, `Blocked`, `Risk reduced`, `Decision changed`, or `Question opened`. Changes that never project back into the plan become invisible drift.

This is why plan drift is easier to see: `Next` contains completed work, `Open Questions` contains settled issues, roadmap and status disagree, or two files describe the same decision. Code drift is more hidden: the program may still run and tests may still pass while module ownership widens, abstractions stop matching reality, shared utilities become junk drawers, and layers learn too much about each other.

Design and maintenance principles:

- Keep node types stable and semantic: roadmap, status, decisions, open questions, topics, history, and ideas.
- Separate intent, decision, current state, unresolved uncertainty, execution evidence, and historical detail.
- Treat implementation discoveries as plan updates before they become silent architecture changes.
- Link related files instead of duplicating the same rule in many places.
- Archive old evidence so active roadmap and handoff files stay short.
- Mark work done only when the artifact, decision, or verification exists.
- Use open questions only for unresolved questions, not as a task list.

## What It Stores

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

## Versioning

`plan-tree` uses Semantic Versioning for public releases:

- `MAJOR`: incompatible changes to the skill contract or default tree model.
- `MINOR`: new work modes, document roles, templates, or provider metadata that remain compatible.
- `PATCH`: wording fixes, small documentation updates, and compatibility-safe refinements.

The current version is stored in `VERSION`. Release tags use the `vX.Y.Z` format, for example `v0.1.0`.

## Usage

The main usage pattern is to add this English memory rule to `AGENTS.md`, team memory, or agent memory. Providers can then invoke `plan-tree` automatically whenever planning, clarification, progress tracking, or plan-to-execution coordination is involved.

```md
## Plan Tree Usage Rule

Any project planning, roadmap discussion, requirement clarification, scope negotiation, implementation strategy, progress tracking, handoff, decision recording, open-question management, or plan-to-execution coordination must use the `plan-tree` skill as the planning authority and state store.

When a request is related to planning or implementation direction, first inspect the relevant plan-tree entrypoint and current plan state when available. If no plan-tree exists and the task needs durable planning state, initialize or propose the minimal `docs/plantree/` structure according to the skill rules.

Before the solution is mature enough to implement, stay in planning and clarification mode. Deeply elicit and expand the user's intent into a concrete solution map: goals, non-goals, constraints, options, tradeoffs, risks, dependencies, acceptance criteria, verification path, and rollout or rollback notes. Record durable clarification results, open questions, assumptions, and decisions in plan-tree files when useful.

Do not start formal implementation in the main project surface while the plan still contains unresolved core ambiguity. At most, create a small isolated prototype or sample only when it helps validate the direction, and keep it clearly separate from the production path.

A plan is implementation-ready only when the scope, chosen approach, expected behavior, affected surfaces, acceptance criteria, verification method, and remaining risks are explicit enough that execution should not rely on "figure it out while coding." Once implementation-ready, proceed autonomously with the project changes, then update plan-tree status, decisions, open questions, and handoff notes to reflect the result.

`plan-tree` governs planning documents and execution readiness. It does not by itself authorize commits, pushes, releases, destructive file operations, or broad unrelated refactors unless the user explicitly asks for them.
```

## Installation

Install the lightweight installer from PyPI or npm, then install the skill for your provider:

```bash
python -m pip install plan-tree
plan-tree install --provider claude
```

```bash
npm install -g plan-tree
plan-tree install --provider opencode
```

Supported providers:

```bash
plan-tree install --provider claude
plan-tree install --provider opencode
plan-tree install --provider codex
plan-tree install --provider all
```

The installer copies only the skill payload: `SKILL.md`, `VERSION`, README files, `references/`, `assets/`, and Codex/OpenAI metadata when installing for Codex. It does not install `.ccb/`, git state, logs, generated artifacts, or project runtime files.

For local development or offline installation, point the installer at this repository:

```bash
plan-tree install --provider claude --source /path/to/plan-tree
```

You can also clone this repository directly into your skill directory:

```bash
mkdir -p "$SKILLS_HOME"
git clone https://github.com/SeemSeam/plan-tree.git "$SKILLS_HOME/plan-tree"
```

Set `SKILLS_HOME` to the skill root used by your provider. Or clone directly to an explicit path:

```bash
git clone https://github.com/SeemSeam/plan-tree.git /path/to/skills/plan-tree
```

## Repository Contents

```text
VERSION
SKILL.md
pyproject.toml
package.json
bin/plan-tree.js
agents/openai.yaml
references/maintenance-patterns.md
references/legacy-migration.md
assets/plan-tree.jpg
README.md
README.zh-CN.md
```
