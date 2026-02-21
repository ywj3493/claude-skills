# Issue 002: Introduce @-reference convention for document navigation

**Status**: Open
**Created**: 2026-02-19

## Background

The current documentation system uses backtick-quoted paths for both illustrative
examples and mandatory references, making it difficult for humans and AI agents
to distinguish between them at a glance.

For example, in CLAUDE.md:

- Line 33: `docs/issue/issue003.md` — an illustrative example (no need to read)
- Line 48: `docs/policy/policy.md` — a mandatory reference (must be loaded)

Both use the same backtick notation, offering no visual or semantic signal about
which files are required context. This slows down onboarding and context loading
for both humans and agents.

## Acceptance Criteria

- [ ] A `reference-convention.md` policy defines the `@`-reference syntax
- [ ] CLAUDE.md uses `[@path](path)` for all mandatory-context files
- [ ] `templates/CLAUDE.md` matches the updated root `CLAUDE.md`
- [ ] `docs/policy/policy.md` uses `@`-references in "Related Policy Files"
- [ ] Existing skills (`new-policy`, `init-docs`) updated to emit `@`-references
- [ ] All Korean mirrors created or updated
- [ ] No broken `@`-references (all referenced files exist)
- [ ] Backtick-only paths remain unchanged for illustrative/example references

## Tasks

- [ ] 1. Create issue002 documents (English + Korean)
- [ ] 2. Create `docs/policy/reference-convention.md` and Korean mirror
- [ ] 3. Restructure CLAUDE.md: rename "Policy Files" to "Required Context", apply `@`-references
- [ ] 4. Update `templates/CLAUDE.md` to match
- [ ] 5. Update `docs/policy/policy.md` "Related Policy Files" with `@`-references
- [ ] 6. Update `skills/new-policy/SKILL.md` to suggest `@`-reference format
- [ ] 7. Update `skills/init-docs/SKILL.md` embedded templates
- [ ] 8. Sync all Korean mirrors

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->

- **Syntax choice**: `[@docs/policy/policy.md](docs/policy/policy.md)` format selected.
  This renders as a clickable link in GitHub/IDEs while the `@` prefix signals
  "required context" to both humans and agents.
- **grep extraction**: `grep -rn '\[@docs/' CLAUDE.md` to list all mandatory references.
