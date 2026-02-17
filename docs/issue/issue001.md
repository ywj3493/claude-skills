# Issue 001: Bootstrap Repository Documentation

**Status**: Done
**Created**: 2026-02-17

## Background

The skills factory repository was initialized with skills and templates but had
no `docs/` structure of its own. This issue tracks applying the `init-docs`
skill to the factory repository itself — verifying that the skills and template
CLAUDE.md work correctly when applied to this project.

## Acceptance Criteria

- [x] `docs/` directory structure created via `create-structure.sh`
- [x] Root `CLAUDE.md` replaced with `templates/CLAUDE.md` content (unified)
- [x] Three initial policy files created in English
- [x] Korean mirrors created in `docs/dev/policy/`
- [x] `README.md` rewritten in Korean with factory developer guide

## Tasks

- [x] 1. Run `skills/init-docs/scripts/create-structure.sh`
- [x] 2. Replace root `CLAUDE.md` with `templates/CLAUDE.md` content
- [x] 3. Create `docs/policy/policy.md`
- [x] 4. Create `docs/policy/commit-message-rule.md`
- [x] 5. Create `docs/policy/naming-conventions.md`
- [x] 6. Create Korean mirrors in `docs/dev/policy/`
- [x] 7. Rewrite `README.md` in Korean with factory developer guide

## Notes

This is the bootstrap issue — created to document the initial setup of the
repository's own documentation system and to verify that the skills and template
work correctly when applied to this project itself.

The root `CLAUDE.md` and `templates/CLAUDE.md` are now identical, which allows
other projects to adopt the template with confidence that it has been tested
in practice.
