# Lightweight Numbering Contract Evidence

Date: 2026-08-13
Role: evidence
Status: accepted
Related: [roadmap](../roadmap.md), [decision 002](../decisions/002-lightweight-numbering-and-module-metadata.md), [active contract](../topics/numbering.md)

## Claim Verified

The repository's maintained Plan Tree example and public Skill contract agree on flat three-digit Plan roots, optional roadmap-owned task IDs, module metadata, same-change consistency, and validation before automation.

## Commands Or Checks

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`
- `python3 -m compileall -q src tests`
- `node --check bin/plan-tree.js`
- `PYTHONPATH=src python3 -m plan_tree_installer.cli version`
- `node bin/plan-tree.js version`
- Python and Node `install all --source . --dry-run`
- `git diff --check`

## Result

- Eight drift-contract tests passed.
- Tests cover Plan directory/registry/metadata agreement, module-key validity, task uniqueness and sole authority, decision ID agreement, local Markdown links, public English/Chinese contract markers, completed normalization mapping, and trailing whitespace.
- Python and Node syntax checks passed.
- Both installers reported version `0.3.0` and completed local-source dry runs for Claude, opencode, and Codex targets.
- Normalization preserved the first transactional proposal under history and removed its registries from active authority.
- Generated Python bytecode caches were removed and added to `.gitignore`.

## Follow-Up

The environment has no `python` alias, so verification uses `python3`. An independent [Luna weak-model audit](2026-08-13-luna-drift-audit.md) subsequently passed with no corrective action; release publishing is not part of this evidence.
