# Storage And State

Role: topic-capsule
Status: active
Updated: 2026-08-13

- Product rules are stored as version-controlled Markdown.
- Provider installations are copied snapshots of the repository payload.
- Provider-global persistent instruction files may contain one installer-owned Plan Tree block; all text outside its markers remains user-owned.
- The npm and PyPI installers duplicate their CLI behavior in JavaScript and Python.
- The repository currently has no persistent runtime database or numbering counter.
- A future numbering mechanism must remain usable in a Markdown-first/manual workflow and must not require a background service.
- Untracked files under `docs/papers/` predate this plan and are outside its write scope.
