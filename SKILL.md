---
name: plan-tree
description: Use when project work involves planning, roadmap discussion, requirement clarification, scope negotiation, implementation strategy, execution-readiness checks, progress tracking, handoff, decision/open-question/evidence management, or maintaining a Markdown planning tree. Helps turn short-lived plans into stable docs/plantree state with registered plan roots, baseline, roadmap/status, topics, decisions, history, ideas, and plan-to-landing traceability across sessions and agents.
---

# Plan Tree

Use this skill as the planning workflow authority for durable project direction, execution readiness, progress state, and Markdown planning trees. It preserves the user's intent, existing document style, reasoning trail, and plan-to-landing evidence across sessions and agents.

## Required Operating Mode

For every plan-tree task, determine the work mode before editing or implementing.

- If the mode is unclear, default to `clarify` or `ready-check`, not `execute-ready`.
- When existing plan-tree state is available, inspect the relevant entrypoint and current plan state before changing direction.
- Before a solution is mature enough to implement, stay in planning and clarification mode. Expand the user's intent into goals, non-goals, constraints, options, tradeoffs, risks, dependencies, acceptance criteria, verification path, and rollout or rollback notes.
- Do not start formal implementation in the main project surface while core ambiguity remains about scope, approach, affected surfaces, expected behavior, acceptance criteria, verification path, or risks.
- A small isolated prototype or sample is allowed only when it validates a direction and remains clearly separate from the production path.
- A plan is implementation-ready only when execution should not rely on "figure it out while coding" for core decisions.
- After implementation lands, update plan-tree status, landed evidence, decisions, open questions, and handoff notes so the implementation projects back into durable plan state.

## Work Modes

Choose one primary mode at the start of a task, then transition only when the state changes.

- `clarify`: intent, scope, constraints, success criteria, or tradeoffs are unclear. Discuss, ask focused questions when needed, and record durable clarification results in plan-tree files when useful. Do not edit main project implementation files.
- `shape-plan`: the direction is mostly known but needs a concrete solution map. Create or update roadmap items, topics, assumptions, decisions, risks, acceptance criteria, and open questions.
- `ready-check`: the user wants to implement or proceed, but readiness is uncertain. Assess whether scope, approach, affected surfaces, acceptance criteria, verification, and risks are explicit enough. If not, return to `clarify` or `shape-plan`.
- `resume`: continue from prior work. Read the root entrypoint, relevant baseline, target plan README, implementation status, roadmap, and only active linked files. Summarize current phase, active TODO, blockers, next target, and last verification before editing.
- `execute-ready`: the plan is ready enough to implement. Modify project files only within the agreed scope, then update plan-tree state and evidence.
- `status-update`: update roadmap state, implementation status, Last Landed, Next Target, blockers, handoff, or plan registry after work or review.
- `archive`: move superseded detail, old status snapshots, accepted evidence, or reference-only material out of active files while preserving retrieval links.
- `normalize`: reorganize an existing plan tree or oversized mixed-role source files into smaller retrieval units. First create or update `indexes/migration-map.md` or the nearest useful index, then classify source material by retrieval role, create short capsules and reader-task detail shards, move accepted verification to `evidence/`, and move old status or reasoning narrative to `history/` without deleting source material unless explicitly approved.
- `audit` or `migrate`: inspect consistency, retrieval, drift, legacy roots, or migration mapping. Default to read-only unless the user asks to repair, normalize, or migrate.

Document actions such as `idea`, `promote`, `question`, and `decision` happen inside these modes:

- `idea`: add a low-commitment thought to `ideas/inbox.md` or the local equivalent.
- `promote`: move an idea into a roadmap item, topic, open question, or decision, and link the original idea.
- `question`: add, narrow, or resolve an unresolved question.
- `decision`: create or update a stable decision record.

## Core Workflow

For every plan-tree task:

1. Select the work mode and allowed write surface: none, plan-tree only, isolated prototype, or project files plus plan-tree update.
2. Identify the plantree root, target plan root, and user intent.
3. Read the root index plus only the relevant roadmap, status, topic, decision, question, idea, history, or baseline files.
4. Preserve existing entrypoints, registered roots, folder names, document style, and authority order unless the task is explicitly to reorganize them.
5. Keep active roadmap, handoff, and topic capsule files small; move details, evidence, and history out of active state.
6. Update indexes, retrieval headers, and links when adding, moving, promoting, archiving, or splitting durable files.
7. Run final checks before replying.
8. Report changed files, unresolved questions, the active mode, and the next useful maintenance action when relevant.

## Default Filesystem

Use `docs/plantree/` as the default cross-project filesystem for plan-tree-managed material. It is the plantree system root and registry, not a single plan root; the name avoids collisions with provider-native or framework-native `plans/` folders.

Default shape:

- `docs/plantree/README.md`: registry, authority order, baseline link, active plans table, and how to read the tree.
- `docs/plantree/baseline/`: project-wide context such as module map, runtime flows, state/storage boundaries, test/release gates, and risk hotspots.
- `docs/plantree/plans/<plan-name>/`: specific plan roots with roadmap/status, topics, decisions, open questions, evidence, indexes, and optional history.
- `docs/plantree/ideas/inbox.md`: low-commitment idea inbox.

Discovery order:

1. Use an explicit user path when provided.
2. Else use `docs/plantree/` when `docs/plantree/README.md` exists.
3. Else preserve another clearly active established tree for the current task; assess migration only when the user asks to adopt, normalize, or migrate it.
4. Else bootstrap `docs/plantree/` before creating or updating a plan.

New specific plans default to `docs/plantree/plans/<plan-name>/`, must be registered in `docs/plantree/README.md`, and should link to the relevant baseline files instead of copying global context.

## First Use

When a plan-tree task is invoked in a project without `docs/plantree/`, create a minimal root unless the user explicitly asks not to create files.

Bootstrap:

- Root: `docs/plantree/README.md`
- Baseline: `baseline/README.md`, `module-map.md`, `runtime-flows.md`, `storage-and-state.md`, `test-and-release-gates.md`, `risk-hotspots.md`
- Containers: `plans/`, `ideas/inbox.md`

Keep bootstrap content lightweight and evidence-based. If not enough code has been inspected, write `Unknown / needs inventory` instead of inventing project facts. For old or unfamiliar projects, build or refresh baseline before creating a detailed plan.

## Plan Model

Use these roles when creating or maintaining a plan root, adapting names to local convention:

- `README.md`: scope, authority, file map, reading path, and active registry when it is the plantree root. For active plan tables, prefer `Plan | Status | Current Phase | Last Landed | Next Target`.
- `roadmap.md`: durable state grouped as `Done`, `In Progress`, `Next`, and `Deferred` unless the tree already uses another model.
- `implementation-status.md`: short operational handoff for `In Progress` plans only. Planning or deferred plans usually do not need this file.
- `open-questions.md`: unresolved questions only.
- `topics/`: durable context, solution maps, options, constraints, acceptance criteria, implementation notes, repo hygiene plans, and risk analysis. Keep top-level topic files as short capsules; split large topics into topic folders with detail shards.
- `decisions/`: stable decisions, indexed when the set grows.
- `evidence/`: current or accepted verification records, review outcomes, artifact notes, and evidence indexes when these need to be retrieved independently from history.
- `history/`: accepted checkpoint logs, old reviews, retired snapshots, archive-only source notes, and superseded detail.
- `indexes/`: optional retrieval maps such as phase maps, topic maps, authority maps, migration maps, and evidence maps when local indexes solve a navigation problem.
- `ideas/`: optional low-commitment idea pool when root-level ideas are not specific enough.

Read `references/maintenance-patterns.md` when creating templates, handling large trees, maintaining decision/status/handoff/history/index files, adding repo hygiene plans, or needing the detailed final-check checklist.

## Dynamic Status And Evidence

- Only `In Progress` plans need `implementation-status.md`; `Planning` plans should express readiness in `roadmap.md`, topics, open questions, or decisions.
- Keep `implementation-status.md` operational and short. Prefer under 100 lines; if it grows, archive or index old detail.
- Keep `Active TODO` to at most five current items. More items usually means the work needs a roadmap phase, topic, or split.
- Include concrete `Current Phase`, `Next Target`, `Last Landed`, `Active TODO`, `Blocked By`, and `Last Verified` or handoff notes when applicable.
- `Last Landed` should point to a commit, artifact, test result, accepted checkpoint, or other evidence with a date when available.
- Use `evidence/README.md`, `indexes/evidence-map.md`, or the local equivalent for phase/package/gate-level evidence. Use `history/evidence-index.md` only for superseded evidence archives. Do not record every small step there.
- Active roadmap/status files should link to old evidence, not absorb repeated logs, old automation output, review job detail, or historical narratives.

## Retrieval Model

Plan-tree is a retrieval-unit system, not a place to grow large omnibus documents. Every durable file should have one primary role:

- Entrypoint or index: routing, authority order, reading paths, and one-line summaries.
- Current state: active roadmap, current phase, blockers, next target, and handoff.
- Topic capsule: a short summary of one domain, feature, constraint set, or workstream with links to detail shards.
- Detail shard: contracts, alternatives, edge cases, implementation notes, rollout, operations, readiness, or repo hygiene detail for one reader task.
- Decision: a stable choice with context and consequences.
- Evidence: verification records, review outcomes, artifact links, accepted test summaries, or evidence indexes.
- History/archive: superseded status, old execution logs, migrated source material, and retired detail.

Do not let one file carry summary, active state, decisions, long reasoning, logs, evidence, and history at the same time. If an update would make a file cross its role boundary, create or update a linked retrieval unit first, then leave only the concise summary and links in the active file.

Use these line counts as split triggers, not hard correctness tests:

- Root README, plan README, roadmap, and implementation status: keep near 150 lines or less.
- Topic capsule: keep near 250 lines or less.
- Ordinary detail shard: split or index around 400 lines.
- History or evidence files: index or split around 500 lines.

When splitting, split by reader task, lifecycle, authority, or domain. Do not create arbitrary `part-1`, `part-2` files unless preserving a literal source archive.
Do not create tiny detail shards for their own sake; if a shard would be under roughly 30 lines and has no independent retrieval value, keep it in the parent capsule or merge it with a related shard.

## Legacy Migration

When planning material already exists outside `docs/plantree/`, preserve it first. Do not move, rename, or delete old plan files merely because `docs/plantree/` is the default.

Read `references/legacy-migration.md` when the user asks to migrate, normalize, adopt, consolidate, or make an old plan tree compatible with the `docs/plantree/` layout or the retrieval model.

Safe default sequence: inventory old roots and oversized files, classify content by retrieval role, create a migration map before moving material, create/refresh `docs/plantree/` and baseline, register legacy sources in `docs/plantree/README.md`, then normalize or migrate one coherent active scope at a time only when mapping is clear.

## Governance

- A project should have one planning entrypoint. By default this is `docs/plantree/README.md`; it points to baseline, registered plan roots, and active legacy roots not yet migrated.
- Add a second plan root only when the scope is independent enough that merging it would blur ownership, authority, or retrieval.
- Name plan roots after stable project content, not dates, workers, review rounds, or one-off tasks.
- Do not scatter unregistered plan folders across the repo or create a new plan root for every task.
- Folder names should represent stable domains or document roles. Add durable folders only when the grouping has proven useful, then update the nearest index.
- Keep project-wide context in `docs/plantree/baseline/`; specific plan roots should link to it.

## Editing Rules

- Inventory before editing; touch the minimum files needed to keep the tree coherent.
- Before appending substantial content, classify it as current state, topic capsule, detail shard, decision, evidence, history, open question, or idea.
- Preserve headings, language, naming style, and chronological order unless they actively prevent clarity.
- Link active tasks to roadmap items, topics, decisions, issues, commits, artifacts, or verification evidence when available.
- Mark work `Done` only when the artifact exists or the user explicitly says it is complete.
- Move resolved questions out of `open-questions.md`; keep remaining uncertainty as narrower follow-up questions.
- Treat ideas as non-commitments until promoted.
- Archive evidence by moving stable, superseded detail behind links; do not delete reasoning trails just because they are noisy.
- During normalization, preserve original decision rationale, rejected alternatives, important constraints, and other reasoning trails verbatim in a moved detail shard, `history/`, or an archive-only source note. Do not replace reasoning with a summary only.
- Keep summaries and current-state files short. If the target file is already large, first split or index it, then add new detail to the appropriate linked retrieval unit.
- For implementation-driving plans, verify important claims against code when cheap; flag drift as an open question rather than silently rewriting plan truth.
- Treat implementation discoveries as plan updates before they become silent architecture changes.

## Resume Workflow

When resuming planning or implementation after a new session:

1. Read `docs/plantree/README.md` when it exists.
2. Read relevant baseline files.
3. Read the target plan root `README.md`.
4. Read `implementation-status.md` or equivalent handoff file if present.
5. Read `roadmap.md` for phase context.
6. Read only active linked topic, decision, question, evidence, history, and detail-shard files.
7. Summarize current phase, active TODO, blockers, next target, last landed evidence, and last verification before editing or implementing.

## Final Checks

Before replying after edits or an audit, confirm:

- The selected work mode and allowed write surface matched the user's request and plan readiness.
- Entry point, registered roots, baseline links, and folder choices follow governance.
- Added, moved, split, promoted, archived, or migrated files are discoverable from a useful index or README.
- Durable files have a single primary retrieval role or are explicitly marked as archive-only/source material.
- Active summaries, roadmaps, handoff files, and topic capsules did not absorb long detail that belongs in detail shards, evidence, or history.
- Active roadmap/status files did not absorb completed history, repeated evidence, or old automation/review detail.
- Open questions contain unresolved questions only; promoted ideas are marked and linked.
- Relative Markdown links introduced or touched by the edit still resolve.
- Decisions, roadmap state, implementation TODOs, and topic notes do not contradict each other.
- Completed work has plan-to-landing evidence when evidence is available.
- Migration work registers or bridges legacy roots and does not delete or rename old files without a written decision and rollback/source note.
- Repo cleanup work has inventory, owner decision, archive/delete rules, safety checks, and rollback notes.

Do not create a large framework when a short roadmap update or one decision record is enough.

## Boundaries

- This skill governs planning workflow, planning documents, execution readiness, and plan-to-landing traceability. It does not by itself authorize commits, pushes, releases, destructive file operations, broad unrelated refactors, or bypassing project-specific review and release gates.
- Do not generate a full plan from scratch unless the user asks for one or durable planning state is clearly needed to proceed.
- Do not force `docs/plantree/` into an established mature tree without user approval.
- Do not mass-migrate or delete older plan trees in one pass; bridge first, then migrate coherent active scopes.
- Do not treat open questions as tasks.
- Do not turn implementation status into a second roadmap or event log.
- Do not hide tradeoffs to make the tree look cleaner.
