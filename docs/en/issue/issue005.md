# Issue 005: Fix Script Path in init-docs Skill

**Status**: Done
**Created**: 2026-03-12

## Background

During the docs restructuring in issue004, all skills were updated to reference
the new `docs/en/` and `docs/ko/` paths. However, the init-docs skill's
self-referencing script paths (`.skills/` and `~/.agents/skills/`) were not
corrected to match the actual directory structure.

In `skills/init-docs/SKILL.md`, the script invocation examples reference
`.skills/init-docs/scripts/create-structure.sh` and
`~/.agents/skills/init-docs/scripts/create-structure.sh`, but the actual path
is `skills/init-docs/scripts/create-structure.sh`.

## Acceptance Criteria

- [x] Script path in `skills/init-docs/SKILL.md` corrected to `skills/init-docs/scripts/create-structure.sh`
- [x] Fallback path updated or removed
- [x] All paths in the skill file match the actual file system

## Tasks

- [x] 1. Create issue005 documents (English + Korean)
- [x] 2. Fix script paths in `skills/init-docs/SKILL.md`
- [x] 3. Verify corrected paths match actual file locations

## Notes

- The script `skills/init-docs/scripts/create-structure.sh` exists and is the
  correct path.
- The `.skills/` prefix was a legacy convention that no longer applies.
