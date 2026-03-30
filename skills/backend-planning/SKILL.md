---
name: backend-planning
version: 0.0.2
description: "[DEPRECATED] Use dev-planning instead. Former 5-step backend planning pipeline."
deprecated: true
superseded_by: dev-planning
---

# backend-planning

> **DEPRECATED**: This skill has been superseded by `dev-planning`.
> Use `dev-planning` instead, which supports backend, frontend, and infrastructure
> domains in a unified pipeline with test traceability.

5-step planning document pipeline for backend projects, organized by domain.

## When to Use

- User says "백엔드 기획", "backend planning", "API 설계", "서버 설계"
- User says "백엔드 문서", "기획 문서 만들어줘", "plan backend"
- Starting a new backend project that needs structured design documents
- Adding a major backend feature that requires multi-document planning

## When NOT to Use

- Frontend-only projects (use the frontend planning pipeline instead)
- Fixing a single endpoint or small API tweak
- Editing or updating existing specification documents
- Non-backend work such as CI/CD, infrastructure, or tooling

## Pipeline Overview

```text
Step 0:   Tech stack detection
Step 0.5: Domain analysis
Step 1:   Requirements Analysis
Step 2:   User Stories
Step 3:   API Specification
Step 4:   Use Cases
Step 5:   Sequence Diagrams
Step 6:   README (table of contents)
```

For multi-domain projects, Steps 1–5 are completed for each domain before
moving to the next. Step 6 runs once at the end to generate the index.

## Output Structure

```text
docs/en/specifications/
├── architecture.md              # Project folder structure (created by init-docs)
├── config.md                    # Environment variables (created by init-docs)
├── infrastructure.md            # Infrastructure description (created by init-docs)
├── README.md                    # Index of all domains/documents (Step 6)
└── <domain>/
    ├── requirements/
    │   ├── requirements.md      # Step 1
    │   ├── user-stories.md      # Step 2
    │   └── api-spec.md          # Step 3
    └── workflows/
        ├── use-cases.md         # Step 4
        └── sequence-diagram.md  # Step 5
```

## Step-by-Step Instructions

### Step 0: Detect Tech Stack

Before generating any documents, detect the project's backend tech stack:

1. Scan for project manifests:
   - Python: `pyproject.toml`, `requirements.txt`, `setup.py`
   - Node.js: `package.json`
   - Java: `pom.xml`, `build.gradle`
   - Go: `go.mod`
   - Rust: `Cargo.toml`
   - Ruby: `Gemfile`
2. Detect web framework: FastAPI, Django, Express, Spring Boot, Gin, Actix, Rails, etc.
3. Detect database and ORM:
   - Prisma, SQLAlchemy, TypeORM, Sequelize, GORM, Diesel, ActiveRecord
   - Migration files, schema definitions
4. Detect API style: REST, GraphQL, gRPC (check for `.proto` files, GraphQL schemas)
5. Detect architecture pattern: DDD, MVC, hexagonal, clean architecture (from directory structure)
6. Check for infrastructure: Docker, Redis, message queues, etc.

Summarize the detected stack and confirm with the user:

> **Detected tech stack:**
> - Language: Python 3.11
> - Framework: FastAPI 0.115
> - Database: Redis (session storage)
> - ORM: None (key-value store)
> - API Style: REST
> - Architecture: 4-Layer DDD
> - Infrastructure: Docker, Redis
>
> I'll generate planning documents based on this stack. Does this look correct?

Wait for confirmation before proceeding.

### Step 0.5: Domain Analysis

After confirming the tech stack, identify the project's domain structure:

1. Ask the user to describe the project's major feature areas
2. Propose domain groupings based on their description (e.g., `auth`, `payment`, `notification`)
3. Always create at least one domain directory — even single-domain projects use `specifications/<domain>/`
4. Present the proposed directory structure for confirmation:

> **Proposed domain structure:**
>
> ```
> docs/en/specifications/
> ├── auth/
> │   ├── requirements/
> │   └── workflows/
> └── notification/
>     ├── requirements/
>     └── workflows/
> ```
>
> I'll generate the 5 planning documents for each domain in sequence.
> Shall I proceed with this structure?

5. Store the confirmed domain list for subsequent steps

Wait for confirmation before proceeding. If the user requests changes to the
domain groupings, adjust and re-confirm.

### Step 1: Requirements Analysis

**Output**: `docs/en/specifications/<domain>/requirements/requirements.md`

1. Load the reference template: `references/requirements-template.md`
2. Check `docs/en/specifications/` for existing documents — reference them if present
3. Ask the user to describe:
   - System purpose and stakeholders
   - Core features and functional requirements
   - Non-functional requirements (performance, security, deployment)
   - Constraints (technical, operational)
4. Generate the document following the template structure, including:
   - System context diagram (C4Context Mermaid)
   - Functional requirements grouped by domain area (FR-XXX-NN format)
   - Non-functional requirements (NFR-XXX-NN format)
   - Constraints (technical, architecture, operational)
   - Requirements traceability matrix
5. Present the document to the user and wait for review

> **Step 1/5 complete**: Requirements analysis generated.
> Please review and let me know if any changes are needed. Ready to proceed to the next step?

### Step 2: User Stories

**Output**: `docs/en/specifications/<domain>/requirements/user-stories.md`

1. Load the reference template: `references/user-stories-template.md`
2. Load Step 1 output: `<domain>/requirements/requirements.md`
3. For each major feature, create user stories:
   - **As a** [role], **I want to** [capability], **So that** [benefit]
   - Acceptance criteria in **Given/When/Then** format (normal and error cases)
   - Non-functional requirements per story
   - Related requirements and API endpoint references
4. Include a story-requirement traceability table
5. Generate the document and wait for review

> **Step 2/5 complete**: User stories generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 3: API Specification

**Output**: `docs/en/specifications/<domain>/requirements/api-spec.md`

1. Load the reference template: `references/api-spec-template.md`
2. Load previous outputs: Steps 1–2
3. For each API endpoint, define:
   - HTTP method, path, authentication requirements
   - Request headers, body schema (with JSON examples)
   - Response schemas for success and error cases
   - curl and JavaScript (Fetch) examples
   - Related use case and sequence diagram references
4. Include:
   - Endpoint catalog table
   - Data models with JSON Schema
   - Authentication flow diagram (sequenceDiagram Mermaid)
   - Error response standard format
5. Generate the document and wait for review

> **Step 3/5 complete**: API specification generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 4: Use Cases

**Output**: `docs/en/specifications/<domain>/workflows/use-cases.md`

1. Load the reference template: `references/use-cases-template.md`
2. Load previous outputs: Steps 1–3
3. For each use case, define:
   - Basic information table (ID, actors, related requirements, API endpoint)
   - Preconditions and postconditions (success and failure)
   - Main flow with **sequenceDiagram** Mermaid diagram
   - Step-by-step description
   - Alternative flows with branch points
   - Test scenarios with curl/JS examples
4. Include:
   - Actor definitions with Mermaid diagrams
   - Use case diagram (graph TD Mermaid)
   - Use case relationship table (include/extend)
5. Generate the document and wait for review

> **Step 4/5 complete**: Use cases generated.
> Please review and let me know if any changes are needed. Ready to proceed?

### Step 5: Sequence Diagrams

**Output**: `docs/en/specifications/<domain>/workflows/sequence-diagram.md`

1. Load the reference template: `references/sequence-diagram-template.md`
2. Load previous outputs: Steps 1–4
3. For each major flow, create:
   - **sequenceDiagram** Mermaid diagram showing architecture layer interactions
   - Participants labeled as `FileName<br/>(Layer)` notation
   - Key steps summary
   - Related code file references
4. Include:
   - Architecture layer structure diagram (ASCII art)
   - Normal flows (authentication, CRUD, business logic)
   - Error handling flows (expired sessions, external service failures)
   - Performance optimization points
5. Generate the document and wait for review

> **Step 5/5 complete**: Sequence diagrams generated.
> Please review and let me know if any changes are needed.

### Step 6: Generate README

**Output**: `docs/en/specifications/README.md`

After all domains have completed Steps 1–5, generate a table of contents.

For single-domain projects:

```markdown
# Specifications

## Domains

### <domain>

| Document | Path | Description |
|----------|------|-------------|
| Requirements | [requirements.md](<domain>/requirements/requirements.md) | Stakeholders, functional/non-functional requirements, constraints |
| User Stories | [user-stories.md](<domain>/requirements/user-stories.md) | User stories with Given/When/Then acceptance criteria |
| API Specification | [api-spec.md](<domain>/requirements/api-spec.md) | API endpoints, request/response schemas, examples |
| Use Cases | [use-cases.md](<domain>/workflows/use-cases.md) | Actor-system interactions with sequence diagrams |
| Sequence Diagrams | [sequence-diagram.md](<domain>/workflows/sequence-diagram.md) | Architecture layer flows and error handling |
```

For multi-domain projects, list each domain in a separate section. Also generate
a per-domain `README.md` at `<domain>/README.md` if there are 2+ domains.

If `docs/en/specifications/README.md` already exists, merge the backend
planning section rather than overwriting.

Report completion:

> **Backend planning complete.** Generated documents for all domains:
> - `docs/en/specifications/<domain>/requirements/requirements.md`
> - `docs/en/specifications/<domain>/requirements/user-stories.md`
> - `docs/en/specifications/<domain>/requirements/api-spec.md`
> - `docs/en/specifications/<domain>/workflows/use-cases.md`
> - `docs/en/specifications/<domain>/workflows/sequence-diagram.md`
> - `docs/en/specifications/README.md`

## Document Rules

- **Language**: English
- **Meta block**: Every document includes Version, Last Updated, Status
- **Document Navigation**: Previous/Next links after the meta block
- **Table of Contents**: Numbered sections
- **Mermaid**: Use `sequenceDiagram` for flows, `C4Context` for system context, `graph TD/LR` for relationships
- **Cross-references**: FR → UC → API → Implementation links
- **Given/When/Then**: Acceptance criteria format in user stories
- **Test scenarios**: curl and JavaScript (Fetch) examples in use cases
- **Participant notation**: `FileName<br/>(Layer)` in sequence diagrams
- **References**: Each step must load all previous step outputs before generating
- **Review gate**: Never proceed to the next step without user approval
