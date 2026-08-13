# Implementation Status

Date: 2026-08-13
Role: current-state
Status: active

## Current Phase

The `0.4.0` release candidate is verified and source commit `dd9031f` is on `origin/main`. Clear the npm Trusted Publisher gate before creating the tag.

## Active TODO

- T006 — Confirm npm trusts `SeemSeam/plan-tree`, workflow `release.yml`, blank environment, for `npm publish`.
- T006 — Create and push `v0.4.0`, then verify npm, PyPI, GitHub Release, workflow, and fresh installs.

## Done This Phase

- T001 — Completed provider-path, version-collision, registry, and workflow audit.
- T002 — Accepted [P002-D001](decisions/001-managed-global-provider-instructions.md).
- T003 — Implemented provider prompt payloads and safe managed-block mutation in both CLIs.
- T004 — Added and passed the cross-provider installer safety suite.
- T005 — Prepared and verified version metadata, docs, workflow, packages, and [bilingual notes](../../../releases/v0.4.0.md).
- T006 — Committed release source as `dd9031f`, pushed it to `origin/main`, and confirmed GitHub recognizes `release.yml`.

## Blockers

Publication only: an unauthenticated `npm trust list plan-tree --json` returned `401 Unauthorized`. An npm package owner must confirm or configure the Trusted Publisher before the release tag is created.

## Next Commit Target

After npm trust is confirmed, create `v0.4.0` at the exact reviewed remote `main` commit and let the tag workflow publish in dependency order.

## Last Verified

- Nineteen source and installer contract tests pass.
- Python wheel, sdist, and npm tarball pass metadata, allowlist, isolated-install, and provider-injection checks.
- Bilingual release notes, Node syntax, local links, version synchronization, and whitespace checks pass.
- Full commands and candidate checksums are recorded in [release-candidate evidence](evidence/2026-08-13-v0.4.0-release-candidate.md).
- GitHub accepted `dd9031fbc645ac87fcdb9edf0d7d33a3808b0932` on `main` and displays the committed release workflow.

## Handoff Notes

Do not create or push `v0.4.0` until the npm OIDC trust relationship is configured. Do not stage unrelated files under `docs/papers/`. The release workflow intentionally orders npm before PyPI to avoid repeating the prior npm/PyPI version split.
