---
name: init-docs
version: 0.2.2
description: Initializes the standard docs/ directory structure for a new project. Asks for a source language and optional translation languages (default en -> ko), records them in docs/config.yml, creates docs/<lang>/{specifications,issue,policy}/ per language plus docs/reference/, seeds initial policy documents in every configured language, and places a CLAUDE.md in the project root. Use this when starting a fresh project that should follow the standard documentation system.
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
   (`ls docs/ CLAUDE.md 2>/dev/null`). Existing files are never overwritten —
   collect any conflicts and present them to the user instead of writing over
   them.
2. **Copy templates verbatim.** Policy file contents come from the blocks
   embedded in this SKILL.md (or the referenced template files). Copy them
   exactly — do not paraphrase, summarize, or regenerate them from memory.
3. **Use the real date.** Fill every `<YYYY-MM-DD>` placeholder from
   `date +%F`, never from an assumed or remembered date.
4. **Verify the tree.** After creation, run `find docs -type f | sort` and
   compare the result against the layout in "What This Skill Creates". If
   anything is missing or unexpected, fix it before reporting — never report
   success on a partial tree.
5. **Translation parity.** Each Korean policy file must have the same heading
   structure and the same code blocks as its English source (code blocks stay
   in English).
6. **Report verified facts only.** The final report lists exactly the files
   and directories confirmed to exist on disk — nothing assumed.
7. **Honor the language configuration.** Every directory, policy file, and
   translation mirror follows the languages confirmed in Step 1 and recorded
   in `docs/config.yml` — never assume English/Korean beyond the defaults the
   user accepted.

## What This Skill Creates

Languages are configurable: one **source language** plus zero or more
**translation languages**, recorded in `docs/config.yml`. The tree below shows
the default `en` → `ko` pairing; substitute the configured language codes.

```
docs/
├── config.yml                   # Language configuration (source + translations)
├── en/
│   ├── specifications/
│   │   ├── architecture.md      # Project folder structure (empty template)
│   │   ├── config.md            # Environment variables (empty template)
│   │   └── infrastructure.md    # Infrastructure description (empty template)
│   ├── issue/
│   └── policy/
│       ├── policy.md
│       ├── commit-message-rule.md
│       ├── naming-conventions.md
│       └── reference-convention.md
├── ko/
│   ├── specifications/
│   │   ├── architecture.md
│   │   ├── config.md
│   │   └── infrastructure.md
│   ├── issue/
│   └── policy/
│       ├── policy.md
│       ├── commit-message-rule.md
│       ├── naming-conventions.md
│       └── reference-convention.md
└── reference/
CLAUDE.md  (placed in project root)
```

**Note:** Domain directories (e.g., `specifications/auth/`, `specifications/dashboard/`)
are created at runtime by planning skills such as the `dev-docs` plugin's
`dev-planning`/`dev-reverse-docs` skills, not by `init-docs`.

## Step-by-Step Instructions

### Step 1: Confirm Languages and Scope Before Acting

Tell the user:

> I'm about to set up the standard `docs/` structure in this project. This will
> create the docs/ directory tree, a language configuration file, four initial
> policy documents (in every configured language), and a CLAUDE.md.
>
> Language configuration (recorded in `docs/config.yml`):
> - Source language: `en` (documents are authored in this language)
> - Translation languages: `ko` (mirror translations; may be empty)
>
> Use these defaults, or tell me a different source/translation setup.
> Shall I proceed?

Wait for confirmation before creating anything. Use the confirmed languages in
every subsequent step — the instructions below show the default `en` → `ko`
pairing as the example.

### Step 2: Create Directory Structure

Run the setup script if available, passing the confirmed languages
(source first, then translation languages):

```bash
bash dev-docs-plugin/skills/init-docs/scripts/create-structure.sh en ko
```

The script also writes `docs/config.yml`. If the script is not available,
create the structure manually — one directory tree per configured language,
`.gitkeep` files so Git tracks the empty directories, and the config file:

```bash
mkdir -p docs/en/specifications docs/en/issue docs/en/policy
mkdir -p docs/ko/specifications docs/ko/issue docs/ko/policy
mkdir -p docs/reference
touch docs/en/specifications/.gitkeep docs/en/issue/.gitkeep docs/en/policy/.gitkeep
touch docs/ko/specifications/.gitkeep docs/ko/issue/.gitkeep docs/ko/policy/.gitkeep
touch docs/reference/.gitkeep
cat > docs/config.yml <<'EOF'
# Documentation language configuration — read by documentation skills.
source_language: en
translation_languages:
  - ko
EOF
```

For a project with no translation languages, omit the mirror directories and
write `translation_languages: []`.

### Step 3: Place CLAUDE.md

Copy the content of this skill's `references/CLAUDE-template.md` into the
project root. If the configured languages differ from the default `en` → `ko`,
adjust the language codes in the template's structure tree, examples, and
`@`-reference paths to match.

- If `CLAUDE.md` **does not exist**: create it with the template content.
- If `CLAUDE.md` **already exists**: do NOT overwrite it. Show the user the
  template and offer to merge relevant sections.

### Step 4: Create Initial Policy Files

Create the following policy files in the source-language policy directory
(`docs/<source>/policy/` — shown here as `docs/en/policy/`). Copy the blocks
verbatim; only adjust language names, language codes, and paths where the
configured languages differ from the default `en` → `ko`:

---

**docs/en/policy/policy.md**

```markdown
# Project Policy

## Documentation

- All documentation lives in `docs/` and is the source of truth
- English documents live in `docs/en/`
- Korean translations live in `docs/ko/` with the same filename
- `docs/reference/` is user-managed only — never create or edit files there

## Workflow

- Every task begins with an issue — either a GitHub Issue (when a git remote
  exists) or a document in `docs/en/issue/` (when no remote is configured)
- GitHub Issues are numbered automatically by GitHub
- Local issue files (fallback) are numbered sequentially: issue001.md, issue002.md, ...
- Do not begin implementation before an issue exists (GitHub Issue or local document)
- Update documentation in the same commit as the code change

## Policy Updates

- Changes to policy files must be discussed with the user first
- Policy changes require updating both the English and Korean versions

## Related Policy Files

- [@docs/en/policy/commit-message-rule.md](docs/en/policy/commit-message-rule.md) — Commit message format
- [@docs/en/policy/naming-conventions.md](docs/en/policy/naming-conventions.md) — Naming conventions for files, code, and branches
- [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md) — Document linking convention
```

---

**docs/en/policy/commit-message-rule.md**

```markdown
# Commit Message Rules

## Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes only
- `style`: Formatting or whitespace (no logic change)
- `refactor`: Code restructuring (no feature or fix)
- `test`: Adding or updating tests
- `chore`: Build process, dependency updates, tooling

## Rules

- Subject line: 72 characters maximum
- Subject: imperative mood, lowercase, no trailing period
- Example: `feat(auth): add OAuth2 login flow`
- Reference the issue number in the body or footer:
  - GitHub Issues: `Refs: #42` (or `Closes #42` to auto-close)
  - Local docs issues: `Refs: issue003`
- Separate body from subject with a blank line
```

---

**docs/en/policy/naming-conventions.md**

```markdown
# Naming Conventions

## Files and Directories

- All filenames: lowercase, hyphen-separated (kebab-case)
- Issue documents: `issue001.md`, `issue002.md` (zero-padded to 3 digits)
- Translated docs use the same filename under `docs/<lang>/`
  - English: `docs/en/policy/policy.md` → Korean: `docs/ko/policy/policy.md`
- No spaces in file or directory names

## Code (language-agnostic defaults)

- Variables and functions: camelCase
- Constants: UPPER_SNAKE_CASE
- Classes and types: PascalCase
- Private members: prefix with underscore `_`

## Branch Names

- Feature: `feat/issue<NNN>-<short-description>`
  - With GitHub Issues: `feat/issue42-user-authentication` (no zero-padding)
  - With local docs issues: `feat/issue003-user-authentication` (zero-padded)
- Bug fix: `fix/issue<NNN>-<short-description>`
- Documentation: `docs/issue<NNN>-<short-description>`

## Notes

- Language-specific conventions override these defaults
- Add language-specific rules to this file as the project evolves
```

---

**docs/en/policy/reference-convention.md**

```markdown
# Document Reference Convention

## Purpose

Establishes a consistent way to mark documents that must be read or loaded
as prerequisite context, distinguishing them from paths mentioned as
examples or illustrations.

## Syntax

Use a markdown link with an `@` prefix to indicate **required context**:

    [@docs/en/policy/policy.md](docs/en/policy/policy.md)

A bare backtick path without `@` is informational or illustrative only:

    `docs/en/issue/issue003.md`

## Rules

1. An `@`-reference means "this file MUST be loaded before proceeding."
2. Use `@`-references in CLAUDE.md, policy files, issue documents, and
   skill definitions where prerequisite files exist.
3. `@`-references use project-root-relative paths (no leading slash).
4. Do not `@`-reference files in `docs/reference/`.
5. When an `@`-referenced file itself contains `@`-references, load them
   recursively (up to 2 levels deep).
6. The markdown link format `[@path](path)` ensures clickable navigation
   in GitHub and IDEs.

## Revision History

- <YYYY-MM-DD>: Initial version
```

---

### Step 5: Create Policy Translation Mirrors

**Skip this step if the project has no translation languages.**

For each configured translation language, translate the four policy files and
place them in that language's policy directory (shown here for `ko`):

- `docs/ko/policy/policy.md`
- `docs/ko/policy/commit-message-rule.md`
- `docs/ko/policy/naming-conventions.md`
- `docs/ko/policy/reference-convention.md`

Translation rules:
- All prose and headings → target language
- Code blocks (``` ... ```) → keep as-is (English)
- File paths, type names, branch examples → keep in English
- Technical acronyms (API, URL, HTTP) → keep in English

### Step 6: Offer First Issue

After completing setup, ask:

> Setup complete. Would you like me to create the first issue document
> (`docs/en/issue/issue001.md`) to track the initial project setup tasks?

### Step 7: Report

List every file and directory created so the user can verify.
