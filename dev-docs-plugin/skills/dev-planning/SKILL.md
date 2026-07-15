---
name: dev-planning
version: 0.1.0
description: Forward planning pipeline for a NEW feature or project (specification -> design documents -> test spec) with ID-based test traceability and lite/full output tiers (invoke as /dev-docs:dev-planning lite or full to pin the tier). Supports backend, frontend, and infrastructure domains. Do NOT use this for documenting or reverse-engineering docs from existing code — use dev-reverse-docs for that.
argument-hint: "[lite|full]"
---

# dev-planning

Forward planning document pipeline for work that doesn't have code yet: a
new feature, a new project, or a major addition. Step 1 produces the
WHAT-level (planning) specification. Step 2 dynamically selects which
HOW-level (design) documents the feature needs. Step 3 generates a test
specification referencing IDs from every previous step.

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
  actor's perspective. `spec.md` lives here, holding requirements (FR/NFR),
  user stories with acceptance criteria, and — only when the feature
  involves 2+ actors or an external system — a **Multi-Actor Flows**
  section of use cases. **Use cases are planning content, not design
  content** — a use case describes actor↔feature relationships (who can
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
   - every `AC-USNN-NN` in spec.md is covered by at least one test
   - every ID referenced in test-spec.md exists in its source document
   Fix any orphan references or uncovered ACs before presenting the step.
5. **Verify links and diagrams.** Every navigation link must point to a file
   that exists or will be produced by this pipeline (with the actual
   generated `design/` filenames substituted for any placeholder). Prev/next
   links point document-to-document in canonical order — never to a folder
   like `../design/`. In-document ID references use GitHub heading-derived
   anchors (e.g. `### UC-AUTH-01: Login` is linked as
   `spec.md#uc-auth-01-login`) — renaming a heading breaks its anchor, so
   re-verify links after any heading change. Every
   Mermaid block must be syntactically complete: matching fences, declared
   participants, no placeholder text left inside.
6. **Respect review gates literally.** In step-by-step mode (the default),
   stop after each step and wait for explicit user approval — never batch
   multiple steps into a single turn. Only when the user chose continuous
   mode in Step 0 (or explicitly says to skip reviews) generate straight
   through, then present one consolidated review at the end.
7. **Report verified paths only.** The completion report lists only files
   confirmed to exist on disk.

## Tier Selection (Lite / Full)

Every domain is planned in one of two tiers. The tier decides the shape
of the output, never its quality bar.

- **Lite** — single primary actor, no external systems, low
  business-logic complexity (typical CRUD). Generates 3 files:
  `planning/spec.md` (no Multi-Actor Flows section), `design/design.md`
  (one merged file holding only the triggered sections), and
  `verification/test-spec.md`.
- **Full** — multiple actors, external-system integration,
  regulated/security-sensitive, or high domain complexity. Generates
  `planning/spec.md` (with Multi-Actor Flows when the gate is true),
  dynamically selected individual `design/*.md` files, and
  `verification/test-spec.md`.

How the tier is chosen (in Step 0):

1. **Explicit argument wins.** If the skill invocation carried an
   argument — `/dev-docs:dev-planning lite` or `/dev-docs:dev-planning
   full` — use that tier without asking.
2. **Otherwise auto-detect and propose.** Evaluate the signals below
   against the user's feature description; any Full signal ⇒ propose
   Full, else propose Lite. The proposal is confirmed (or overridden) by
   the user in the Step 0 summary — the user's answer always wins.

| Signal | Lite | Full |
|---|---|---|
| Distinct primary actors | 1 | 2+ |
| External systems (Secondary Actors) | 0 | 1+ |
| Design categories triggered by the selection table | ≤ 3 | ≥ 4 |
| Regulated / security-sensitive domain (payments, PII, healthcare, auth infrastructure) | No | Yes |

The tier is per **domain**: in a multi-domain project each domain gets
its own evaluation (a `payment` domain can be Full while `profile` is
Lite).

## Pipeline Overview

```text
Step 0:   Tech stack detection + domain classification + tier selection
Step 0.5: Domain analysis & document discovery
Step 1:   Specification -> <domain>/planning/spec.md               [common, WHAT]
             requirements (FR/NFR) + user stories/acceptance criteria
             + Multi-Actor Flows (only with 2+ actors or an external system)
--- Planning -> Design review gate (see below) ---
Step 2:   Design Documents                                         [dynamic, HOW]
             Full: <domain>/design/*.md — selected from: api-spec.md,
                   sequence-diagram.md, component-diagram.md,
                   domain-state-machine.md, client-store.md,
                   data-model.md, user-flows.md, infra-spec.md
             Lite: <domain>/design/design.md — one merged file; the
                   same selection table picks its sections
Step 3:   Test Specification -> <domain>/verification/test-spec.md [common]
Step 4:   README (table of contents)
```

For multi-domain projects, Steps 1-3 repeat per domain. Step 4 runs once.

## Output Structure

`docs/en/` denotes the project's source-language directory as configured in
`docs/config.yml` (default `en`); substitute the configured code if different.

```text
docs/en/specifications/
├── architecture.md              # Cross-cutting (created by init-docs)
├── infrastructure.md            # Cross-cutting (created by init-docs)
├── config.md                    # Cross-cutting (created by init-docs)
├── README.md                    # Index of all domains/documents (Step 4)
└── <domain>/
    ├── planning/
    │   └── spec.md              # Step 1
    ├── design/                  # Step 2 — dynamic subset of:
    │   ├── api-spec.md
    │   ├── sequence-diagram.md
    │   ├── component-diagram.md
    │   ├── domain-state-machine.md
    │   ├── client-store.md
    │   ├── data-model.md
    │   ├── user-flows.md
    │   └── infra-spec.md
    └── verification/
        └── test-spec.md         # Step 3
```

In **Lite tier** the `design/` directory holds a single merged file
instead of the dynamic subset:

```text
    ├── design/
    │   └── design.md            # Step 2 (Lite) — sections per the same selection table
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
the selection with the user at the start of Step 2 rather than guessing
from Step 0's domain classification alone; a "backend" project can still
need `component-diagram.md` if the feature includes an admin UI.

In **Lite tier** this same table selects *sections of
`design/design.md`* instead of individual files — each section of that
template carries the matching trigger and Domain tag.

## ID System

Each document assigns its own IDs. These IDs are referenced by `test-spec.md`
to derive test cases. Planning/design documents contain **no test
definitions** — only IDs.

| Document / Section | ID Format | Example |
|--------------------|-----------|---------|
| spec.md — Requirements | `FR-<AREA>-NN`, `NFR-<CAT>-NN` | FR-AUTH-01, NFR-SEC-01 |
| spec.md — User Stories | `US-NN`, `AC-USNN-NN` | US-01, AC-US01-01 |
| spec.md — Multi-Actor Flows (only when generated) | `UC-<AREA>-NN` | UC-AUTH-01 |
| Design Documents | (endpoint/component/model names; multiple files possible, no unified ID format) | — |

## Navigation

**Canonical pipeline order** — navigation always follows this order,
skipping any design file not generated for the domain:

```text
spec
  → [user-flows → sequence-diagram → api-spec → data-model
     → component-diagram → domain-state-machine → client-store
     → infra-spec]                                       (generated subset)
  → test-spec
```

In **Lite tier** the chain is fixed — `spec → design → test-spec` — and
the All Documents index is just those three documents.

Every domain document includes two navigation blocks:

**Top** — line 1 of the file, sequential prev/next for linear reading:
```markdown
> [← Specification](../planning/spec.md) | [API Spec →](api-spec.md)
```
The first document (`spec.md`) omits "←", the last
(`test-spec.md`) omits "→". The chain crosses domain boundaries
document-to-document so a reader can click straight from planning through
design to verification: `spec.md`'s next is the **first generated**
design document, the **last generated** design document's next is
`../verification/test-spec.md`, and `test-spec.md`'s prev is the last
generated design document. Never use a folder link (e.g. `../design/`) in
prev/next.

**Bottom** — full index to jump to any document, placed after the
Document Information section:
```markdown
---
> **All Documents**
> [Specification](../planning/spec.md) | ... | [Test Spec](../verification/test-spec.md)
```
The index lists every generated document in canonical order; the current
document is shown in **bold** instead of a link. Since `design/` holds a
dynamic set of files, include only the `design/*.md` files actually
generated for this domain — never link a file that wasn't produced. The
templates ship with the full canonical set plus a NAV NOTE comment;
substitute the real set at generation time.

## Planning → Design Review Gate

After Step 1 (`spec.md`) is approved, stop and explicitly confirm the
Step 2 design-document selection (the dynamic table above) with the user
before generating anything under `design/`. This is a distinct checkpoint
from the per-step review gates in Execution Requirement 6 — its purpose is
to lock in *which* design documents will exist (Full tier) or which
sections `design.md` will contain (Lite tier) before producing any of
them, since the set isn't fixed.

> **Specification approved.** Based on the requirements, stories, and
> flows in `spec.md`, this feature needs:
> `<selected design/*.md files — or design.md sections in Lite tier>`.
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
   / Infrastructure / a mix) — used as a starting hint for Step 2's
   design-document selection, not as a rigid branch
5. Determine the **tier** per the Tier Selection section: an explicit
   `lite`/`full` invocation argument wins without asking; otherwise
   evaluate the auto-detect signals and propose a default in the summary
   below
6. The detected stack is recorded in the **Document Information** table of
   design/verification documents only — planning documents stay
   technology-free (see Document Rules)

Summarize and confirm with the user, including the review mode for the rest
of the pipeline:

> **Detected tech stack:**
> - Language: ...
> - Framework: ...
> - Domain type: Backend / Frontend / Infrastructure / a mix
>
> **Tier**: Lite / Full (auto-detected — signals: `<one line>`) —
> confirm or override? *(omit this question when the invocation already
> carried `lite` or `full`)*
>
> **Review mode** — how should I run Steps 1–4?
> - `step-by-step` (default): pause for your review after every step
> - `continuous`: generate all documents, then one consolidated review
>
> Does this look correct?

Wait for confirmation before proceeding. In continuous mode, skip the
per-step "Please review. Ready to proceed?" gates below and instead present
all generated documents for a single review after Step 4.

### Step 0.5: Domain Analysis & Document Discovery

**Domain Analysis**

1. Ask the user to describe major feature areas
2. Propose domain groupings (e.g., `auth`, `dashboard`, `payment`)
3. Always create at least one domain directory
4. Present proposed structure and wait for confirmation

**Document Discovery**

5. Scan `README.md`, `CLAUDE.md`, all `.md` files under `docs/en/specifications/` and `docs/en/policy/`
6. Classify each by first 30 lines: `spec` / `requirements` / `user-stories` / `use-case` / `api-spec` / `sequence-diagram` / `architecture` / `config` / `infrastructure` / `deployment` / `policy` / `other` (the last three planning categories cover legacy documents from the pre-`spec.md` pipeline)
7. Present discovered documents grouped by category using `@`-reference format
8. Carry confirmed document list to all subsequent steps

If no documents found, record "No project documents found" and proceed.

### Step 1: Specification

**Output**: `<domain>/planning/spec.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/planning/spec.md`
2. Load discovered docs classified as `spec`, `requirements`,
   `user-stories`, `use-case`, or `architecture`
3. Ask user for: system purpose, actors, core features, non-functional
   requirements, constraints
4. Generate the document section by section:
   - **Overview**: purpose & scope, the Actors table (Primary/Secondary
     with goals), and — only when the Multi-Actor gate below is true —
     the System Context diagram (C4Context Mermaid)
   - **Functional Requirements** grouped by area (`FR-<AREA>-NN` format)
   - **Non-Functional Requirements** (`NFR-<CAT>-NN` format) as
     measurable, stakeholder-facing targets
   - **Constraints** (business, operational, development process —
     implementation-technology constraints belong in Step 2's design
     documents, not here)
   - **User Stories**: for each major feature, **As a** [role], **I want
     to** [capability], **So that** [benefit], with acceptance criteria
     (`AC-USNN-NN` IDs) in **Given/When/Then** format, normal and error
     cases, and related requirement references
   - **Multi-Actor Flows** (`UC-<AREA>-NN`) — **gated**: generate this
     section only when the feature involves 2+ actors or an external
     system (Secondary Actor). Each use case defines basic information
     (actors, related requirements/stories), preconditions and
     postconditions, a main flow as an actor-level interaction outline
     (who does what, in order — not a component call chain; that belongs
     in Step 2's `sequence-diagram.md`), and alternative flows with
     branch points. When the gate is false, omit the entire section, its
     Table of Contents entry, and the Traceability matrix's UC column.
   - **Traceability**: one matrix linking FR → US (AC range) → UC
5. Wait for review

> **Step 1 complete**: Specification generated.
> Please review. Ready to proceed to design-document selection?

Then run the **Planning → Design Review Gate** above before Step 2.

### Step 2: Design Documents (dynamic)

**Output**: Full tier — `<domain>/design/*.md` (only the files selected
at the review gate); Lite tier — `<domain>/design/design.md` (only the
sections selected at the review gate)

**Lite tier**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/design.md`,
keep only the selected sections (each carries its trigger comment and
Domain tag), drop the unused Table of Contents entries, and skip the
per-file instructions below — they describe Full tier. The content rules
still apply section by section (e.g. the Core Flows section follows the
`sequence-diagram.md` rules, including omitting Source-Linked Mode for
forward planning).

**Full tier** — for each selected file:

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
  relationship diagram — exception paths feed Step 3's E2E scenarios
- **`infra-spec.md`**: load `${CLAUDE_PLUGIN_ROOT}/templates/design/infra-spec.md`;
  define deployment topology, environments, CI/CD pipeline, resource
  definitions, monitoring/alerting, and security for the feature

For every file: load previous outputs (Step 1's spec.md, plus any other
`design/` files already generated in this step), omit the `## Sources
Read` section entirely (nothing to cite — this is forward planning), and
wait for review after all selected files are generated.

> **Step 2 complete**: Design documents generated: `<list of files>`.
> Please review. Ready to proceed?

### Step 3: Test Specification

**Output**: `<domain>/verification/test-spec.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/verification/test-spec.md`
2. Load **all** previous outputs: Steps 1-2
3. Derive test cases by scanning IDs from earlier documents:
   - `AC-USNN-NN` from spec.md's User Stories section -> E2E and acceptance tests
   - `UC-<AREA>-NN` main/alternative flows from spec.md's Multi-Actor
     Flows section (when generated) -> integration and unit tests
   - `user-flows.md` exception/alternative paths (when generated) -> E2E scenarios
   - Generated design documents' endpoints/components/models -> contract tests
   - In Lite tier, design references point at `design.md` section anchors
     (e.g. `../design/design.md#api`) instead of individual files
4. Generate:
   - Test matrix with Test IDs (`T-NNN`), source references, type, priority
   - Mocking boundaries for unit/integration/E2E levels
   - Proposed test file structure
   - Test-requirement traceability matrix
5. Wait for review

> **Step 3 complete**: Test specification generated.
> Please review. Ready to proceed to README?

### Step 4: Generate README

**Output**: `docs/en/specifications/README.md`

After all domains complete Steps 1-3:

- Single-domain: table of contents linking `planning/`, `design/`, and
  `verification/` documents for that domain
- Multi-domain: section per domain + optional per-domain README.md
- Note each domain's tier (`Tier: Lite` / `Tier: Full`) in its section,
  so a later Full upgrade of a Lite domain is visible
- If README exists, merge rather than overwrite
- Include discovered documents in a **Related Project Documents** section

Report all generated file paths on completion.

> **Planning complete.** Tier per domain: Lite / Full. Generated documents:
> - `<domain>/planning/spec.md`
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
- **Planning docs are non-technical**: `planning/spec.md` contains no
  implementation technology — no stacks/frameworks, code-level types, API
  paths, or architecture patterns, and no Tech Stack row in its Document
  Information table. Apply the tech-neutrality test to every sentence: if
  the stack were swapped (Python→Java, REST→GraphQL, PostgreSQL→MongoDB),
  the sentence must still be true — otherwise it is HOW content and moves
  to a `design/` document. Refer to external systems by role (Secondary
  Actor), never by protocol. Measurable NFR targets and business/
  operational/process constraints stay in planning; technology choices and
  technical constraints are recorded in `design/` documents.
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
  Navigation section (Lite tier: the fixed `spec → design → test-spec`
  chain) — document-to-document across domain boundaries, never folder
  links
- **`@`-references**: Use for discovered docs per [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md)
