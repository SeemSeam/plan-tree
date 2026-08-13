# Identity Contract

Role: detail-shard
Status: superseded
Lifecycle: archive-only
Read when: reviewing the original transactional identity proposal
Related: [archived proposal](README.md), [decision 001](../../decisions/001-stable-identity-and-immediate-sync.md)

## Current State

The released skill currently defines:

- Stable semantic Plan roots named `plans/<plan-name>/`.
- Roadmap items grouped by `Done`, `In Progress`, `Next`, and `Deferred`.
- A suggested decision filename `decisions/001-<decision>.md`.
- No Plan ID, task ID, question ID, allocator, counter, or reconciliation rule.

The installers copy skill files only. They do not create or mutate project Plan Trees.

## Namespace

| Entity | Canonical Form | Scope | Filesystem Form | Required? |
| --- | --- | --- | --- | --- |
| Plan | `P001` | Project-wide | `plans/001-<stable-slug>/` | Yes for newly numbered trees |
| Task | `P001-T001` | Counter is Plan-local | Normally a roadmap label; short form `T001` inside P001 | Yes for accepted roadmap work |
| Decision | `P001-D001` | Counter is Plan-local | `decisions/001-<slug>.md` | Existing filename convention remains |
| Open question | `P001-Q001` | Counter is Plan-local | Label in `open-questions.md` | When the question needs durable reference |
| Idea | None before promotion | N/A | Inbox entry | No; ideas remain non-commitments |
| Evidence | Date or gate key | Plan-local | Existing date/gate filename | No sequential ID |

The kind letter prevents a task and a decision with the same numeric suffix from being confused. The Plan prefix makes local IDs globally unambiguous without requiring a single global task counter.

## Format

- Decimal digits only.
- Fixed width of three digits in version 1.
- Sequence begins at `001`.
- Lower values are not zero, negative, dates, priorities, or semantic categories.
- Slugs use lowercase kebab-case and describe stable content.
- The numeric directory prefix must equal the Plan ID suffix.
- The ID remains fixed if a slug or title changes.

Examples:

```text
P001
P001-T004
P001-D002
P001-Q003
plans/001-numbering-system/
decisions/002-lock-and-recovery.md
```

## Allocation Invariants

1. Each namespace starts at `001`.
2. Allocate `max(all reserved, issued, and retired numbers) + 1`.
3. Never reuse a number, including after deletion, merge, cancellation, or interrupted creation.
4. Gaps are valid and are not repaired by renumbering.
5. A successful allocation is recorded in its canonical ledger.
6. A reservation left by interruption is either completed or retired; it is not reclaimed.
7. Allocation and business status are different fields.
8. Priority and Markdown order never influence the next ID.
9. Reordering never changes a directory prefix or entity ID.
10. At `999`, allocation stops with migration guidance; width does not expand silently.

## Directory Semantics

Only Plan roots receive the global numeric folder prefix. This improves scanning under `docs/plantree/plans/` without weakening the rule that a Plan root represents a stable workstream.

Tasks do not receive separate directories by default. A task that needs detail links to a topic, decision, readiness shard, evidence record, issue, or implementation artifact. This avoids recreating an unregistered mini-Plan for every TODO.

The directory order therefore represents immutable creation/issuance order, not current execution priority. Current priority remains visible in the root active-plan table and the Plan roadmap.

## Identity Versus Mutable State

| Field | Mutable? | Reason |
| --- | --- | --- |
| ID | No | Stable references and traceability |
| Numeric directory prefix | No | Mirrors Plan ID |
| Slug/title | Yes, explicitly | Domain wording can improve |
| Roadmap section | Yes | Work progresses |
| Priority/order | Yes | Execution decisions change |
| Owner | Yes | Handoffs occur |
| Evidence links | Yes, append/update | Verification accumulates |
| Allocation history | Append-only | Prevents reuse and explains gaps |

## Compatibility

- Existing mature trees remain valid and unnumbered unless their owners opt in.
- A tree may declare numbered mode for new Plan roots while registering legacy roots unchanged.
- Migration first creates a source-to-target map and validates all inbound links.
- Conflicting existing numeric prefixes are resolved through explicit mapping, never by guessing.
- External issue or ticket IDs remain external references; they do not replace Plan Tree IDs.
