# Claude Skills Repository

This repository is a **skill factory** — it contains reusable Claude Code skills
and templates for standardizing project setup across all projects.

## Repository Structure

```
templates/          # Reusable file templates (CLAUDE.md and others)
skills/             # Claude Code skill definitions
  init-docs/        # /init-docs — bootstrap docs/ structure in a new project
  new-issue/        # /new-issue — create a numbered issue document
  sync-dev/         # /sync-dev  — sync Korean mirrors in docs/dev/
  new-policy/       # /new-policy — add a new policy document
```

## Working in This Repo

When **modifying an existing skill**:
1. Edit the `SKILL.md` — keep the YAML frontmatter (`name`, `description`) accurate
2. Update any `scripts/` or `references/` the skill relies on

When **adding a new skill**:
1. Create `skills/<skill-name>/SKILL.md` with YAML frontmatter + markdown instructions
2. Add `scripts/` or `references/` subdirectories as needed
3. Document the skill in `README.md`

## Skill Installation (after pushing to GitHub)

```bash
npx skills add <github-username>/claude@init-docs
npx skills add <github-username>/claude@new-issue
npx skills add <github-username>/claude@sync-dev
npx skills add <github-username>/claude@new-policy
```

For local development testing, copy into `.skills/` of the target project:

```bash
cp -r skills/init-docs /path/to/target-project/.skills/init-docs
```
