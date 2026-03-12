# Issue 005: Improve frontend-planning and init-docs Skills

**Status**: In Progress
**Created**: 2026-03-12

## Background

The `frontend-planning` skill (issue003) has several gaps that need addressing:

- All prompts, templates, and user-facing messages are in Korean, but should
  be English to match the `docs/en/` convention
- No domain analysis step — all 6 documents are generated flat into
  `specifications/` with no logical grouping
- Output filenames use number prefixes (`01-requirements.md`) which should
  be removed
- The `init-docs` skill and `CLAUDE.md` need to reflect the new
  domain-based directory structure under `specifications/`

See [@docs/en/issue/issue003.md](docs/en/issue/issue003.md) for the original
skill creation issue.

## Acceptance Criteria

- [ ] `SKILL.md` description and all user-facing messages are in English
- [ ] New Step 0.5 (Domain Analysis) added between tech stack detection and requirements
- [ ] Output paths use domain-based structure: `specifications/<domain>/requirements/` and `specifications/<domain>/workflows/`
- [ ] Top-level cross-cutting docs at `specifications/` root: `architecture.md`, `config.md`, `infrastructure.md`
- [ ] All 6 reference templates renamed (number prefixes removed) and rewritten in English
- [ ] Multi-domain flow: complete all 6 steps per domain before moving to the next
- [ ] Step 7 generates `README.md` listing all domains and documents
- [ ] `init-docs` SKILL.md updated with new structure diagram
- [ ] `create-structure.sh` creates top-level spec template files
- [ ] `CLAUDE.md` documentation structure section updated
- [ ] No stale references to old numbered filenames remain
- [ ] Korean text only remains in "When to Use" trigger phrases

## Tasks

- [ ] 1. Create issue005 documents (English + Korean)
- [ ] 2. Rewrite `skills/frontend-planning/SKILL.md`
- [ ] 3. Rename and rewrite 6 reference templates in English
- [ ] 4. Create top-level spec reference templates for init-docs
- [ ] 5. Update `skills/init-docs/SKILL.md` and `scripts/create-structure.sh`
- [ ] 6. Update `CLAUDE.md` documentation structure section
- [ ] 7. Add cross-reference note to issue003

## Notes

- Domain directories are always created, even for single-domain projects
- Template files in `skills/frontend-planning/references/` are renamed without number prefixes
- Three new templates added to `skills/init-docs/references/`: `architecture-template.md`, `config-template.md`, `infrastructure-template.md`
