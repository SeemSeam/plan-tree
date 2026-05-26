---
name: plan-tree
description: Maintain a structured planning document tree made of roadmap/status files, implementation status or handoff TODO files, topic notes, decision records, open questions, ideas/inspiration pools, and repository/file-structure hygiene plans. Use when an AI agent needs to create, reorganize, audit, or update a multi-file plan, design-doc folder, roadmap tree, active implementation-status file, repo cleanup/filesystem plan, ADR/decision log, ideas inbox, or linked planning knowledge base; reconcile Done/In Progress/Next state; resume work from TODO/handoff state; move resolved questions into decisions; promote ideas into formal plan artifacts; or keep plan documents and file-structure planning internally consistent without making this project-specific.
---

# Plan Tree

Use this skill to manage Markdown planning trees while preserving the user's intent, existing document style, and reasoning trail.

## Core Workflow

For every plan-tree task:

1. Identify the plantree root, target plan root, and user intent before editing.
2. Read the root index plus only the relevant roadmap, status, topic, decision, question, idea, history, or baseline files.
3. Classify the request as idea, promotion, status, question, decision, archive, audit, resume, migrate, restructure, or consistency repair.
4. Preserve existing entrypoints, registered roots, folder names, document style, and authority order unless the task is explicitly to reorganize them.
5. Keep active roadmap and handoff files small; move historical evidence out of active state.
6. Update indexes, retrieval headers, and links when adding, moving, promoting, archiving, or splitting durable files.
7. Run final checks before replying.
8. Report changed files, unresolved questions, and the next useful maintenance action.

## Intent Routing

- `idea`: add a low-commitment thought to `ideas/inbox.md` or the local equivalent.
- `promote`: move an idea into a roadmap item, topic, open question, or decision, and link the original idea.
- `status`: update roadmap or active implementation/handoff state.
- `question`: add, narrow, or resolve an open question.
- `decision`: create or update a stable decision record.
- `archive`: move superseded evidence, old status detail, or reference-only material out of active files.
- `audit`: run consistency, retrieval, and drift checks without changing structure unless asked.
- `resume`: summarize current phase, active TODO, blockers, next target, and last verification before editing.
- `migrate`: assess or move an older planning tree toward `docs/plantree/` while preserving links, authority, and rollback evidence.

## Default Filesystem

Use `docs/plantree/` as the default cross-project filesystem for plan-tree-managed material. It is the plantree system root and registry, not a single plan root; the name avoids collisions with provider-native or framework-native `plans/` folders.

Default shape:

- `docs/plantree/README.md`: registry, authority order, baseline link, active plans table, and how to read the tree.
- `docs/plantree/baseline/`: project-wide context such as module map, runtime flows, state/storage boundaries, test/release gates, and risk hotspots.
- `docs/plantree/plans/<plan-name>/`: specific plan roots with roadmap/status, topics, decisions, open questions, and optional history.
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

- `README.md`: scope, authority, file map, reading path.
- `roadmap.md`: durable state grouped as `Done`, `In Progress`, `Next`, and `Deferred` unless the tree already uses another model.
- `implementation-status.md`: optional active handoff for current phase, active TODO, blockers, next commit target, and last verification.
- `open-questions.md`: unresolved questions only.
- `topics/`: durable context, options, constraints, implementation notes, and repo hygiene plans.
- `decisions/`: stable decisions, indexed when the set grows.
- `history/`: accepted checkpoint logs, old reviews, retired snapshots, and superseded evidence.
- `ideas/`: optional local idea pool when root-level ideas are not specific enough.

Read `references/maintenance-patterns.md` when creating templates, handling large trees, maintaining decision/status/handoff/history/index files, adding repo hygiene plans, or needing the detailed final-check checklist.

## Legacy Migration

When planning material already exists outside `docs/plantree/`, preserve it first. Do not move, rename, or delete old plan files merely because `docs/plantree/` is the default.

Read `references/legacy-migration.md` when the user asks to migrate, normalize, adopt, consolidate, or make an old plan tree compatible with the `docs/plantree/` layout.

Safe default sequence: inventory old roots, classify files by role, create/refresh `docs/plantree/` and baseline, register legacy sources in `docs/plantree/README.md`, then migrate one coherent active scope at a time only when mapping is clear.

## Governance

- A project should have one planning entrypoint. By default this is `docs/plantree/README.md`; it points to baseline, registered plan roots, and active legacy roots not yet migrated.
- Add a second plan root only when the scope is independent enough that merging it would blur ownership, authority, or retrieval.
- Name plan roots after stable project content, not dates, workers, review rounds, or one-off tasks.
- Do not scatter unregistered plan folders across the repo or create a new plan root for every task.
- Folder names should represent stable domains or document roles. Add durable folders only when the grouping has proven useful, then update the nearest index.
- Keep project-wide context in `docs/plantree/baseline/`; specific plan roots should link to it.

## Editing Rules

- Inventory before editing; touch the minimum files needed to keep the tree coherent.
- Preserve headings, language, naming style, and chronological order unless they actively prevent clarity.
- Link active tasks to roadmap items, topics, decisions, issues, commits, or verification evidence when available.
- Mark work `Done` only when the artifact exists or the user explicitly says it is complete.
- Move resolved questions out of `open-questions.md`; keep remaining uncertainty as narrower follow-up questions.
- Treat ideas as non-commitments until promoted.
- Archive evidence by moving stable, superseded detail behind links; do not delete reasoning trails just because they are noisy.
- For implementation-driving plans, verify important claims against code when cheap; flag drift as an open question rather than silently rewriting plan truth.

## Resume Workflow

When resuming planning or implementation after a new session:

1. Read `docs/plantree/README.md` when it exists.
2. Read relevant baseline files.
3. Read the target plan root `README.md`.
4. Read `implementation-status.md` or equivalent handoff file if present.
5. Read `roadmap.md` for phase context.
6. Read only active linked topic/decision/question/history files.
7. Summarize current phase, active TODO, blockers, next commit target, and last verification before editing or implementing.

## Final Checks

Before replying after edits or an audit, confirm:

- Entry point, registered roots, baseline links, and folder choices follow governance.
- Added, moved, split, promoted, archived, or migrated files are discoverable from a useful index or README.
- Active roadmap/status files did not absorb completed history, repeated evidence, or old automation/review detail.
- Open questions contain unresolved questions only; promoted ideas are marked and linked.
- Relative Markdown links introduced or touched by the edit still resolve.
- Decisions, roadmap state, implementation TODOs, and topic notes do not contradict each other.
- Migration work registers or bridges legacy roots and does not delete or rename old files without a written decision and rollback/source note.
- Repo cleanup work has inventory, owner decision, archive/delete rules, safety checks, and rollback notes.

Do not create a large framework when a short roadmap update or one decision record is enough.

## Boundaries

- This skill manages planning documents; it does not perform code review, architecture scoring, implementation, or release gating.
- Do not generate a full plan from scratch unless the user asks for one.
- Do not force `docs/plantree/` into an established mature tree without user approval.
- Do not mass-migrate or delete older plan trees in one pass; bridge first, then migrate coherent active scopes.
- Do not treat open questions as tasks.
- Do not turn implementation status into a second roadmap.
- Do not hide tradeoffs to make the tree look cleaner.
