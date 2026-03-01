# Issue 004: Fix frontend-planning Skill Distribution via npx

**Status**: Open
**Created**: 2026-03-01

## Background

Issue 003 introduced the `frontend-planning` skill. The skill's acceptance
criteria and notes specify the target installation path as
`.agents/skills/frontend-planning/SKILL.md` — that is, where the skill lives
inside a *user's* project after installation.

However, the skill source files were placed (or planned to be placed) directly
under `.agents/skills/` in *this* repository rather than under `skills/`.
The `npx skills add` installer reads from `skills/` when copying skill
definitions into a target project's `.agents/skills/` directory. Because
`frontend-planning` is not in `skills/`, the installer cannot find or deploy it.

All four existing skills (`init-docs`, `new-issue`, `new-policy`, `sync-dev`)
live under `skills/<name>/SKILL.md` in this repository and are successfully
installed via `npx skills add`. The `frontend-planning` skill must follow the
same pattern to be distributable the same way.

## Acceptance Criteria

- [ ] `skills/frontend-planning/SKILL.md` exists in this repository with correct YAML front matter
- [ ] Six reference templates exist under `skills/frontend-planning/references/`
- [ ] `npx skills add` successfully installs `frontend-planning` into a target project's `.agents/skills/frontend-planning/`
- [ ] README skill table is updated to include `frontend-planning`
- [ ] Issue 003 acceptance criteria updated to reflect `skills/frontend-planning/` as the source path
- [ ] Korean issue mirror exists at `docs/dev/issue/issue004.ko.md`

## Tasks

- [ ] 1. Create this issue document (English + Korean mirror)
- [ ] 2. Create `skills/frontend-planning/SKILL.md` with YAML front matter and full skill instructions
- [ ] 3. Create six reference templates in `skills/frontend-planning/references/`
- [ ] 4. Verify `npx skills add` installs the skill correctly into a target project
- [ ] 5. Update `README.md` skill table with `frontend-planning` entry
- [ ] 6. Update issue 003 acceptance criteria to use `skills/frontend-planning/` as the source path

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->

- **Root cause**: Issue 003 described the *target* path (`.agents/skills/frontend-planning/`) rather
  than the *source* path (`skills/frontend-planning/`) that the installer reads from. This led to the
  skill being created in the wrong location for distribution.
- **Fix strategy**: Create the skill source at `skills/frontend-planning/` — consistent with all other
  skills in this repository. The `npx skills add` installer will then copy it to
  `.agents/skills/frontend-planning/` in the target project, matching the intended installation path.
- **No installer changes needed**: The existing installer logic already handles this pattern; only the
  skill source location needs to be corrected.
