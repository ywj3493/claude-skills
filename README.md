# claude-skills — Claude Code Plugin Factory

Reusable [Claude Code](https://claude.com/claude-code) skills for a
docs-driven development workflow — a standardized `docs/` structure,
planning pipelines, citation-verified reverse-engineering docs, and
translation mirrors — distributed as two plugins: **dev-docs** (English)
and **explainable** (Korean, with frontend and backend design split apart).

한국어 문서: [README.ko.md](README.ko.md)

## Purpose

Standardize the work that repeats at the start of every project — setting up
the docs structure, planning features, documenting existing code, and keeping
translations in sync — as one Claude Code plugin.

Install once, and every project gets the same documentation system with the
same commands and the same quality. Each skill carries explicit **Execution
Requirements** so results do not depend on which model runs it.

## The dev-docs plugin

Commands are namespaced (`/dev-docs:init-docs`) and never collide with other
plugins:

| Skill / Agent | Command / Name | Purpose |
| --- | --- | --- |
| init-docs | `/dev-docs:init-docs` | Create the standard `docs/` structure, source-language configuration, working rules in `.claude/rules/` (chosen via setup questions), and CLAUDE.md |
| dev-planning | `/dev-docs:dev-planning` | Forward planning pipeline for a new feature: requirements → user stories → use case → design documents → test spec, with ID-based test traceability |
| dev-reverse-docs | `/dev-docs:dev-reverse-docs` | Grounded, citation-verified documentation of existing code (`[REF: path:line]` on every claim) |
| domain-overview | `/dev-docs:domain-overview` | Diagram-first DDD domain overview: a Mermaid context map of bounded contexts, aggregate roots, and pattern-labeled relationships |
| flow-diagram | `/dev-docs:flow-diagram` | After implementation: writes or merges ONE Source-Linked sequence diagram for the flow just built or changed |
| sync-translations | `/dev-docs:sync-translations` | Opt in to translation mirroring and keep mirrors in sync with source docs |
| doc-verifier | `doc-verifier` (agent) | Read-only subagent that checks every `dev-reverse-docs` citation against the actual source |

## The explainable plugin

A Korean-language planning and design pipeline
([explainable-plugin/](explainable-plugin/)). Same purpose as `dev-docs`,
four things done differently: every prompt and template is Korean, frontend
and backend design are separate skills, the reverse pipeline runs
design-first, and exploration subagents each have one narrow job.

| Skill / Agent | Command / Name | Purpose |
| --- | --- | --- |
| init-planning | `/explainable:init-planning` | New project: infrastructure and project setup first, then glossary → requirements → user stories → interface contract → traceability |
| init-design-backend | `/explainable:init-design-backend` | 4-Layered DDD: layer mapping → domain model → ERD → user-story-based sequence diagrams |
| init-design-frontend | `/explainable:init-design-frontend` | FSD: layer/slice structure → routing → UI composition → render flow → state flow → user flows |
| reverse-design-backend | `/explainable:reverse-design-backend` | Existing backend: infra → codebase → domain → per-operation Source-Linked sequence diagrams → domain model and ERD |
| reverse-design-frontend | `/explainable:reverse-design-frontend` | Existing frontend: infra → framework detection → FSD fit → app shell → per-route code and render flow |
| reverse-planning | `/explainable:reverse-planning` | Derives requirements and user stories from the design docs plus code evidence; never overwrites forward-written planning docs |
| translate-docs | `/explainable:translate-docs` | Audit and sync translation mirrors, or opt in to mirroring |
| infra-explorer | `infra-explorer` (agent) | Read-only: deployment, CI/CD, environment, and external-service facts, each cited |
| operation-tracer | `operation-tracer` (agent) | Read-only: one backend operation's call chain, protocol-neutral |
| render-flow-tracer | `render-flow-tracer` (agent) | Read-only: one route's code flow and render flow, framework-neutral |
| citation-verifier | `citation-verifier` (agent) | Read-only: checks every citation against source; same contract as `doc-verifier` |

Backend design uses 4-Layered DDD and frontend uses FSD as baselines, but
the plugin is **framework-neutral** — it never assumes React, and concrete
frameworks enter only as detected facts or user decisions recorded in
`architecture.md`.

Current versions live in each skill's `SKILL.md` frontmatter; changes are
recorded in [CHANGELOG.md](CHANGELOG.md).

## Installation

Install from this repository's marketplace
([.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)):

```bash
claude
/plugin marketplace add ywj3493/claude-skills
/plugin install dev-docs@claude-skills
/plugin install explainable@claude-skills
```

Install either one on its own — they are independent. Or load directly for
local development:

```bash
claude --plugin-dir ./dev-docs-plugin
claude --plugin-dir ./explainable-plugin
```

See [dev-docs-plugin/README.md](dev-docs-plugin/README.md) and
[explainable-plugin/README.md](explainable-plugin/README.md) for details.

## Which plugin to use

| | `dev-docs` | `explainable` |
| --- | --- | --- |
| Language | English | Korean |
| Design split | one pipeline | separate frontend and backend skills |
| Reverse order | planning → design | **design → planning** |
| Architecture baseline | none | backend 4-Layered DDD, frontend FSD |
| Issue management | included as policy | out of scope |
| Output tiers | Lite / Full | none (operation selection gate instead) |
| `docs/` scaffolding | `init-docs` | minimal output paths only |

They can coexist in one project. `explainable` does not scaffold the full
`docs/` tree, so run `/dev-docs:init-docs` first if you want the complete
structure including `issue/`, `reference/`, and `.claude/rules/`.

## Skill Dependencies

`init-docs` establishes the structure the other skills build on.
`sync-translations` checks for that structure and guides you to run
`/dev-docs:init-docs` first when it is missing. `dev-planning` and
`dev-reverse-docs` work best inside that structure but can run without it.

In `explainable`, planning feeds design in the forward direction and design
feeds planning in the reverse direction. Every skill detects the docs
environment on its own and creates only the output paths it needs, so none
of them hard-stops on a missing structure.

## Language Configuration

The docs system supports one **source language** (the base language docs are
authored in) and zero or more **translation languages**, recorded in
`docs/config.yml`. `/dev-docs:init-docs` sets the source language only:

```yaml
source_language: en
translation_languages: []
```

Mirroring is opt-in and comes later: the first `/dev-docs:sync-translations`
run offers to add a translation language (e.g. `ko`), records it in
`docs/config.yml`, creates the mirror directories, and translates the
existing documents. All skills read this file instead of assuming a language
pair; a project that never opts in keeps a single-language docs tree with no
mirror overhead.

## Typical Workflow

```text
New project
  └─ /dev-docs:init-docs            docs/ structure + source language + .claude/rules + CLAUDE.md
      └─ create an issue            GitHub Issue (or docs/<lang>/issue/issue001.md)
          └─ /dev-docs:dev-planning      planning documents for a new feature (structured design)
          └─ /dev-docs:dev-reverse-docs  grounded docs for code that already exists
          └─ /dev-docs:domain-overview   diagram-first DDD context map across all domains
          └─ implementation...
              └─ /dev-docs:flow-diagram       one Source-Linked sequence diagram for the change just made
              └─ /dev-docs:sync-translations  opt in to a translation mirror / resync when docs drift
```

With the `explainable` plugin, planning and design run in opposite orders
depending on whether the code exists yet:

```text
New project (planning first)
  └─ /explainable:init-planning            infra + project setup, then planning docs
      └─ /explainable:init-design-backend      4-Layered DDD
      └─ /explainable:init-design-frontend     FSD
          └─ /explainable:translate-docs       translation mirror

Existing codebase (design first)
  └─ /explainable:reverse-design-backend   infra → codebase → domain → operations
  └─ /explainable:reverse-design-frontend  infra → framework → app shell → routes
      └─ /explainable:reverse-planning         requirements and stories derived from the design
          └─ /explainable:translate-docs       translation mirror
```

Reverse goes design-first because writing requirements before reading what
the code enforces means guessing. The design pass surfaces the validation,
guards, branches, and timeout settings that the requirements are then
derived from.

## Repository Structure

```text
.claude-plugin/
  marketplace.json        # Plugin marketplace manifest (lists dev-docs, explainable)
dev-docs-plugin/          # dev-docs plugin (.claude-plugin/plugin.json)
  skills/init-docs/            # /dev-docs:init-docs (+ scripts/, references/ incl. CLAUDE.md template)
  skills/dev-planning/         # /dev-docs:dev-planning
  skills/dev-reverse-docs/     # /dev-docs:dev-reverse-docs
  skills/domain-overview/      # /dev-docs:domain-overview (+ references/ incl. its template)
  skills/flow-diagram/         # /dev-docs:flow-diagram
  skills/sync-translations/    # /dev-docs:sync-translations
  agents/doc-verifier.md       # read-only citation-vs-code verifier
  templates/              # shared by the planning skills: planning/, design/, verification/
explainable-plugin/       # explainable plugin (Korean; .claude-plugin/plugin.json)
  skills/init-planning/            # /explainable:init-planning
  skills/init-design-backend/      # /explainable:init-design-backend
  skills/init-design-frontend/     # /explainable:init-design-frontend
  skills/reverse-design-backend/   # /explainable:reverse-design-backend
  skills/reverse-design-frontend/  # /explainable:reverse-design-frontend
  skills/reverse-planning/         # /explainable:reverse-planning
  skills/translate-docs/           # /explainable:translate-docs
  agents/                 # infra-explorer, operation-tracer, render-flow-tracer, citation-verifier
  templates/              # overview/, planning/, design/{backend,frontend}/, verification/
  references/             # document-order.md — canonical navigation order
  scripts/check-docs.sh   # deterministic ID, link, placeholder, and fence checks
templates/
  CLAUDE.md               # Standard CLAUDE.md for new projects (same as init-docs' bundled template)
docs/                     # This repository's own docs (dogfooding the system)
  config.yml              # Language configuration (en → ko)
  en/                     # Source documents (policy/, issue/, specifications/)
  ko/                     # Korean mirrors
  reference/              # User-managed reference material
CHANGELOG.md              # Newest-first change log for all skills and plugins
```

## Versioning

Skills follow semantic versioning with a v0.x development phase — see
[.claude/rules/skill-versioning.md](.claude/rules/skill-versioning.md)
(this repository's own policy rules live in `.claude/rules/` in English
only; they are not part of the bilingual `docs/ko/` mirror).
Git tags use the `<skill-name>/v<major>.<minor>.<patch>` form
(e.g., `init-docs/v0.3.0`), and every skill modification bumps the
`version` field in its `SKILL.md` and adds a `CHANGELOG.md` entry. Plugins
(e.g. `dev-docs`) version as a single unit under `<plugin-name>/v<version>`,
independently of the `version` field each bundled skill/agent still keeps.

## Skill Development Guide

### Modifying an existing skill

1. Edit `SKILL.md` — keep the YAML frontmatter (`name`, `version`,
   `description`) accurate
2. Update any `scripts/` or `references/` the skill depends on
3. Bump the `version` field and add a `CHANGELOG.md` entry

### Adding a new skill

1. Create `dev-docs-plugin/skills/<skill-name>/SKILL.md` with YAML
   frontmatter (start at `version: 0.0.1`) and markdown instructions
2. Add `scripts/` or `references/` subdirectories if needed — keep every file
   the skill needs inside its own directory so installed copies are
   self-contained; use `${CLAUDE_PLUGIN_ROOT}` for paths in instructions
3. Document the skill in this README (both language versions), the plugin
   README, and add a `CHANGELOG.md` entry; bump the plugin version in
   `dev-docs-plugin/.claude-plugin/plugin.json` (packaging change)
