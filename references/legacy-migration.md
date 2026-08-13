# Legacy Plan Tree Migration

Read this reference only when the user asks to migrate, normalize, adopt, consolidate, or make older planning documents compatible with the `docs/plantree/` layout or retrieval model.

## Migration Modes

- Adopt in place: create `docs/plantree/README.md` as the registry and link to the old tree without moving files. Use when the old tree is mature, externally referenced, or governed by repo policy.
- Bridge: create `docs/plantree/`, build baseline context, register legacy roots, and direct new numbered work to `docs/plantree/plans/<NNN>-<plan-name>/` when the project adopts that convention. Use as the default first migration step.
- Normalize in place: keep the root location, but split oversized or mixed-role files into topic capsules, detail shards, evidence records, indexes, and history archives. Use when the tree already lives under `docs/plantree/` or when moving paths would create unnecessary churn.
- Move active scope: move one coherent active Plan root into `docs/plantree/plans/<NNN>-<plan-name>/`, update links, and leave a moved stub at the old entrypoint. Use only when the mapping and ID allocation are clear.
- Archive: mark old material as superseded or archive-only, usually in place. Delete only when the user explicitly approves and a rollback/source note exists.

## Assessment Checklist

Inventory likely plan locations, including `docs/plans/`, `docs/plan/`, `plans/`, `planning/`, design-doc folders, ADR folders, implementation-status files, and repo-local docs indexes. Treat provider-native or framework-native `plans/` folders as potential conflicts until proven otherwise.

For each candidate, record:

- Entrypoint and nearest index.
- Whether it is active, historical, reference-only, or unclear.
- Owner or authority if known.
- Links from README, AGENTS, docs indexes, roadmap, decisions, or implementation status.
- Files that look like baseline context, active plan state, topics, decisions, open questions, ideas, history, evidence, or generated output.
- Line counts, mixed-role files, dense heading clusters, repeated status sections, and files that should become topic capsules plus detail shards.
- Broken or ambiguous links that must be repaired before moving.

## Target Mapping

- Project-wide architecture, module maps, runtime flows, state boundaries, and verification gates go to `docs/plantree/baseline/`.
- Active workstream Plans go to `docs/plantree/plans/<NNN>-<plan-name>/` when the target tree uses lightweight numbering; otherwise preserve its registered local convention.
- Active roadmap/status material goes to that plan root's `roadmap.md` or `implementation-status.md`.
- Durable topic summaries go to short topic capsules under `topics/`; long topic detail goes to same-name topic folders or reader-task shards.
- Stable decisions go to the nearest relevant `decisions/` folder and must be indexed or linked.
- Unresolved questions go to `open-questions.md`.
- Accepted verification records, review outcomes, and artifact evidence go to `evidence/` when they need independent retrieval.
- Low-commitment future thoughts go to `docs/plantree/ideas/inbox.md` or the plan-local ideas area.
- Completed checkpoint logs, old review detail, superseded evidence, and execution narratives go to `history/` or remain in place as archive-only material.
- Unknown material stays in place and is registered as unresolved mapping work.

## Migration Map

Before splitting or moving large existing material, create a compact migration map in the nearest `indexes/` folder or the root README if no index exists yet. Use `history/` only when recording an already-completed migration for archival traceability.

```md
# Migration Map

Date: YYYY-MM-DD

| Source | Source Role | Target | Target Role | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| `<old-path>#heading` | mixed | `<new-path>` | topic-capsule | planned | <why> |
```

Common statuses: `planned`, `moved`, `summarized`, `archive-only`, `left-in-place`, `blocked`, `unknown`.

The map is not bureaucracy; it protects searchability and makes it clear where old reasoning went.

## Safe Move Rules

- Prefer bridge before move. A working registry with legacy links is already a valid migration result.
- Move one coherent scope per pass; do not reorganize the whole docs tree at once.
- Use `git mv` for tracked files when moving inside a repository.
- Update all relative Markdown links introduced or broken by the move.
- Leave a short moved stub at the old entrypoint when external links, user habits, or provider workflows may still point there.
- Preserve old file names when they carry authority, external references, or search value.
- Do not delete old roots until every file is either migrated, archived, explicitly rejected by the user, or recorded as intentionally left behind.
- Do not archive unresolved blockers, active TODOs, current owner decisions, or unsatisfied gates.
- Do not split by arbitrary part numbers except when preserving a literal source archive. Split by retrieval role, reader task, lifecycle, authority, or domain.
- Preserve original decision rationale, rejected alternatives, important constraints, and source excerpts verbatim when they matter. Do not replace reasoning trails with summaries only.
- If an old path remains useful for search or external links, leave a moved stub or archive-only source note that points to the new active files.

Moved stub shape:

```md
# Moved

This plan moved to `<target-path>`.

Target README: `<relative-link-from-this-stub-to-target-readme>`.

Migration note: <date>, source path `<old-path>`, target path `<target-path>`, unresolved items if any.
```

## Root README Migration Notes

Add a compact migration section to `docs/plantree/README.md` when old roots exist:

```md
## Legacy Sources

| Source | Status | Target | Notes |
| --- | --- | --- | --- |
| `<old-path>` | active legacy source | `<target-or-none>` | <reason or next action> |
```

Common statuses: `active legacy source`, `bridged`, `migrated`, `superseded`, `archive-only`, `unknown`.

## Done Criteria

A legacy migration pass is complete when:

- `docs/plantree/README.md` exists and explains the authority order.
- Baseline files exist or explicitly say `Unknown / needs inventory`.
- Every touched old root is registered with status and target.
- Active migrated plans are discoverable under `docs/plantree/plans/`.
- Links are repaired or moved stubs exist.
- Oversized active files are either split into retrieval units, indexed with a reason, or recorded as follow-up work.
- Current-state files, topic capsules, evidence, and history have distinct roles after the pass.
- Deletions, if any, have explicit user approval and rollback/source notes.
- Remaining unknowns are listed as open questions or migration TODOs, not hidden.
