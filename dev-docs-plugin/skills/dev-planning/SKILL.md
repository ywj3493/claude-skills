---
name: dev-planning
version: 0.1.0
description: Forward planning pipeline for a NEW feature or project (requirements -> user stories -> use case -> design documents -> test spec) with ID-based test traceability. Supports backend, frontend, and infrastructure domains. Do NOT use this for documenting or reverse-engineering docs from existing code — use dev-reverse-docs for that.
---

# dev-planning

Forward planning document pipeline for work that doesn't have code yet: a
new feature, a new project, or a major addition. The first 3 steps are
shared across all domains and produce WHAT-level (planning) documents. Step
4 dynamically selects which HOW-level (design) documents the feature needs.
Step 5 generates a test specification referencing IDs from every previous
step.

## When to Use

- User says "기획", "planning", "설계", "plan backend", "plan frontend", "plan infra"
- User says "기획 문서", "기획 문서 만들어줘", "dev planning", "API 설계", "UI 설계"
- "design this feature", "create planning docs", "spec out a new feature"
- Starting a new project that needs structured design documents
- Adding a major feature that requires multi-document planning

## When NOT to Use

- Fixing a single endpoint, component, or small tweak
- Editing or updating existing specification documents
- Work that doesn't need multi-document planning
- **Documenting or reverse-engineering docs from an existing codebase** —
  use `dev-reverse-docs` instead. This skill assumes no code exists yet for
  what's being planned; it never reads source code as evidence, and has no
  citation/verification apparatus. Using it to describe existing code
  produces undated, unverifiable documents.

## Document Classification (WHAT / HOW / Verification)

Every document this skill produces falls into exactly one of three
categories. Keep them separate — do not blend WHAT content into a HOW
document or vice versa.

- **`planning/` — WHAT** (stakeholder view): what the system does, from the
  actor's perspective. `requirements.md`, `user-stories.md`, and
  `use-case.md` live here. **Use cases are planning documents, not design
  documents** — a use case describes actor↔feature relationships (who can
  do what, under what pre/postconditions), not how components call each
  other internally. Even though a use case's main flow is drawn as a
  Mermaid `sequenceDiagram`, it stays at the actor/system boundary; it is
  not an implementation call chain.
- **`design/` — HOW** (developer view): how the system implements what
  planning described — component call order, API contracts, data shapes,
  UI structure, state transitions. `sequence-diagram.md` belongs here
  specifically *because* it shows inter-component call order (HOW), which
  is the opposite axis from a use case's actor-facing flow (WHAT). The set
  of files generated under `design/` is not fixed — see the dynamic
  selection table below.
- **`verification/` — a separate axis**: `test-spec.md` is neither WHAT nor
  HOW; it is the single source of truth for test definitions, referencing
  IDs from both `planning/` and `design/` documents.

## Execution Requirements

These rules are part of the skill contract. They make the expected working
discipline explicit so document quality does not depend on which model
executes the skill.

1. **Templates are mandatory.** Every step loads its template file from
   `${CLAUDE_PLUGIN_ROOT}/templates/` before generating. If a template file
   is missing, stop and report the missing path — never improvise the
   document structure from memory of what the template "probably" contains.
2. **Re-read inputs from disk.** Each step loads all previous step outputs
   from their files, even if their content appeared earlier in the
   conversation. The generated documents are the source of truth, not chat
   history — a document may have been edited by the user between steps.
3. **IDs are assigned, never guessed.** Use the exact formats from the ID
   System table, numbered sequentially with no gaps or duplicates within a
   document. When referencing an ID from an earlier document, verify it
   exists there before writing the reference.
4. **Validate traceability before finishing the test-spec step.**
   Cross-check the generated test-spec against the earlier documents:
   - every `AC-USNN-NN` in user-stories.md is covered by at least one test
   - every ID referenced in test-spec.md exists in its source document
   Fix any orphan references or uncovered ACs before presenting the step.
5. **Verify links and diagrams.** Every navigation link must point to a file
   that exists or will be produced by this pipeline (with the actual
   generated `design/` filenames substituted for any placeholder). Prev/next
   links point document-to-document in canonical order — never to a folder
   like `../design/`. Every
   Mermaid block must be syntactically complete: matching fences, declared
   participants, no placeholder text left inside.
6. **Respect review gates literally.** In step-by-step mode (the default),
   stop after each step and wait for explicit user approval — never batch
   multiple steps into a single turn. Only when the user chose continuous
   mode in Step 0 (or explicitly says to skip reviews) generate straight
   through, then present one consolidated review at the end.
7. **Report verified paths only.** The completion report lists only files
   confirmed to exist on disk.

## Pipeline Overview

```text
Step 0:   Tech stack detection + domain type classification
Step 0.5: Domain analysis & document discovery
Step 1:   Requirements   -> <domain>/planning/requirements.md      [common, WHAT]
Step 2:   User Stories   -> <domain>/planning/user-stories.md      [common, WHAT]
Step 3:   Use Case       -> <domain>/planning/use-case.md          [common, WHAT]
--- Planning -> Design review gate (see below) ---
Step 4:   Design Documents -> <domain>/design/*.md                 [dynamic, HOW]
             selected from: api-spec.md, sequence-diagram.md,
             component-diagram.md, domain-state-machine.md,
             client-store.md, data-model.md, user-flows.md, infra-spec.md
Step 5:   Test Specification -> <domain>/verification/test-spec.md [common]
Step 6:   README (table of contents)
```

For multi-domain projects, Steps 1-5 repeat per domain. Step 6 runs once.

## Output Structure

`docs/en/` denotes the project's source-language directory as configured in
`docs/config.yml` (default `en`); substitute the configured code if different.

```text
docs/en/specifications/
├── architecture.md              # Cross-cutting (created by init-docs)
├── infrastructure.md            # Cross-cutting (created by init-docs)
├── config.md                    # Cross-cutting (created by init-docs)
├── README.md                    # Index of all domains/documents (Step 6)
└── <domain>/
    ├── planning/
    │   ├── requirements.md      # Step 1
    │   ├── user-stories.md      # Step 2
    │   └── use-case.md          # Step 3
    ├── design/                  # Step 4 — dynamic subset of:
    │   ├── api-spec.md
    │   ├── sequence-diagram.md
    │   ├── component-diagram.md
    │   ├── domain-state-machine.md
    │   ├── client-store.md
    │   ├── data-model.md
    │   ├── user-flows.md
    │   └── infra-spec.md
    └── verification/
        └── test-spec.md         # Step 5
```

## Design Document Selection (dynamic)

`design/` is not a fixed single-domain branch — decide which files the
feature actually needs based on what it will touch:

| The feature will have... | Generate |
|---|---|
| REST/GraphQL endpoints | `design/api-spec.md` |
| Backend service/component call chains | `design/sequence-diagram.md` |
| Frontend component trees | `design/component-diagram.md` |
| Domain entity/workflow states with transitions | `design/domain-state-machine.md` |
| Client-side state management (Redux/Vuex/Pinia, etc.) | `design/client-store.md` |
| ORM/DB schema changes | `design/data-model.md` |
| Multi-step UI journeys / screen-to-screen flows | `design/user-flows.md` |
| Deployment, environments, CI/CD, or infra resources | `design/infra-spec.md` |

A feature can need more than one — a typical full-stack feature needs
`api-spec.md` + `data-model.md` + `sequence-diagram.md` together. Confirm
the selection with the user at the start of Step 4 rather than guessing
from Step 0's domain classification alone; a "backend" project can still
need `component-diagram.md` if the feature includes an admin UI.

## ID System

Each document assigns its own IDs. These IDs are referenced by `test-spec.md`
to derive test cases. Planning/design documents contain **no test
definitions** — only IDs.

| Document | ID Format | Example |
|----------|-----------|---------|
| Requirements | `FR-<AREA>-NN`, `NFR-<CAT>-NN` | FR-AUTH-01, NFR-SEC-01 |
| User Stories | `US-NN`, `AC-USNN-NN` | US-01, AC-US01-01 |
| Use Case | `UC-<AREA>-NN` | UC-AUTH-01 |
| Design Documents | (endpoint/component/model names; multiple files possible, no unified ID format) | — |

## Navigation

**Canonical pipeline order** — navigation always follows this order,
skipping any design file not generated for the domain:

```text
requirements → user-stories → use-case
  → [user-flows → sequence-diagram → api-spec → data-model
     → component-diagram → domain-state-machine → client-store
     → infra-spec]                                       (generated subset)
  → test-spec
```

Every domain document includes two navigation blocks:

**Top** — line 1 of the file, sequential prev/next for linear reading:
```markdown
> [← Requirements](requirements.md) | [User Stories →](user-stories.md)
```
The first document (`requirements.md`) omits "←", the last
(`test-spec.md`) omits "→". The chain crosses domain boundaries
document-to-document so a reader can click straight from planning through
design to verification: `use-case.md`'s next is the **first generated**
design document, the **last generated** design document's next is
`../verification/test-spec.md`, and `test-spec.md`'s prev is the last
generated design document. Never use a folder link (e.g. `../design/`) in
prev/next.

**Bottom** — full index to jump to any document, placed after the
Document Information section:
```markdown
---
> **All Documents**
> [Requirements](../planning/requirements.md) | ... | [Test Spec](../verification/test-spec.md)
```
The index lists every generated document in canonical order; the current
document is shown in **bold** instead of a link. Since `design/` holds a
dynamic set of files, include only the `design/*.md` files actually
generated for this domain — never link a file that wasn't produced. The
templates ship with the full canonical set plus a NAV NOTE comment;
substitute the real set at generation time.

## Planning → Design Review Gate

After Step 3 (`use-case.md`) is approved, stop and explicitly confirm the
Step 4 design-document selection (the dynamic table above) with the user
before generating anything under `design/`. This is a distinct checkpoint
from the per-step review gates in Execution Requirement 6 — its purpose is
to lock in *which* design documents will exist before producing any of
them, since the set isn't fixed.

> **Use case approved.** Based on the requirements and use cases, this
> feature needs: `<selected design/*.md files>`.
> Proceed with these, or adjust the selection?

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
2. Detect framework, database, ORM, API style, architecture pattern
3. Scan directory structure — `src/`, `app/`, `pages/`, `components/`
4. Classify the **domain type** based on detected stack (Backend / Frontend
   / Infrastructure / a mix) — used as a starting hint for Step 4's
   design-document selection, not as a rigid branch
5. The detected stack is recorded in the **Document Information** table of
   design/verification documents only — planning documents stay
   technology-free (see Document Rules)

Summarize and confirm with the user, including the review mode for the rest
of the pipeline:

> **Detected tech stack:**
> - Language: ...
> - Framework: ...
> - Domain type: Backend / Frontend / Infrastructure / a mix
>
> **Review mode** — how should I run Steps 1–6?
> - `step-by-step` (default): pause for your review after every step
> - `continuous`: generate all documents, then one consolidated review
>
> Does this look correct?

Wait for confirmation before proceeding. In continuous mode, skip the
per-step "Please review. Ready to proceed?" gates below and instead present
all generated documents for a single review after Step 6.

### Step 0.5: Domain Analysis & Document Discovery

**Domain Analysis**

1. Ask the user to describe major feature areas
2. Propose domain groupings (e.g., `auth`, `dashboard`, `payment`)
3. Always create at least one domain directory
4. Present proposed structure and wait for confirmation

**Document Discovery**

5. Scan `README.md`, `CLAUDE.md`, all `.md` files under `docs/en/specifications/` and `docs/en/policy/`
6. Classify each by first 30 lines: `requirements` / `user-stories` / `use-case` / `api-spec` / `sequence-diagram` / `architecture` / `config` / `infrastructure` / `deployment` / `policy` / `other`
7. Present discovered documents grouped by category using `@`-reference format
8. Carry confirmed document list to all subsequent steps

If no documents found, record "No project documents found" and proceed.

### Step 1: Requirements

**Output**: `<domain>/planning/requirements.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/planning/requirements.md`
2. Load discovered docs classified as `requirements`, `user-stories`, or `architecture`
3. Ask user for: system purpose, stakeholders, core features, non-functional requirements, constraints
4. Generate document with:
   - System context diagram (C4Context Mermaid)
   - Functional requirements grouped by area (`FR-<AREA>-NN` format)
   - Non-functional requirements (`NFR-<CAT>-NN` format) as measurable,
     stakeholder-facing targets
   - Constraints (business, operational, development process —
     implementation-technology constraints belong in Step 4's design
     documents, not here)
   - Requirements traceability matrix
5. Wait for review

> **Step 1 complete**: Requirements generated.
> Please review. Ready to proceed?

### Step 2: User Stories

**Output**: `<domain>/planning/user-stories.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/planning/user-stories.md`
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

### Step 3: Use Case

**Output**: `<domain>/planning/use-case.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/planning/use-case.md`
2. Load previous outputs: Steps 1-2
3. Load discovered docs classified as `use-case` or `architecture`
4. For each use case (`UC-<AREA>-NN`), define:
   - Basic information (actors, related requirements, related user stories)
   - Preconditions and postconditions
   - Main flow as an actor-level interaction outline (who does what, in
     order — not a component call chain; that belongs in Step 4's
     `sequence-diagram.md`)
   - Alternative flows with branch points
5. Include actor definitions, use case diagram, relationship table
6. Wait for review

> **Step 3 complete**: Use case generated.
> Please review. Ready to proceed to design-document selection?

Then run the **Planning → Design Review Gate** above before Step 4.

### Step 4: Design Documents (dynamic)

**Output**: `<domain>/design/*.md` (only the files selected at the review gate)

For each selected file:

- **`api-spec.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/api-spec.md`;
  define HTTP method/path/auth per endpoint, request/response schemas with
  JSON examples, curl/JS examples, error responses, endpoint catalog,
  authentication flow, error codes
- **`sequence-diagram.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/sequence-diagram.md`;
  for each major flow, a `sequenceDiagram` Mermaid showing architecture
  layer interactions, participants labeled `FileName<br/>(Layer)`, key
  steps and related code references, normal/error/performance flows.
  **Omit the Source-Linked Mode section entirely** — no code exists yet
  for a feature being planned, so there is nothing to link or cite.
- **`component-diagram.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/component-diagram.md`;
  define UI overview (views, URLs, access levels, responsive strategy),
  component tree with Mermaid hierarchy, shared and page-specific
  components with TypeScript prop interfaces
- **`domain-state-machine.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/domain-state-machine.md`;
  define the entity/workflow state machine and its transition table
- **`client-store.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/client-store.md`;
  define the store strategy, state classification, and store definitions
  for client-side state
- **`data-model.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/data-model.md`;
  define the entity relationship diagram and JSON-Schema-per-model
- **`user-flows.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/user-flows.md`;
  for each multi-step UI journey, a `flowchart TD` Mermaid with happy,
  alternative, and exception paths plus entry/exit conditions, and a flow
  relationship diagram — exception paths feed Step 5's E2E scenarios
- **`infra-spec.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/infra-spec.md`;
  define deployment topology, environments, CI/CD pipeline, resource
  definitions, monitoring/alerting, and security for the feature

For every file: load previous outputs (Steps 1-3, plus any other `design/`
files already generated in this step), omit the `## Sources Read` section
entirely (nothing to cite — this is forward planning), and wait for review
after all selected files are generated.

> **Step 4 complete**: Design documents generated: `<list of files>`.
> Please review. Ready to proceed?

### Step 5: Test Specification

**Output**: `<domain>/verification/test-spec.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/verification/test-spec.md`
2. Load **all** previous outputs: Steps 1-4
3. Derive test cases by scanning IDs from earlier documents:
   - `AC-USNN-NN` from user stories -> E2E and acceptance tests
   - `UC-<AREA>-NN` main/alternative flows -> integration and unit tests
   - `user-flows.md` exception/alternative paths (when generated) -> E2E scenarios
   - Generated design documents' endpoints/components/models -> contract tests
4. Generate:
   - Test matrix with Test IDs (`T-NNN`), source references, type, priority
   - Mocking boundaries for unit/integration/E2E levels
   - Proposed test file structure
   - Test-requirement traceability matrix
5. Wait for review

> **Step 5 complete**: Test specification generated.
> Please review. Ready to proceed to README?

### Step 6: Generate README

**Output**: `docs/en/specifications/README.md`

After all domains complete Steps 1-5:

- Single-domain: table of contents linking `planning/`, `design/`, and
  `verification/` documents for that domain
- Multi-domain: section per domain + optional per-domain README.md
- If README exists, merge rather than overwrite
- Include discovered documents in a **Related Project Documents** section

Report all generated file paths on completion.

> **Planning complete.** Generated documents:
> - `<domain>/planning/requirements.md`
> - `<domain>/planning/user-stories.md`
> - `<domain>/planning/use-case.md`
> - `<domain>/design/<selected files>`
> - `<domain>/verification/test-spec.md`
> - `docs/en/specifications/README.md`

## Document Rules

- **Language**: English
- **Document Information**: every document ends with a `## Document
  Information` section — a table of Created, Last Modified, Status, Tech
  Stack (design/verification documents only), and Reference Documents,
  followed by the Version History list. No metadata block at the top of
  the document.
- **Planning docs are non-technical**: `planning/` documents contain no
  implementation technology — no stacks/frameworks, code-level types, API
  paths, or architecture patterns, and no Tech Stack row in their Document
  Information table. Measurable NFR targets and business/operational/
  process constraints stay in planning; technology choices and technical
  constraints are recorded in `design/` documents.
- **Mermaid**: `sequenceDiagram` for flows, `C4Context` for system context, `graph TD/LR` for hierarchies, `stateDiagram-v2` for state machines, `erDiagram` for data relationships
- **TypeScript**: `interface` for props, stores, DTOs — design documents
  only, never in planning documents
- **IDs**: FR-XXX, NFR-XXX, US-NN, AC-USNN-NN, UC-XXX — no test content in planning docs
- **Cross-references**: FR -> UC -> Design Documents -> Test Spec links
- **Given/When/Then**: Acceptance criteria format in user stories
- **Participant notation**: `FileName<br/>(Layer)` in sequence diagrams
- **`## Sources Read`**: omitted from every generated document — forward
  planning has no code to cite yet. If you find yourself wanting to add
  one, you are probably reverse-engineering existing code and should stop
  and use `dev-reverse-docs` instead.
- **References**: Each step loads all previous step outputs before generating
- **Review gate**: Never proceed to the next step without user approval
  (unless continuous mode was chosen in Step 0)
- **Navigation**: Every domain document has top (line-1 prev/next) and
  bottom (all documents) navigation following the canonical order in the
  Navigation section — document-to-document across domain boundaries,
  never folder links
- **`@`-references**: Use for discovered docs per [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md)
