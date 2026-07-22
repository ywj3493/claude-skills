---
name: init-docs
version: 0.4.0
description: Initializes the standard docs/ directory structure for a new project. Asks for the source (base) language of the documentation (default en), records it in docs/config.yml, creates docs/<source>/{specifications,issue}/ plus docs/reference/, asks which working-rule files to install and seeds them into the project's .claude/rules/, and places a CLAUDE.md in the project root. Translation mirrors are NOT created here — they are added later, opt-in, by the sync-translations skill. Use this when starting a fresh project that should follow the standard documentation system.
---

# init-docs

Sets up the standard project documentation structure from scratch.

## When to Use

- Starting a new project that needs the standard `docs/` layout
- User says "set up the project structure", "initialize docs", "프로젝트 초기화", or "docs 만들어줘"
- The project has no `docs/` directory yet

## Execution Requirements

These rules are part of the skill contract. They make the expected working
discipline explicit so the result does not depend on which model executes the
skill.

1. **Survey before creating.** Before Step 2, check what already exists
   (`ls docs/ CLAUDE.md .claude/rules/ 2>/dev/null`). Existing files are
   never overwritten — collect any conflicts and present them to the user
   instead of writing over them.
2. **Copy templates verbatim.** File contents come from the bundled template
   files under `references/` (CLAUDE-template.md, the specification
   templates, and the rule templates under `references/rules/`). Copy them
   exactly — do not paraphrase, summarize, or regenerate them from memory.
   The only permitted deviations are the adjustments the user explicitly
   requests in Step 4.
3. **Use the real date.** Fill every `<YYYY-MM-DD>` placeholder from
   `date +%F`, never from an assumed or remembered date.
4. **Verify the tree.** After creation, run
   `find docs .claude/rules -type f | sort` and compare the result against
   the layout in "What This Skill Creates". If anything is missing or
   unexpected, fix it before reporting — never report success on a partial
   tree.
5. **Report verified facts only.** The final report lists exactly the files
   and directories confirmed to exist on disk — nothing assumed.
6. **Source language only.** This skill creates the source-language tree and
   records `translation_languages: []` in `docs/config.yml`. It never creates
   translation mirror directories or translated documents — that is the
   opt-in job of `/dev-docs:sync-translations`, run later.

## What This Skill Creates

The **source language** (the base language documents are authored in) is
confirmed in Step 1 and recorded in `docs/config.yml`. The tree below shows
the default source language `en`; substitute the configured language code.

```
docs/
├── config.yml                   # Language configuration (source; translations added later)
├── en/
│   ├── specifications/
│   │   ├── architecture.md      # Project folder structure (empty template)
│   │   ├── config.md            # Environment variables (empty template)
│   │   └── infrastructure.md    # Infrastructure description (empty template)
│   └── issue/
└── reference/
.claude/rules/                   # Working rules selected in Step 4 (English-only, auto-loaded)
CLAUDE.md                        # Placed in project root
```

**Note:** Domain directories (e.g., `specifications/auth/`, `specifications/dashboard/`)
are created at runtime by this plugin's `dev-planning`/`dev-reverse-docs`
skills, not by `init-docs`.

**Note:** Translation mirror trees (e.g., `docs/ko/`) are not part of this
skill's output. Run `/dev-docs:sync-translations` later to opt in to
mirroring — it records the translation languages in `docs/config.yml`,
creates the mirror directories, and translates the existing documents.

## Step-by-Step Instructions

### Step 1: Confirm the Source Language and Scope Before Acting

Tell the user:

> I'm about to set up the standard `docs/` structure in this project. This will
> create the docs/ directory tree, a language configuration file, a CLAUDE.md,
> and working-rule files in `.claude/rules/` (you choose which in a later step).
>
> Language configuration (recorded in `docs/config.yml`):
> - Source language: `en` (the base language documents are authored in)
>
> Translation mirrors are not created now — run `/dev-docs:sync-translations`
> later to add a translation language (e.g. `ko`) and generate the mirrors.
>
> Use the default source language `en`, or tell me a different one.
> Shall I proceed?

Wait for confirmation before creating anything. Use the confirmed source
language in every subsequent step — the instructions below show the default
`en` as the example.

### Step 2: Create Directory Structure

Run the setup script, passing the confirmed source language:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/init-docs/scripts/create-structure.sh" en
```

The script also writes `docs/config.yml` with an empty translation list. If
the script is not available, create the structure manually — the
source-language directory tree, `.gitkeep` files so Git tracks the empty
directories, and the config file:

```bash
mkdir -p docs/en/specifications docs/en/issue
mkdir -p docs/reference
touch docs/en/specifications/.gitkeep docs/en/issue/.gitkeep
touch docs/reference/.gitkeep
cat > docs/config.yml <<'EOF'
# Documentation language configuration — read by documentation skills.
# source_language: language of authored documents (docs/<source_language>/)
# translation_languages: mirror languages kept in sync by sync-translations
source_language: en
translation_languages: []
EOF
```

### Step 3: Place CLAUDE.md

Copy the content of this skill's bundled template at
`${CLAUDE_PLUGIN_ROOT}/skills/init-docs/references/CLAUDE-template.md` into
the project root. If the configured source language differs from the default
`en`, adjust the language codes in the template's structure tree, examples,
and `@`-reference paths to match. Where the template describes the
translation mirror (`docs/ko/`), keep it conditional on `docs/config.yml` —
it becomes active once `sync-translations` adds a translation language.

- If `CLAUDE.md` **does not exist**: create it with the template content.
- If `CLAUDE.md` **already exists**: do NOT overwrite it. Show the user the
  template and offer to merge relevant sections.

### Step 4: Configure .claude/rules/

Operative working rules live in `.claude/rules/` at the project root —
Claude Code loads every file in that directory automatically at session
start, so no manual loading or `@`-referencing is needed. Rule files are
written in English regardless of the docs source language (they are Claude
Code configuration, not part of the bilingual docs product), and they are
**not** mirrored by `sync-translations`.

The bundled rule templates live in
`${CLAUDE_PLUGIN_ROOT}/skills/init-docs/references/rules/`:

| Template | Purpose |
| --- | --- |
| `policy.md` | General workflow policy: docs as source of truth, issue-driven work, `docs/reference/` read-only |
| `commit-message-rule.md` | Commit message format, types, and issue references |
| `naming-conventions.md` | File, code, and branch naming |
| `reference-convention.md` | The `@`-reference convention for required context |

1. **Ask which rule sets to install.** Use the AskUserQuestion tool if
   available (multi-select, all four options pre-selected as the
   recommended default); otherwise ask in plain text:

   > Which working rules should I set up in `.claude/rules/`? These load
   > automatically at the start of every Claude Code session.
   >
   > 1. General workflow policy (docs-driven, issue-first)
   > 2. Commit message rules
   > 3. Naming conventions
   > 4. `@`-reference convention
   >
   > Default: all four.

2. **Ask about adjustments.** Before writing, ask whether the defaults need
   changes — for example extra commit types, different branch prefixes, or
   a different issue-numbering scheme. If the user requests adjustments,
   apply them to the affected template content; otherwise copy verbatim
   (Execution Requirement 2).

3. **Create the files.** Make the directory and copy each selected template:

   ```bash
   mkdir -p .claude/rules
   cp "${CLAUDE_PLUGIN_ROOT}/skills/init-docs/references/rules/<name>.md" .claude/rules/
   ```

   - If the configured source language differs from `en`, adjust the `docs/`
     example paths inside the copied files to the configured language code
     (the prose stays in English).
   - If the user skipped some rule sets, edit the "See also" line at the end
     of the copied `policy.md` to list only the files actually installed
     (drop the line entirely if `policy.md` is the only one).
   - If a file already exists in `.claude/rules/`, do NOT overwrite it —
     report the conflict and skip that file (Execution Requirement 1).

### Step 5: Offer First Issue

After completing setup, ask:

> Setup complete. Would you like me to create the first issue document
> (`docs/en/issue/issue001.md`) to track the initial project setup tasks?
>
> When you want a translation mirror later (e.g. Korean), run
> `/dev-docs:sync-translations` — it will record the language in
> `docs/config.yml` and generate the mirrors.

### Step 6: Report

List every file and directory created — including the rule files installed
in `.claude/rules/` — so the user can verify.
