# Runtime Flows

Role: topic-capsule
Status: active
Updated: 2026-08-13

## Current Installer Flow

1. Parse `version` or `install`.
2. Resolve a local source or download/clone a tagged source.
3. Validate the skill and provider-prompt payload.
4. Preflight every selected skill target and provider instruction file.
5. Copy the payload to one or more provider skill directories.
6. Unless opted out, create or update one marker-bounded block in each provider's global persistent instruction file.

Dry-run reports both the skill and instruction targets without writing. Existing user instructions remain outside the managed block and are preserved during upgrades.

## Current Planning Flow

Planning behavior is instruction-driven. An agent reads `SKILL.md`, inspects a project's Markdown tree, edits the relevant files, and performs link and consistency checks. No daemon, file watcher, allocator, or transaction manager exists.

## Numbering Maintenance Flow

For new numbered trees, a maintainer reads the root Plan registry, chooses the next retained Plan number, creates the flat numbered root, updates the registry in the same change, and runs drift checks. Task labels remain in the roadmap, affected modules remain metadata, and no background watcher or transaction manager is required.
