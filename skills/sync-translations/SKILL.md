---
name: sync-translations
version: 0.1.0
description: Audits docs/en/specifications/, docs/en/issue/, and docs/en/policy/ for English documents that are missing a Korean translation in docs/ko/, or where the Korean version appears out of date compared to the English source, then creates or updates those translations. Use this to keep docs/ko/ in sync. Triggered by "sync docs", "번역 동기화", "update translations", "sync translations", or "mirror docs".
---

# sync-translations

Keeps the `docs/ko/` Korean translations synchronized with the English source documents in `docs/en/`.

## When to Use

- User says "sync docs", "update translations", "sync translations", "번역 동기화", "mirror docs"
- After a batch of documentation updates where Korean translations may be missing
- Periodically to audit translation completeness across the project

## Directories in Scope

| English source | Korean translation |
|---|---|
| `docs/en/specifications/` | `docs/ko/specifications/` |
| `docs/en/issue/` | `docs/ko/issue/` |
| `docs/en/policy/` | `docs/ko/policy/` |

`docs/reference/` is **excluded** — user-managed, language-neutral, no translations needed.

## Execution Requirements

These rules are part of the skill contract. They make the expected working
discipline explicit so translation quality does not depend on which model
executes the skill.

1. **Audit exhaustively.** The Missing and Stale lists must be derived from
   the actual `find` output and cover every English file — no sampling, no
   "representative subset". Report exact counts.
2. **Timestamps are a heuristic.** Git commit-date comparison produces false
   positives (e.g., a formatting-only commit touching the English file).
   Before rewriting an existing translation flagged as stale, compare the
   actual content and skip it if the Korean version already reflects the
   English source — and say so in the report.
3. **Translate from disk, fully.** Read the entire English source immediately
   before translating. Never translate from memory, from a summary, or from
   an earlier conversation excerpt. Long files are translated completely —
   never truncated with "..." or "(remainder unchanged)".
4. **Verify structural parity.** After writing each translation, check it
   against the source: same number of headings, code blocks, table rows, and
   checkbox items, in the same order. Fix any mismatch before moving to the
   next file.
5. **Write only under `docs/ko/`.** English sources and `docs/reference/` are
   read-only for this skill — never "fix" an English file while translating,
   even if it contains an error; report the error instead.
6. **Report per file.** The final report lists every file created, updated,
   or skipped, with the reason for each skip. Never report a file as synced
   without having written and verified it.

## Step-by-Step Instructions

### Step 1: Audit — Find Missing Translations

List all English source files in the three directories:

```bash
find docs/en/specifications docs/en/issue docs/en/policy \
  -name "*.md" ! -name ".gitkeep" 2>/dev/null | sort
```

For each file found (e.g., `docs/en/issue/issue003.md`), check whether the
corresponding translation exists (e.g., `docs/ko/issue/issue003.md`).

Build a **Missing** list of files with no Korean translation.

### Step 2: Audit — Find Stale Translations

For files where a Korean translation exists, compare modification times using git:

```bash
git log --follow -1 --format="%ai" -- docs/en/issue/issue003.md
git log --follow -1 --format="%ai" -- docs/ko/issue/issue003.md
```

If the English source has a more recent commit than the Korean translation, add it
to a **Stale** list.

### Step 3: Report and Confirm

Tell the user:

> Sync audit complete:
>
> **Missing translations** (<N> files):
> - docs/en/issue/issue004.md
> - docs/en/specifications/architecture.md
>
> **Potentially stale** (<N> files):
> - docs/en/policy/policy.md (English updated 2025-11-01, Korean updated 2025-10-15)
>
> Shall I create/update all of them?

Wait for confirmation before writing any files.

### Step 4: Create or Update Translations

For each file in the Missing or Stale lists:

1. Read the English source file completely
2. Translate all prose content into Korean
3. Write the file to the corresponding `docs/ko/` path with the same filename

**Naming rule**: Replace `docs/en/` with `docs/ko/` (same filename):
- `docs/en/issue/issue003.md` → `docs/ko/issue/issue003.md`
- `docs/en/specifications/requirements.md` → `docs/ko/specifications/requirements.md`
- `docs/en/policy/commit-message-rule.md` → `docs/ko/policy/commit-message-rule.md`

### Step 5: Report Results

List every file created or updated with their paths.

## Translation Rules

**Translate to Korean:**
- All prose paragraphs and sentences
- Section headings
- List item descriptions
- Table cell text

**Keep in English:**
- Code blocks (``` ... ```) — never translate the content inside
- File paths (`docs/en/issue/issue001.md`)
- Function names, variable names, class names
- Branch names and command-line examples
- Technical acronyms: API, URL, HTTP, JSON, Git, etc.
- Checkbox markers: `- [ ]`, `- [x]`

**For technical acronyms on first use**, optionally add a brief Korean
explanation in parentheses, then use the acronym alone thereafter.

**Preserve markdown structure exactly:**
- Same heading levels (`#`, `##`, `###`)
- Same list and checkbox formatting
- Same bold/italic markers
- Same horizontal rules and table structure
