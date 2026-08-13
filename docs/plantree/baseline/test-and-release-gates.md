# Test And Release Gates

Role: topic-capsule
Status: active
Updated: 2026-08-13

## Current Gates

- Repository contract tests validate the maintained Plan Tree example and public numbering rules.
- npm and PyPI expose equivalent `plan-tree` installers through separate implementations.
- Public releases synchronize `VERSION`, `package.json`, `pyproject.toml`, and both CLI constants.
- Installer tests exercise both CLIs against isolated provider homes and verify instruction preservation, idempotency, opt-out, dry-run, malformed-marker rejection, and official target paths.
- Tag releases validate source and bilingual notes, then create or verify the GitHub Release before publishing in `npm → PyPI` order through registry OIDC.
- GitHub Release availability and registry availability are verified independently; a staged release must not imply that npm or PyPI already exposes the version.

## Numbering Gates

- Unique, well-formed Plan IDs that match directory prefixes, local metadata, and the root registry.
- Unique optional task IDs within each roadmap, with no parallel active task registry.
- Affected module keys that resolve through the baseline module map.
- Read-only drift detection before any future automatic repair or migration command.
- Documentation checks for valid relative links and matching examples in English and Simplified Chinese.
- Installer syntax, version, and local-source dry-run checks for both implementations.

## Provider Instruction Gates

- Provider templates exist for Claude Code, OpenCode, and Codex and are included in installed skill payloads.
- Exactly one valid managed block may exist in a provider instruction file.
- User-owned content and file permissions survive install and forced upgrade.
- A malformed block stops before an existing skill directory can be replaced.
- `--no-instructions` and `--dry-run` do not mutate provider instruction files.
