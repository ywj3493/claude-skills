# claude-skills — Claude Code Skill Factory

A collection of reusable [Claude Code](https://claude.com/claude-code) skills
for a docs-driven development workflow: a standardized `docs/` structure,
issue-first work tracking, policy documents, planning pipelines, and
translation mirrors.

한국어 문서: [README.ko.md](README.ko.md)

## Purpose

Standardize the work that repeats at the start of every project — setting up
the docs structure, writing policy documents, tracking issues, and keeping
translations in sync — as Claude Code skills.

Install once, and every project gets the same documentation system with the
same commands and the same quality. Each skill carries explicit **Execution
Requirements** so results do not depend on which model runs it.

## Skills

| Skill | Command | Purpose |
| --- | --- | --- |
| new-policy | `/new-policy` | Add a policy document with translation mirrors |

Current versions live in each skill's `SKILL.md` frontmatter; changes are
recorded in [CHANGELOG.md](CHANGELOG.md). The docs-system lifecycle skills
(`init-docs`, `new-issue`, `sync-translations`) now ship inside the `dev-docs`
plugin below.

## Plugins

| Plugin | Skills | Purpose |
| --- | --- | --- |
| dev-docs | `/dev-docs:init-docs`, `/dev-docs:new-issue`, `/dev-docs:sync-translations`, `/dev-docs:dev-planning`, `/dev-docs:dev-reverse-docs` | The full docs-driven development workflow: scaffold the `docs/` structure (`init-docs`), track work as issues (`new-issue`), keep translation mirrors in sync (`sync-translations`), and plan a new feature (`dev-planning`) or reverse-engineer specs from existing code (`dev-reverse-docs`) into the same `planning/`/`design/`/`verification/` structure. Bundles a read-only `doc-verifier` subagent that checks every `dev-reverse-docs` claim against the actual source before the skill reports done. |

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

See [dev-docs-plugin/README.md](dev-docs-plugin/README.md) for details. Plugin
skills are namespaced (`/dev-docs:init-docs`, not `/init-docs`) so multiple
plugins never collide, unlike the loose `new-policy` skill above.

## Installation

```bash
npx skills add https://github.com/ywj3493/claude-skills.git
```

Follow the interactive guide to choose which skills to install.

## Skill Dependencies

`/dev-docs:init-docs` establishes the structure the other skills build on. The
loose `new-policy` skill and the `dev-docs` plugin's `sync-translations` and
`new-issue` (docs mode) skills check for that structure and guide you to run
`/dev-docs:init-docs` first when it is missing. `new-issue` in GitHub mode and
the specification skills (`dev-planning`, `dev-reverse-docs`) can be used
independently.

## Language Configuration

The docs system supports one **source language** and zero or more
**translation languages**, chosen when running `/dev-docs:init-docs` and
recorded in `docs/config.yml`:

```yaml
source_language: en
translation_languages:
  - ko
```

All skills read this file instead of assuming a language pair. A project with
`translation_languages: []` keeps a single-language docs tree with no mirror
overhead. The default pairing is `en` → `ko`.

## Typical Workflow

```text
New project
  └─ /dev-docs:init-docs            docs/ structure + language config + policy files + CLAUDE.md
      └─ /dev-docs:new-issue        GitHub Issue + branch + draft PR (or local issue docs)
          └─ /dev-docs:dev-planning      planning documents for a new feature (structured design)
          └─ /dev-docs:dev-reverse-docs  grounded docs for code that already exists
          └─ implementation...
              └─ /dev-docs:new-issue         repeat for each unit of work
              └─ /new-policy                 when a new rule needs formalizing
              └─ /dev-docs:sync-translations when translation mirrors drift
```

## Repository Structure

```text
skills/                   # Loose Claude Code skill definitions
  new-policy/             # /new-policy
.claude-plugin/
  marketplace.json        # Plugin marketplace manifest (lists dev-docs)
dev-docs-plugin/          # dev-docs plugin (.claude-plugin/plugin.json)
  skills/init-docs/            # /dev-docs:init-docs (+ scripts/, references/ incl. CLAUDE.md template)
  skills/new-issue/            # /dev-docs:new-issue
  skills/sync-translations/    # /dev-docs:sync-translations
  skills/dev-planning/         # /dev-docs:dev-planning
  skills/dev-reverse-docs/     # /dev-docs:dev-reverse-docs
  agents/doc-verifier.md       # read-only citation-vs-code verifier
  templates/              # shared by the specification skills: planning/, design/, verification/
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
(e.g., `new-issue/v0.3.0`), and every skill modification bumps the
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

1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter
   (start at `version: 0.0.1`) and markdown instructions
2. Add `scripts/` or `references/` subdirectories if needed — keep every file
   the skill needs inside its own directory so installed copies are
   self-contained
3. Document the skill in this README (both language versions) and add a
   `CHANGELOG.md` entry
