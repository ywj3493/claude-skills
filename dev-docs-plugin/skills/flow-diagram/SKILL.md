---
name: flow-diagram
version: 0.1.0
description: Make an implementation change explainable by writing or updating ONE Source-Linked sequence diagram for the flow that was just built or changed, merged into the domain's design/sequence-diagram.md. Triggers on "explain what you just built", "diagram this change", "시퀀스 다이어그램으로 설명해줘", "방금 작업 다이어그램으로 남겨줘", or a request to document the call flow of a finished feature/fix. Do NOT use this to produce a full planning/design/verification document set — use dev-planning (new feature) or dev-reverse-docs (existing codebase) for that.
argument-hint: "[domain]"
---

# flow-diagram

Produces exactly one artifact: a **sequence diagram of the flow you just
implemented**, grounded in the code that was actually written.

The full pipelines in this plugin (`dev-planning`, `dev-reverse-docs`)
generate a whole `planning/` → `design/` → `verification/` tree behind
multi-step review gates. That is the right shape when a feature needs to be
specified from scratch or a codebase needs to be documented cold. It is the
wrong shape after ordinary implementation work, where the code is already in
context and the only thing missing is a picture of the call order. This
skill is the minimal version of that: one document, one merge, no tier
selection, no review gates, no `doc-verifier` loop.

## When to Use

- Right after implementing a feature, endpoint, or fix — "explain what you
  built", "방금 작업 다이어그램으로 남겨줘"
- "diagram this change", "이 flow 시퀀스 다이어그램으로 그려줘"
- A reviewer needs the call chain of a change to be legible without reading
  the whole diff
- An existing `design/sequence-diagram.md` has gone stale for a flow that
  was just modified

## When NOT to Use

- **A new feature that has no code yet** — nothing to ground the diagram in.
  Use `dev-planning`.
- **Documenting a whole codebase or module cold** — that needs the
  overview-then-module passes and the `doc-verifier` gate. Use
  `dev-reverse-docs`.
- **A change with no inter-component call chain** — a copy tweak, a config
  bump, a rename. A one-participant sequence diagram is noise; say so and
  skip instead of drawing it.

## Output

One file, merged in place:

```text
docs/<source>/specifications/<domain>/design/sequence-diagram.md
```

`<source>` is the source language configured in `docs/config.yml` (default
`en`). `<domain>` is the domain the change belongs to — see Step 1.

**Lite-tier domains** (a domain whose `design/` holds a single merged
`design.md` instead of individual files) get the same content merged into
that file's `## Core Flows` section instead. Never create a
`sequence-diagram.md` next to an existing `design.md` — that splits one
domain's design across two conventions.

This skill writes the source-language document only. Translation mirrors are
`sync-translations`' job; mention it in the completion report if
`docs/config.yml` declares a translation language.

## Grounding Contract

Every diagram this skill writes is in **Source-Linked Mode**, defined in
`${CLAUDE_PLUGIN_ROOT}/templates/design/sequence-diagram.md`:

1. Every participant gets a `link <alias>: Source @ <repo_url>/blob/<branch>/<path>`
   line — `<repo_url>` from `git remote get-url origin` normalized to
   `https://`, `<branch>` from the branch checked out right now.
2. Every message arrow is followed by a `Note` carrying the real
   `path:line` of the call site.
3. A message that cannot be pinned to a call site gets
   `[ASSUMED: <inference>; basis: <evidence>]` instead — **never** a guessed
   `path:line`. A fabricated citation is worse than an honest gap.
4. Each flow section ends with the hidden `<!-- CALLGRAPH: ... -->` block
   listing the raw call edges the diagram was drawn from.
5. Extract the call graph **first** (read the changed files and follow the
   call sites outward), then draw the diagram from that extraction. Never
   draw the diagram from memory of what you implemented and back-fill the
   `Note`s.

`doc-verifier` is deliberately **not** invoked — the code was written or read
in this same session, so the verification loop would re-read what is already
in context. If the change set is large enough that you are no longer sure the
citations hold, that is the signal to use `dev-reverse-docs` instead.

## Steps

### Step 1: Scope the change and pick the domain

1. Determine the change set — in order of preference: files the user named,
   then `git diff --name-only` against the merge base with the default
   branch, then the uncommitted working tree. State which one you used.
2. Read the changed files and follow their call sites outward until each
   flow terminates (external system, storage, or return to the caller).
   Follow calls, not directories — a flow that leaves the changed files is
   still part of the flow.
3. Pick `<domain>`: an explicit skill argument wins; otherwise match against
   the existing directories under `docs/<source>/specifications/`; otherwise
   propose one derived from the change paths and confirm it before writing.
4. Name each flow after the behavior, not the entrypoint ("Refresh expired
   session token", not "POST /auth/refresh"). The name becomes a heading
   anchor that later runs of this skill match on, so keep it stable.

Report the scope in one line — change set source, files read, flows found,
target domain — then proceed. Do not stop for approval unless the domain had
to be proposed rather than matched.

### Step 2: Extract the call graph

For each flow, record its raw call edges before drawing anything:

```text
<caller>:<line> -> <callee> | <path>:<line>
```

This becomes the `CALLGRAPH` block verbatim. Edges you cannot resolve stay
out of it — they become `[ASSUMED: ...]` messages in the diagram.

### Step 3: Write or merge the document

**If the target file does not exist**: load
`${CLAUDE_PLUGIN_ROOT}/templates/design/sequence-diagram.md`, fill only the
sections this change supports, and delete the rest — placeholder Core Flows,
empty Error Handling Flows, and the Performance Optimization Points section
all go if the change has no evidence for them. Keep the `## Sources Read`
ledger; this skill cites code, so it applies here.

**If the target file exists**: this is a merge, not a rewrite.

- A flow whose heading already exists → update that section in place
  (diagram, Key Steps, Related Code, `CALLGRAPH`).
- A new flow → append a new `### <Flow Name> Flow` section under
  `## Core Flows`, after the existing ones.
- Error paths introduced by the change → same rules under
  `## Error Handling Flows`.
- Leave every unrelated section byte-for-byte untouched.
- Append the file's own `## Sources Read` ledger with the files read this
  run; do not drop entries from previous runs.

**Use Case links**: the template's `**Use Case**: [UC-...](../planning/spec.md#...)`
line is only written when that anchor actually exists in the domain's
`spec.md`. If there is no `spec.md`, or no matching `UC-` heading, omit the
line entirely rather than linking into nothing.

**Navigation**: if the file is new, chain its line-1 prev/next and its
bottom All Documents index through the design documents that actually exist
in this domain, in the canonical order
(`spec → user-flows → sequence-diagram → api-spec → data-model →
component-diagram → domain-state-machine → client-store → infra-spec →
test-spec`), and add the new file to the neighboring documents' navigation
blocks so the chain stays connected in both directions. If the file already
exists, leave its navigation alone.

### Step 4: Update document metadata

Set `Last Modified` in the Document Information table to today's date, set
`Tech Stack` from what the changed files actually use, and add one Version
History line naming the flows added or updated. On a new file, `Created` is
today and Status is `Draft`.

### Step 5: Report

One short report — no ceremony:

- The file path (confirmed to exist on disk)
- Flows added vs. flows updated, by name
- Any `[ASSUMED: ...]` messages written, and why they could not be pinned
- Whether a translation mirror is configured and therefore stale
  (`/dev-docs:sync-translations` to refresh it)

## Document Rules

- **Language**: the source language configured in `docs/config.yml`
  (default English)
- **Mermaid**: `sequenceDiagram` for flows; `alt`/`opt`/`loop` blocks for
  branching rather than a separate diagram per branch
- **Participant notation**: `FileName<br/>(Layer)`, per the template's
  Participant Notation section
- **Citations**: `path:line` in per-message `Note`s;
  `[ASSUMED: <inference>; basis: <evidence>]` where a call site cannot be
  resolved
- **`## Sources Read`**: required — every `Note` and `CALLGRAPH` edge must
  trace back to a file listed there
- **Merge, never overwrite**: an existing document's unrelated sections are
  out of scope for this skill
- **No new document types**: if the change calls for an API contract, a data
  model, or a test spec, say so in the report and point at `dev-planning` /
  `dev-reverse-docs` — do not generate them here
- **`@`-references**: use for any discovered document — the convention lives
  in the host project's `.claude/rules/reference-convention.md` (auto-loaded
  when present): `[@path](path)` with a project-root-relative path marks
  required context; bare backtick paths are informational only
