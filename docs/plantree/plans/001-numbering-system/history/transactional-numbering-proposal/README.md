# Transactional Numbering Proposal

Role: archive-only
Status: superseded
Preserved: original transactional numbering proposal
Migration date: 2026-08-13
Target: [active lightweight contract](../../topics/numbering.md)
Related: [roadmap](../../roadmap.md), [decision 001](../../decisions/001-stable-identity-and-immediate-sync.md)

This material is retained for reasoning traceability. It proposed allocator locks, recovery journals, and synchronized derived views before the design was simplified around Plan Tree's Markdown-first control-plane model.

## One-Screen Summary

Plan Tree needs two independent concepts:

1. **Stable identity** answers “which Plan or task is this?” and never changes.
2. **Mutable order and status** answer “what should be read or done next?” and may change often.

The proposed default is:

```text
docs/plantree/plans/
  001-authentication/       # Plan ID P001
  002-storage-refactor/     # Plan ID P002
  003-release-automation/   # Plan ID P003
```

Inside `P001`, roadmap tasks use `T001`, `T002`, and so on. Their globally unambiguous forms are `P001-T001` and `P001-T002`. Decisions retain the existing three-digit filename convention and can be referenced as `P001-D001`. Open questions use `P001-Q001` when durable cross-references are useful.

## Why Three Digits

The original ergonomic goal was numbering from `01` so folders remain easy to find. Fixed-width `001` serves the same goal while preserving ordinary lexical sorting through `999` and aligning with the existing `decisions/001-...` convention. Width never expands automatically; exhaustion requires an explicit migration.

## What Changes In Real Time

IDs do not change in real time. The following views do:

- Root active-Plan registry.
- Plan roadmap status and ordering.
- Plan-local task allocation ledger when a new task is issued or retired.
- `implementation-status.md` when a Plan is actively being implemented.
- Paths and inbound links when a slug is explicitly renamed.
- Evidence links when work becomes Done.

Synchronization happens before the creating or mutating operation reports success. Manual edits are checked on the next Plan Tree operation and in CI once validation tooling exists.

## Authority Boundaries

| Concern | Authority | Derived Views |
| --- | --- | --- |
| Plan ID allocation | Root ID ledger | Plan directory prefix, Plan README, active-plan table |
| Task ID allocation | Plan-local task ledger | Roadmap labels and cross-references |
| Plan status | Root active-plan table | Optional dashboards |
| Task status and priority | `roadmap.md` | `implementation-status.md` active slice |
| Decision identity | Decision filename and metadata | Decision indexes and references |
| Question identity | Active question entry | Topic and roadmap references |

## Archived Details

- [Identity contract](identity-contract.md)
- [Lifecycle and synchronization](lifecycle-and-sync.md)
- [Rollout and verification](rollout-and-verification.md)
