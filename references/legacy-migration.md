# Legacy Plan Tree Migration

Read this reference only when the user asks to migrate, normalize, adopt, consolidate, or make older planning documents compatible with the `docs/plantree/` layout.

## Migration Modes

- Adopt in place: create `docs/plantree/README.md` as the registry and link to the old tree without moving files. Use when the old tree is mature, externally referenced, or governed by repo policy.
- Bridge: create `docs/plantree/`, build baseline context, register legacy roots, and direct all new work to `docs/plantree/plans/`. Use as the default first migration step.
- Move active scope: move one coherent active plan root into `docs/plantree/plans/<plan-name>/`, update links, and leave a moved stub at the old entrypoint. Use only when the mapping is clear.
- Archive: mark old material as superseded or archive-only, usually in place. Delete only when the user explicitly approves and a rollback/source note exists.

## Assessment Checklist

Inventory likely plan locations, including `docs/plans/`, `docs/plan/`, `plans/`, `planning/`, design-doc folders, ADR folders, implementation-status files, and repo-local docs indexes. Treat provider-native or framework-native `plans/` folders as potential conflicts until proven otherwise.

For each candidate, record:

- Entrypoint and nearest index.
- Whether it is active, historical, reference-only, or unclear.
- Owner or authority if known.
- Links from README, AGENTS, docs indexes, roadmap, decisions, or implementation status.
- Files that look like baseline context, active plan state, topics, decisions, open questions, ideas, history, evidence, or generated output.
- Broken or ambiguous links that must be repaired before moving.

## Target Mapping

- Project-wide architecture, module maps, runtime flows, state boundaries, and verification gates go to `docs/plantree/baseline/`.
- Active workstream plans go to `docs/plantree/plans/<plan-name>/`.
- Active roadmap/status material goes to that plan root's `roadmap.md` or `implementation-status.md`.
- Durable topic notes go to the plan root's `topics/`.
- Stable decisions go to the nearest relevant `decisions/` folder and must be indexed or linked.
- Unresolved questions go to `open-questions.md`.
- Low-commitment future thoughts go to `docs/plantree/ideas/inbox.md` or the plan-local ideas area.
- Completed checkpoint logs, old review detail, and one-off evidence go to `history/` or remain in place as archive-only material.
- Unknown material stays in place and is registered as unresolved mapping work.

## Safe Move Rules

- Prefer bridge before move. A working registry with legacy links is already a valid migration result.
- Move one coherent scope per pass; do not reorganize the whole docs tree at once.
- Use `git mv` for tracked files when moving inside a repository.
- Update all relative Markdown links introduced or broken by the move.
- Leave a short moved stub at the old entrypoint when external links, user habits, or provider workflows may still point there.
- Preserve old file names when they carry authority, external references, or search value.
- Do not delete old roots until every file is either migrated, archived, explicitly rejected by the user, or recorded as intentionally left behind.

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
- Deletions, if any, have explicit user approval and rollback/source notes.
- Remaining unknowns are listed as open questions or migration TODOs, not hidden.
