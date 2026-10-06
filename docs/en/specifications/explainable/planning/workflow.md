# Reference-based planning workflow

Implemented for [GitHub issue #43](https://github.com/ywj3493/claude-skills/issues/43),
including the screen ownership decisions raised in #42. Plugin version: 0.4.0.

## Entry and ownership

Planning starts with the service purpose, actors, core tasks, success criteria, scope,
UI need, and a screen count classified as a fixed constraint or a target. An unknown
technology stack does not prevent requirements, screens, review, or static mockups.
Projects without a UI retain requirements/stories and omit the screen documents.

| Task | Skill | Input | Output | Review |
|---|---|---|---|---|
| Register references | prepare-planning | Workflow, skill material, design system, icons, UI guidance, storyboard | Reference register, immutable snapshot, three HTML pattern candidates | Material selection and pattern choice |
| Generate planning | init-planning | Service brief and selected snapshot | Requirements, stories, IA, flows, screen specifications, decisions, state, annotations | Exact planning version |
| Revise planning | revise-planning | Latest documents, retained decisions, change request | Scoped edits, archived previous version, retired/replacement IDs, stale artifacts | Change scope and revised version |
| Build mockups | build-storyboard | Approved screen specifications and annotations | Static HTML with badges and generated description tables | Visual and functional review |
| Exchange designs | sync-design | Approved HTML, exchange package, actual connector or manual transfer | Mapping, three-way change/conflict/loss report | Adoption of external changes |
| Prepare development | prepare-design | Approved planning | Architecture, infrastructure, API contract, hashed readiness inputs | Technology and contract decisions |

Backend/frontend development design follows prepare-design. Existing code still follows
reverse-design → reverse-planning, with code citations and verifier checks.

## Screen model decisions

Storyboard is both an optional input and a generated review artifact. Planning owns
the user-visible screen → section → conceptual component → element → action hierarchy
in screen-spec.md; component-tree.md owns implementation units and FSD structure.
Requirements/stories, IA, flows, and screen specifications have distinct responsibilities.
Only flows describe screen transitions; only implementation design describes code execution.

Section/component/element IDs are stable and traced to FR/US/AC/SCR/UF, annotations,
mockup badges, and external node mappings. A badge is a display number, not an identity.
Decorative content has no functional badge. Page screens map to routes; overlays and
state variants map through a parent page. Loading, empty, error, and permission states
are specified or explicitly marked inapplicable.

Issue 010 consolidated ui-spec into implementation specifications in another workflow.
It does not establish that user-facing screen semantics must never exist. This workflow
separates semantic ownership, implementation ownership, and derived visual artifacts
to prevent duplicate sources of truth.

## Evidence and lifecycle

Reference records retain type, registering party, origin, version, scope, search query,
selected range, and SHA-256. Snapshot bytes and manifests are immutable. Search starts
with file/range selection; no vector database or embedding implementation is claimed.
Skill amendments preserve originals, differences, and approval status. Registered
skill/HTML/SVG material is data, not execution authority.

Decision records distinguish user decisions, AI proposals/assumptions, conflicting rules,
affected screens, and unresolved items. Historical decisions can retain their own
snapshotId after references are reselected. Unknown evidence is not replaced with invented facts.

Four revision modes are implemented: single screen, whole planning with screen IDs
preserved, full restructuring, and reference reselection. New versions archive current
documents and annotations; deleted IDs remain retired, and replacement relationships
are explicit. Restoring an archive creates a new review version and preserves newer
human decisions. It does not restore approval automatically.

Status is draft/in-review/changes-requested/approved. Approval targets an exact version
and requires no unresolved items. Development readiness is separate: designReadyVersion
and hashes of architecture/infrastructure/API inputs are recorded after review. Planning
edits clear readiness and mark affected artifacts stale. Unchanged scoped artifacts retain
their generation version and record verifiedForVersion for reuse. Changed technical input hashes
invalidate readiness until prepare-design is reviewed again.

Forward/reverse classification prioritizes state mode and producer/mode markers.
Legacy code-source ledgers are fallback evidence, not a reason to delete ambiguous
documents. A reference register in forward planning never makes it reverse output.

## Executable support

Python 3.9+ standard library and Bash are sufficient. planning-tools.py provides
snapshot, classify, check/check-tree, freeze, revise, restore, approve, build,
ready-design, export-sync, and compare-sync commands. check-docs.sh runs the structured
checks alongside existing document/link/citation/traceability checks and excludes
archived versions and reference snapshots. Its array loading works on macOS Bash 3.

HTML uses a local subset of Tailwind utility styles, with escaped labels, a restrictive
content security policy, and no JS or CDN. Badges and description rows are derived from
the same annotations. Regeneration detects manual HTML edits instead of overwriting them.
Rendering in a real browser is a separate visual review requirement.

Design exchange packages retain baseline version, Figma file/node mappings, HTML hashes,
capabilities, and losses. Three-way comparison uses baseline/current/incoming values and
reports visual/functional changes, entity additions/deletions, and concurrent conflicts.
Returned designs are change proposals; they are never treated as code facts or auto-applied.

## Integration boundaries

BSS Sync, a custom Figma plugin, universal HTML/CSS conversion, embedding infrastructure,
and a new web application are not bundled. An actual connector must normalize its data
to the exchange contract; manual file transfer is supported. Text/style/layout/badges/
annotation preservation and icon losses are explicit. The default exporter reports icon
conversion unsupported. Missing mappings, unsupported capabilities, or losses prevent
the report from being marked ready. Actual Figma round-trip success requires a real
connector and sample execution, followed by human approval.

## Verification

Temporary fixtures verify valid planning without a stack; immutable/tampered snapshots;
orphan and duplicate IDs; blocked approval; HTML escaping and badge correspondence;
four revision modes; unrelated-screen and human-decision preservation; archived versions;
retired-ID rejection; stale mockups; concurrent design changes; explicit provenance;
UI-free projects; and legacy/new checker compatibility. Additional negative cases verify
mapping/capability losses, structural edits, restoration, and development readiness hashes.
Representative HTML was additionally rendered at 1440px and 390px in headless Chrome.
Both widths have no horizontal overflow and four matching badges/description rows.
This visual smoke check does not constitute user approval or actual Figma conversion.

## Document information

| Field | Value |
|---|---|
| Updated | 2026-10-05 |
| Related issues | #43, #42, #40 |
| Plugin version | 0.4.0 |
