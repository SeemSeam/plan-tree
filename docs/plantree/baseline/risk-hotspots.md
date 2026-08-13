# Risk Hotspots

Role: topic-capsule
Status: active
Updated: 2026-08-13

- Renumbering directories can break Markdown links, external bookmarks, open editor state, and Git history.
- Concurrent Plan creation remains cooperatively serialized; repeated collisions would be evidence for allocator tooling.
- Root summaries can drift from Plan-local state unless the same change updates required derived context.
- Optional task labels can drift if duplicated into a second task ledger.
- Physical module grouping can force path churn when architecture or ownership changes.
- A two-digit prefix silently loses lexical ordering after `99` unless width expansion is explicitly migrated.
- Existing mature trees may have their own naming conventions and must not be mass-renamed automatically.
- Generated indexes can become competing authorities unless canonical and derived fields are explicit.
- Provider instruction injection can corrupt personal guidance unless updates are marker-bounded, atomic, idempotent, and reject malformed managed blocks.
- npm and PyPI can diverge when registry jobs publish independently; release ordering and pre-tag authentication gates must minimize partial publication.
