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

- **T006 — Publish and verify.** The revised workflow, immutable `v0.4.0` tag, and bilingual GitHub Release are published and verified. The npm package inspection passed, but `npm publish` returned a permission-related `E404`, so PyPI was safely skipped. Correct npm Trusted Publisher or package authorization, rerun registry publication without moving the tag, then verify both registries and fresh installs. See the [GitHub Release evidence](evidence/2026-08-13-v0.4.0-github-release.md).
