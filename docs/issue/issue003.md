# Issue 003: Add frontend-planning Skill

**Status**: In Progress
**Created**: 2026-02-25

## Background

The project already uses a backend planning pipeline (requirements →
user-stories → use-cases → sequence-diagram → api-spec) to produce
structured design documents before implementation begins.

Frontend projects need an equivalent pipeline adapted for UI concerns:
requirements → user-flows → page-spec → use-cases → component-tree →
state-api-integration (6 steps).

This issue tracks creating the `frontend-planning` skill, which guides
Claude through producing six planning documents in `docs/specifications/`
sequentially, pausing for user review and feedback after each step.

All planning documents are written in Korean with technical terms in
English, following the user's preference for frontend design documentation.

## Acceptance Criteria

- [ ] `skills/frontend-planning/SKILL.md` exists with correct YAML front matter
- [ ] Six reference templates exist in `skills/frontend-planning/references/`
- [ ] Skill generates documents in `docs/specifications/` (01 through 06)
- [ ] Each step references outputs of all previous steps
- [ ] User review is solicited after each step before proceeding
- [ ] Tech stack is auto-detected from `package.json` / `tsconfig.json`
- [ ] Existing backend docs in `docs/specifications/` are referenced if present
- [ ] All documents include meta info (creation date, last modified, status)
- [ ] Mermaid diagrams included in user-flows and component-tree
- [ ] TypeScript interfaces included in component-tree and state-api-integration
- [ ] After step 6, `docs/specifications/README.md` is generated as table of contents
- [ ] Correct trigger phrases (Korean and English) documented
- [ ] Non-trigger conditions documented
- [ ] Korean issue mirror exists at `docs/dev/issue/issue003.ko.md`

## Tasks

- [ ] 1. Create issue documents (English + Korean)
- [ ] 2. Create `skills/frontend-planning/SKILL.md`
- [ ] 3. Create six reference templates in `skills/frontend-planning/references/`

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->

- **Pipeline**: 6 steps — requirements → user-flows → page-spec → use-cases →
  component-tree → state-api-integration
- **Output directory**: `docs/specifications/` (same as other specification documents)
- **Language**: Korean with English technical terms (not English-first + Korean mirror)
- **Distribution**: git + `add skill` (no manual copy to `skills/` or symlink needed)
