# Rollout And Verification

Role: detail-shard
Status: superseded
Lifecycle: archive-only
Read when: reviewing the original allocator and migration rollout
Related: [roadmap](../../roadmap.md), [lifecycle and sync](lifecycle-and-sync.md)

## Staged Rollout

### Stage 1 — Contract And Manual Convention

- Add the identity and synchronization contract to `SKILL.md` and maintenance guidance.
- Update English and Simplified-Chinese examples.
- Mark numbering as the default for newly created Plan Trees.
- Preserve mature existing trees unless they explicitly opt in.
- Document the manual `max + 1`, no-reuse workflow.

### Stage 2 — Read-Only Validation

- Add `plan-tree ids check` before mutation commands.
- Share fixture trees and expected diagnostics across npm and PyPI implementations.
- Make validation safe on unnumbered and partially migrated trees.
- Add CI examples without forcing them on consumers.

### Stage 3 — Allocation And Immediate Sync

- Add locked Plan and task creation.
- Add status transition and explicit slug rename commands.
- Add operation manifests and interrupted-write recovery.
- Guarantee that a command reports success only after derived views validate.

### Stage 4 — Opt-In Migration

- Inventory legacy roots and inbound links.
- Produce a stable old-to-new mapping.
- Preview all path and link changes.
- Apply only with explicit approval.
- Leave bridge stubs when old paths may be externally referenced.

## Proposed Command Surface

Names remain subject to the CLI architecture decision, but behavior should cover:

```text
plan-tree ids check [--root PATH]
plan-tree ids sync [--dry-run | --apply]
plan-tree plan add <slug>
plan-tree task add <PLAN_ID> --title <text>
plan-tree task move <TASK_ID> --status <status>
plan-tree plan rename <PLAN_ID> <new-slug> --dry-run
plan-tree ids recover [--operation <id>]
plan-tree migrate-numbering --dry-run
```

All mutating commands should support a dry run where meaningful. Ambiguous repairs stop and request owner direction.

## Acceptance Criteria

- New Plan directories sort lexically from `001` upward.
- Creating from an empty tree yields `P001`; the next allocation yields `P002`.
- Concurrent creators cannot receive the same ID.
- Deleting or retiring `P003` never causes `P003` to be reused.
- Reordering, deferring, completing, or reprioritizing a task preserves its full ID.
- Renaming a slug preserves the numeric prefix and updates all repository-local inbound links.
- A crash after reservation leaves a recoverable gap rather than a reused ID.
- Root and Plan-local ledgers distinguish allocation state from work status.
- `ids check` is read-only and returns actionable diagnostics.
- `ids sync --dry-run` is deterministic and idempotent.
- Existing unnumbered trees remain readable and unchanged by default.
- Node and Python packages pass the same behavioral fixtures.
- At width exhaustion, allocation stops with an explicit migration path.

## Verification Matrix

| Scenario | Expected Result |
| --- | --- |
| Empty project | P001/T001 allocated and all views created |
| Existing P001–P009 | P010 allocated without lexical disorder |
| Gap at P003 | Next is max + 1, not P003 |
| Duplicate P005 | Mutation blocked; validator names both locations |
| Prefix says 006, README says P007 | Mutation blocked with mismatch diagnostic |
| Two simultaneous Plan creates | Unique sequential reservations under one lock |
| Crash after reservation | Incomplete manifest detected; ID not reused |
| Task moves Next → In Progress → Done | Same task ID in every state; handoff slice synchronized |
| Slug rename | ID/prefix unchanged; links updated or ambiguity reported |
| Legacy unnumbered tree | Audit succeeds in compatibility mode; no writes |
| Migration dry run repeated | Identical mapping and patch |
| Allocation after 999 | Clean failure with width-migration guidance |

## Rollback

- Documentation-only adoption can be rolled back by disabling numbered mode for future roots; issued IDs remain as harmless stable prefixes.
- Validator rollout is read-only and can be removed without changing trees.
- Mutation tooling must keep a pre-operation manifest and original content snapshots sufficient to reverse incomplete writes.
- A completed migration rolls back through its recorded mapping and link patch, never through heuristic renumbering.
- Rollback never reclaims an issued number.
