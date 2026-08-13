# Implementation Status

Date: 2026-08-13
Role: current-state
Status: active

## Current Phase

The immutable `v0.4.0` tag and bilingual GitHub Release are published at commit `763e4a0`. Registry recovery is the remaining phase: npm rejected publication with `E404`, and the dependent PyPI job was skipped.

## Active TODO

- T006 — Confirm or correct npm Trusted Publisher and package authorization for `SeemSeam/plan-tree` and `release.yml`.
- T006 — Rerun registry publication without moving `v0.4.0`, then verify npm, PyPI, and fresh registry installs.

## Done This Phase

- T001 — Completed provider-path, version-collision, registry, and workflow audit.
- T002 — Accepted [P002-D001](decisions/001-managed-global-provider-instructions.md).
- T003 — Implemented provider prompt payloads and safe managed-block mutation in both CLIs.
- T004 — Added and passed the cross-provider installer safety suite.
- T005 — Prepared and verified version metadata, docs, workflow, packages, and [bilingual notes](../../../releases/v0.4.0.md).
- T006 — Committed release source as `dd9031f`, pushed it to `origin/main`, and confirmed GitHub recognizes `release.yml`.
- T006 — Accepted [P002-D002](decisions/002-github-release-before-registries.md) after explicit user authorization to publish GitHub first.
- T006 — Landed the staged workflow as `763e4a0`, pushed annotated tag `v0.4.0`, and verified the formal bilingual [GitHub Release](evidence/2026-08-13-v0.4.0-github-release.md).

## Blockers

Registry completion only: workflow run `31667800673` built and inspected `plan-tree@0.4.0`, but `npm publish` returned `E404 Not Found` or insufficient permission. The public package still exposes `0.2.2`. An npm package owner must confirm or correct the Trusted Publisher/package authorization before npm and the dependent PyPI job can complete.

## Next Commit Target

After npm authorization is corrected, rerun the registry path against the existing immutable tag and record independent npm, PyPI, and clean-install evidence.

## Last Verified

- Nineteen source and installer contract tests pass.
- Python wheel, sdist, and npm tarball pass metadata, allowlist, isolated-install, and provider-injection checks.
- Bilingual release notes, Node syntax, local links, version synchronization, and whitespace checks pass.
- Full commands and candidate checksums are recorded in [release-candidate evidence](evidence/2026-08-13-v0.4.0-release-candidate.md).
- GitHub accepted `dd9031fbc645ac87fcdb9edf0d7d33a3808b0932` on `main` and displays the committed release workflow.
- Annotated tag `v0.4.0` dereferences to `763e4a05bdb2a3b3fbcb13085f6edefc2b0bad5f`.
- Workflow validation and GitHub Release jobs passed; the formal Release contains both `## English` and `## 中文` sections.
- npm `0.4.0` and PyPI `0.4.0` remain absent after the failed/skipped registry jobs.

## Handoff Notes

Do not move or recreate `v0.4.0`; rerun against the existing tag after authorization repair. Do not claim npm or PyPI availability until each registry is independently verified. Do not stage unrelated files under `docs/papers/`. npm remains before PyPI to avoid repeating the prior npm/PyPI version split.
