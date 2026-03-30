---
name: dev-planning
version: 0.1.0
description: Unified planning document pipeline (requirements -> user stories -> use cases -> sequence diagrams -> domain-specific spec -> test spec) with ID-based test traceability. Supports backend, frontend, and infrastructure domains.
---

# dev-planning

Unified planning document pipeline for all project types, organized by domain.
The first 4 steps are shared across all domains. Step 5 branches by domain type.
Step 6 generates a test specification referencing IDs from all previous steps.

## When to Use

- User says "기획", "planning", "설계", "plan backend", "plan frontend", "plan infra"
- User says "기획 문서", "기획 문서 만들어줘", "dev planning", "API 설계", "UI 설계"
- Starting a new project that needs structured design documents
- Adding a major feature that requires multi-document planning

## When NOT to Use

- Fixing a single endpoint, component, or small tweak
- Editing or updating existing specification documents
- Work that doesn't need multi-document planning

## Pipeline Overview

```text
Step 0:   Tech stack detection + domain type classification
Step 0.5: Domain analysis & document discovery
Step 1:   Requirements          -> <domain>/requirements/requirements.md       [common]
Step 2:   User Stories           -> <domain>/requirements/user-stories.md       [common]
Step 3:   Use Cases              -> <domain>/workflows/use-cases.md             [common]
Step 4:   Sequence Diagrams      -> <domain>/workflows/sequence-diagram.md      [common]
Step 5:   Domain-Specific Spec   -> <domain>/workflows/<spec>.md               [branched]
             Backend:  api-spec.md
             Frontend: component-spec.md
             Infra:    infra-spec.md
Step 6:   Test Specification     -> <domain>/workflows/test-spec.md             [common]
Step 7:   README (table of contents)
```

For multi-domain projects, Steps 1-6 repeat per domain. Step 7 runs once.

## Output Structure

```text
docs/en/specifications/
├── architecture.md              # Cross-cutting (created by init-docs)
├── infrastructure.md            # Cross-cutting (created by init-docs)
├── config.md                    # Cross-cutting (created by init-docs)
├── README.md                    # Index of all domains/documents (Step 7)
└── <domain>/
    ├── requirements/
    │   ├── requirements.md      # Step 1
    │   └── user-stories.md      # Step 2
    └── workflows/
        ├── use-cases.md         # Step 3
        ├── sequence-diagram.md  # Step 4
        ├── api-spec.md          # Step 5 (backend only)
        ├── component-spec.md    # Step 5 (frontend only)
        ├── infra-spec.md        # Step 5 (infra only)
        └── test-spec.md         # Step 6
```

## ID System

Each document assigns its own IDs. These IDs are referenced by `test-spec.md`
to derive test cases. Planning/design documents (Steps 1-5) contain **no test
definitions** — only IDs.

| Document | ID Format | Example |
|----------|-----------|---------|
| Requirements | `FR-<AREA>-NN`, `NFR-<CAT>-NN` | FR-AUTH-01, NFR-SEC-01 |
| User Stories | `US-NN`, `AC-USNN-NN` | US-01, AC-US01-01 |
| Use Cases | `UC-<AREA>-NN` | UC-AUTH-01 |
| Sequence Diagrams | (references UC-XXX) | — |
| Domain Spec | (endpoint/component names) | — |

## Navigation

Every domain document includes two navigation blocks:

**Top** — sequential prev/next for linear reading:
```markdown
> [← Requirements](requirements.md) | [User Stories →](user-stories.md)
```
First document omits "←", last document omits "→".

**Bottom** — full index to jump to any document:
```markdown
---
> **All Documents**
> [Requirements](../requirements/requirements.md) | ... | [Test Spec](test-spec.md)
```
The current document is shown in **bold** instead of a link.

## Step-by-Step Instructions

### Step 0: Detect Tech Stack + Domain Type

Before generating any documents, detect the project's tech stack and classify
the domain type.

1. Scan for project manifests:
   - Python: `pyproject.toml`, `requirements.txt`, `setup.py`
   - Node.js: `package.json`, `tsconfig.json`
   - Java: `pom.xml`, `build.gradle`
   - Go: `go.mod`
   - Rust: `Cargo.toml`
   - Ruby: `Gemfile`
   - Infrastructure: `terraform/`, `kubernetes/`, `docker-compose.yml`, `ansible/`
2. Detect framework, database, ORM, API style, architecture pattern
3. Scan directory structure — `src/`, `app/`, `pages/`, `components/`, `deploy/`
4. Classify the **domain type** based on detected stack:
   - **Backend**: Server framework detected (FastAPI, Express, Spring Boot, Gin, etc.)
   - **Frontend**: UI framework detected (React, Vue, Angular, Next.js, Nuxt, etc.)
   - **Infra**: Infrastructure-as-code detected (Terraform, Kubernetes, Ansible, etc.)
   - If both backend and frontend exist, ask the user which domain to plan first

Summarize and confirm with the user:

> **Detected tech stack:**
> - Language: ...
> - Framework: ...
> - Domain type: Backend / Frontend / Infra
>
> Does this look correct?

Wait for confirmation before proceeding.

### Step 0.5: Domain Analysis & Document Discovery

**Domain Analysis**

1. Ask the user to describe major feature areas
2. Propose domain groupings (e.g., `auth`, `dashboard`, `payment`)
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

1. Load template: `references/common/requirements-template.md`
2. Load discovered docs classified as `requirements`, `user-stories`, or `architecture`
3. Ask user for: system purpose, stakeholders, core features, non-functional requirements, constraints
4. Generate document with:
   - System context diagram (C4Context Mermaid)
   - Functional requirements grouped by area (`FR-<AREA>-NN` format)
   - Non-functional requirements (`NFR-<CAT>-NN` format)
   - Constraints (technical, architecture, operational)
   - Requirements traceability matrix
5. Wait for review

> **Step 1 complete**: Requirements generated.
> Please review. Ready to proceed?

### Step 2: User Stories

**Output**: `<domain>/requirements/user-stories.md`

1. Load template: `references/common/user-stories-template.md`
2. Load Step 1 output
3. For each major feature, create user stories:
   - **As a** [role], **I want to** [capability], **So that** [benefit]
   - Acceptance criteria with `AC-USNN-NN` IDs in **Given/When/Then** format
   - Non-functional requirements per story
   - Related requirements references
4. Include story-requirement traceability table with AC count
5. Wait for review

> **Step 2 complete**: User stories generated.
> Please review. Ready to proceed?

### Step 3: Use Cases

**Output**: `<domain>/workflows/use-cases.md`

1. Load template: `references/common/use-cases-template.md`
2. Load previous outputs: Steps 1-2
3. Load discovered docs classified as `use-cases` or `architecture`
4. For each use case (`UC-<AREA>-NN`), define:
   - Basic information (actors, related requirements, related user stories)
   - Preconditions and postconditions
   - Main flow with sequenceDiagram Mermaid
   - Alternative flows with branch points
5. Include actor definitions, use case diagram, relationship table
6. Wait for review

> **Step 3 complete**: Use cases generated.
> Please review. Ready to proceed?

### Step 4: Sequence Diagrams

**Output**: `<domain>/workflows/sequence-diagram.md`

1. Load template: `references/common/sequence-diagram-template.md`
2. Load previous outputs: Steps 1-3
3. For each major flow, create:
   - sequenceDiagram Mermaid showing architecture layer interactions
   - Participants labeled as `FileName<br/>(Layer)` notation
   - Key steps and related code references
4. Include:
   - Architecture layer structure
   - Normal flows, error handling flows
   - Performance optimization points
5. Wait for review

> **Step 4 complete**: Sequence diagrams generated.
> Please review. Ready to proceed?

### Step 5: Domain-Specific Specification

**Output**: `<domain>/workflows/<spec>.md`

Branch based on the domain type detected in Step 0:

#### If Backend: API Specification

**Output**: `<domain>/workflows/api-spec.md`

1. Load template: `references/backend/api-spec-template.md`
2. Load previous outputs: Steps 1-4
3. For each API endpoint, define:
   - HTTP method, path, authentication requirements
   - Request/response schemas with JSON examples
   - curl and JavaScript examples
   - Error responses
4. Include: endpoint catalog, data models, authentication flow, error codes
5. Wait for review

#### If Frontend: Component Specification

**Output**: `<domain>/workflows/component-spec.md`

1. Load template: `references/frontend/component-spec-template.md`
2. Load previous outputs: Steps 1-4
3. Load discovered docs classified as `api-spec` — use as endpoint source
4. Define:
   - UI overview (views, URLs, access levels, responsive strategy)
   - Component tree with Mermaid hierarchy
   - Shared and page-specific components with TypeScript prop interfaces
   - State management strategy and store definitions
   - API endpoint list with request/response DTOs
   - Caching strategy and error handling patterns
5. Wait for review

#### If Infra: Infrastructure Specification

**Output**: `<domain>/workflows/infra-spec.md`

1. Load template: `references/infra/infra-spec-template.md`
2. Load previous outputs: Steps 1-4
3. Define:
   - Deployment topology
   - Environment configurations
   - CI/CD pipeline
   - Resource definitions, monitoring, security
4. Wait for review

> **Step 5 complete**: Domain specification generated.
> Please review. Ready to proceed?

### Step 6: Test Specification

**Output**: `<domain>/workflows/test-spec.md`

1. Load template: `references/common/test-spec-template.md`
2. Load **all** previous outputs: Steps 1-5
3. Derive test cases by scanning IDs from earlier documents:
   - `AC-USNN-NN` from user stories -> E2E and acceptance tests
   - `UC-<AREA>-NN` main/alternative flows -> integration and unit tests
   - Domain spec endpoints/components -> contract tests
4. Generate:
   - Test matrix with Test IDs (`T-NNN`), source references, type, priority
   - Mocking boundaries for unit/integration/E2E levels
   - Proposed test file structure
   - Test-requirement traceability matrix
5. Wait for review

> **Step 6 complete**: Test specification generated.
> Please review. Ready to proceed to README?

### Step 7: Generate README

**Output**: `docs/en/specifications/README.md`

After all domains complete Steps 1-6:

- Single-domain: table of contents linking all documents (6 per domain + test-spec)
- Multi-domain: section per domain + optional per-domain README.md
- If README exists, merge rather than overwrite
- Include discovered documents in a **Related Project Documents** section

Report all generated file paths on completion.

> **Planning complete.** Generated documents:
> - `<domain>/requirements/requirements.md`
> - `<domain>/requirements/user-stories.md`
> - `<domain>/workflows/use-cases.md`
> - `<domain>/workflows/sequence-diagram.md`
> - `<domain>/workflows/<domain-spec>.md`
> - `<domain>/workflows/test-spec.md`
> - `docs/en/specifications/README.md`

## Document Rules

- **Language**: English
- **Meta block**: Created, Last Modified, Status, Tech Stack, Reference Documents
- **Mermaid**: `sequenceDiagram` for flows, `C4Context` for system context, `graph TD/LR` for hierarchies
- **TypeScript**: `interface` for props, stores, DTOs (frontend domain)
- **IDs**: FR-XXX, NFR-XXX, US-NN, AC-USNN-NN, UC-XXX — no test content in planning docs
- **Cross-references**: FR -> UC -> Domain Spec -> Test Spec links
- **Given/When/Then**: Acceptance criteria format in user stories
- **Participant notation**: `FileName<br/>(Layer)` in sequence diagrams
- **References**: Each step loads all previous step outputs before generating
- **Review gate**: Never proceed to the next step without user approval
- **Navigation**: Every domain document has top (prev/next) and bottom (all documents) navigation
- **Navigation placeholders**: Templates use `<domain-spec>` as a placeholder in navigation links. When generating documents, replace with the actual domain spec filename: `api-spec` (backend), `component-spec` (frontend), `infra-spec` (infra)
- **`@`-references**: Use for discovered docs per [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md)
