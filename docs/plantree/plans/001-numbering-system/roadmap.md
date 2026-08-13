# Roadmap

Role: current-state
Status: active
Updated: 2026-08-13

## Done

- **T001 — Audit current numbering.** Confirmed that only decision filenames had a defined sequence; Plan folders and roadmap tasks had no IDs. See the archived [identity contract](history/transactional-numbering-proposal/identity-contract.md).
- **T002 — Shape the identity model.** Separated immutable identity from mutable priority, status, and display order. See [decision 001](decisions/001-stable-identity-and-immediate-sync.md).
- **T003 — Evaluate immediate synchronization.** Explored locks, interrupted-write recovery, and reconciliation, then archived them as premature complexity. See the [archived proposal](history/transactional-numbering-proposal/README.md).
- **T004 — Close implementation choices.** Chose flat numbered Plan roots, module metadata, roadmap-owned task IDs, and validation before automation. See [decision 002](decisions/002-lightweight-numbering-and-module-metadata.md).
- **T005 — Update the public skill contract.** Amended `SKILL.md`, maintenance and migration references, both READMEs, and provider metadata. See [contract verification](evidence/2026-08-13-lightweight-numbering-contract.md).
- **T006 — Add read-only drift tests.** Added repository checks for IDs, modules, task authority, decisions, links, public-contract parity, migration completion, and whitespace. See [contract verification](evidence/2026-08-13-lightweight-numbering-contract.md).
- **T010 — Run a Luna weak-model drift audit.** Luna recovered one unambiguous current state and next action, found no authority conflicts or invalid module classifications, and required no corrections. See the [Luna drift audit](evidence/2026-08-13-luna-drift-audit.md).

## Deferred

- **T007 — Add allocation commands.** Reconsider only after repeated concurrent allocation conflicts provide evidence for locks or a shared allocator.
- **T008 — Add opt-in legacy migration.** Reconsider after the convention is stable in real numbered trees; never mass-rename automatically.
- **T009 — Background watching.** Keep deferred because explicit same-change maintenance and read-only checks have clearer authority boundaries.
