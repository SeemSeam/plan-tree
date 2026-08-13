# Repository Cleanup And Filesystem Plan

Date: 2026-08-13
Role: detail-shard
Status: completed
Read when: normalizing P001 or adding repository-level contract tests
Related: [migration map](../indexes/migration-map.md)

## Purpose

Reduce duplicate planning authorities while preserving the first numbering proposal and adding a small test surface for drift detection.

## Current Inventory

- The active P001 topic is split across one capsule and three detail shards.
- Plan and task allocations are duplicated in separate registries and current-state files.
- The repository has no committed automated tests.
- Untracked files under `docs/papers/` predate P001 and are unrelated user material.

## Target Structure

- One active numbering capsule under `topics/numbering.md`.
- One roadmap as the task identity and status authority.
- One small project Plan registry in `docs/plantree/README.md`.
- Superseded transactional detail under `history/transactional-numbering-proposal/`.
- Standard-library contract tests under `tests/`.

## Keep / Move / Archive / Delete Rules

- Keep stable decisions; supersede them through a new decision rather than rewriting history.
- Move detailed lock, journal, allocator, and watcher reasoning to history.
- Merge allocation facts into their current authoritative files.
- Delete only redundant registry files after their information is represented elsewhere.
- Do not modify, move, stage, or delete `docs/papers/`.

## Generated And Runtime Files

Tests may create only temporary directories through the platform temporary-file API. No generated artifacts belong in the repository.

## Cleanup Sequence

1. Record the migration map.
2. Create the lightweight contract and superseding decision.
3. Archive the original detail shards.
4. Remove redundant registries and update indexes/links.
5. Add and run drift tests.
6. Record verification evidence and final status.

Completed on 2026-08-13. The separate [Luna semantic drift audit](../evidence/2026-08-13-luna-drift-audit.md) also passed with no corrective action.

## Safety Checks

- Capture `git status` before and after changes.
- Verify every local Markdown link.
- Compare Plan IDs with directory prefixes and the root registry.
- Compare roadmap task IDs for uniqueness without a second task ledger.
- Confirm unrelated untracked files remain unchanged.
