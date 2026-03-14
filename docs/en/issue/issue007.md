# Issue 007: Create backend-planning Skill

**Status**: Done
**Created**: 2026-03-12

## Background

The project has a `frontend-planning` skill that generates a 6-step planning
document pipeline for frontend projects. An analogous skill is needed for
backend projects, following the document format established in the
`auth-gateway` project's specification documents (requirements, user stories,
API specification, use cases, sequence diagrams).

## Acceptance Criteria

- [x] Skill directory exists at `~/.agents/skills/backend-planning/`
- [x] `SKILL.md` defines a 5-step pipeline with tech stack detection and domain analysis
- [x] Five reference templates exist under `references/`:
  - `requirements-template.md`
  - `user-stories-template.md`
  - `api-spec-template.md`
  - `use-cases-template.md`
  - `sequence-diagram-template.md`
- [x] Each template includes Document Navigation links (Previous/Next)
- [x] Templates use the auth-gateway document format (meta header, ToC, Mermaid diagrams, cross-references)
- [x] README generation step produces a table of contents with clickable links
- [x] Issue documents created in both `docs/en/issue/` and `docs/ko/issue/`

## Tasks

1. [x] Create issue documents (EN + KO)
2. [x] Create `~/.agents/skills/backend-planning/SKILL.md`
3. [x] Create `references/requirements-template.md`
4. [x] Create `references/user-stories-template.md`
5. [x] Create `references/api-spec-template.md`
6. [x] Create `references/use-cases-template.md`
7. [x] Create `references/sequence-diagram-template.md`
8. [x] Verify all files and navigation links

## Notes

- The backend-planning skill produces 5 content documents (vs 6 for frontend)
- Navigation chain: requirements -> user-stories -> api-spec -> use-cases -> sequence-diagram
- Output goes to `docs/en/specifications/<domain>/requirements/` and `docs/en/specifications/<domain>/workflows/`
- Templates are generalized from the `auth-gateway` project's actual specification documents

Refs: issue007
