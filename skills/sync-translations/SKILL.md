---
name: sync-translations
version: 0.2.0
description: Audits the source-language documentation directories (per docs/config.yml, default docs/en/) for documents that are missing a translation in a configured translation language (default docs/ko/), or where a translation appears out of date compared to its source, then creates or updates those translations. Use this to keep translation mirrors in sync. Triggered by "sync docs", "번역 동기화", "update translations", "sync translations", or "mirror docs".
---

# sync-translations

Keeps translation mirror directories synchronized with the source-language
documents, using the language pair(s) configured in `docs/config.yml`.
The examples below show the default `en` → `ko` pairing.

## When to Use

- User says "sync docs", "update translations", "sync translations", "번역 동기화", "mirror docs"
- After a batch of documentation updates where translations may be missing
- Periodically to audit translation completeness across the project

## Directories in Scope

For each configured translation language (shown here for `ko`):

| Source (`docs/<source>/`) | Translation (`docs/<target>/`) |
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
   the actual `find` output and cover every source file in every configured
   translation language — no sampling, no "representative subset". Report
   exact counts.
2. **Timestamps are a heuristic.** Git commit-date comparison produces false
   positives (e.g., a formatting-only commit touching the English file).
   Before rewriting an existing translation flagged as stale, compare the
   actual content and skip it if the translation already reflects the source
   — and say so in the report.
3. **Translate from disk, fully.** Read the entire source document immediately
   before translating. Never translate from memory, from a summary, or from
   an earlier conversation excerpt. Long files are translated completely —
   never truncated with "..." or "(remainder unchanged)".
4. **Verify structural parity.** After writing each translation, check it
   against the source: same number of headings, code blocks, table rows, and
   checkbox items, in the same order. Fix any mismatch before moving to the
   next file.
5. **Write only under translation directories.** Source-language documents and
   `docs/reference/` are read-only for this skill — never "fix" a source file
   while translating, even if it contains an error; report the error instead.
6. **Report per file.** The final report lists every file created, updated,
   or skipped, with the reason for each skip. Never report a file as synced
   without having written and verified it.

## Step-by-Step Instructions

### Step 0: Load Language Configuration

1. Read `docs/config.yml` for `source_language` and `translation_languages`.
2. If the file is missing, infer the configuration from the directory layout:
   language-code directories under `docs/` (excluding `reference/`). If `en/`
   is present, treat it as the source and the others as translation targets.
   State the inference in the final report and suggest recording it in
   `docs/config.yml`.
3. If `docs/` does not exist or contains no language directories, stop and
   tell the user:

   > No documentation structure found. Run `/init-docs` to set it up first.

4. If `translation_languages` is empty, report that the project has no
   translation mirrors configured and stop.

Run Steps 1–4 once per configured translation language. The commands below
show the default `en` → `ko` pairing; substitute the actual language codes.

### Step 1: Audit — Find Missing Translations

List all source files in the three directories:

```bash
find docs/en/specifications docs/en/issue docs/en/policy \
  -name "*.md" ! -name ".gitkeep" 2>/dev/null | sort
```

For each file found (e.g., `docs/en/issue/issue003.md`), check whether the
corresponding translation exists (e.g., `docs/ko/issue/issue003.md`).

Build a **Missing** list of files with no translation.

### Step 2: Audit — Find Stale Translations

For files where a translation exists, compare modification times using git:

```bash
git log --follow -1 --format="%ai" -- docs/en/issue/issue003.md
git log --follow -1 --format="%ai" -- docs/ko/issue/issue003.md
```

If the source document has a more recent commit than its translation, add it
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

1. Read the source file completely
2. Translate all prose content into the target language
3. Write the file to the corresponding translation path with the same filename

**Naming rule**: Replace `docs/<source>/` with `docs/<target>/` (same
filename), e.g. for `en` → `ko`:
- `docs/en/issue/issue003.md` → `docs/ko/issue/issue003.md`
- `docs/en/specifications/requirements.md` → `docs/ko/specifications/requirements.md`
- `docs/en/policy/commit-message-rule.md` → `docs/ko/policy/commit-message-rule.md`

### Step 5: Report Results

List every file created or updated with their paths.

## Translation Rules

**Translate to the target language:**
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

**For technical acronyms on first use**, optionally add a brief
target-language explanation in parentheses, then use the acronym alone
thereafter.

**Preserve markdown structure exactly:**
- Same heading levels (`#`, `##`, `###`)
- Same list and checkbox formatting
- Same bold/italic markers
- Same horizontal rules and table structure
