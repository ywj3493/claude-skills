---
name: domain-overview
version: 0.0.1
description: Generate a diagram-first DDD domain overview document (docs/en/specifications/domain-overview.md) — one large Mermaid context map of bounded contexts and their aggregate roots, edges labeled with DDD context-map patterns (ACL, OHS, PL, SK, C/S, CF, Partnership) and upstream/downstream direction, plus a per-domain aggregate summary. Auto-detects its source per domain, preferring existing docs under docs/en/specifications/ and falling back to a cited codebase scan ([REF: path:line]) verified by doc-verifier. Triggers on "domain overview", "context map", "bounded context map", "aggregate map", "도메인 지도", "도메인 개요". Do NOT use this for documenting one domain in detail — use dev-planning or dev-reverse-docs for that.
---

# domain-overview

Produces the one document a reader opens **before** diving into any single
domain's spec or design docs: a diagram-first map of the whole system's
bounded contexts, the aggregate roots inside each, and how the contexts
relate — drawn with standard DDD context-map notation. The document is
deliberately prose-poor: the diagrams and tables carry the content, and
anything deeper links to the domain's own documents instead of being
restated here.

## When to Use

- "domain overview", "도메인 개요 문서 만들어줘"
- "context map", "bounded context map", "도메인 지도 그려줘"
- "show me how the domains/aggregates relate", "애그리거트 관계 보여줘"
- Onboarding: several domains are documented (or implemented) and nobody
  has the big picture in one place

## When NOT to Use

- **Documenting one domain in detail** — use `dev-reverse-docs` (existing
  code) or `dev-planning` (new feature). This skill stays at the
  context/aggregate-root level by design.
- **A project with a single trivial domain** — a context map of one box
  adds nothing. Say so and stop instead of generating a one-subgraph
  diagram.
- **Layer/module architecture diagrams** — `architecture.md` (seeded by
  `init-docs`) owns layer structure and module boundaries; this document
  owns *domain* boundaries and their DDD relationships.

## Source Auto-Detection

The skill decides **per domain** where its facts come from; the run as a
whole is naturally hybrid.

1. Read `docs/config.yml` for the source language (default `en`); all
   `docs/en/` paths below substitute the configured code if different.
2. Inventory `docs/en/specifications/`: domain directories and their
   `planning/spec.md` / `design/data-model.md` / `design/design.md` /
   `design/domain-state-machine.md`, plus top-level `overview.md` and
   `architecture.md` if present.
3. A domain is **docs-covered** when it has at least a `spec.md` or a
   design document naming its entities — `data-model.md` is the strongest
   signal. Docs-covered domains are derived from those documents (cited by
   doc path); uncovered domains fall back to a code scan (cited
   `[REF: path:line]`).
4. **Modes**: all domains docs-covered → docs-mode; no docs tree at all →
   code-mode; mixed → hybrid. In code-mode/hybrid, additionally run a
   module-boundary scan (manifests, package/directory structure — the same
   scan as `dev-reverse-docs` Step 0) to *discover* domains the docs don't
   mention.
5. Step 0 states the detected mode and the per-domain source and asks for
   confirmation before anything is generated.

## DDD Notation Rules

The context map uses the standard DDD Crew context-mapping vocabulary.

**Patterns and abbreviations**: Partnership (P), Shared Kernel (SK),
Customer/Supplier (C/S), Conformist (CF), Anticorruption Layer (ACL),
Open Host Service (OHS), Published Language (PL), Separate Ways (SW),
Big Ball of Mud (BBoM). The template ships the full legend table — never
trim it.

**Direction**: every asymmetric edge points **upstream → downstream** and
is labeled `"U/D · <patterns>"` (e.g.
`OrderContext -->|"U/D · OHS+PL"| ShippingContext`). Symmetric patterns
(P, SK) use `<-->` with the abbreviation only. SW pairs get **no edge** —
they appear only in the Context Relationships table.

**Classification evidence guide** — classify each relationship from what
the docs/code actually show:

| Evidence at the boundary | Pattern |
|---|---|
| Translation/adapter layer on the consumer side (mapper, anti-corruption module, DTO translation) | ACL |
| Versioned public API or event schema built for multiple consumers | OHS (+ PL when the schema/format is itself documented) |
| Shared library/types package imported by both contexts | SK |
| Downstream imports the upstream's model directly, no translation | CF |
| Explicit consumer-driven contract (contract tests, negotiated interface) | C/S |
| Mutual synchronous dependency in both directions | P |
| No integration found between the pair | SW (table row only, no edge) |

A classification the evidence doesn't directly support gets
`[ASSUMED: <inference>; basis: <evidence>]` in the table's Evidence
column. An unclassifiable relationship gets Pattern `?` plus an
`[ASSUMED: ...]` — never a silently omitted label.

**Mermaid conventions**: the context map is a `flowchart` — one subgraph
per bounded context, nodes are aggregate roots only, short labels,
`classDef aggregateRoot` styling. Per-domain summaries are `classDiagram`
blocks with `<<AggregateRoot>>` / `<<Entity>>` / `<<ValueObject>>`
stereotypes and empty class bodies (`*--` for owned entities, `o--` for
value objects) — a deliberate type switch that signals the zoom from
context level to aggregate level.

## Grounding & Citation Rules

The `dev-reverse-docs` grounding contract applies, restated briefly:

1. Every claim cites its source — a doc path for docs-derived claims
   (e.g. `[REF: docs/en/specifications/order/design/data-model.md:12]`)
   or `[REF: path:line]` / `[REF: path:start-end]` for code-derived
   claims. Never cite a file not actually opened during this run.
2. Content needed for completeness but not verifiable gets
   `[ASSUMED: <inference>; basis: <evidence>]` — pattern classification
   is the main consumer of this tag here.
3. Every generated document ends with a `## Sources Read` ledger; every
   citation must trace back to a file listed there.

## Execution Requirements

1. **Diagram-first is a hard constraint**: intro prose ≤ 5 sentences;
   each domain section ≤ 3 sentences of prose; no attribute/field/method
   detail anywhere. Anything longer belongs in the domain's own documents
   — link, don't restate.
2. **Aggregate identification is evidence-based**: a docs-covered domain's
   roots come from its documents; a code-scanned domain's roots need code
   evidence (repository-per-aggregate, transactional boundary,
   invariant-owning entity). Never invent an aggregate to make the
   diagram fuller.
3. **Every edge is accounted for**: each context-map edge has a matching
   Context Relationships row with evidence; unclassifiable relationships
   use `?` + `[ASSUMED: ...]` rather than a missing label or row.
4. **Template is mandatory**: load
   `${CLAUDE_PLUGIN_ROOT}/skills/domain-overview/references/domain-overview-template.md`
   before generating. If it is missing, stop and report the missing path
   — never improvise the structure.
5. **Merge, don't overwrite**: if `docs/en/specifications/domain-overview.md`
   already exists, summarize what would change and ask before
   regenerating.
6. **Translation mirror is out of scope**: this skill writes the source
   language only. If `docs/config.yml` lists translation languages, remind
   the user to run `/dev-docs:sync-translations` afterward.

## Step-by-Step Instructions

### Step 0: Scope & Source Detection

1. Run the Source Auto-Detection procedure; build the candidate domain
   list with each domain's source (docs vs. code)
2. Present the detected mode (docs / code / hybrid), the domain list, and
   the per-domain source; confirm with the user
3. Confirm review mode: step-by-step (default) or continuous
4. If only one trivial domain is detected, report that a context map adds
   no value and stop (per When NOT to Use)

### Step 1: Bounded Context Identification

1. Docs-covered: one context per domain directory, plus any contexts that
   `architecture.md` / `overview.md` name — cite the establishing document
2. Code-scanned: derive contexts from the module-boundary scan — cite the
   manifest/directory evidence that establishes each boundary
3. Present the confirmed context list before extracting anything

### Step 2: Aggregate Extraction (per domain)

1. Docs-covered: read the domain's `data-model.md` / `design.md` /
   `spec.md`; extract aggregate roots and their direct members (entities,
   value objects), citing each
2. Code-scanned: read entity/model/aggregate sources; apply the evidence
   heuristics from Execution Requirement 2, citing each root and member
3. The output of this step is a raw per-domain list (root → members) with
   citations, built **before** any diagram is drawn — the same
   extract-then-draw discipline as `dev-reverse-docs`' CALLGRAPH rule

### Step 3: Relationship Classification

1. Find inter-context dependencies — docs: cross-references and Related
   Documents between domain docs, API specs naming other domains; code:
   cross-module imports, HTTP/RPC clients, events/queues, shared packages
2. Classify every pair via the evidence guide; record direction,
   pattern(s), integration mechanism, and evidence per relationship
3. Pairs with no integration are recorded as SW (table only)

### Step 4: Generate the Document

**Output**: `docs/en/specifications/domain-overview.md`

1. Load the template (Execution Requirement 4)
2. Fill: context map from Steps 1–3, Context Relationships table from
   Step 3, per-domain sections from Step 2, Sources Read, Related
   Documents (link only documents that exist), Document Information. The
   Pattern Legend ships complete in the template — leave it as-is
3. Enforce the diagram-first caps (Execution Requirement 1) before
   presenting
4. Wait for review (unless continuous mode)

### Step 5: Verify

1. Invoke `doc-verifier` on the generated document (it verifies doc-path
   citations and code citations alike)
2. For every `MISMATCHED` or `UNSUPPORTED` claim: re-open the cited
   location, correct the claim/citation or convert it to
   `[ASSUMED: ...]`, and re-invoke — repeat until the report is clean or
   the user explicitly accepts known gaps. Never touch `MATCHED` /
   `EXCLUDED` items

### Step 6: Completion Report

Report only after Step 5 ends clean (or gaps were explicitly accepted):

- The generated file path (verified to exist on disk)
- Final `doc-verifier` counts (matched / excluded / accepted gaps)
- Per-domain source mode used (docs / code)
- Relationships left as `[ASSUMED: ...]` or `?`, if any
- Reminder to run `/dev-docs:sync-translations` if a translation mirror
  is configured

## Document Rules

- **Language**: English (the configured source language)
- **Output path**: `docs/en/specifications/domain-overview.md` — a
  top-level cross-cutting document beside `architecture.md`, never inside
  a `<domain>/` directory
- **No pipeline navigation**: this document is outside the
  spec → design → test-spec chain — no NAV NOTE, no prev/next line, no
  `> **Domain**:` tag, no All Documents index
- **Fixed section order**: Context Map → Context Relationships → Domains
  → Pattern Legend → Sources Read → Related Documents → Document
  Information (table + Version History at the end; no metadata block at
  the top)
- **Mermaid**: `flowchart` for the context map, `classDiagram` with
  stereotypes for per-domain summaries — per the DDD Notation Rules
- **`@`-references**: Use for discovered docs — the convention is defined
  in the host project's `.claude/rules/reference-convention.md`
  (auto-loaded when present): a `[@path](path)` link with a
  project-root-relative path marks required context; bare backtick paths
  are informational only
