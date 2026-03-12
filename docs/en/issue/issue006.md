# Issue 006: Improve frontend-planning Skill with Document Discovery and @-reference Links

**Status**: Done

## Background

The current `frontend-planning` skill has weak project document referencing:
- Steps 1 and 6 contain vague instructions like "check for existing backend documents"
- Only hardcoded paths (`docs/en/specifications/api-spec.md`) are mentioned, failing to handle nested directory structures (e.g., `auth/requirements/api-spec.md`)
- Uses backtick paths only, not following the `@`-reference convention from [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md)

For projects with rich documentation (like auth-gateway), the skill should automatically discover existing documents and generate proper `@`-reference links.

## Acceptance Criteria

- [x] SKILL.md Step 0.5 extended to include "Document Discovery" after domain analysis
- [x] Pipeline overview updated to reflect "Domain analysis & document discovery"
- [x] Steps 1-4, 6, 7 reference document discovery results with specific document type mappings
- [x] A "Document Discovery Rules" section is added to SKILL.md
- [x] All 6 template files convert backtick prerequisite paths to `@`-reference format
- [x] All 6 template files include a `**Reference Documents**` placeholder field in the meta block
- [x] `requirements-template.md` section 6 replaces hardcoded path with placeholder
- [x] `state-api-integration-template.md` endpoint table includes a Source column

## Tasks

1. [x] Create issue document (en + ko)
2. [x] Update `skills/frontend-planning/SKILL.md`
   - Extend Step 0.5 to include document discovery (items 6-10)
   - Update pipeline overview
   - Modify Steps 1-4, 6 with document type references
   - Add Step 7 related project docs section
   - Add Document Discovery Rules section
3. [x] Update 6 template files
   - Convert backtick paths to `@`-references
   - Add `**Reference Documents**` placeholder
   - Fix `requirements-template.md` section 6
   - Add Source column to `state-api-integration-template.md` endpoint table

## Notes

- Document type classification: `requirements`, `user-stories`, `use-cases`, `api-spec`, `sequence-diagram`, `architecture`, `config`, `infrastructure`, `deployment`, `policy`, `other`
- Scan targets: `README.md`, `CLAUDE.md`, `docs/en/specifications/` (recursive), `docs/en/policy/`
- `docs/reference/` files must never use `@`-prefix per reference-convention.md
- Merged document discovery into existing Step 0.5 (Domain Analysis) to avoid awkward numbering
