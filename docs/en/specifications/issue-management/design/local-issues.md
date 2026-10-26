# Local issue management and optional Orca integration

## Background and decision record

Source: [GitHub issue #60](https://github.com/ywj3493/claude-skills/issues/60).
On 2026-10-26 the user changed the original proposal: local issue management belongs
in `explainable`, with an independent, optional Orca adapter in the same plugin.
The GitHub issue's original requirement to reuse the other plugin's reference at
runtime is superseded by this decision. Its epic/leaf principles are adapted into
an independently distributed contract. No change to `orca-with-gh-issue` is needed.

Implementation contracts live in `explainable-plugin/references/issue-rules.md`
and `explainable-plugin/references/issue-orca-rules.md`.

## Responsibility boundaries

| Component | Owns | Dependencies |
|---|---|---|
| `explainable:issue-local` | Issue files, hierarchy, dependencies, sizing, lifecycle, epic tables and configured mirrors | Python 3; git optional |
| `explainable:issue-orca-worktree` | Workspace creation, parent linkage, display name, optional requested agent | Issue read contract, git, installed/running Orca |
| `local-issues.py` | Read-only validation, candidate numbering, explicit shared source registration | Python standard library; git only for register/locate |

The adapter never changes an issue's lifecycle. Issue management never calls gh
or Orca. No cross-plugin file reference is required. Existing planning and design
skills do not automatically create issues or launch agents.

## File and state decisions

Files use `docs/<source>/issue/issueNNN.md`, with JSON-valued YAML frontmatter.
The authoritative fields are id, type, status, parent, blocked_by and size.
Statuses are Open, In Progress, Done and Cancelled. Blocked is derived separately
from nonterminal prerequisites. A child owns its parent relation; the epic table
is a projection, rewritten only inside its markers.

Completion requires acceptance criteria and recorded evidence, or an explicit
user completion decision recorded as evidence. A branch, PR or merge is optional.
Cancelled dependencies release blocking but do not prove acceptance criteria.
An epic cannot finish with active children or unresolved relationship errors.

Existing issues without frontmatter reserve numbers and remain unchanged until
an explicit migration. New local IDs are distinct from GitHub issue numbers.
Translation mirrors follow configured languages and are maintained by issue-local.
No automatic commits, pushes, merges or configuration scaffolding are performed.

## Shared source and concurrency

Git worktrees register one absolute source directory in the git common directory.
The registry is local machine metadata, not a tracked document. Every operation
reads and writes that source, including when it belongs to another checkout.
Without git, an explicit issue directory is sufficient.

A missing source or a conflicting registration is an error. Moving/removing the
source checkout requires explicit relocation of the source and registry.
Number candidates include legacy filenames and extend beyond 999. Candidates
are not reservations: writes acquire an exclusive directory lock, reread inputs,
and create new files exclusively. Conflicting inputs stop without overwriting.
Multi-file writes can partially succeed; report those files and resume from disk.

## Orca contract

Workspace identity is the combination of repository, execution host, issue ID
and resolved source directory. The source and ID are recorded in the comment.
Legacy provider reference flags and file URLs are not used. Branch-only matches
are candidates requiring confirmation because GitHub IDs can overlap.

The workspace parent follows the issue parent; its git base is the verified
repository default branch, including a local branch when no remote exists.
A missing parent requires a decision before creating anything. Existing
workspaces are reused without launching another agent. Agents default to none.
Failed creation/launch is not retried automatically; inspect for partial success.

## Validation

```bash
python3 -m unittest discover -s explainable-plugin/tests -v
python3 explainable-plugin/scripts/local-issues.py check --root docs/en/issue
```

Tests cover a remote-free epic with two leaves, dependency release, premature
epic completion, legacy preservation, cross-parent dependencies, missing and
cyclic relationships, sizing, metadata, numbering beyond 999, shared stores across
real git worktrees and command exit codes. A PATH trap verifies that file-only
commands invoke neither git, gh nor Orca.

Live Orca workspace creation and model-driven skill execution are separate
integration checks; Python tests do not establish either behavior.

## Prompt authoring review

The user-requested `prompt-triwizard` skill was used as an authoring reference:
create mode, Korean, agentic tool use, independent semantic XML containers.
The repository's SKILL.md packaging is preserved. The reference is an authoring
aid, not an installation dependency. Outcomes and write scopes come first;
operation-specific rules are loaded progressively. Every stop names a missing
decision or observable failure. Local reversible work continues within the
request, and workspace creation never implicitly starts an issue.

The repository prompt checklist was reviewed: retry caps and after-cap actions;
consistent statuses; caller/reader inputs; values fixed before writes; explicit
common-rule exceptions; field/filter agreement; legacy and missing-data handling;
no invented acceptance criteria; named decision gates; qualified section
references; and documented defaults with missing-value behavior. No independent
model evaluation or rubric scores are claimed.

## Document information

| Field | Value |
|---|---|
| Updated | 2026-10-26 |
| Related issue | #60 |
| Status | Implemented; live Orca execution not covered by automated tests |
