# Lightweight Numbering And Module Metadata

Decision ID: P001-D002
Date: 2026-08-13
Role: decision
Status: accepted
Supersedes: [P001-D001](001-stable-identity-and-immediate-sync.md)
Related: [roadmap](../roadmap.md), [numbering contract](../topics/numbering.md)

## Context

The first proposal separated stable identity from priority correctly, but added Plan and task allocation ledgers, locks, recovery journals, mutation commands, and physical module-placement considerations. For a Markdown-first planning control plane, those mechanisms create more authorities and synchronization surfaces than the original folder-ordering problem requires.

## Decision

1. New numbered Plan roots use a project-global, fixed-width ID such as `P001` and a flat directory such as `plans/001-numbering-system/`.
2. IDs are stable, monotonic, never reused, and never encode priority, status, module, owner, or date.
3. While the Plan registry is small, `docs/plantree/README.md` is its identity and lifecycle authority; split it into an index only after navigation requires it.
4. Roadmap task IDs such as `T001` are optional and Plan-local. When used, `roadmap.md` is the sole active identity and status authority; no parallel task allocation ledger is created.
5. A Plan lists zero or more affected module keys from `baseline/module-map.md`. Modules are classification metadata, not physical Plan-directory parents.
6. Maintainers use same-change consistency: update the canonical file and required entrypoint summary together, then run drift checks before finishing.
7. Read-only validation precedes automatic allocation or repair. Locks, journals, watchers, and module directories require observed need and a later decision.
8. Existing unnumbered or differently organized mature trees remain compatible and are not renamed automatically.

## Consequences

- File-browser ordering remains predictable without coupling paths to architecture or priority.
- Cross-module work is represented naturally without duplicating or moving Plan roots.
- Task identity and task status cannot drift between a roadmap and a separate ledger.
- Manual maintenance remains possible with ordinary Markdown and Git tools.
- Concurrent Plan creation is cooperatively serialized until real collision evidence justifies allocator tooling.
- Derived summaries may still drift, so final checks must compare IDs, paths, module keys, roadmap labels, status, and relative links.
