# Prompt Authoring Rules

## Purpose

Rules for writing the prompts in this repository: SKILL.md files, agent
definitions, plugin `references/` documents, and templates whose comments
instruct a model. A model follows these documents literally. A sentence a
human would read charitably can stall a run, loop forever, or invent content
when a model reads it.

These rules come from the explainable plugin prompt review (#47, PR #48).
The problems it found were not one-off bad sentences. They were writing
patterns that kept coming back. Each rule below names the pattern, says
what to do instead, and gives a check you can run against a draft.

## Rules

### 1. Every loop has a cap and an after-cap action

Do not write "repeat until it passes" or "fix and re-run until clean".
State the maximum number of rounds and what happens when the cap is hit:
report what is left, then wait for the user to decide.

Also say what the model must not do to get out of the loop. For example:
do not delete a failing test, weaken an assertion, or mask a correct
claim as assumed just to make the loop end.

- Check: search the draft for `until`, `again`, `re-run`, `retry`, `반복`,
  `다시`, `까지`. Each hit has a number and an after-cap action.

### 2. One term, one meaning

When a word labels a state or category (`unresolved`, `미정`, `미해결`,
`not applicable`), give it one meaning across every file in the plugin. If
two things need names, use two words and define both where they first
appear.

- Check: for each status word the draft introduces, grep the plugin for it.
  Every existing use has the same meaning.

### 3. Caller and callee contracts match

When a skill invokes an agent or another skill, every input the caller
passes is in the callee's input table, with the same name and shape. Every
input the callee requires is passed by every caller. The same goes for
outputs the caller reads.

- Check: for each invocation in the draft, open the callee and compare the
  input list line by line.

### 4. Values are fixed before anything uses them

A step must not write to a path, name, or ID that a later step decides.
For example, writing to `<domain>/...` before domains are identified breaks
this rule. Reorder the steps, or have the earlier step write to a neutral
location and the later step move it.

The same applies to decisions. If step N needs a decision that step M > N
makes, step N must not guess it. Say that step M adds it later.

- Check: for each output path and each value a step reads, find the step
  that fixes it. That step comes first.

### 5. Exceptions live next to the rule they break

If rule A has an exception, write the exception inside rule A, or have
rule A point to it. Never let an exception exist only in the step that
uses it. "Never edit planning documents" in one file and "update the
planning document in step 6" in another is a direct contradiction. A
literal reader will obey one and break the other at random.

This applies especially to ownership lists ("this skill writes only X, Y").
Every document any step of that skill writes must be on the list, together
with its scope.

- Check: for every "only", "never", "do not", `만`, `않는다`, `금지` in the
  draft, search the same skill/agent for steps that do the forbidden thing.
  Each one is named as an exception at the rule.

### 6. Output schema and filtering rules agree

If a rule says "drop items without evidence", every field the rule covers
must have an evidence slot. Exempt the fields that cannot carry evidence
(ledgers, `not_found`, `unresolved`) by name. If a field is required, the
schema must not let it be omitted.

- Check: for each filter rule, list the schema fields it applies to and
  confirm each has the slot the rule tests for.

### 7. Absence is handled one way

Empty sections follow the plugin's one shared rule. In the explainable
plugin that is `common-rules.md` §5: a section that does not apply is
deleted with its TOC entry, and a section that was checked but has no
evidence stays with `없음 — 확인한 경로: ...`. A document must not invent
its own variant.

When a value can be unknown, give it an explicit token (for example `미정`)
instead of an empty cell. Then say which later step consumes that token and
what it does with it.

Say explicitly what a missing section or column means when an older
document predates it. For example: "missing column = `미정`" or "missing
section = none".

- Check: every "if absent / if empty / 없으면" in the draft resolves to the
  shared rule or to a named token with a named consumer.

### 8. Do not force a guess

Never write a rule that can only be satisfied by inventing content:
"must not be empty", "fill every row", "always pick one". When the input
may not contain the answer, give the model an honest outcome:

- record the gap (`미정`, `[ASSUMED: ...; basis: ...]`, `없음 — 확인한 경로`)
- ask the user, giving a recommended option and a one-line reason
- stop

Defaults are allowed only when they are written down as defaults, with the
source of the default.

- Check: for each "must", "always", `반드시`, `비어 있으면 안 된다` in the
  draft, ask whether the input could lack the information. If it could, an
  honest outcome is named.

### 9. Review gates are explicit

A step-by-step run stops only where the document says it stops. Mark each
gate with the plugin's gate form (for explainable:
`> **단계 N 완료**: ... 진행할까요?`). If a question must be asked even in
continuous mode, say so at the question.

- Check: list the gates in the draft. Every step that needs user input
  before it can continue has one, or says that it waits.

### 10. Numbered references are unambiguous

Steps (`단계 3.2`), contract items (`계약 2`), skill-specific items
(`고유 항목 5`), and reference-document sections (`구현 규약 §4.8`) are
different numbering systems. Always qualify a number with its system. Do
not write a bare `§3` or `3번` when more than one system is in scope.

When you renumber a section, grep for every reference to it in the plugin
and fix them in the same change. Prefer appending a new subsection over
renumbering existing ones.

- Check: grep the plugin for each section or step number the draft changes
  or adds.

### 11. Design decisions come from documents, not from the implementer

When a downstream skill (implementation, reverse extraction) reaches a
choice that belongs to an upstream document, read the choice from that
document. If the document lacks it, ask the user and record the answer in
that document, within an explicitly listed scope. Do not pick a "sensible"
option silently.

- Check: for each branch in a rule ("if optimistic ... if pessimistic"),
  confirm which document field selects the branch and what happens when
  the field is missing.

## Self-Review Checklist

Run this against every new or changed prompt before committing. Note any
"no" in the PR description, with the reason it is acceptable.

| # | Check | Rule |
|---|---|---|
| 1 | Every loop has a numeric cap, an after-cap action, and a forbidden-shortcut list | 1 |
| 2 | Every status word means the same thing everywhere in the plugin | 2 |
| 3 | Inputs and outputs match between every caller and callee | 3 |
| 4 | No step reads or writes a value that a later step fixes | 4 |
| 5 | Every exception is stated at the rule it breaks; ownership lists are complete | 5 |
| 6 | Filter rules and output schemas agree; exempt fields are named | 6 |
| 7 | Absence uses the shared rule or a named token with a named consumer | 7 |
| 8 | No rule can be satisfied only by inventing content | 8 |
| 9 | Every stop point is a marked gate | 9 |
| 10 | Every number reference names its numbering system; renumbered references are updated | 10 |
| 11 | Every branch on a design choice names the field that selects it and the missing-field behavior | 11 |

See also: `policy.md`, `skill-versioning.md` — both in this same
directory, loaded automatically alongside this file.
