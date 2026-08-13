# Provider Instruction Contract

Date: 2026-08-13
Role: contract
Status: accepted
Read when: changing installer behavior, prompt payloads, or release gates
Related: [decision 001](../decisions/001-managed-global-provider-instructions.md), [roadmap](../roadmap.md)

## Provider Targets

| Provider | Installed skill | Persistent instruction file |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/plan-tree` | `~/.claude/CLAUDE.md` |
| OpenCode | `~/.config/opencode/skill/plan-tree` | `~/.config/opencode/AGENTS.md` |
| Codex | `$CODEX_HOME/skills/plan-tree` | `$CODEX_HOME/AGENTS.md` |

`$CODEX_HOME` defaults to `~/.codex`. Custom skill `--target` does not silently redirect the provider instruction file.

## Mutation Rules

- Default install writes one block delimited by `<!-- plan-tree:instructions:start -->` and `<!-- plan-tree:instructions:end -->`.
- No existing block means append after the user's content with one blank-line boundary.
- One valid existing block means replace only that block with the current provider payload.
- Missing, duplicated, reversed, or otherwise ambiguous markers stop before any install write.
- Writes use a temporary sibling and atomic replacement where supported.
- A valid symbolic link is preserved and its regular-file target is updated; dangling links and special files are rejected.
- `--dry-run` reports both targets without writing; `--no-instructions` leaves provider instructions untouched.
- `--force` controls skill-directory replacement only and never authorizes replacing the entire instruction file.

## Prompt Boundary

The persistent block tells the provider when to load Plan Tree and where durable project state lives. Detailed planning procedure remains in `SKILL.md`, preventing startup context from duplicating the full contract.

The files are provider-loaded persistent context, not an immutable provider system prompt and not a security enforcement mechanism.

## Acceptance Criteria

- Python and npm installers produce semantically equivalent blocks for all three providers.
- Existing user content and file mode survive create/update flows.
- Existing symbolic-link based dotfile management remains intact.
- A second forced install contains exactly one managed block.
- Opt-out and dry-run perform no instruction-file writes.
- Malformed markers fail before replacing an existing skill directory.
- Installed payload includes all three prompt templates.
- Public English and Chinese documentation describes default injection, paths, opt-out, upgrade behavior, and the terminology boundary.
- Release tests validate source contracts, artifacts, clean installs, and exact `0.4.0` identity.

## Release Gate

Use tag-triggered `validate → npm → PyPI → GitHub Release` ordering. npm must use Trusted Publishing without `NODE_AUTH_TOKEN`; PyPI retains its existing trusted `pypi` environment. The tag is blocked until npm trusts owner `SeemSeam`, repository `plan-tree`, workflow `release.yml`, blank environment, and action `npm publish`.
