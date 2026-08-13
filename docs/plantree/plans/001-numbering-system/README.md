# Numbering System

Plan ID: P001
Role: entrypoint
Status: Done
Updated: 2026-08-13
Affected Modules: `skill-contract`, `maintenance-guidance`, `public-docs`
Related baseline: [Project baseline](../../baseline/README.md)

## Goal

Introduce lightweight identifiers that keep Plan folders predictably sorted and make durable work easy to reference without turning Plan Tree into a task database or transaction engine.

## Scope

- Stable Plan IDs and flat numbered Plan directory prefixes.
- Optional Plan-local task and open-question references.
- Module classification as metadata rather than physical path ownership.
- Same-change consistency and drift-focused final checks.
- Compatibility rules for existing unnumbered trees.

## Non-Goals

- Treating every TODO as a separate Plan directory.
- Encoding priority, status, owner, phase, or dates into an immutable ID.
- Continuously renumbering folders to remove gaps.
- Requiring module folders, a background watcher, locks, or recovery journals.
- Maintaining a second task allocation ledger beside `roadmap.md`.
- Adding automatic allocation or repair before repeated drift demonstrates the need.
- Automatically migrating existing trees without an explicit dry run and approval.

## Current Position

Use fixed-width, three-digit Plan IDs for new numbered trees. `P001` maps to `plans/001-<stable-slug>/`; mutable execution order stays in `roadmap.md`. Task IDs such as `T001` are optional, Plan-local labels used only when stable cross-references help, and the roadmap is their sole active authority.

Affected code or product modules are declared in Plan metadata using keys from the baseline module map. Changing module impact does not move a Plan directory or change its ID. Maintainers update the canonical file and required entrypoint summaries in the same change, then validate IDs, module keys, status consistency, and links.

## Reading Path

1. [Roadmap](roadmap.md)
2. [Numbering contract](topics/numbering.md)
3. [Lightweight numbering decision](decisions/002-lightweight-numbering-and-module-metadata.md)
4. [Open questions](open-questions.md)
5. Read the [archived transactional proposal](history/transactional-numbering-proposal/README.md) only when reconsidering automation.

## Plan Files

| File | Role |
| --- | --- |
| [roadmap.md](roadmap.md) | Current planning state. |
| [topics/numbering.md](topics/numbering.md) | Active lightweight contract. |
| [decisions/002-lightweight-numbering-and-module-metadata.md](decisions/002-lightweight-numbering-and-module-metadata.md) | Current design decision. |
| [open-questions.md](open-questions.md) | Deferred, non-blocking automation trigger. |
| [evidence/2026-08-13-lightweight-numbering-contract.md](evidence/2026-08-13-lightweight-numbering-contract.md) | Local contract and installer verification. |
| [evidence/2026-08-13-luna-drift-audit.md](evidence/2026-08-13-luna-drift-audit.md) | Independent weak-model semantic drift review. |
| [history/2026-08-13-implementation-status.md](history/2026-08-13-implementation-status.md) | Archived implementation handoff; not active authority. |

## Readiness

The lightweight documentation contract and repository drift tests have landed. Local verification and the Luna weak-model audit both passed with no corrective action, so P001 is done. Release publishing remains a separate decision, and public allocation commands remain deferred until usage evidence justifies their complexity.
