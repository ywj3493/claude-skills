# dev-docs plugin

A [Claude Code plugin](https://docs.claude.com/en/docs/claude-code/plugins)
bundling two documentation skills and a verification subagent. Both skills
produce the same `planning/` / `design/` / `verification/` document
structure under `docs/<lang>/specifications/<domain>/` — one writes it
forward for code that doesn't exist yet, the other reverse-engineers it
from code that does.

## Contents

| Component | Command / Name | Purpose |
| --- | --- | --- |
| skill | `/dev-docs:dev-planning` | Forward planning pipeline for a new feature or project: requirements → user stories → use case → dynamic design documents → test spec, with ID-based test traceability |
| skill | `/dev-docs:dev-reverse-docs` | Grounded documentation of existing code: every claim carries a `[REF: path:line]` or `[ASSUMED: ...]` marker, generated pass-by-pass (overview, then per module) |
| agent | `doc-verifier` | Read-only (`Read, Grep, Glob`) subagent that checks every citation in a `dev-reverse-docs` output against the actual source before the skill reports done |

## Document model

Both skills classify documents on the same axes:

- **`planning/` — WHAT** (stakeholder view): `requirements.md`,
  `user-stories.md`, `use-case.md`
- **`design/` — HOW** (developer view): a dynamic subset of `api-spec.md`,
  `sequence-diagram.md`, `component-diagram.md`, `state-diagram.md`,
  `data-model.md`, `user-flows.md`, `infra-spec.md` — only the files the
  feature (or the code evidence) actually calls for
- **`verification/`**: `test-spec.md`, the single source of truth for test
  definitions, referencing IDs from the other two

## Templates

Shared by both skills, loaded via `${CLAUDE_PLUGIN_ROOT}/templates/`:

```text
templates/
├── planning/      requirements.md, user-stories.md, use-case.md
├── design/        api-spec.md, sequence-diagram.md, component-diagram.md,
│                  state-diagram.md, data-model.md, user-flows.md, infra-spec.md
└── verification/  test-spec.md
```

## Installation

From the marketplace at this repository's root:

```bash
claude
/plugin marketplace add ywj3493/claude-skills
/plugin install dev-docs@claude-skills
```

Or load directly for local/team use:

```bash
claude --plugin-dir ./dev-docs-plugin
```

## Host-project expectations

The skills are designed to run inside a project that follows the
docs-driven structure created by this repository's `init-docs` skill
(`docs/config.yml`, `docs/<lang>/specifications/`, policy documents).
References such as `[@docs/en/policy/reference-convention.md]` inside the
skill definitions point at the **host project's** files — `init-docs`
seeds them there. They are not paths inside this plugin, and this
repository itself keeps its own policy in `.claude/rules/` instead. The
skills still work without that structure; they simply skip the discovered
project documents.

## Versioning

The plugin versions as a single unit (`plugin.json` `version`, git tag
`dev-docs/v<x.y.z>`); each bundled skill and agent keeps its own
independent `version` field. Changes are recorded in the repository-root
[CHANGELOG.md](../CHANGELOG.md).
