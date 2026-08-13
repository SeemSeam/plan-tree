# Module Map

Role: topic-capsule
Status: active
Updated: 2026-08-13

Module keys are stable classification metadata for planning and validation. They do not create physical folders under `plans/` and are not encoded into Plan IDs.

| Key | Surface | Responsibility |
| --- | --- | --- |
| `skill-contract` | `SKILL.md` | Normative Plan Tree workflow and governance. |
| `maintenance-guidance` | `references/` | Templates, maintenance rules, and migration guidance. |
| `public-docs` | `README.md`, `README.zh-CN.md` | Public product explanation and installation instructions. |
| `npm-installer` | `bin/plan-tree.js`, `package.json` | npm installer CLI and package metadata. |
| `python-installer` | `src/plan_tree_installer/`, `pyproject.toml` | PyPI installer CLI and package metadata. |
| `provider-metadata` | `agents/openai.yaml` | Codex/OpenAI skill metadata. |
| `provider-instructions` | `prompts/` and provider instruction files | Provider-specific persistent activation rules managed by the installers. |
| `release-automation` | `.github/workflows/release.yml`, `docs/releases/` | Validated package publication and bilingual GitHub Release records. |

There is currently no project-plan creation, numbering, or synchronization runtime. Both CLIs only install the skill payload. Repository tests validate the maintained example tree and public contract without turning module classification into filesystem ownership.
