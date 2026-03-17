# Issue 008: Restructure frontend-planning skill pipeline and templates

**Status**: Open
**Created**: 2026-03-16

## Background

The current frontend-planning skill has a 6-step document pipeline with
`user-flows` placed under `workflows/`. The directory structure does not clearly
separate planning (requirements/design) documents from implementation
(development) documents. Additionally, the skill lacks templates for
`architecture.md` and `infrastructure.md`, and domain documents have no
cross-navigation links.

This issue restructures the skill to:

1. Add `architecture.md` and `infrastructure.md` templates with Mermaid diagrams
2. Move planning documents (`user-flows`, `ui-spec`) under `requirements/`
3. Add document navigation headers to every domain document

## Proposed Directory Structure

```text
docs/en/specifications/
├── architecture.md              # Project directory structure (Mermaid)
├── infrastructure.md            # Deployment & infra (Mermaid) — outside domains
├── config.md
├── README.md
└── <domain>/
    ├── requirements/
    │   ├── requirements.md      # Step 1: Functional/non-functional requirements
    │   ├── user-flows.md        # Step 2: User journey flowcharts (was workflows/)
    │   └── ui-spec.md            # Step 3: UI specifications (renamed from page-spec)
    └── workflows/
        ├── use-cases.md         # Step 4: Actor-system interactions
        ├── component-tree.md    # Step 5: Component hierarchy & props
        └── state-api-integration.md  # Step 6: State management & API layer
```

## Change Details

### 1. architecture.md & infrastructure.md templates

- `architecture.md`: Mermaid graph showing project directory structure, module
  boundaries, and key file relationships. Lives at `docs/en/specifications/`
  (cross-cutting, not domain-specific).
- `infrastructure.md`: Mermaid diagram of deployment topology, CI/CD pipeline,
  external services, and environments. Lives at `docs/en/specifications/`
  (cross-cutting, not domain-specific).
- Both templates emphasize visual representation via Mermaid.

### 2. Reorganize planning vs implementation documents

- Move `user-flows.md` from `workflows/` to `requirements/` — user flows
  describe the planned user journey and belong with requirements.
- Rename `page-spec.md` to `ui-spec.md` and move from `workflows/` to
  `requirements/` — UI specs define layout structure, responsive rules, and
  interaction patterns. The name "ui-spec" covers page-based apps, design
  systems, and component libraries equally. Component mapping details are
  covered in `component-tree.md`.
- `requirements/` = planning/design docs (what to build)
- `workflows/` = implementation docs (how to build)

### 3. Domain document navigation

Every document within a domain has two navigation blocks:

**Top navigation** — previous/next sequential links for linear reading:

```markdown
> [← Requirements](requirements/requirements.md) | [User Flows →](requirements/user-flows.md)
```

**Bottom navigation** — full index to jump to any document:

```markdown
---
> **All Documents**
> [Requirements](requirements/requirements.md) |
> [User Flows](requirements/user-flows.md) |
> [UI Spec](requirements/ui-spec.md) |
> [Use Cases](workflows/use-cases.md) |
> [Component Tree](workflows/component-tree.md) |
> [State & API](workflows/state-api-integration.md)
```

The document order is:
1. Requirements → 2. User Flows → 3. UI Spec → 4. Use Cases → 5. Component Tree → 6. State & API

The first document omits the "←" link; the last document omits the "→" link.
Links use relative paths from the current file so they work in GitHub and IDEs.

## Acceptance Criteria

- [ ] `architecture.md` template added to `references/` with Mermaid diagram
- [ ] `infrastructure.md` template added to `references/` with Mermaid diagram
- [ ] `user-flows` output path changed to `<domain>/requirements/user-flows.md`
- [ ] `page-spec` renamed to `ui-spec` and output path changed to `<domain>/requirements/ui-spec.md`
- [ ] All domain document templates include navigation header
- [ ] SKILL.md updated to reflect new pipeline structure
- [ ] SKILL.md simplified where possible
- [ ] Existing templates updated to match new paths and navigation

## Tasks

- [ ] 1. Add `architecture-template.md` to `references/`
- [ ] 2. Add `infrastructure-template.md` to `references/`
- [ ] 3. Update `user-flows-template.md` — add navigation header
- [ ] 4. Rename `page-spec-template.md` to `ui-spec-template.md` — update content and add navigation header
- [ ] 5. Update `use-cases-template.md` — add navigation header
- [ ] 6. Update `component-tree-template.md` — add navigation header
- [ ] 7. Update `state-api-integration-template.md` — add navigation header
- [ ] 8. Update `requirements-template.md` — add navigation header
- [ ] 9. Rewrite SKILL.md pipeline to reflect new structure and simplify
- [ ] 10. Verify all template cross-references use correct relative paths

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->

- **page-spec → ui-spec rename**: Renamed to `ui-spec` to cover page-based apps,
  design systems, and component libraries. Moved to `requirements/` because its
  content (layouts, responsive rules, interaction patterns) represents planning
  decisions. Component-level detail is handled by `component-tree.md` in `workflows/`.
- The pipeline step numbering remains 1–6 but the output paths change.
- `architecture.md` and `infrastructure.md` are generated in Step 0 or as a
  separate optional step, since they are cross-cutting and not domain-specific.
