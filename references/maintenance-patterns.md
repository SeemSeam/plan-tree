# Plan Tree Maintenance Patterns

Read this reference only when the core `SKILL.md` says the task needs detailed templates, large-tree handling, decision/status/handoff/history/index maintenance, repo hygiene planning, or the expanded final-check list.

## Plan Root Template

Use this generic shape when no local convention exists:

```text
<NNN>-<plan-name>/
  README.md
  roadmap.md
  implementation-status.md
  open-questions.md
  indexes/
    phase-map.md
    evidence-map.md
  topics/
    README.md
    repository-cleanup-and-filesystem-plan.md
    <topic>.md                  # short topic capsule
    <topic>/
      contracts.md
      alternatives.md
      edge-cases.md
      rollout.md
  decisions/
    README.md
    001-<decision>.md
  evidence/
    README.md
    <date-or-gate>-verification.md
  history/
    <optional-status-or-checkpoint-history>.md
  ideas/
    <optional-idea-or-inbox>.md
```

The tree defines document roles, not a mandatory directory template. Create only the pieces the plan actually uses. Keep topic nesting shallow: a topic capsule can have a same-name folder for detail shards, but avoid deep trees unless an established project convention already exists.

For a new numbered Plan with no local convention, use a short entry header:

```md
Plan ID: P001
Affected Modules: `authentication`, `storage`
Related baseline: [Project baseline](../../baseline/README.md)
```

Affected module keys come from `baseline/module-map.md`. They classify impact and do not create physical parents under `plans/`.

## Retrieval Layers

Use three layers to keep large plans maintainable:

- Control layer: entrypoints, indexes, roadmap, implementation status, and topic capsules. These files are optimized for fast resume and routing.
- Knowledge layer: topic detail shards, contracts, alternatives, edge cases, rollout plans, runbooks, readiness notes, and decision records.
- Evidence/history layer: verification records, review outcomes, accepted test summaries, old execution logs, retired snapshots, and archive-only source material.

The three layers are a reading-load heuristic. The retrieval roles below are per-file classifications. For example, decisions usually live in the knowledge layer, and open questions usually live in the control layer while unresolved.

The control layer should summarize and link. It should not store long reasoning, raw logs, repeated verification output, or historical narratives.

## Ideas

- Ideas carry no commitment. They are not requirements, roadmap items, or open questions.
- When an idea matures, promote it to a roadmap item, topic, open question, or decision, and mark the original idea as promoted with a link.
- Do not force status labels or metadata on ideas.
- Periodically remove duplicates, mark promoted ideas, and delete ideas the user explicitly rejects. Do not auto-reject ideas based on age alone.

## Large Trees

Use large-tree maintenance when the root README is dense, roadmap/status files are mostly history, implementation status requires old job detail to understand, topics mix many roles, or decisions need active/superseded views.

- Keep `README.md` as an entrypoint, not the full catalog.
- Split long catalogs into local indexes such as `topics/README.md`, `decisions/README.md`, `indexes/phase-map.md`, or `indexes/authority-map.md`.
- Keep `roadmap.md` focused on current phase state and upcoming direction.
- Keep `implementation-status.md` short enough for session resume.
- Keep top-level topic files as capsules. Move contracts, alternatives, edge cases, evidence/readiness, operations/runbooks, reviews, and legacy/context to same-name topic folders or dedicated evidence/history files.
- Prefer indexes over mass renames.

## Retrieval Units

- Prefer one responsibility per Markdown file.
- Use line counts as split signals: active entrypoints/status files around 150 lines, topic capsules around 250 lines, ordinary detail shards around 400 lines, and large contracts/history/evidence files over roughly 500 lines indexed or split.
- Split by topic, lifecycle, authority, or reader task; do not split into arbitrary part numbers.
- Do not create a detail shard shorter than roughly 30 lines unless it has independent authority or retrieval value. Merge tiny detail into the parent capsule or a related shard.
- Use short retrieval headers on durable topic, decision, history, and expanded idea files when the tree is large. Typical fields: `Role`, `Status`, `Authority`, `Domain`, `Phase`, `Lifecycle`, `Read when`, `Related`.
- Keep controlled vocabulary small and project-local keywords defined in the nearest folder index.

Primary retrieval roles:

- `entrypoint`: routing, registry, authority order, and reading path.
- `current-state`: roadmap, current phase, active TODO, blockers, next target.
- `topic-capsule`: one-screen topic summary with links to detail shards.
- `detail-shard`: one reader task such as contracts, alternatives, edge cases, rollout, operations, implementation notes, or readiness.
- `decision`: stable choice with context and consequences.
- `evidence`: verification, review, artifact, or accepted test summary.
- `history`: superseded state, archive-only source material, old logs, and retired snapshots.

If a file has more than one primary role, either split it or state that it is archive-only/source material.

## Lightweight Plan And Task IDs

Use IDs only when they improve retrieval or cross-file references:

- New numbered Plan roots use `001-<stable-slug>/`, `002-<stable-slug>/`, and so on; their readable IDs are `P001`, `P002`, and so on.
- Allocate `max(retained Plan numbers) + 1`. Keep archived or retired IDs registered, allow gaps, and never renumber to express priority.
- Keep the Plan registry in the root README while it remains small. A useful shape is `ID | Plan | Affected Modules | Status | Current Phase | Last Landed | Next Target`.
- Optional roadmap labels use `T001`, `T002`, and so on within one Plan. The roadmap owns their title, state, and relative order.
- Do not create a task allocation index merely to mirror the roadmap. If old Done items leave the active roadmap, retain their IDs in linked evidence or history.
- Keep decision filename numbering local to `decisions/`. Use question IDs only when questions need durable references; do not number ideas before promotion.
- Preserve an established project's naming or issue convention. Numbering is a default for new trees, not a reason to mass-rename mature roots.

Same-change maintenance is enough by default: update the authority and required entrypoint summary, then validate uniqueness, path/metadata agreement, module keys, status consistency, and links. Add automated allocation, locks, journals, or repair only after repeated observed drift justifies them.

## Topic Capsules And Detail Shards

Use a topic capsule when a topic must be discoverable but has more detail than a session should read by default.
Use only the sections that have content; omit empty sections rather than preserving the template mechanically.

Topic capsule shape:

```md
# <Topic>

Role: topic-capsule
Status: active | planning | reference | archive-only
Read when: <reader task>
Related: <links>

## One-Screen Summary

## Current Position

## Active Constraints

## Open Risks Or Questions

## Details

- [Contracts](<topic>/contracts.md)
- [Alternatives](<topic>/alternatives.md)
- [Edge Cases](<topic>/edge-cases.md)
- [Rollout](<topic>/rollout.md)
```

Common detail shard names:

- `contracts.md`: stable boundaries, invariants, API/data contracts.
- `alternatives.md`: considered options, rejected paths, tradeoffs.
- `edge-cases.md`: tricky states, compatibility cases, failure modes.
- `implementation-notes.md`: approach detail too large for the capsule.
- `rollout.md`: deployment, migration, rollback, and operational notes.
- `readiness.md`: acceptance criteria, gates, and remaining risk.

Keep the capsule current when detail shards change. The capsule should tell a new session what matters now and where to drill in.

## Decision Records

Minimal shape:

```md
# Short Decision Title

Date: YYYY-MM-DD

## Context

Why the decision was needed.

## Decision

The chosen direction.

## Consequences

What this enables, constrains, or defers.
```

Rules:

- Keep decisions descriptive, not promotional.
- Do not rewrite old decisions as if they were made today; append a superseding decision when direction changes.
- Link decisions back to the relevant topic and roadmap item when those files exist.
- Move resolved questions out of `open-questions.md`.
- Maintain a decision index when records become numerous.
- Keep implementation progress, review outcomes, and operational evidence in status/history files rather than decision files.

## Roadmap And Status

- `Done`: only when the supporting artifact exists or the user explicitly says it is complete.
- `In Progress`: active implementation, review, or concrete next action underway.
- `Next`: unscheduled but accepted work.
- `Deferred`: intentionally postponed work.
- If a task has an ID, keep that ID when moving it between status sections. `roadmap.md` remains its sole active identity and status authority.
- Keep items short and link to source topic, decision, PR, issue, commit, artifact, or file when available.
- Move changelog detail, repeated test counts, review ids, and checkpoint narratives to history.
- Promote long roadmap sub-bullets to a phase/topic file.

## Implementation Status / Handoff

Suggested filename: `implementation-status.md`.

Minimal shape:

```md
# Implementation Status

Date: YYYY-MM-DD

## Current Phase

## Active TODO

## Done This Phase

## Blockers

## Next Commit Target

## Last Verified Commands

## Handoff Notes
```

Rules:

- Keep this file operational and short.
- Link active tasks back to roadmap items, phase details, topics, decisions, or issues.
- Reuse optional roadmap task IDs in `Active TODO`; do not maintain a second active task ledger in the handoff.
- Move completed items into `Done This Phase` with evidence such as commit hash, test command, or created artifact.
- Keep `Blockers` limited to issues that currently stop progress.
- Keep `Next Commit Target` concrete enough for a new session to resume.
- Keep old automation, CI, review job ids, and routing details out of active handoff unless they still block the next action.

## History And Archival

Good history candidates:

- Accepted checkpoint logs and older commit/test summaries.
- Review/job ids after acceptance.
- Retired phase status snapshots.
- Old verification outputs superseded by newer gate evidence.
- Resolved review findings when the final decision or fix is linked elsewhere.

Rules:

- Archive by moving stable, superseded detail behind a link.
- Keep active documents with short current summaries and pointers to history.
- Do not archive unresolved blockers, current owner decisions, active TODOs, or unsatisfied gates.
- Prefer chronological history files for execution logs and thematic history files for searchable evidence.
- Preserve original rationale, rejected alternatives, important constraints, and source excerpts verbatim when they matter. Do not replace reasoning trails with summaries only.

Archive-only source note shape:

```md
# <Original Title>

Role: archive-only
Status: migrated | superseded | reference
Preserved: verbatim source material
Migration date: YYYY-MM-DD
Target: <new capsule/detail/evidence/history link>

This file is retained for search and reasoning traceability. Active summaries and current state now live at `<target>`.
```

## Evidence Records

Use `evidence/` when verification material needs to be retrieved independently from historical narrative.

Evidence record shape:

```md
# <Gate Or Artifact> Evidence

Date: YYYY-MM-DD
Role: evidence
Status: accepted | superseded | failed | partial
Related: <roadmap/topic/decision links>

## Claim Verified

## Commands Or Checks

## Result

## Follow-Up
```

Do not paste long raw logs unless the exact output is the artifact. Summarize results, link to artifacts or CI when available, and keep failure investigation detail in a linked history or topic shard.

## Index And Link Hygiene

- Create only indexes that solve a real navigation problem.
- Root README: purpose, scope, authority/order, reading paths, and links to indexes.
- Module index: create a derived `indexes/by-module.md` only when module-based retrieval is demonstrably difficult. Never duplicate Plan files into module folders or make the module view an identity authority.
- Topic index: group files by role or theme with one-line descriptions.
- Decision index: group by theme/phase and show active/superseded relationships.
- Phase map: link each phase to roadmap item, implementation detail, gate/checklist, evidence, and accepted checkpoint.
- Authority map: identify which file wins when roadmap, topic, decision, and implementation status disagree.
- Migration map: record old path/heading, new retrieval unit, status, and unresolved mapping when normalizing an existing tree.
- When adding a new topic or decision, update the nearest useful index if one exists.

Migration map shape:

```md
# Migration Map

Date: YYYY-MM-DD

| Source | Source Role | Target | Target Role | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `<old-path>#heading` | mixed | `<new-path>` | topic-capsule | planned | <reason> |
```

Statuses: `planned`, `moved`, `summarized`, `archive-only`, `left-in-place`, `blocked`, `unknown`.

## Normalizing Existing Plan Trees

Use normalization when an existing `docs/plantree/` or legacy planning tree has oversized files, mixed responsibilities, duplicate status, or poor retrieval.

Safe sequence:

1. Inventory files, line counts, headings, inbound links, and obvious roles.
2. Create or update an index/migration map before moving content.
3. Classify material as current state, topic capsule, detail shard, decision, open question, evidence, history, idea, or unknown.
4. Create short capsules and move detail into reader-task shards.
5. Move accepted verification and review outcomes into `evidence/`; move old status and raw execution narrative into `history/`.
6. Preserve source reasoning verbatim when it contains decision rationale, rejected alternatives, or important constraints; use a detail shard, `history/`, or an archive-only source note rather than summary-only replacement.
7. Leave source stubs or archive-only notes when old paths may still be searched or externally linked.
8. Verify links and ensure unresolved blockers, active TODOs, and unsatisfied gates remain in active state.

Do not normalize the whole tree in one pass unless the tree is small. Prefer one coherent plan root, topic cluster, or oversized file at a time.

## Repository And File-Structure Hygiene

Create or update a repo hygiene topic when cleanup, restructuring, generated artifacts, legacy files, media/assets, migrations, tests, or archive/delete decisions matter.

Suggested filename: `topics/repository-cleanup-and-filesystem-plan.md`.

Minimal shape:

```md
# Repository Cleanup And Filesystem Plan

Date: YYYY-MM-DD

## Purpose

## Current Inventory

## Target Structure

## Keep / Move / Archive / Delete Rules

## Generated And Runtime Files

## Legacy Freeze Rules

## Cleanup Sequence

## Safety Checks
```

Rules:

- Inventory before deleting or moving files.
- Prefer archive/quarantine before irreversible deletion unless the user explicitly asks for deletion and the files are clearly generated/disposable.
- Preserve user-created source, docs, scripts, reusable assets, seeds, migrations, and production data unless a written rule says otherwise.
- Give generated/runtime artifacts clear ignore or cleanup rules.
- Keep old and new structures side by side during strangler/rebuild work until the old path is proven unused.
- Define target directories before moving files.
- Record git status, backup/archive path, link/import search, tests or startup smoke, and rollback path before cleanup.
- Update README or tree index when a new canonical directory or cleanup plan becomes part of the workflow.

## Expanded Final Checks

Governance and structure:

- Planning entrypoint, registered plan roots, and folder choices follow governance.
- `docs/plantree/README.md` registers stable roots under `docs/plantree/plans/`.
- New numbered roots are flat, lexically sortable, and agree with their root registry ID and Plan README metadata.
- Specific plan roots link to `docs/plantree/baseline/README.md` or relevant baseline files.
- Durable files are discoverable from the nearest useful index or root README.
- Active roadmap and implementation-status files did not absorb completed history.
- Ideas promoted into formal artifacts are marked promoted with links.
- Open questions contain unresolved questions only.
- Large or drifting files were split, indexed, archived, or explicitly left as-is with a reason.
- Active files and topic capsules stayed within the retrieval role and size budget, or a follow-up split was recorded.

Content and consistency:

- Relative Markdown links introduced or touched by the edit resolve.
- Topic files that mention decisions link to them.
- Decision files are referenced from a topic, index, or roadmap when discoverability matters.
- Duplicate decisions covering the same choice are resolved or marked.
- Open questions already answered by decisions are removed or narrowed.
- Active implementation TODOs do not contradict roadmap, phase gates, or decisions.
- Optional task IDs are unique within a Plan and have no competing active task registry.
- Affected module keys exist in `baseline/module-map.md`; module reclassification did not move or duplicate Plan roots.
- Completed implementation-status items have evidence such as artifact, commit, or verification note.
- Repository cleanup tasks include inventory, archive/backup rule, owner decision, and rollback note.
- Newly introduced top-level directories or generated artifacts are documented, ignored, or assigned an owner.
- Legacy plan roots affected by migration are registered, bridged, moved with updated links, or left in place with an explicit reason.
- Old plan files are not deleted or renamed without a written migration decision, source mapping, and rollback note.
- Roadmap completion claims have artifact or decision trails.
- Multiple names for the same workstream are reconciled.
- Durable leaf files have retrieval headers, folder index entries, or project-local keywords when the tree is large enough to need them.
- Normalization work has a migration map or equivalent source-to-target record.
