# Implementation Status

Date: 2026-08-13
Role: current-state
Status: active

## Current Phase

The `0.4.0` release candidate is verified. The user explicitly accepted staged publication, so the GitHub Release can be created before npm and PyPI authorization is complete.

## Active TODO

- T006 — Land and verify the `validate → GitHub Release → npm → PyPI` workflow.
- T006 — Create and push `v0.4.0`, then verify the tag and bilingual GitHub Release.
- T006 — Confirm npm trust, complete npm and PyPI publication, and verify fresh registry installs.

## Done This Phase

- T001 — Completed provider-path, version-collision, registry, and workflow audit.
- T002 — Accepted [P002-D001](decisions/001-managed-global-provider-instructions.md).
- T003 — Implemented provider prompt payloads and safe managed-block mutation in both CLIs.
- T004 — Added and passed the cross-provider installer safety suite.
- T005 — Prepared and verified version metadata, docs, workflow, packages, and [bilingual notes](../../../releases/v0.4.0.md).
- T006 — Committed release source as `dd9031f`, pushed it to `origin/main`, and confirmed GitHub recognizes `release.yml`.
- T006 — Accepted [P002-D002](decisions/002-github-release-before-registries.md) after explicit user authorization to publish GitHub first.

## Blockers

There is no blocker to the GitHub tag and Release. Registry completion remains gated because an unauthenticated `npm trust list plan-tree --json` returned `401 Unauthorized`; an npm package owner must confirm or configure the Trusted Publisher before npm and the dependent PyPI job can complete.

## Next Commit Target

Commit and push the revised staged-release contract, create `v0.4.0` at that exact reviewed remote `main` commit, and verify the GitHub Release before treating registry publication as complete.

## Last Verified

- Nineteen source and installer contract tests pass.
- Python wheel, sdist, and npm tarball pass metadata, allowlist, isolated-install, and provider-injection checks.
- Bilingual release notes, Node syntax, local links, version synchronization, and whitespace checks pass.
- Full commands and candidate checksums are recorded in [release-candidate evidence](evidence/2026-08-13-v0.4.0-release-candidate.md).
- GitHub accepted `dd9031fbc645ac87fcdb9edf0d7d33a3808b0932` on `main` and displays the committed release workflow.

## Handoff Notes

The user explicitly authorized creating `v0.4.0` before the npm OIDC trust relationship is confirmed. Do not claim npm or PyPI availability until each registry is independently verified. Do not stage unrelated files under `docs/papers/`. npm remains before PyPI to avoid repeating the prior npm/PyPI version split.
