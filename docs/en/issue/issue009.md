# Issue 009: Introduce skill version management system

**Status**: Done
**Created**: 2026-03-19

## Background

Skills in this project are installed externally via `npx skills add` and are
actively being modified, but there is no formal version management in place.
Changes are only tracked implicitly through git commit history. This makes it
difficult to know which version of a skill is installed, whether a breaking
change was introduced, or what changed between releases.

## Requirements

1. **Per-skill versioning** — each skill must have a version identifier that
   is tracked and updated when the skill changes.
2. **Git tag alignment** — skill versions must align with git tags so that
   releases are clearly marked in the repository history.
3. **Changelog with newest-first ordering** — change history must be recorded
   with the most recent entry at the top.

## Acceptance Criteria

- [ ] Each SKILL.md contains a `version` field in its frontmatter
- [ ] A versioning policy document exists in `docs/en/policy/` (with Korean translation)
- [ ] Git tags follow a defined naming convention for skill versions
- [ ] A CHANGELOG.md exists at the project root with newest-first ordering
- [ ] All existing skills have initial version numbers assigned
- [ ] The versioning policy defines when to bump major, minor, and patch versions

## Tasks

1. [ ] Define the versioning policy (semantic versioning rules, tag naming
       convention, changelog format)
2. [ ] Create `docs/en/policy/skill-versioning.md` and Korean translation
3. [ ] Add `version` field to all existing SKILL.md frontmatter files
4. [ ] Create project-level CHANGELOG.md with newest-first format
5. [ ] Tag the current state as the initial release in git
6. [ ] Update CLAUDE.md to reference the new versioning policy

## Design Decisions

### Tag naming convention

Since multiple skills share one repository, tags should include the skill name:

```text
<skill-name>/v<major>.<minor>.<patch>
```

Examples:
- `backend-planning/v1.0.0`
- `new-issue/v1.0.0`
- `frontend-planning/v1.1.0`

For project-wide releases, use a plain version tag:

```text
v<major>.<minor>.<patch>
```

### Semantic versioning rules

- **v0.x.y** — initial development phase; skills start at v0.0.1
- **v1.0.0** — promoted only when the skill is confirmed stable and working as intended
- **Major (1+)** — breaking changes to skill behavior, output format, or required input
- **Minor** — new features, templates, or non-breaking enhancements
- **Patch** — bug fixes, typo corrections, minor wording changes

### CHANGELOG format

```markdown
# Changelog

## [skill-name/v1.1.0] - 2026-03-17

### Added
- New template for architecture.md

### Changed
- Restructured pipeline steps

## [skill-name/v1.0.0] - 2026-03-10

### Added
- Initial release
```

## Notes

- All existing skills will start at v0.0.1
- Future skill modifications must include a version bump and changelog entry
