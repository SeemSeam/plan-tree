# Provider Instruction Injection

Plan ID: P002
Role: entrypoint
Status: In Progress
Updated: 2026-08-13
Affected Modules: `npm-installer`, `python-installer`, `provider-instructions`, `public-docs`, `release-automation`
Related baseline: [Project baseline](../../baseline/README.md)

## Goal

Make a normal `plan-tree install <provider>` install the skill and a concise provider-specific persistent instruction so Plan Tree can act as the long-term planning authority across projects and sessions.

## Scope

- Claude Code, OpenCode, and Codex global persistent-instruction files.
- Marker-bounded, idempotent updates that preserve all user-owned content.
- Equivalent behavior in the Python and npm installers.
- An explicit `--no-instructions` opt-out and read-only dry-run reporting.
- A staged `0.4.0` release with bilingual GitHub notes first and independently verified npm and PyPI publication afterward.

## Non-Goals

- Replacing a provider's immutable built-in system prompt.
- Editing repository-local `CLAUDE.md` or `AGENTS.md` during a global skill install.
- Enforcing instructions as a security policy.
- Automatically repairing malformed or user-edited managed markers.
- Adding a daemon, watcher, project database, or hidden runtime state.

## Current Position

Provider instruction files are the supported durable surface: `~/.claude/CLAUDE.md` for Claude Code, `~/.config/opencode/AGENTS.md` for OpenCode, and `$CODEX_HOME/AGENTS.md` for Codex. Each installer appends or replaces only one Plan Tree managed block, while preserving surrounding content byte-for-byte apart from necessary trailing separation.

Release publication is intentionally staged. After validation, the immutable tag and bilingual GitHub Release become available before registry publication. npm and PyPI remain separately verified delivery surfaces and must not be described as published until their registries expose `0.4.0`.

## Reading Path

1. [Roadmap](roadmap.md)
2. [Provider instruction contract](topics/provider-instruction-contract.md)
3. [Managed global instruction decision](decisions/001-managed-global-provider-instructions.md)
4. [GitHub-first staged release decision](decisions/002-github-release-before-registries.md)
5. [Implementation status](implementation-status.md)
6. [GitHub Release evidence](evidence/2026-08-13-v0.4.0-github-release.md)
7. [Release-candidate evidence](evidence/2026-08-13-v0.4.0-release-candidate.md)

## Readiness

The immutable `v0.4.0` tag and bilingual GitHub Release are published and verified. npm publication reached `npm publish` but returned a permission-related `E404`; PyPI was correctly skipped because it depends on npm. The Plan remains in progress until registry authorization, publication, and clean installs are verified.
