# claude — Claude Code Skills

A collection of reusable Claude Code skills for standardizing project setup with
a bilingual (English + Korean) documentation system.

## Skills

| Skill | Command | Purpose |
|---|---|---|
| init-docs | `/init-docs` | Bootstrap the standard `docs/` structure in a new project |
| new-issue | `/new-issue` | Create the next numbered issue document (+ Korean mirror) |
| sync-dev | `/sync-dev` | Audit and sync Korean translations in `docs/dev/` |
| new-policy | `/new-policy` | Add a new policy document with Korean mirror |

## Installation

### Global (available in all projects)

```bash
npx skills add <your-github-username>/claude@init-docs
npx skills add <your-github-username>/claude@new-issue
npx skills add <your-github-username>/claude@sync-dev
npx skills add <your-github-username>/claude@new-policy
```

### Local (single project, for development/testing)

```bash
mkdir -p .skills
cp -r /path/to/this/repo/skills/init-docs .skills/init-docs
cp -r /path/to/this/repo/skills/new-issue .skills/new-issue
cp -r /path/to/this/repo/skills/sync-dev  .skills/sync-dev
cp -r /path/to/this/repo/skills/new-policy .skills/new-policy
```

## Usage

After installing, invoke a skill from any Claude Code session:

```
/init-docs     ← run once when starting a new project
/new-issue     ← run every time you start a new work item
/sync-dev      ← run to catch up on missing Korean translations
/new-policy    ← run when you need to formalize a new working rule
```

## Typical Workflow

```
New project
  └─ /init-docs       creates docs/ tree + policy files + CLAUDE.md
      └─ /new-issue   creates issue001.md + Korean mirror
          └─ work...
              └─ /new-issue    for each subsequent task
              └─ /new-policy   when a new rule is needed
              └─ /sync-dev     to catch up on missing translations
```

## Templates

`templates/CLAUDE.md` is the standard CLAUDE.md template that `/init-docs`
places in the root of any new project. You can also copy it manually:

```bash
cp /path/to/this/repo/templates/CLAUDE.md /path/to/new-project/CLAUDE.md
```
