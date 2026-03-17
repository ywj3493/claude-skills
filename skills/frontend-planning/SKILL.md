---
name: frontend-planning
description: Generates a 6-step frontend planning document pipeline (requirements → user flows → UI spec → use cases → component tree → state/API integration) into docs/en/specifications/<domain>/, with domain analysis, tech stack detection, and user review gates at each step.
---

# frontend-planning

6-step planning document pipeline for frontend projects, organized by domain.

## When to Use

- User says "프론트엔드 기획", "frontend planning", "UI 설계", "화면 설계"
- User says "프론트엔드 문서", "기획 문서 만들어줘", "plan frontend"
- Starting a new frontend project that needs structured design documents
- Adding a major frontend feature that requires multi-page planning

## When NOT to Use

- Backend-only projects (use the backend planning pipeline instead)
- Fixing a single component or small UI tweak
- Editing or updating existing specification documents
- Non-UI work such as CI/CD, infrastructure, or tooling

## Pipeline Overview

```text
Step 0:   Tech stack detection
Step 0.5: Domain analysis & document discovery
Step 1:   Requirements          → <domain>/requirements/requirements.md
Step 2:   User Flows            → <domain>/requirements/user-flows.md
Step 3:   UI Spec               → <domain>/requirements/ui-spec.md
Step 4:   Use Cases             → <domain>/workflows/use-cases.md
Step 5:   Component Tree        → <domain>/workflows/component-tree.md
Step 6:   State & API Integration → <domain>/workflows/state-api-integration.md
Step 7:   README (table of contents)
```

Steps 1–3 are **planning/design** documents (what to build).
Steps 4–6 are **implementation** documents (how to build).

For multi-domain projects, Steps 1–6 repeat per domain. Step 7 runs once.

## Output Structure

```text
docs/en/specifications/
├── architecture.md              # Project structure (Mermaid) — cross-cutting
├── infrastructure.md            # Deployment & infra (Mermaid) — cross-cutting
├── config.md                    # Environment variables
├── README.md                    # Index of all domains/documents (Step 7)
└── <domain>/
    ├── requirements/
    │   ├── requirements.md      # Step 1
    │   ├── user-flows.md        # Step 2
    │   └── ui-spec.md           # Step 3
    └── workflows/
        ├── use-cases.md         # Step 4
        ├── component-tree.md    # Step 5
        └── state-api-integration.md  # Step 6
```

## Navigation

Every domain document includes two navigation blocks:

**Top** — sequential prev/next for linear reading:
```markdown
> [← Requirements](requirements.md) | [UI Spec →](ui-spec.md)
```
First document omits "←", last document omits "→".

**Bottom** — full index to jump to any document:
```markdown
---
> **All Documents**
> [Requirements](requirements.md) | ... | [State & API](state-api-integration.md)
```
The current document is shown in **bold** instead of a link.

## Step-by-Step Instructions

### Step 0: Detect Tech Stack

1. Read `package.json` — framework, dependencies
2. Read `tsconfig.json` — TypeScript usage
3. Scan directory structure — `src/`, `app/`, `pages/`, `components/`
4. Check styling and state management solutions

Summarize and confirm with the user before proceeding.

### Step 0.5: Domain Analysis & Document Discovery

**Domain Analysis**

1. Ask the user to describe major feature areas
2. Propose domain groupings (e.g., `auth`, `dashboard`)
3. Always create at least one domain directory
4. Present proposed structure and wait for confirmation

**Document Discovery**

5. Scan `README.md`, `CLAUDE.md`, all `.md` files under `docs/en/specifications/` and `docs/en/policy/`
6. Classify each by first 30 lines: `requirements` / `user-stories` / `use-cases` / `api-spec` / `sequence-diagram` / `architecture` / `config` / `infrastructure` / `deployment` / `policy` / `other`
7. Present discovered documents grouped by category using `@`-reference format
8. Carry confirmed document list to all subsequent steps

If no documents found, record "No project documents found" and proceed.

### Step 1: Requirements

**Output**: `<domain>/requirements/requirements.md`

1. Load template: `references/requirements-template.md`
2. Load discovered docs classified as `requirements`, `user-stories`, or `architecture`
3. Ask user for: project purpose, target users, core features, non-functional requirements
4. Generate document and wait for review

### Step 2: User Flows

**Output**: `<domain>/requirements/user-flows.md`

1. Load template: `references/user-flows-template.md`
2. Load Step 1 output
3. Load discovered docs classified as `use-cases` or `sequence-diagram`
4. For each major feature: Mermaid flowchart (happy path), alternative/exception paths
5. Generate document and wait for review

### Step 3: UI Spec

**Output**: `<domain>/requirements/ui-spec.md`

1. Load template: `references/ui-spec-template.md`
2. Load Steps 1–2 outputs
3. Skim discovered docs classified as `api-spec` or `architecture`
4. For each view: URL/trigger, layout structure, key components, responsive behavior, SEO (if applicable)
5. Generate document and wait for review

### Step 4: Use Cases

**Output**: `<domain>/workflows/use-cases.md`

1. Load template: `references/use-cases-template.md`
2. Load Steps 1–3 outputs
3. Load discovered docs classified as `use-cases` or `architecture`
4. For each use case: actor, preconditions/postconditions, main/alternative/exception flows
5. Generate document and wait for review

### Step 5: Component Tree

**Output**: `<domain>/workflows/component-tree.md`

1. Load template: `references/component-tree-template.md`
2. Load Steps 1–4 outputs
3. Define: Mermaid graph of component hierarchy, shared vs page-specific components, TypeScript prop interfaces
4. Generate document and wait for review

### Step 6: State & API Integration

**Output**: `<domain>/workflows/state-api-integration.md`

1. Load template: `references/state-api-integration-template.md`
2. Load Steps 1–5 outputs
3. Load discovered docs classified as `api-spec` — use as authoritative endpoint source
4. Define: state strategy, store interfaces, API endpoints table, DTOs, caching, error handling
5. Generate document and wait for review

### Step 7: Generate README

**Output**: `docs/en/specifications/README.md`

After all domains complete Steps 1–6:

- Single-domain: table of contents linking all 6 documents
- Multi-domain: section per domain + optional per-domain `README.md`
- If README exists, merge rather than overwrite
- Include discovered documents in a **Related Project Documents** section

Report all generated file paths on completion.

## Document Rules

- **Language**: English
- **Meta block**: Created, Last Modified, Status, Tech Stack, Prerequisites, Reference Documents
- **Mermaid**: `flowchart TD` for user flows, `graph TD` for component trees
- **TypeScript**: `interface` for props, stores, DTOs
- **References**: Each step loads all previous outputs before generating
- **Review gate**: Never proceed without user approval
- **Navigation**: Every domain document has top (prev/next) and bottom (all documents) navigation
- **`@`-references**: Use for discovered docs per [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md); never `@`-prefix `docs/reference/` files
