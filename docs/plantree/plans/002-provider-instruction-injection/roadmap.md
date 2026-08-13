# Roadmap

Role: current-state
Status: active
Updated: 2026-08-13

## Done

- **T001 — Audit provider and release contracts.** Verified official persistent-instruction paths, established `0.4.0` as an unused compatible minor version, and identified npm token publishing as the existing release blocker. See the [provider instruction contract](topics/provider-instruction-contract.md).
- **T002 — Choose the managed instruction model.** Accepted global provider scope, marker-bounded replacement, user-content preservation, opt-out behavior, and explicit terminology. See [decision 001](decisions/001-managed-global-provider-instructions.md).
- **T003 — Implement installer parity.** Added provider templates, managed-block preflight and writes, symlink preservation, UTF-8 validation, opt-out, and dry-run behavior to both CLIs. See the [release candidate](evidence/2026-08-13-v0.4.0-release-candidate.md).
- **T004 — Add drift and safety tests.** Added subprocess coverage for all providers and both CLIs, including preservation, idempotency, malformed input, symlinks, opt-out, dry run, and custom targets. See the [release candidate](evidence/2026-08-13-v0.4.0-release-candidate.md).
- **T005 — Prepare the release.** Synchronized `0.4.0` metadata, public docs, OIDC workflow gates, package contents, and bilingual notes; source and clean-package validation passed. See the [release candidate](evidence/2026-08-13-v0.4.0-release-candidate.md).

## In Progress

- **T006 — Publish and verify.** Source commit `dd9031f` is on `origin/main` and GitHub recognizes the release workflow. Verify npm trust, tag `v0.4.0`, then verify GitHub, npm, PyPI, and fresh installs.
