---
name: dev-reverse-docs
version: 0.1.0
description: Reverse-engineer grounded planning/design/verification documentation from an EXISTING codebase, module, or feature, with mandatory per-claim source citation, a doc-verifier check after every pass, and lite/full output tiers (invoke as /dev-docs:dev-reverse-docs lite or full to pin the tier). Triggers on "document this codebase", "generate docs from existing code", "reverse-engineer a spec for this repo/module". Do NOT use this for planning a NEW feature that has no code yet — use dev-planning for that.
argument-hint: "[lite|full]"
---

# dev-reverse-docs

Documents an **existing** codebase, module, or feature by reading the actual
source and citing it — never by inferring "typical" behavior from framework
familiarity. This skill exists because generic planning pipelines hallucinate
when pointed at existing code: they fill gaps with plausible-sounding,
unverified prose. Every claim this skill writes must be traceable to a file
it actually opened, and every generated document is checked by the
`doc-verifier` subagent before the skill reports anything as complete.

## When to Use

- "document this codebase", "이 레포 문서화해줘"
- "generate docs from existing code", "기존 코드 기반으로 기획/설계 문서 만들어줘"
- "reverse-engineer a spec for this module/feature", "이 모듈 스펙 문서 뽑아줘"
- Onboarding docs are needed for code that already exists and has no
  up-to-date specification

## When NOT to Use

- **Planning a new feature that has no code yet** — use `dev-planning`
  instead. This skill only ever writes claims backed by code it read; if
  there's no code, there's nothing to ground the document in.
- Small, well-understood modules that don't need a formal spec — just
  answer the question directly instead of running the full pipeline

## Document Classification (WHAT / HOW / Verification)

Every document this skill produces falls into exactly one of three
categories. Keep them separate — do not blend WHAT content into a HOW
document or vice versa.

- **`planning/` — WHAT** (stakeholder view): what the system does, from the
  actor's perspective. `spec.md` lives here, holding requirements (FR/NFR),
  user stories with acceptance criteria, and — only when the code shows
  2+ actors or an external system — a **Multi-Actor Flows** section of
  use cases. **Use cases are planning content, not design content** — a
  use case describes actor↔feature relationships (who can do what, under
  what pre/postconditions), not how components call each other internally.
  Even though a use case's main flow is drawn as a Mermaid
  `sequenceDiagram`, it stays at the actor/system boundary; it is not an
  implementation call chain.
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

> In this skill, `verification/test-spec.md` describes *existing*, cited
> test coverage — not tests yet to be written, which is what `dev-planning`
> produces for a feature that doesn't exist yet.

## Grounding & Citation Rules

This is the hallucination-prevention contract. It applies to every document
this skill writes, and `doc-verifier` enforces it after the fact.

1. **State only facts directly confirmed in code.** No speculative language,
   no "typically this would...", no filling gaps with framework-idiom
   assumptions. If you didn't read it, don't write it as fact.
2. **Every claim needs a citation**: `[REF: path:line]` or
   `[REF: path:start-end]`, using a workspace-relative path and plain
   integers. Forbidden variants: no vague "see relevant file", no
   parenthetical prose citations, no citing a file you did not actually
   open via Read/Grep during this pass. A citation you can't back with an
   actual tool-verified read is worse than no citation — remove the claim
   or mark it `[ASSUMED: ...]` instead.
3. **Content needed for completeness but not verifiable from code** gets
   `[ASSUMED: <inference>; basis: <evidence>]` in place of a citation — e.g.
   inferring intent behind a design choice, or a business rule the code
   doesn't comment. Never fabricate a file:line to make an assumption look
   verified.
4. **Sections that require inferring intent from code** (most of
   `spec.md`'s Purpose/stakeholder framing, and any User Story
   "So that" clause) get a banner at the top of the
   document: "This section is inferred from code — verify with
   stakeholders", plus a citation or `[ASSUMED: ...]` tag on each item.
5. **Every generated document ends with a `## Sources Read` ledger** —
   every file (and line range, if partial) actually opened while writing
   it. Every `[REF: ...]` citation in the document must point to a file
   listed here.
6. **Sequence diagrams get additional, stricter rules** (per
   `templates/design/sequence-diagram.md`'s "Source-Linked Mode" section):
   - every participant gets a `link <alias>: Source @ <repo_url>/blob/<branch>/<path>` line
   - every message arrow is followed by a `Note` with the real `path:line`
   - a message/flow that can't be confirmed from code gets `[ASSUMED: ...]`
     instead of a `Note` — never a guessed file:line
   - every diagram ends with a hidden `<!-- CALLGRAPH: ... -->` block
     listing the raw call edges it was built from, extracted *before*
     drawing the diagram, so `doc-verifier` can cross-check the rendered
     `Note`s against it independently
   - resolve `<repo_url>` from `git remote get-url origin` (normalized to
     `https://`) and `<branch>` from the branch checked out during
     generation

## Hierarchical Scope Strategy

Large repos cannot be documented in detail in one pass — don't try.

**Pass 1 — repo-wide overview** (`docs/en/specifications/overview.md`):
module/service boundaries and tech stack only, citing what establishes each
boundary (e.g. a top-level `package.json`/`go.mod` per service directory).
No `planning/`/`design/`/`verification/` detail docs in this pass. Run
`doc-verifier` on `overview.md` before moving on.

**Module selection**: if the user already named a module/feature, skip to
Pass 2 for it. Otherwise, present the Pass 1 overview and ask which
module/domain to detail next — never attempt full-repo detailed
documentation in one shot.

**Pass 2 — module-scoped detail**: generate `planning/`, `design/`, and
`verification/` documents only for the selected module, following the
Design Document Selection table below. Run `doc-verifier` on this pass's
output before reporting it complete. If the user wants another module
documented next, repeat Pass 2 for it (Pass 1 does not need to re-run).

## Tier Selection (Lite / Full)

Pass 2 runs in one of two tiers per module. The tier decides the output
shape, never the grounding bar — citations and the doc-verifier loop are
mandatory in both tiers.

- **Lite** — small module, one actor-facing surface, no external
  integrations. Pass 2 generates 3 files: `planning/spec.md` (no
  Multi-Actor Flows section), `design/design.md` (one merged file
  holding only the evidence-backed sections), and
  `verification/test-spec.md`.
- **Full** — the per-file pipeline: `planning/spec.md` (with Multi-Actor
  Flows when the code evidence supports it), dynamically selected
  individual `design/*.md` files, and `verification/test-spec.md`.

How the tier is chosen (in Step 0):

1. **Explicit argument wins.** If the skill invocation carried an
   argument — `/dev-docs:dev-reverse-docs lite` or `... full` — use that
   tier without asking.
2. **Otherwise auto-detect from code signals** gathered during Step 0's
   scan (or Pass 1's overview): any Full signal ⇒ propose Full, else
   propose Lite. The user confirms or overrides in Step 0.

| Signal (from the module's code) | Lite | Full |
|---|---|---|
| Actor-facing surfaces (distinct API consumers, UIs, roles enforced in auth code) | 1 | 2+ |
| External integrations (third-party clients, webhooks, message brokers) | 0 | 1+ |
| Design categories with code evidence (selection table below) | ≤ 3 | ≥ 4 |
| Module size (source files in scope) | ≲ 30 | larger |

The tier is per **module**: each Pass 2 target gets its own evaluation.

## Design Document Selection (dynamic)

`design/` is not a fixed set — generate only the files the evidence in the
selected module's code actually supports:

| Evidence found in code | Generate |
|---|---|
| REST/GraphQL endpoints | `design/api-spec.md` |
| Backend service/component call chains | `design/sequence-diagram.md` |
| Frontend component trees | `design/component-diagram.md` |
| Domain entity/workflow states with transitions | `design/domain-state-machine.md` |
| Client-side state management (Redux/Vuex/Pinia, etc.) | `design/client-store.md` |
| ORM/DB schema | `design/data-model.md` |
| Multi-step UI journeys (routes, wizards, funnels) | `design/user-flows.md` |
| IaC / CI-CD / deployment configuration | `design/infra-spec.md` |

Do not generate a file for a category with no evidence — an empty/invented
`api-spec.md` for a module with no endpoints is exactly the kind of
hallucination this skill exists to prevent.

In **Lite tier** this same table selects *sections of
`design/design.md`* instead of individual files — the no-evidence rule
applies per section.

## Step-by-Step Instructions

### Step 0: Scope & Stack Detection

1. Scan project manifests and directory structure to identify module/service
   boundaries and the tech stack per boundary (same manifest scan as
   `dev-planning` Step 0, but the output here is a boundary list, not a
   single domain classification)
2. Confirm with the user: full Pass-1 overview first, or (if a module was
   already named) skip straight to Pass 2 for it
3. Determine the **tier** per the Tier Selection section: an explicit
   `lite`/`full` invocation argument wins without asking; otherwise
   propose a default from the code signals and confirm with the user
4. Confirm review mode (step-by-step default vs. continuous), same as
   `dev-planning` Step 0

### Step 1: Pass 1 — Overview

**Output**: `docs/en/specifications/overview.md`

1. For each detected module/service boundary, cite the file that
   establishes it (manifest, directory-level config, etc.)
2. Summarize tech stack per boundary, each claim cited
3. No detail docs in this step
4. Invoke `doc-verifier` on `overview.md`; if it reports any `MISMATCHED`
   or `UNSUPPORTED` claims, fix only those items (re-check the code, correct
   the doc) and re-invoke until clean
5. Present the overview and ask which module to detail in Pass 2

> **Pass 1 complete and verified**: `docs/en/specifications/overview.md`.
> Which module should I document in detail?

### Step 2: Pass 2 — Planning Document

**Output**: `<domain>/planning/spec.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/planning/spec.md`
2. Read the selected module's code — controllers/entry points, then inward
   through its call chain — before writing anything
3. Requirements sections: derive `FR-<AREA>-NN`/`NFR-<CAT>-NN` from what
   the code actually enforces (validation, auth checks, config) — cite
   each; mark the Purpose/stakeholder framing as inferred per Grounding
   Rule 4. Write the requirements themselves in stakeholder language —
   planning documents stay non-technical (no stacks, code types, API
   paths); the technical detail the code revealed goes into Step 3's
   design documents. `[REF: path:line]` citations are provenance, not
   technical content — they are still required on every claim here.
4. User Stories section: derive from the requirements and observed API/UI
   surface — mark "So that" clauses `[ASSUMED: ...]` unless the intent is
   stated somewhere (comment, doc, commit message you actually read)
5. Multi-Actor Flows section — **gated**: generate only when the code
   evidence shows 2+ actors or an external system (spec.md's Multi-Actor
   gate). Derive actors and flows from the actual call paths;
   preconditions/postconditions must cite the validation/guard code that
   enforces them. Omit the section (and its ToC entry and the
   Traceability UC column) otherwise.
6. Wait for review

### Step 3: Pass 2 — Design Documents

**Output**: Full tier — `<domain>/design/*.md` (dynamic selection);
Lite tier — `<domain>/design/design.md`

1. Apply the Design Document Selection table to the module's actual code
2. **Full tier**: for each selected file, load its template from
   `${CLAUDE_PLUGIN_ROOT}/templates/design/`. **Lite tier**: load
   `${CLAUDE_PLUGIN_ROOT}/templates/design/design.md` and fill only the
   evidence-backed sections, dropping the unused Table of Contents
   entries
3. Sequence diagrams specifically (the `sequence-diagram.md` file in
   Full, the Core Flows section of `design.md` in Lite): extract the raw
   call graph first (grep/read call sites), record it in the hidden
   `<!-- CALLGRAPH: -->` block, *then* draw the diagram and `Note`s from
   that extraction — never draw the diagram first and back-fill
   citations. Source-Linked Mode rules apply identically in both tiers
4. Wait for review

### Step 4: Pass 2 — Verification Document

**Output**: `<domain>/verification/test-spec.md`

1. Load template: `${CLAUDE_PLUGIN_ROOT}/templates/verification/test-spec.md`
2. Find existing tests for the module; populate the test matrix's Source
   column with `[REF: path:line]` per test found
3. Mark requirements/use-case flows with no corresponding test as
   "Missing" in Status — do not invent a test that doesn't exist
4. Wait for review

### Step 5: Verify

Invoke `doc-verifier` once per document generated in Steps 2-4 (or once per
pass if the skill's invocation budget favors batching — but every document
must be checked before Step 6). Lite tier is not exempt: its 3 documents
(plus `overview.md` from Pass 1) are each verified.

### Step 6: Fix-Mismatches Loop

For every `MISMATCHED` or `UNSUPPORTED` claim in a `doc-verifier` report:

1. Re-open the cited (or claimed) location in the actual code
2. Correct the document — fix the claim, fix the citation, or convert it to
   `[ASSUMED: ...]` if it genuinely can't be verified
3. Do **not** touch claims the report marked `MATCHED` or `EXCLUDED`
4. Re-invoke `doc-verifier` on the corrected document
5. Repeat until the report is clean, or the user explicitly says to stop
   with known gaps recorded

**Never report a document, a pass, or the overall task as complete while
any `doc-verifier` report for it still has unresolved `MISMATCHED` or
`UNSUPPORTED` entries.**

### Step 7: Completion Report

Report only after Step 6 ends clean (or the user explicitly accepted known
gaps). List:

- Generated file paths (verified to exist on disk)
- Final `doc-verifier` counts per document (matched / excluded, and any
  gaps the user accepted)
- Modules not yet documented (from Pass 1's overview), if any

## Document Rules

- **Language**: English
- **Document Information**: every document ends with a `## Document
  Information` section — a table of Created, Last Modified, Status, Tech
  Stack (design/verification documents only), and Reference Documents,
  followed by the Version History list. No metadata block at the top of
  the document.
- **Planning docs are non-technical**: `planning/` documents contain no
  implementation technology (no stacks, code-level types, API paths,
  architecture patterns) and no Tech Stack row in their Document
  Information table — the technical detail lives in `design/` documents.
  `[REF:]`/`[ASSUMED:]` citations are provenance markers, not technical
  content, and remain mandatory in planning documents.
- **Mermaid**: `sequenceDiagram` (Source-Linked Mode) for flows, `graph TD/LR` for hierarchies, `stateDiagram-v2` for state machines, `erDiagram` for data relationships
- **Citations**: `[REF: path:line]` / `[REF: path:start-end]`; `[ASSUMED: <inference>; basis: <evidence>]` for unverifiable-but-needed content
- **`## Sources Read`**: required in every generated document — every
  citation must trace back to a file listed there. It sits after the body
  sections, before Related Documents and Document Information.
- **IDs**: FR-XXX, NFR-XXX, US-NN, AC-USNN-NN, UC-XXX — same ID system as `dev-planning`, so a module documented here and later extended via `dev-planning` shares one traceability scheme
- **Cross-references**: FR -> UC -> Design Documents -> Test Spec links
- **Given/When/Then**: Acceptance criteria format in user stories
- **Participant notation**: `FileName<br/>(Layer)` in sequence diagrams, plus the `link`/`Note`/`CALLGRAPH` Source-Linked Mode elements
- **Review gate**: Never proceed to the next step without user approval (unless continuous mode was chosen in Step 0)
- **Verification gate**: Never report a document complete before a clean `doc-verifier` pass on it
- **Navigation**: Every domain document has top (line-1 prev/next) and
  bottom (all documents) navigation, same convention and canonical order
  as `dev-planning` — document-to-document across domain boundaries, never
  folder links, and only files actually generated for the domain
- **`@`-references**: Use for discovered docs per [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md)
