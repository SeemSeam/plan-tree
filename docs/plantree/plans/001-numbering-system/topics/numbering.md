# Lightweight Numbering Contract

Role: topic-capsule
Status: active
Read when: creating, referencing, classifying, or checking Plan Tree work
Related: [decision 002](../decisions/002-lightweight-numbering-and-module-metadata.md), [roadmap](../roadmap.md)

## Purpose

Numbering improves filesystem scanning and durable cross-references. It must not become a second roadmap, encode mutable meaning, or require a task database.

## Plan Identity

For newly numbered trees:

```text
docs/plantree/plans/
  001-numbering-system/   # P001
  002-release-process/    # P002
  003-storage-redesign/   # P003
```

- The canonical form is `P` plus three decimal digits.
- The directory prefix equals the numeric part of the Plan ID.
- The suffix is a stable, lowercase kebab-case workstream name.
- Allocate the next value as the maximum issued or retained Plan number plus one.
- Never reuse an ID or renumber to close a gap.
- Stop and make an explicit migration decision before exceeding `999`.
- Existing mature trees keep their established names unless they opt into migration.

The root Plan registry is the authority for issued identity and lifecycle while it remains small. A Plan README repeats its own ID only as local retrieval context; validation checks agreement.

## Roadmap References

Roadmap items may use `T001`, `T002`, and so on when they need stable references from handoff, decisions, evidence, or discussions.

- Task IDs are optional and local to one Plan.
- The roadmap is the sole active authority for task title, status, and order.
- Moving a task among `Next`, `In Progress`, `Done`, and `Deferred` preserves its ID.
- Do not create a task folder or task allocation ledger by default.
- When old Done detail leaves the roadmap, retain the task ID in linked evidence or history.
- Priority is expressed by roadmap state and order, never by changing the ID.

Decision filenames keep their existing `001-<decision>.md` convention. Open questions may use `Q001` only when durable cross-references help; ideas remain unnumbered until promoted.

## Module Classification

Plans stay flat under `plans/`. A Plan README may list affected module keys defined in [the baseline module map](../../../baseline/module-map.md):

```md
Affected Modules: `skill-contract`, `public-docs`
```

- Affected modules may be empty, singular, or multiple.
- Changing affected modules does not change the Plan ID or path.
- Do not force a primary module for genuinely cross-cutting work.
- Add a derived `indexes/by-module.md` only when the root registry is no longer enough for retrieval.
- Do not duplicate Plan files into module views or use symlinks as a second tree.
- Physical module directories require stable boundaries, demonstrated navigation need, migration mapping, and a separate decision.

## Authority Map

| Fact | Authority | Derived Context |
| --- | --- | --- |
| Plan ID and lifecycle | Root Plan registry | Directory prefix and Plan README header |
| Plan scope and affected modules | Plan README | Root registry module summary |
| Task ID, title, status, and order | `roadmap.md` | Handoff, evidence, and history references |
| Decision identity and content | Decision file | Roadmap/topic links |
| Open question state | `open-questions.md` | Topic and roadmap references |

If two files disagree, repair the derived context from its authority. Do not create another registry to mediate the conflict.

## Same-Change Consistency

“Current” means consistent when the maintaining edit finishes, not continuously synchronized by a background service.

1. Read the root registry and target Plan before editing.
2. Change the authoritative file.
3. Update only required entrypoint summaries and cross-references.
4. Check IDs, paths, module keys, roadmap uniqueness, status claims, and relative links.
5. Finish only when the tree has one unambiguous current state.

No watcher renames folders, no process closes number gaps, and no automatic repair guesses through ambiguous conflicts.

## Progressive Scaling

- Start with the root registry, one Plan README, and one roadmap.
- Add optional task IDs only after cross-file references need them.
- Add module or evidence indexes only after navigation is measurably difficult.
- Add a read-only public validator only after repository-local checks reveal recurring drift patterns.
- Add allocation locks only after concurrent creators actually collide.
- Archive superseded automation designs instead of keeping them in the active reading path.

This keeps complexity proportional to observed retrieval and coordination pressure.

## Acceptance Checks

- Numbered Plan directories sort lexically and match their `Pnnn` metadata.
- Every numbered Plan is registered from the root entrypoint.
- Issued IDs are unique; gaps do not trigger renumbering.
- Task IDs, when present, are unique within their roadmap.
- Affected module keys exist in the baseline module map.
- Changing a module or task status does not move the Plan directory.
- Local Markdown links resolve.
- Active summaries do not contradict the roadmap or current decision.
