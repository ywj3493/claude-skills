# Changelog

All notable changes to skills and plugins in this project are documented here.
Entries are ordered newest first. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [explainable/v0.1.0] - 2026-07-28

### Added
- New plugin `explainable`, registered in `.claude-plugin/marketplace.json` — a Korean-language planning and design documentation pipeline that splits frontend and backend design into separate skills and runs its reverse pipeline design-first (Refs: #38)
- 20 Korean templates: 5 cross-cutting (`architecture.md`, `infrastructure.md`, `glossary.md`, `domain-map.md`, `README.md`), 4 planning, 4 backend design (4-Layered DDD), 6 frontend design (FSD), 1 verification. The `## 문서 정보` block gains a `분석 기준 커밋` field so a citation-bearing document records which commit it was true of (Refs: #38)
- `domain-map.md` — the inter-domain document the design set previously lacked: DDD context map, FSD slice dependency graph, integration contracts, and `FLOW-CROSS-` cross-domain flows that link to each domain's own flow keys instead of duplicating their diagrams (Refs: #38)
- `references/document-order.md` holds the canonical navigation order once, instead of repeating a NAV NOTE in every template (Refs: #38)
- `scripts/check-docs.sh` — deterministic checks that need no model judgment: leftover placeholders, mermaid fence balance, relative-link targets, `[REF:]` file and line existence, ID duplication and coverage, and the `T-1NN`/`T-2NN`/`T-3NN` band split (Refs: #38)

### Changed
- Protocol neutrality: `api-interface.md` keeps a fixed document structure while the contract block format follows the detected API style (REST → OpenAPI 3.1, GraphQL → SDL, gRPC → `.proto`, message-based → AsyncAPI). Skills and templates never hardcode a framework or protocol — those enter only as detected facts or user decisions recorded in `architecture.md` (Refs: #38)

## [translate-docs/v0.0.1] - 2026-07-28

### Added
- Initial skill, structurally a copy of `dev-docs`'s `sync-translations` with the body translated to Korean. Scope drops `issue/` (this plugin does not manage issues) and recurses through `specifications/` for the nested design tree (Refs: #38)
- Do-not-translate list covering mermaid block interiors, hidden `CALLGRAPH` blocks, contract blocks, `[REF:]`/`[ASSUMED:]` markers, verifier verdict vocabulary, ID prefixes, and `OWNER`/`GENERATED-BY` markers — translating any of them breaks the verification loop in the mirror (Refs: #38)

## [reverse-planning/v0.0.1] - 2026-07-28

### Added
- Initial skill: derives requirements, user stories, the interface contract, and the traceability matrix from already-generated design documents plus code evidence. A binding derivation table maps evidence class to output (validation/guard code → FR, timeout/retry/rate-limit settings → NFR, entry point + auth role → US, error branches → AC) (Refs: #38)
- Three rules against restating the design docs: citations point at source code and never at a `.md` file, user stories are per (actor, capability) rather than per operation, and the tech-neutrality swap test applies sentence by sentence (Refs: #38)
- Forward planning documents are never overwritten — detected by the absence of a `## 읽은 소스` ledger, they get a `reverse-diff.md` report of plan-versus-implementation drift instead (Refs: #38)

## [reverse-design-frontend/v0.0.1] - 2026-07-28

### Added
- Initial skill: infra → framework detection → FSD fit assessment → one app-shell trace → per-route traces. FSD is a comparison baseline in reverse mode, not a target — code that does not follow it is recorded as it is, without a refactoring proposal (Refs: #38)
- The app shell is traced once rather than per route, and its summary is passed into every route invocation so N identical shell traces never drift apart (Refs: #38)

## [reverse-design-backend/v0.0.1] - 2026-07-28

### Added
- Initial skill: infra → codebase structure → domain identification → per-operation Source-Linked sequence diagrams → domain model and ERD, with a `citation-verifier` fix loop that blocks completion while any `MISMATCHED` or `UNSUPPORTED` claim remains (Refs: #38)
- An operation selection gate replaces the lite/full tier system: trivial pass-through operations become a table row and only those with 3+ participants or a branch get an agent invocation, so a 60-operation service does not produce 60 near-identical CRUD diagrams (Refs: #38)
- Re-running discards that domain's reverse output and rebuilds it against the current commit, after showing the deletion list and checking the working tree is clean. Cross-cutting documents and the glossary are never discarded — only their sections for that domain are updated (Refs: #38)

## [init-design-frontend/v0.0.1] - 2026-07-28

### Added
- Initial skill: FSD layer/slice structure, routing, UI composition, render flow, state flow, and user flows, plus the frontend and E2E sections of the test spec (Refs: #38)
- Framework-neutral vocabulary throughout — "UI 단위", "라우트", "렌더링 모드", "상태 저장소" — so the same templates describe React, Vue, Svelte, or Angular projects. Concrete library names appear only where a detected value is filled in (Refs: #38)
- Document boundaries are pinned so `render-flow.md` and `state-flow.md` cannot repeat each other: local state and re-render triggers belong to render flow, shared and server state to state flow, split on whether the state outlives the route (Refs: #38)

## [init-design-backend/v0.0.1] - 2026-07-28

### Added
- Initial skill: 4-Layered DDD layer mapping, domain model, conditional ERD, user-story-based sequence diagrams with `FLOW-` keys, and the backend section of the test spec (Refs: #38)
- Layer roles and dependency rules live once in `architecture.md`; the per-domain document carries only what is true of that domain, so the generic four-layer diagram is not pasted into every domain (Refs: #38)

## [init-planning/v0.0.1] - 2026-07-28

### Added
- Initial skill: infrastructure and project setup first, then glossary, requirements (FR/NFR), user stories with acceptance criteria, the interface contract, inter-domain integration, and the traceability matrix (Refs: #38)
- The interface contract sits in planning rather than design because both design skills consume it — generating it downstream would let the two skills invent conflicting contracts (Refs: #38)

## [citation-verifier/v0.0.1] - 2026-07-28

### Added
- Initial agent, ported from `dev-docs`'s `doc-verifier` with an identical verification contract and a Korean body. Renamed so two same-named agents cannot diverge across the two plugins. Adds structured-table checks for `architecture.md`, `glossary.md`, and `traceability.md` (Refs: #38)

## [render-flow-tracer/v0.0.1] - 2026-07-28

### Added
- Initial read-only agent: traces the app shell or one route — entry point, UI tree, data sources, state scope, render boundaries, and re-render triggers — and returns a fixed schema. Receives the detected framework as input so it never guesses one (Refs: #38)

## [operation-tracer/v0.0.1] - 2026-07-28

### Added
- Initial read-only agent: traces one backend operation from entry point to repository or external adapter. "Operation" is protocol-neutral — a REST endpoint, GraphQL resolver, gRPC method, message consumer, or scheduled job — and the API style arrives as input (Refs: #38)
- Returns a structured edge list rather than rendered markdown, with `from:` (call site) alongside `[REF:]` (call target), so the calling skill renders the diagram, the per-message `Note`s, and the hidden `CALLGRAPH` block from one source and the verifier's bidirectional check passes by construction (Refs: #38)

## [infra-explorer/v0.0.1] - 2026-07-28

### Added
- Initial read-only agent: collects runtime, container, deployment, environment, CI/CD, datastore, external-service, and observability facts with a citation on every item. Environment variable values are never emitted — only names, purpose, and whether a value exists. Numeric operational parameters are gathered into a `tunables` section that the reverse planning skill uses as NFR evidence (Refs: #38)

## [dev-docs/v0.7.0] - 2026-07-28

### Changed
- Bundled skill `explainable` renamed to `flow-diagram`; `plugin.json` description and `marketplace.json`'s dev-docs description updated to match, and the plugin README (intro, Contents table, Workflow tree, Templates note) re-pointed at the new command (Refs: #38)
- Root `README.md` / `README.ko.md` skill tables, workflow trees, and repository-structure listings now include the skill, which had been missing since it was added in v0.6.0 (Refs: #38)

## [flow-diagram/v0.1.0] - 2026-07-28

### Changed
- Renamed from `explainable` (`skills/explainable/` → `skills/flow-diagram/`, `name:` frontmatter, `# flow-diagram` heading), freeing the `explainable` name for the new sibling plugin. Behavior is unchanged — the command is now `/dev-docs:flow-diagram` (Refs: #38)

## [dev-docs/v0.6.0] - 2026-07-24

### Added
- `explainable` skill bundled in the plugin — a lightweight complement to the two full pipelines, surfaced in the README Contents table, Workflow diagram, and Templates note; plugin description updated to mention it (Refs: #35)

## [explainable/v0.0.1] - 2026-07-24

### Added
- New single-artifact skill: after implementation work, writes or merges ONE Source-Linked sequence diagram for the flow just built or changed into the domain's `design/sequence-diagram.md` (Lite-tier domains: the `## Core Flows` section of `design.md`). Reuses `templates/design/sequence-diagram.md` in Source-Linked Mode (participant `link` lines, per-message `path:line` `Note`s, `[ASSUMED: ...]` fallback, hidden `CALLGRAPH` block) but drops the tier system, the review gates, and the `doc-verifier` loop. Scope is derived from the actual change set (named files → git diff vs. merge base → working tree), and the skill points at `dev-planning`/`dev-reverse-docs` for the full document set (Refs: #35)

## [dev-docs/v0.5.0] - 2026-07-23

### Added
- `domain-overview` skill bundled into the plugin (packaging change; the skill's own changes are recorded under `[domain-overview/v0.0.1]`) (Refs: #34)

### Changed
- `plugin.json` description mentions the diagram-first DDD domain overview (context map) generator; keywords gain `ddd` and `context-map`; `marketplace.json`'s dev-docs description synced back to `plugin.json`'s (Refs: #34)
- Plugin README (Contents table, Workflow tree, Templates note, Host-project expectations) and root README.md / README.ko.md list the new skill (Refs: #34)

## [domain-overview/v0.0.1] - 2026-07-23

### Added
- Initial `domain-overview` skill: generates a diagram-first DDD domain overview at `docs/<source>/specifications/domain-overview.md` — one large Mermaid context map (subgraph = bounded context, node = aggregate root) with edges labeled by DDD context-map patterns (P, SK, C/S, CF, ACL, OHS, PL, SW, BBoM) and upstream→downstream direction, a Context Relationships evidence table, per-domain aggregate summaries as stereotype `classDiagram` blocks, and a fixed pattern legend (Refs: #34)
- Per-domain source auto-detection: docs-covered domains derive from existing specification documents (data-model.md is the strongest signal), uncovered domains fall back to a cited code scan (`[REF: path:line]`), mixed runs are hybrid; generated output is checked by the existing `doc-verifier` agent with the standard fix-mismatches loop (Refs: #34)
- Skill-local template `references/domain-overview-template.md` — a cross-cutting top-level document outside the spec → design → test-spec pipeline (no NAV NOTE, prev/next, Domain tag, or All Documents index), with hard diagram-first caps (intro ≤ 5 sentences, ≤ 3 sentences per domain section, no attribute-level detail) (Refs: #34)

## [init-docs/v0.4.0] - 2026-07-22

### Added
- Step 4 "Configure .claude/rules/": asks which rule sets to install (general workflow policy, commit message rules, naming conventions, `@`-reference convention — all four the default) and whether the defaults need adjustments, then seeds the selected files into the host project's `.claude/rules/`, where Claude Code auto-loads them every session (Refs: #32)
- `references/rules/` — the four rule templates, moved out of SKILL.md's embedded blocks and adapted for auto-loaded `.claude/rules/` (plain "See also" cross-references instead of `@`-references, `.claude/rules/` exempted from `@`-referencing) (Refs: #32)

### Changed
- `references/CLAUDE-template.md` (and the matching root `templates/CLAUDE.md`): Core Rule 5 "Policy is law" and Required Context now point at auto-loaded `.claude/rules/` instead of `@`-referencing four policy files; `policy/` removed from the structure tree and the translation-mirror rule (Refs: #32)
- `scripts/create-structure.sh` no longer creates `policy/` directories; next-steps output announces the `.claude/rules/` setup question instead of policy file creation (Refs: #32)

### Removed
- `docs/<source>/policy/` scaffolding and the four seeded policy documents (`policy.md`, `commit-message-rule.md`, `naming-conventions.md`, `reference-convention.md`) — downstream projects now keep their operative rules in `.claude/rules/`, the same pattern this repository adopted in #22 (Refs: #32)

## [sync-translations/v0.4.0] - 2026-07-22

### Removed
- `policy/` from the mirrored directory set (scope table, mirroring offer, mirror-directory creation, audit `find`, and examples) — init-docs no longer scaffolds a policy directory, and `.claude/rules/` is English-only Claude Code configuration, not a translation target (Refs: #32)

## [dev-planning/v0.1.1] - 2026-07-22

### Fixed
- Document Discovery scans `docs/en/policy/` only if that directory exists (init-docs no longer creates it), and the `@`-reference document rule states the convention inline, sourced from the host project's `.claude/rules/reference-convention.md` instead of `@`-referencing the no-longer-seeded `docs/en/policy/reference-convention.md` (Refs: #32)

## [dev-reverse-docs/v0.1.1] - 2026-07-22

### Fixed
- `@`-reference document rule states the convention inline, sourced from the host project's `.claude/rules/reference-convention.md` instead of `@`-referencing the no-longer-seeded `docs/en/policy/reference-convention.md` (Refs: #32)

## [dev-docs/v0.4.0] - 2026-07-15

### Added
- `templates/planning/spec.md` — single planning template merging requirements, user stories, and use cases into a hierarchical FR → US/AC → UC layout; use cases survive as a conditional **Multi-Actor Flows** section gated on "2+ actors or an external system", and the System Context diagram shares the same gate (Refs: #30)
- `templates/design/domain-state-machine.md` (Backend-only) and `templates/design/client-store.md` (Frontend-only) — the two halves of the former `state-diagram.md`, so entity/workflow state machines and client-side stores are selected independently
- Every design template's note callout now carries a parsable `> **Domain**: Backend-only | Frontend-only | Infra-only` tag
- `templates/design/design.md` — Lite-tier single design document whose H2 sections are condensed forms of the individual design templates, each with its own trigger comment and Domain tag; the fixed Lite chain is spec → design → test-spec

### Changed
- Canonical navigation order now runs spec → [design subset] → test-spec, with component-diagram → domain-state-machine → client-store → infra-spec inside the design subset; NAV NOTE comments, prev/next links, Related Documents, and All Documents indexes updated across all templates
- UC anchors moved from `use-case.md#uc-<area>-nn` to `spec.md#uc-<area>-nn` (heading-derived anchors unchanged in format), preserving test-spec traceability paths

### Removed
- `templates/planning/requirements.md`, `templates/planning/user-stories.md`, `templates/planning/use-case.md` — merged into `spec.md`; dropped en route: stakeholders table, actor/use-case Mermaid diagrams, use-case category/relationship tables, per-FR Input/Process/Output blocks, per-story NFR tables, and two duplicate footers
- `templates/design/state-diagram.md` — split into the two design templates above

Known limitation: re-running a Lite domain in Full tier (splitting its `design.md` into individual files) is not automated in this release — rely on the merge-don't-overwrite behavior and manual review.

## [dev-planning/v0.1.0] - 2026-07-15

### Added
- Lite/Full tier selection in Step 0: an explicit invocation argument (`/dev-docs:dev-planning lite|full`) wins; otherwise an auto-detect heuristic (primary actor count, external systems, triggered design categories, regulated domain) proposes a default the user confirms or overrides. Lite generates spec.md + a single merged design.md + test-spec.md; Full keeps the dynamic individual design files (Refs: #30)

### Changed
- Steps 1–3 (requirements, user stories, use case) collapsed into a single Step 1 that generates `planning/spec.md`; the pipeline is now Step 1 spec → gate → Step 2 design → Step 3 test-spec → Step 4 README (Refs: #30)
- Multi-Actor Flows (use cases) and the System Context diagram are generated only when the feature involves 2+ actors or an external system
- Planning → Design review gate now locks the design selection after spec.md approval; Document Rules state the tech-neutrality test ("still true if the stack were swapped?") and role-based (Secondary Actor) naming for external systems
- Design Document Selection now offers `domain-state-machine.md` and `client-store.md` as independent rows instead of a single `state-diagram.md`
- Execution Requirement 5 documents the heading-derived anchor scheme for ID links (e.g. `spec.md#uc-auth-01-login`)

## [dev-reverse-docs/v0.1.0] - 2026-07-15

### Added
- Lite/Full tier selection in Step 0: an explicit invocation argument (`/dev-docs:dev-reverse-docs lite|full`) wins; otherwise code signals (actor-facing surfaces, external integrations, evidence-backed design categories, module size) propose a default the user confirms or overrides. Lite generates spec.md + a single merged design.md + test-spec.md; citations and the doc-verifier loop stay mandatory in both tiers (Refs: #30)

### Changed
- Pass 2 planning output is a single `planning/spec.md` (was `requirements.md` + `user-stories.md` + `use-case.md`); grounding, citation, and doc-verifier rules unchanged (Refs: #30)
- Multi-Actor Flows section is generated only when code evidence shows 2+ actors or an external system
- Design Document Selection now offers `domain-state-machine.md` and `client-store.md` as independent rows instead of a single `state-diagram.md`

## [dev-docs/v0.3.0] - 2026-07-15

### Added
- `init-docs` (v0.3.0) and `sync-translations` (v0.3.0) skills bundled into the plugin, moved from the standalone `skills/` directory — the plugin now covers the full docs-driven workflow: scaffold → plan/reverse-doc → translation sync (Refs: #28)

### Changed
- Plugin description and keywords expanded to cover docs scaffolding and opt-in translation mirror sync (`plugin.json`, `marketplace.json`); plugin README documents the four-skill workflow

### Removed
- Standalone `skills/` directory — every skill now ships inside the `dev-docs` plugin

## [init-docs/v0.3.0] - 2026-07-15

### Changed
- Moved into the `dev-docs` plugin (`/dev-docs:init-docs`); script and template paths now resolve via `${CLAUDE_PLUGIN_ROOT}` (Refs: #28)
- Initialization is source-language only: Step 1 confirms just the source (base) language, `docs/config.yml` is written with `translation_languages: []`, and no mirror directories or translated policy files are created — mirroring is deferred to `sync-translations` as an opt-in step
- Seeded policy templates describe translation mirrors as conditional on `docs/config.yml` instead of assuming an `en` → `ko` pairing
- `create-structure.sh` defaults to `en` only (translation-language arguments remain supported for later mirror creation) and its next-steps message no longer references the removed `/new-issue` skill

### Removed
- Step 5 (policy translation mirrors) — replaced by a pointer to `/dev-docs:sync-translations`

## [sync-translations/v0.3.0] - 2026-07-15

### Added
- Mirror opt-in flow: when `translation_languages` is empty, the skill offers to enable mirroring — records the confirmed language(s) in `docs/config.yml`, creates the mirror directories, then runs the normal audit-and-translate flow (Refs: #28)
- Execution Requirement 7: `docs/config.yml` is only updated after explicit user confirmation of the language choice

### Changed
- Moved into the `dev-docs` plugin (`/dev-docs:sync-translations`); missing-structure guidance now points to `/dev-docs:init-docs`

## [new-issue] - 2026-07-15

### Removed
- Skill removed from the repository (not absorbed into the plugin consolidation; create GitHub Issues directly via `gh`, or local `docs/<lang>/issue/` documents, instead) (Refs: #28)

## [new-policy] - 2026-07-15

### Removed
- Skill removed from the repository (its scope shrank after this repository's own policy moved to `.claude/rules/`; ad-hoc `docs/*/policy/` documents can be authored directly) (Refs: #28)

## [dev-docs/v0.2.0] - 2026-07-15

### Changed
- All 11 document templates share one skeleton: line-1 prev/next navigation (first document omits "←", last omits "→"), title, optional classification/generation note, table of contents, body, `## Sources Read` (reverse-docs only), `## Related Documents` (supporting references only), `## Document Information`, and the "All Documents" index (Refs: #26)
- Document metadata (Created, Last Modified, Status, Tech Stack, Reference Documents) moved from the top-of-file blockquote into a bottom `## Document Information` table, with the Version History list beneath it
- Navigation now chains document-to-document across domain boundaries in a canonical order (requirements → user-stories → use-case → [user-flows → sequence-diagram → api-spec → data-model → component-diagram → state-diagram → infra-spec] → test-spec); folder links (`../design/`) are no longer used in prev/next, and NAV NOTE comments in `use-case.md`, the design templates, and `test-spec.md` instruct substituting the design files actually generated
- "All Documents" indexes list the full canonical set in every template, with a substitution comment to keep only generated files and bold the current document

### Fixed
- `templates/planning/requirements.md` used a `## Document Navigation` section instead of the line-1 navigation every other template uses
- Contradictory design-template navigation (`sequence-diagram.md` and `user-flows.md` both claimed prev = use-case)
- `templates/design/data-model.md` example referenced the removed `NFR-ARCH` category

### Removed
- Implementation technology from the planning templates: Tech Stack metadata row, the Architecture project-info field, Technical/Architecture constraint tables (replaced by Business / Operational / Development Process constraints), `NFR-ARCH`/`NFR-DEPLOY` categories (replaced by `NFR-AVAIL`/`NFR-USE`), the traceability matrix's Implementation column, and implementation-level detail (API paths, server/DB participants) in the use-case main-flow example

## [dev-planning/v0.0.2] - 2026-07-15

### Changed
- Document Rules describe the bottom `## Document Information` table instead of a top meta block, restrict TypeScript interfaces to design documents, and add a "planning docs are non-technical" rule (Refs: #26)
- Navigation section defines the canonical pipeline order and document-to-document chaining across domain boundaries; Execution Requirement 5 forbids folder links in prev/next
- Step 0 records the detected tech stack only in design/verification documents; Step 1 derives business/operational/process constraints instead of technical/architecture ones

## [dev-reverse-docs/v0.0.2] - 2026-07-15

### Changed
- Document Rules describe the bottom `## Document Information` table, the non-technical planning rule (citations stay mandatory as provenance), the `## Sources Read` placement before Related Documents/Document Information, and the canonical navigation order shared with `dev-planning` (Refs: #26)
- Step 2 writes requirements in stakeholder language, deferring code-revealed technical detail to Step 3's design documents

## [dev-docs/v0.1.0] - 2026-07-12

### Added
- New `dev-docs` plugin (`dev-docs-plugin/`, `.claude-plugin/plugin.json`) bundling two skills and a verification subagent, replacing the standalone `dev-planning` skill (Refs: #20)
- `dev-planning` skill (v0.0.1): forward-only planning pipeline for new features, now emitting `planning/`/`design/`/`verification/` documents with a dynamic multi-file design-document selection table instead of a rigid backend/frontend/infra branch
- `dev-reverse-docs` skill (v0.0.1, new): reverse-engineers grounded documentation from existing code, enforcing `[REF: path:line]`/`[ASSUMED: ...]` citation on every claim, a hierarchical overview-then-module scope strategy for large repos, and mandatory `doc-verifier` verification after every generation pass before reporting completion
- `doc-verifier` agent (v0.0.1, new): read-only (`Read, Grep, Glob`) subagent that checks every citation in a generated doc against the actual source, with an additional cross-check for sequence diagrams between the visible source-linked `Note`s and a hidden `<!-- CALLGRAPH: ... -->` block
- Sequence diagrams generated by `dev-reverse-docs` link every participant to its source file (`link <alias>: Source @ <repo_url>/blob/<branch>/<path>`) and cite real `path:line` evidence per message
- `templates/design/user-flows.md` and `templates/design/infra-spec.md` restored from the old skill into the dynamic design-document set (selection-table rows in both skills); `component-diagram.md` regains the caching / API-client / error-handling guidance, and `test-spec.md` regains the user-flows exception-path → E2E derivation
- Marketplace manifest (`.claude-plugin/marketplace.json` at the repository root) and a plugin `README.md`, so the plugin installs via `/plugin marketplace add` as well as `--plugin-dir`

### Fixed
- Broken `(#)` anchor in `templates/planning/use-case.md`; hardcoded prev/next and "All Documents" links in the `design/` templates replaced with generation-time substitution notes consistent with the dynamic design-document selection

### Removed
- `dev-planning` skill removed from `skills/` (superseded by the `dev-docs` plugin's `dev-planning`/`dev-reverse-docs` skills)

## [init-docs/v0.2.1] - 2026-07-12

### Changed
- Domain-directory note references the `dev-docs` plugin's `dev-planning`/`dev-reverse-docs` skills instead of the removed standalone `dev-planning` skill

## [v0.1.0] - 2026-07-12

Project-wide structural change (not tied to a single skill):

### Changed
- This repository's own operative policy (general policy, commit messages, naming, `@`-reference convention, skill/plugin versioning) relocated from bilingual `docs/{en,ko}/policy/` to `.claude/rules/` — English-only, auto-loaded every session; `skill-versioning.md` extended with plugin versioning rules (Refs: #22)
- `docs/{en,ko}/policy/` retained (with `.gitkeep`) as scaffolding for downstream-style ad-hoc policy documents created via `new-policy`

## [init-docs/v0.2.0] - 2026-07-07

### Added
- Configurable languages: Step 1 asks for a source language and translation languages, recorded in docs/config.yml; create-structure.sh accepts language arguments
- CLAUDE.md template bundled at references/CLAUDE-template.md so installed copies are self-contained

### Changed
- architecture and infrastructure templates upgraded to the richer format from the removed frontend-planning skill (module boundaries, key files, deployment topology, CI/CD pipeline, external services)

### Changed
- Directory, policy, and mirror creation follows the configured languages instead of hardcoded en/ko; projects may configure zero translation languages
- Planning-skill note references dev-planning instead of deprecated frontend-planning

## [new-issue/v0.3.0] - 2026-07-07

### Added
- Docs mode verifies the docs structure exists and guides to /init-docs when missing

### Changed
- Draft PR creation is optional — settled at the issue-content confirmation gate ("issue only" skips it)
- Docs-mode mirrors follow the translation languages in docs/config.yml instead of hardcoded Korean

## [dev-planning/v0.3.0] - 2026-07-07

### Added
- Review mode choice at Step 0: step-by-step (default) or continuous generation with one consolidated review at the end
- Optional Step 3.5 (frontend only): user-flows document restored from the removed frontend-planning skill as references/frontend/user-flows-template.md; exception/alternative paths feed E2E scenarios in the test spec

### Changed
- Output paths documented as source-language-relative (docs/config.yml) instead of hardcoded docs/en

## [new-policy/v0.2.0] - 2026-07-07

### Added
- Docs-structure precondition check with guidance to /init-docs when missing

### Changed
- Translation mirrors follow the configured translation languages; source-only projects skip mirrors

## [sync-translations/v0.2.0] - 2026-07-07

### Added
- Step 0 loads docs/config.yml (with directory-layout inference fallback) and stops with guidance when no docs structure exists

### Changed
- Generalized from hardcoded en → ko to the configured source and translation languages

## [backend-planning] - 2026-07-07

### Removed
- Skill removed from the repository (deprecated since v0.0.2; superseded by dev-planning)

## [frontend-planning] - 2026-07-07

### Removed
- Skill removed from the repository (deprecated since v0.0.2; superseded by dev-planning)

## [dev-planning/v0.2.0] - 2026-07-07

### Added
- Execution Requirements section: mandatory template loading, disk-based input re-reading, sequential ID assignment, pre-completion traceability validation, link/diagram verification, literal review gates, verified-path reporting

## [new-issue/v0.2.0] - 2026-07-07

### Added
- Execution Requirements section: output-based mode detection, no invented identifiers, overwrite protection for local issue numbers, explicit failure recovery, pre-report artifact verification, structural parity between issue/PR/mirror

## [init-docs/v0.1.0] - 2026-07-07

### Added
- Execution Requirements section: pre-creation survey with overwrite protection, verbatim template copying, real-date placeholders, post-creation tree verification, translation parity, verified-facts-only reporting

## [new-policy/v0.1.0] - 2026-07-07

### Added
- Execution Requirements section: kebab-case filename validation with collision check, real-date revision history, paired-language creation in one run, explicit policy.md gate, pre-report verification

## [sync-translations/v0.1.0] - 2026-07-07

### Added
- Execution Requirements section: exhaustive audit coverage, content-level stale confirmation over timestamp heuristics, full-source translation from disk, structural parity verification, docs/ko-only write scope, per-file reporting

## [new-issue/v0.1.0] - 2026-03-31

### Added
- GitHub Issues mode via `gh issue create` when git remote exists
- Automatic branch creation for new issues
- Draft PR creation linked to the issue (`Resolves #N`)
- Automatic mode detection (`git remote -v` + `gh auth status`)
- GitHub-native issue references (`Refs: #N`, `Closes #N`)

### Changed
- Local docs-based issue creation is now fallback for repos without a remote
- Korean mirror step skipped in GitHub mode
## [dev-planning/v0.1.0] - 2026-03-30

### Added
- Unified planning pipeline: requirements -> user stories -> use cases -> sequence diagrams -> domain spec -> test spec
- Domain type branching: backend (api-spec), frontend (component-spec), infra (infra-spec placeholder)
- ID-based test traceability (FR-XXX, AC-XXX, UC-XXX) with dedicated test-spec document
- Common templates shared across all domain types
- Document navigation (prev/next and all-documents index) on every template

## [backend-planning/v0.0.2] - 2026-03-30

### Deprecated
- Superseded by dev-planning. Use dev-planning instead.

## [frontend-planning/v0.0.2] - 2026-03-30

### Deprecated
- Superseded by dev-planning. Use dev-planning instead.

## [backend-planning/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- 5-step backend planning pipeline (requirements → user stories → API spec → use cases → sequence diagrams)

## [frontend-planning/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- 6-step frontend planning pipeline (requirements → user flows → UI spec → use cases → component tree → state/API integration)

## [new-issue/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Issue document creation with Korean translation

## [new-policy/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Policy document creation with Korean translation

## [sync-translations/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Audit and sync Korean translations for docs/en/

## [init-docs/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Standard docs/ directory structure initialization
