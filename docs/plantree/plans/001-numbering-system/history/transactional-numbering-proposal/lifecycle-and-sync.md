# Lifecycle And Immediate Synchronization

Role: detail-shard
Status: superseded
Lifecycle: archive-only
Read when: reviewing the deferred lock, journal, and recovery design
Related: [identity contract](identity-contract.md), [rollout and verification](rollout-and-verification.md)

## Meaning Of “Real-Time”

Real-time means **immediate consistency at the successful operation boundary**. It does not mean a permanent background process watches the filesystem.

For example, `task move P001-T004 --status done` is successful only after the roadmap, active handoff slice, and required evidence reference agree. If synchronization cannot finish, the operation reports a partial transaction and leaves enough information for deterministic recovery.

## Canonical And Derived State

Canonical state must be small and explicit:

- Root ID ledger: global Plan allocations and retired IDs.
- Plan-local task ledger: task allocations and retired IDs.
- Plan `roadmap.md`: task work status and relative priority.
- Decision file: decision identity and content.
- `open-questions.md`: unresolved question identity and content.

Derived state includes the root active-plan table, implementation handoff slices, indexes, and dashboards. Derived views never allocate or redefine an ID.

## Mutation Protocol

Every allocator or mutating command follows this sequence:

1. Resolve the Plan Tree root and validate schema compatibility.
2. Acquire the narrowest safe lock: project-wide for Plan IDs and Plan-local for tasks, decisions, or questions.
3. Re-read the canonical ledger and filesystem after acquiring the lock.
4. Validate preconditions and reject duplicates or inconsistent existing state.
5. Reserve the next monotonic ID in the ledger.
6. Create or update the canonical entity.
7. Refresh all affected derived views and links.
8. Run postcondition validation.
9. Mark the reservation issued and release the lock.

If interruption occurs after step 5, recovery completes the entity or retires the reservation. It never decrements the counter or fills the gap.

## Event Matrix

| Event | Identity Behavior | Synchronized State |
| --- | --- | --- |
| Create Plan | Allocate next `Pnnn` | Ledger, directory, Plan README, root active-plan table |
| Create task | Allocate next local `Tnnn` | Task ledger and roadmap |
| Start task | Preserve ID | Move/update roadmap; add to active handoff when applicable |
| Reprioritize | Preserve ID | Reorder roadmap or update rank only |
| Complete | Preserve ID | Move to Done, attach artifact/evidence, remove from active handoff |
| Defer/resume | Preserve ID | Change roadmap section and active handoff slice |
| Rename title | Preserve ID | Update canonical title and derived labels |
| Rename slug | Preserve ID and prefix | Move path explicitly; update registry and all repository-local links |
| Archive | Preserve ID | Update canonical path/lifecycle and navigation indexes |
| Delete | Retire ID | Preserve ledger tombstone and remove derived active views |
| Merge | Preserve old IDs as superseded | Allocate/choose survivor explicitly and record relationships |
| Split | Preserve source ID | Allocate new IDs and record `split-from` relationships |
| Import | Validate requested IDs | Reserve non-conflicting IDs or create an explicit mapping |

## Locking

- Plan allocation uses one repository-scoped lock.
- Plan-local allocations use one lock per Plan.
- Lock creation must be atomic on the supported filesystem.
- Lock content records operation ID, process/agent identity when available, start time, and target scope.
- A lock timeout reports a conflict; it does not silently allocate without the lock.
- Stale locks are inspected and recovered through an explicit command. They are not deleted merely because their timestamp is old.
- Lock artifacts are runtime state and should be ignored by version control.

This design serializes only competing allocations. Independent edits to different Plans can still proceed concurrently.

## Interrupted Writes

Multi-file filesystem updates are not truly atomic, so the implementation needs a small recovery journal:

1. Write an operation manifest containing the intended ID and affected paths.
2. Reserve the ID.
3. Write changed files through temporary siblings and atomic rename where supported.
4. Validate the resulting tree.
5. Mark the manifest complete, then remove or archive it.

On the next mutation, an incomplete manifest blocks new writes in the same scope until `recover` or `check` classifies it. Read-only inspection remains available.

## Reconciliation

A read-only `ids check` operation should detect:

- Duplicate IDs or numeric prefixes.
- Ledger entries without entities and entities without ledger entries.
- Plan README IDs that disagree with directory prefixes.
- Task labels missing from the local ledger.
- IDs reused after retirement.
- Stale active-plan or handoff views.
- Broken relative links introduced by a rename or migration.
- Width overflow or mixed-width numbered directories.
- Incomplete mutation manifests and active/stale locks.

`ids sync --dry-run` produces a proposed patch. Applying repair requires an explicit flag, never changes an ID merely to close a gap, and refuses ambiguous conflicts.

## Manual Workflow Before Tooling

Until allocator commands exist, an agent that adds a Plan or task must perform the same logical transaction:

1. Inventory the ledger, filesystem, and current Git status.
2. Re-read the ledger immediately before allocating.
3. Choose `max + 1` and update the ledger, entity, and derived view in one patch.
4. Search for duplicate IDs and stale references.
5. Report any concurrency uncertainty instead of guessing.

This is cooperative concurrency rather than a hard lock. Therefore automated allocation is required before claiming safe simultaneous creation by multiple writers.

## Why No Watcher

A watcher cannot reliably determine whether a half-written Markdown edit is intentional, competes poorly with Git operations and multiple agents, and could rename paths while another tool holds them open. Event-driven commands plus read-only CI validation provide clearer success boundaries and deterministic recovery.
