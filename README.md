# claude-skills — Claude Code Plugin Factory

Reusable [Claude Code](https://claude.com/claude-code) skills for a
docs-driven development workflow — a standardized `docs/` structure,
planning pipelines, citation-verified reverse-engineering docs, and
translation mirrors — distributed as the **dev-docs plugin**.

한국어 문서: [README.ko.md](README.ko.md)

## Purpose

Standardize the work that repeats at the start of every project — setting up
the docs structure, planning features, documenting existing code, and keeping
translations in sync — as one Claude Code plugin.

Install once, and every project gets the same documentation system with the
same commands and the same quality. Each skill carries explicit **Execution
Requirements** so results do not depend on which model runs it.

## The dev-docs plugin

All skills live in the `dev-docs` plugin ([dev-docs-plugin/](dev-docs-plugin/)),
so commands are namespaced (`/dev-docs:init-docs`) and never collide with
other plugins:

| Skill / Agent | Command / Name | Purpose |
| --- | --- | --- |
| init-docs | `/dev-docs:init-docs` | Create the standard `docs/` structure, source-language configuration, working rules in `.claude/rules/` (chosen via setup questions), and CLAUDE.md |
| dev-planning | `/dev-docs:dev-planning` | Forward planning pipeline for a new feature: requirements → user stories → use case → design documents → test spec, with ID-based test traceability |
| dev-reverse-docs | `/dev-docs:dev-reverse-docs` | Grounded, citation-verified documentation of existing code (`[REF: path:line]` on every claim) |
| sync-translations | `/dev-docs:sync-translations` | Opt in to translation mirroring and keep mirrors in sync with source docs |
| doc-verifier | `doc-verifier` (agent) | Read-only subagent that checks every `dev-reverse-docs` citation against the actual source |

Current versions live in each skill's `SKILL.md` frontmatter; changes are
recorded in [CHANGELOG.md](CHANGELOG.md).

## Installation

Install from this repository's marketplace
([.claude-plugin/marketplace.json](.claude-plugin/marketplace.json)):

```bash
claude
/plugin marketplace add ywj3493/claude-skills
/plugin install dev-docs@claude-skills
```

Or load directly for local development:

```bash
claude --plugin-dir ./dev-docs-plugin
```

See [dev-docs-plugin/README.md](dev-docs-plugin/README.md) for details.

## Skill Dependencies

`init-docs` establishes the structure the other skills build on.
`sync-translations` checks for that structure and guides you to run
`/dev-docs:init-docs` first when it is missing. `dev-planning` and
`dev-reverse-docs` work best inside that structure but can run without it.

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
          └─ implementation...
              └─ /dev-docs:sync-translations  opt in to a translation mirror / resync when docs drift
```

## Repository Structure

```text
.claude-plugin/
  marketplace.json        # Plugin marketplace manifest (lists dev-docs)
dev-docs-plugin/          # dev-docs plugin (.claude-plugin/plugin.json)
  skills/init-docs/            # /dev-docs:init-docs (+ scripts/, references/ incl. CLAUDE.md template)
  skills/dev-planning/         # /dev-docs:dev-planning
  skills/dev-reverse-docs/     # /dev-docs:dev-reverse-docs
  skills/sync-translations/    # /dev-docs:sync-translations
  agents/doc-verifier.md       # read-only citation-vs-code verifier
  templates/              # shared by the planning skills: planning/, design/, verification/
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
