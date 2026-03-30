# Issue 010: Unify planning skills into dev-planning with test traceability

**Status**: In Progress
**Created**: 2026-03-30

## Background

The repository currently has two separate planning skills — `backend-planning`
and `frontend-planning` — with different pipeline structures. In practice, the
first four steps (requirements, user stories, use cases, sequence diagrams) are
domain-agnostic. Only the final specification step differs by domain type.

This issue unifies both skills into a single `dev-planning` skill with:

1. A shared 4-step common pipeline followed by a domain-specific step
2. ID-based linking across documents (FR-XXX, AC-XXX, UC-XXX)
3. A new `test-spec.md` final step that owns all test definitions, referencing
   IDs from earlier steps to build a test matrix

This also supersedes Issue 008 (frontend-planning restructuring), absorbing its
goals into the broader unification.

## Unified Pipeline

```text
Step 0:   Tech stack detection + domain type (backend/frontend/infra)
Step 0.5: Domain analysis & document discovery
Step 1:   Requirements          → <domain>/requirements/requirements.md   [common, FR-XXX]
Step 2:   User Stories           → <domain>/requirements/user-stories.md   [common, US-XXX, AC-XXX]
Step 3:   Use Cases              → <domain>/workflows/use-cases.md         [common, UC-XXX]
Step 4:   Sequence Diagrams      → <domain>/workflows/sequence-diagram.md  [common]
Step 5:   Domain-Specific Spec   → <domain>/workflows/<spec>.md           [branched]
             Backend:  api-spec.md
             Frontend: component-spec.md
             Infra:    infra-spec.md
Step 6:   Test Specification     → <domain>/workflows/test-spec.md         [common]
Step 7:   README (table of contents)
```

## Skill Directory Structure

```text
skills/dev-planning/
├── SKILL.md                          # v0.1.0
└── references/
    ├── common/
    │   ├── requirements-template.md
    │   ├── user-stories-template.md
    │   ├── use-cases-template.md
    │   ├── sequence-diagram-template.md
    │   └── test-spec-template.md
    ├── backend/
    │   └── api-spec-template.md
    ├── frontend/
    │   └── component-spec-template.md
    └── infra/
        └── infra-spec-template.md
```

## Acceptance Criteria

- [ ] `skills/dev-planning/` created with SKILL.md and 9 templates
- [ ] Common templates (Steps 1-4) contain only IDs, no test definitions
- [ ] `test-spec-template.md` references IDs from earlier steps (FR, AC, UC)
- [ ] `component-spec-template.md` merges component-tree + state-api + ui-spec
- [ ] `infra-spec-template.md` exists as a placeholder
- [ ] `backend-planning` and `frontend-planning` marked as deprecated (v0.0.2)
- [ ] CHANGELOG.md updated with all version entries
- [ ] Issue 008 marked as Superseded

## Tasks

- [ ] 1. Create issue documents (EN/KO)
- [ ] 2. Mark Issue 008 as Superseded
- [ ] 3. Create `skills/dev-planning/` directory structure
- [ ] 4. Create common templates (requirements, user-stories, use-cases, sequence-diagram)
- [ ] 5. Create `backend/api-spec-template.md` (from existing)
- [ ] 6. Create `frontend/component-spec-template.md` (merge 3 templates)
- [ ] 7. Create `infra/infra-spec-template.md` (placeholder)
- [ ] 8. Create `common/test-spec-template.md`
- [ ] 9. Write `dev-planning/SKILL.md`
- [ ] 10. Deprecate `backend-planning` and `frontend-planning` (v0.0.2)
- [ ] 11. Update CHANGELOG.md

## Notes

- `backend-planning` and `frontend-planning` directories are kept but deprecated,
  not deleted, to provide a migration path.
- The `infra-spec-template.md` is a placeholder — full infra support is future work.
- Planning/design documents (Steps 1-5) contain no test-related content (no test
  types, mocking boundaries). All test definitions live exclusively in test-spec.
- Issue 008 goals (navigation headers, directory restructuring) are absorbed into
  this unified approach.
