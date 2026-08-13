# Roadmap

Role: current-state
Status: active
Updated: 2026-08-13

## Done

- **T001 — Audit provider and release contracts.** Verified official persistent-instruction paths, established `0.4.0` as an unused compatible minor version, and identified npm token publishing as the existing release blocker. See the [provider instruction contract](topics/provider-instruction-contract.md).
- **T002 — Choose the managed instruction model.** Accepted global provider scope, marker-bounded replacement, user-content preservation, opt-out behavior, and explicit terminology. See [decision 001](decisions/001-managed-global-provider-instructions.md).
- **T003 — Implement installer parity.** Added provider templates, managed-block preflight and writes, symlink preservation, UTF-8 validation, opt-out, and dry-run behavior to both CLIs. See the [release candidate](evidence/2026-08-13-v0.4.0-release-candidate.md).
- **T004 — Add drift and safety tests.** Added subprocess coverage for all providers and both CLIs, including preservation, idempotency, malformed input, symlinks, opt-out, dry run, and custom targets. See the [release candidate](evidence/2026-08-13-v0.4.0-release-candidate.md).
- **T005 — Prepare the release.** Synchronized `0.4.0` metadata, public docs, OIDC workflow gates, package contents, and bilingual notes; source and clean-package validation passed. Changed the dependency order to make the GitHub Release available before registry publication, with an idempotent verification path for reruns. See the [release candidate](evidence/2026-08-13-v0.4.0-release-candidate.md) and [decision 002](decisions/002-github-release-before-registries.md).

## In Progress

- **T006 — Publish and verify.** The user authorized GitHub-first staged publication. Land the revised workflow, tag `v0.4.0`, verify the bilingual GitHub Release, then publish and independently verify npm, PyPI, and fresh installs.
