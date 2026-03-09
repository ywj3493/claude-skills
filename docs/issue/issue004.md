# Issue 004: Restructure docs/ to Language-Code-Based Directory Layout

**Status**: In Progress
**Created**: 2026-03-09

## Background

The current `docs/` structure places English documents at the root and Korean
translations in `docs/dev/` with a `.ko.md` suffix. This layout is asymmetric
between languages and does not scale consistently when adding new languages.

The goal is to adopt a `docs/en/`, `docs/ko/` pattern that treats each language
equally and makes the structure extensible.

## Acceptance Criteria

- [ ] English docs moved to `docs/en/{specifications,issue,policy}/`
- [ ] Korean docs moved to `docs/ko/{specifications,issue,policy}/` without `.ko.md` suffix
- [ ] `docs/reference/` stays at root level (language-neutral)
- [ ] `docs/dev/` directory removed
- [ ] CLAUDE.md and `templates/CLAUDE.md` updated to new paths
- [ ] All policy files updated with new path references
- [ ] All skills updated to reference new paths
- [ ] `skills/sync-dev/` renamed to `skills/sync-translations/`
- [ ] README.md updated
- [ ] No residual references to old paths (`docs/dev/`, `docs/policy/`, `.ko.md` in skills)

## Tasks

- [ ] 1. Create issue004 documents (English + Korean) under old structure
- [ ] 2. Migrate files with `git mv` to new directory layout
- [ ] 3. Update CLAUDE.md and `templates/CLAUDE.md`
- [ ] 4. Update policy files (English and Korean)
- [ ] 5. Update all skills for new paths
- [ ] 6. Rename `skills/sync-dev/` to `skills/sync-translations/`
- [ ] 7. Update README.md
- [ ] 8. Verify no residual old-path references

## Notes

- Historical issues (001–003) are preserved as-is since they reflect the structure
  at the time they were written.
- The `reference/` directory remains at `docs/reference/` because reference
  materials are language-neutral and user-managed.
