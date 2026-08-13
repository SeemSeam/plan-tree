# Stable Identity And Immediate Event-Driven Synchronization

Decision ID: P001-D001
Date: 2026-08-13
Role: decision
Status: superseded by [P001-D002](002-lightweight-numbering-and-module-metadata.md)
Related: [roadmap](../roadmap.md), [archived proposal](../history/transactional-numbering-proposal/README.md)

This decision is retained as the original design record. Its stable-identity direction remains valid, while its mandatory task ledgers and transactional synchronization model are superseded.

## Context

Number prefixes can make folders easy to scan, but using them as live priority positions would require frequent renames. Renames break links, disturb Git history, and race with concurrent agents. The current Plan Tree model also has no task identifier or synchronization runtime.

## Decision

1. Separate immutable identity from mutable priority, status, and presentation order.
2. Use project-global Plan IDs and Plan-local task, decision, and question IDs.
3. Use fixed-width three-digit numbers beginning at `001` in version 1.
4. Prefix numbered Plan directories with the Plan number; do not create a Plan directory for every task.
5. Allocate monotonically and never reuse or automatically renumber IDs.
6. Treat gaps as valid allocation history.
7. Define real-time updates as event-driven immediate consistency at a successful operation boundary.
8. Prefer explicit commands, recovery, and validation over a background filesystem watcher.
9. Keep existing unnumbered trees compatible and migrate them only through an explicit, reversible workflow.

## Consequences

- Folder order is predictable and stable, but it represents issuance order rather than current priority.
- Roadmap order and status remain the correct place for active execution ordering.
- A canonical allocation ledger is required to preserve retired IDs and explain gaps.
- Concurrent allocation requires scoped locks; instruction-only allocation cannot guarantee collision freedom.
- Multi-file mutation requires an operation manifest and reconciliation because filesystem writes are not atomically committed as a group.
- The default capacity is 999 IDs per namespace; expansion requires an explicit width migration.
- JavaScript and Python implementations need shared behavioral fixtures to prevent parity drift.
