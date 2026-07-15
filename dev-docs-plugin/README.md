# dev-docs plugin

A [Claude Code plugin](https://docs.claude.com/en/docs/claude-code/plugins)
for the full docs-driven development workflow: scaffold the standard `docs/`
structure, plan features forward or reverse-engineer docs from existing
code, and keep translation mirrors in sync. The two core documentation
skills produce the same `planning/` / `design/` / `verification/` document
structure under `docs/<lang>/specifications/<domain>/` — one writes it
forward for code that doesn't exist yet, the other reverse-engineers it
from code that does.

## Contents

| Component | Command / Name | Purpose |
| --- | --- | --- |
| skill | `/dev-docs:init-docs` | Scaffold the standard `docs/` structure: source-language tree, `docs/config.yml`, initial policy documents, and a project CLAUDE.md. Initializes the source language only — mirroring comes later via `sync-translations` |
| skill | `/dev-docs:dev-planning` | Forward planning pipeline for a new feature or project: specification (requirements + user stories + conditional multi-actor flows) → dynamic design documents → test spec, with ID-based test traceability. Accepts a `lite`/`full` tier argument (`/dev-docs:dev-planning lite`) |
| skill | `/dev-docs:dev-reverse-docs` | Grounded documentation of existing code: every claim carries a `[REF: path:line]` or `[ASSUMED: ...]` marker, generated pass-by-pass (overview, then per module). Accepts a `lite`/`full` tier argument (`/dev-docs:dev-reverse-docs lite`) |
| skill | `/dev-docs:sync-translations` | Audit and sync translation mirrors; when no translation language is configured yet, offers to enable mirroring (updates `docs/config.yml`, creates the mirror tree, translates everything) |
| agent | `doc-verifier` | Read-only (`Read, Grep, Glob`) subagent that checks every citation in a `dev-reverse-docs` output against the actual source before the skill reports done |

## Workflow

```text
/dev-docs:init-docs              docs/ structure + source language + policy files + CLAUDE.md
  └─ /dev-docs:dev-planning          planning documents for a new feature
  └─ /dev-docs:dev-reverse-docs      grounded docs for code that already exists
  └─ /dev-docs:sync-translations     opt in to a translation mirror, keep it in sync
```

## Document model

Both documentation skills classify documents on the same axes:

- **`planning/` — WHAT** (stakeholder view): `spec.md` — requirements
  (FR/NFR), user stories with acceptance criteria, and a conditional
  Multi-Actor Flows section (only with 2+ actors or an external system)
- **`design/` — HOW** (developer view): a dynamic subset of `api-spec.md`,
  `sequence-diagram.md`, `component-diagram.md`, `domain-state-machine.md`,
  `client-store.md`, `data-model.md`, `user-flows.md`, `infra-spec.md` —
  only the files the feature (or the code evidence) actually calls for
- **`verification/`**: `test-spec.md`, the single source of truth for test
  definitions, referencing IDs from the other two

Both skills run in one of two **tiers**, chosen by invocation argument or
an auto-detect heuristic confirmed by the user: **Full** produces the
structure above; **Lite** (single actor, no external systems, low
complexity) collapses `design/` into a single `design.md` whose sections
are condensed forms of the individual design templates.

## Templates

Shared by `dev-planning` and `dev-reverse-docs`, loaded via
`${CLAUDE_PLUGIN_ROOT}/templates/` (`init-docs` bundles its own templates
under `skills/init-docs/references/` and `skills/init-docs/scripts/`):

```text
templates/
├── planning/      spec.md
├── design/        api-spec.md, sequence-diagram.md, component-diagram.md,
│                  domain-state-machine.md, client-store.md, data-model.md,
│                  user-flows.md, infra-spec.md, design.md (Lite tier)
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

`dev-planning`, `dev-reverse-docs`, and `sync-translations` are designed to
run inside a project that follows the docs-driven structure created by this
plugin's own `init-docs` skill (`docs/config.yml`,
`docs/<lang>/specifications/`, policy documents) — run
`/dev-docs:init-docs` first on a fresh project. References such as
`[@docs/en/policy/reference-convention.md]` inside the skill definitions
point at the **host project's** files — `init-docs` seeds them there. They
are not paths inside this plugin, and this repository itself keeps its own
policy in `.claude/rules/` instead. The documentation skills still work
without that structure; they simply skip the discovered project documents.

## Versioning

The plugin versions as a single unit (`plugin.json` `version`, git tag
`dev-docs/v<x.y.z>`); each bundled skill and agent keeps its own
independent `version` field. Changes are recorded in the repository-root
[CHANGELOG.md](../CHANGELOG.md).
