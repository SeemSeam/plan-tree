# GitHub Release Before Registries

Decision ID: P002-D002
Date: 2026-08-13
Status: accepted
Related: [provider instruction contract](../topics/provider-instruction-contract.md), [roadmap](../roadmap.md), [release notes](../../../../releases/v0.4.0.md)

## Context

The `0.4.0` source and packages have passed release-candidate verification, but npm Trusted Publisher ownership cannot be confirmed from the current unauthenticated environment. The previous workflow made GitHub Release depend on npm and PyPI, so an npm authorization failure would prevent users from accessing the reviewed tag and bilingual source release.

The user explicitly authorized publishing the GitHub Release first and completing registry publication afterward. This is an intentional staged release, not evidence that npm or PyPI already contains `0.4.0`.

## Decision

The tag workflow uses `validate → GitHub Release → npm → PyPI` dependencies. GitHub Release creation must be idempotent: a rerun verifies the existing release contains both English and Chinese sections and does not replace it.

The tag remains immutable. npm and PyPI availability are reported and verified independently, and public notes disclose that registry publication may lag behind GitHub.

## Consequences

- A valid source tag and bilingual GitHub Release remain available even if registry authorization fails.
- npm stays ahead of PyPI, preventing a new Python-only version split if npm cannot publish.
- Registry recovery can rerun after trust configuration without moving the tag or duplicating the GitHub Release.
- Release status remains In Progress until npm, PyPI, and clean registry installs are verified.
- No communication may claim that a package registry has published `0.4.0` based only on tag or workflow creation.
