---
name: init-docs
description: Initializes the standard docs/ directory structure for a new project. Creates docs/en/{specifications,issue,policy}/, docs/ko/{specifications,issue,policy}/, and docs/reference/, seeds initial policy documents in both English and Korean, and places a CLAUDE.md in the project root. Use this when starting a fresh project that should follow the standard documentation system.
---

# init-docs

Sets up the standard project documentation structure from scratch.

## When to Use

- Starting a new project that needs the standard `docs/` layout
- User says "set up the project structure", "initialize docs", "프로젝트 초기화", or "docs 만들어줘"
- The project has no `docs/` directory yet

## What This Skill Creates

```
docs/
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
are created at runtime by planning skills such as `frontend-planning`, not by `init-docs`.

## Step-by-Step Instructions

### Step 1: Confirm Before Acting

Tell the user:

> I'm about to set up the standard `docs/` structure in this project. This will
> create the docs/ directory tree, three initial policy documents (English +
> Korean), and a CLAUDE.md. Shall I proceed?

Wait for confirmation before creating anything.

### Step 2: Create Directory Structure

Run the setup script if available:

```bash
bash .skills/init-docs/scripts/create-structure.sh
```

Or fall back to the global install:

```bash
bash ~/.agents/skills/init-docs/scripts/create-structure.sh
```

If neither is available, create directories manually and add `.gitkeep` files
so Git tracks the empty directories:

```bash
mkdir -p docs/en/specifications docs/en/issue docs/en/policy
mkdir -p docs/ko/specifications docs/ko/issue docs/ko/policy
mkdir -p docs/reference
touch docs/en/specifications/.gitkeep docs/en/issue/.gitkeep docs/en/policy/.gitkeep
touch docs/ko/specifications/.gitkeep docs/ko/issue/.gitkeep docs/ko/policy/.gitkeep
touch docs/reference/.gitkeep
```

### Step 3: Place CLAUDE.md

Copy the content from the skill's template (see `references/CLAUDE-template.md`
or the `templates/CLAUDE.md` in the source repository) into the project root.

- If `CLAUDE.md` **does not exist**: create it with the template content.
- If `CLAUDE.md` **already exists**: do NOT overwrite it. Show the user the
  template and offer to merge relevant sections.

### Step 4: Create Initial Policy Files

Create the following English policy files in `docs/en/policy/`:

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

- Every task begins with an issue document in `docs/en/issue/`
- Issue files are numbered sequentially: issue001.md, issue002.md, ...
- Do not begin implementation before an issue document exists
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
  `Refs: issue003`
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
  - Example: `feat/issue003-user-authentication`
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

### Step 5: Create Korean Policy Mirrors

Translate the four policy files into Korean and place them in `docs/ko/policy/`:

- `docs/ko/policy/policy.md`
- `docs/ko/policy/commit-message-rule.md`
- `docs/ko/policy/naming-conventions.md`
- `docs/ko/policy/reference-convention.md`

Translation rules:
- All prose and headings → Korean
- Code blocks (``` ... ```) → keep as-is (English)
- File paths, type names, branch examples → keep in English
- Technical acronyms (API, URL, HTTP) → keep in English

### Step 6: Offer First Issue

After completing setup, ask:

> Setup complete. Would you like me to create the first issue document
> (`docs/en/issue/issue001.md`) to track the initial project setup tasks?

### Step 7: Report

List every file and directory created so the user can verify.
