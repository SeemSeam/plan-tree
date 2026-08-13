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
- A synchronized `0.4.0` release to npm, PyPI, and GitHub with bilingual notes.

## Non-Goals

- Replacing a provider's immutable built-in system prompt.
- Editing repository-local `CLAUDE.md` or `AGENTS.md` during a global skill install.
- Enforcing instructions as a security policy.
- Automatically repairing malformed or user-edited managed markers.
- Adding a daemon, watcher, project database, or hidden runtime state.

## Current Position

Provider instruction files are the supported durable surface: `~/.claude/CLAUDE.md` for Claude Code, `~/.config/opencode/AGENTS.md` for OpenCode, and `$CODEX_HOME/AGENTS.md` for Codex. Each installer appends or replaces only one Plan Tree managed block, while preserving surrounding content byte-for-byte apart from necessary trailing separation.

## Reading Path

1. [Roadmap](roadmap.md)
2. [Provider instruction contract](topics/provider-instruction-contract.md)
3. [Managed global instruction decision](decisions/001-managed-global-provider-instructions.md)
4. [Implementation status](implementation-status.md)
5. [Release-candidate evidence](evidence/2026-08-13-v0.4.0-release-candidate.md)

## Readiness

Implementation and release preparation are complete. The verified `0.4.0` source commit is on `origin/main`, and GitHub recognizes the tag-triggered release workflow. Publication remains gated on confirming npm Trusted Publisher configuration before creating the tag.
