# Plan Tree Maintenance Patterns

Read this reference only when the core `SKILL.md` says the task needs detailed templates, large-tree handling, decision/status/handoff/history/index maintenance, repo hygiene planning, or the expanded final-check list.

## Plan Root Template

Use this generic shape when no local convention exists:

```text
<plan-root>/
  README.md
  roadmap.md
  implementation-status.md
  open-questions.md
  topics/
    repository-cleanup-and-filesystem-plan.md
    <topic>.md
  decisions/
    README.md
    001-<decision>.md
  history/
    <optional-status-or-checkpoint-history>.md
  ideas/
    <optional-idea-or-inbox>.md
```

The tree defines document roles, not a mandatory directory template. Create only the pieces the plan actually uses. Keep topic nesting to at most two levels, such as `topics/frontend/interaction-contract.md`.

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
- Classify topic files by role when large: contracts, implementation plans, evidence/readiness, operations/runbooks, reviews, and legacy/context.
- Prefer indexes over mass renames.

## Retrieval Units

- Prefer one responsibility per Markdown file.
- Use line counts as split signals: active entrypoints/status files around 150 lines, ordinary topics around 300 lines, large contracts/history files over roughly 500 lines indexed or split.
- Split by topic, lifecycle, authority, or reader task; do not split into arbitrary part numbers.
- Use short retrieval headers on durable topic, decision, history, and expanded idea files when the tree is large. Typical fields: `Role`, `Status`, `Authority`, `Domain`, `Phase`, `Lifecycle`, `Read when`, `Related`.
- Keep controlled vocabulary small and project-local keywords defined in the nearest folder index.

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

## Index And Link Hygiene

- Create only indexes that solve a real navigation problem.
- Root README: purpose, scope, authority/order, reading paths, and links to indexes.
- Topic index: group files by role or theme with one-line descriptions.
- Decision index: group by theme/phase and show active/superseded relationships.
- Phase map: link each phase to roadmap item, implementation detail, gate/checklist, evidence, and accepted checkpoint.
- Authority map: identify which file wins when roadmap, topic, decision, and implementation status disagree.
- When adding a new topic or decision, update the nearest useful index if one exists.

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
- Specific plan roots link to `docs/plantree/baseline/README.md` or relevant baseline files.
- Durable files are discoverable from the nearest useful index or root README.
- Active roadmap and implementation-status files did not absorb completed history.
- Ideas promoted into formal artifacts are marked promoted with links.
- Open questions contain unresolved questions only.
- Large or drifting files were split, indexed, archived, or explicitly left as-is with a reason.

Content and consistency:

- Relative Markdown links introduced or touched by the edit resolve.
- Topic files that mention decisions link to them.
- Decision files are referenced from a topic, index, or roadmap when discoverability matters.
- Duplicate decisions covering the same choice are resolved or marked.
- Open questions already answered by decisions are removed or narrowed.
- Active implementation TODOs do not contradict roadmap, phase gates, or decisions.
- Completed implementation-status items have evidence such as artifact, commit, or verification note.
- Repository cleanup tasks include inventory, archive/backup rule, owner decision, and rollback note.
- Newly introduced top-level directories or generated artifacts are documented, ignored, or assigned an owner.
- Legacy plan roots affected by migration are registered, bridged, moved with updated links, or left in place with an explicit reason.
- Old plan files are not deleted or renamed without a written migration decision, source mapping, and rollback note.
- Roadmap completion claims have artifact or decision trails.
- Multiple names for the same workstream are reconciled.
- Durable leaf files have retrieval headers, folder index entries, or project-local keywords when the tree is large enough to need them.
