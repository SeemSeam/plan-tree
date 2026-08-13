# Plan Tree

Role: entrypoint
Status: active
Updated: 2026-08-13

## Purpose

This tree records durable planning state for the `plan-tree` skill and its installers. Product behavior remains governed by the released [SKILL.md](../../SKILL.md); this tree records planned changes until they land there.

## Authority Order

1. Released behavior: [SKILL.md](../../SKILL.md) and its bundled references.
2. Accepted design decisions under the relevant plan root.
3. Current plan roadmap and topic contracts.
4. Operational handoff files, when an implementation is in progress.
5. History and evidence.

## Reading Path

1. Read the [baseline](baseline/README.md) for repository-wide context.
2. Select a plan from the registry below.
3. Read that plan's `README.md`, then its roadmap and only the linked active topic files.

## Plan Registry

This table is the Plan identity and lifecycle registry while it remains small. Keep issued IDs here when a Plan is archived or retired; split the registry into an index only after the root entrypoint becomes difficult to scan.

| ID | Plan | Affected Modules | Status | Current Phase | Last Landed | Next Target |
| --- | --- | --- | --- | --- | --- | --- |
| P001 | [Numbering system](plans/001-numbering-system/README.md) | `skill-contract`, `maintenance-guidance`, `public-docs` | Done | Contract verified | [Luna drift audit](plans/001-numbering-system/evidence/2026-08-13-luna-drift-audit.md) | Make a separate release decision outside P001 |
| P002 | [Provider instruction injection](plans/002-provider-instruction-injection/README.md) | `npm-installer`, `python-installer`, `provider-instructions`, `public-docs`, `release-automation` | In Progress | GitHub-first publication | [GitHub-first release decision](plans/002-provider-instruction-injection/decisions/002-github-release-before-registries.md) | Tag and verify GitHub Release, then complete registries |
