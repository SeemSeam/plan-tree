# Managed Global Provider Instructions

Decision ID: P002-D001
Date: 2026-08-13
Status: accepted
Related: [provider instruction contract](../topics/provider-instruction-contract.md)

## Context

Installing the Plan Tree skill makes its workflow available, but current usage still asks users to copy a long activation rule into provider memory manually. Silent replacement of a provider instruction file would be unsafe, while project-local injection during a global install would mix scopes and unexpectedly dirty repositories.

## Decision

Every provider install adds a concise managed block to that provider's official user-global instruction file by default. The installer owns only text between stable markers, preserves all surrounding user content, updates the block idempotently, and offers `--no-instructions`.

Prompt templates live under `prompts/` and contain only activation, durable-state, synchronization, and authority boundaries. `SKILL.md` remains the detailed workflow authority.

## Consequences

- New sessions can discover Plan Tree without repeating manual setup in every project.
- Existing instruction files remain user-owned and reviewable.
- A global install has global instruction scope; repository-local policy remains an explicit project action.
- Corrupt or ambiguous markers become a visible error rather than an automatic repair.
- The same behavior must be maintained twice because the npm and Python CLIs remain separate implementations.
