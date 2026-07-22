# Document Reference Convention

## Purpose

Establishes a consistent way to mark documents that must be read or loaded
as prerequisite context, distinguishing them from paths mentioned as
examples or illustrations.

## Syntax

Use a markdown link with an `@` prefix to indicate **required context**:

    [@docs/en/specifications/architecture.md](docs/en/specifications/architecture.md)

A bare backtick path without `@` is informational or illustrative only:

    `docs/en/issue/issue003.md`

## Rules

1. An `@`-reference means "this file MUST be loaded before proceeding."
2. Use `@`-references in issue documents and specification documents where
   prerequisite files exist. Files in `.claude/rules/` load automatically
   every session and never need `@`-referencing.
3. `@`-references use project-root-relative paths (no leading slash).
4. Do not `@`-reference files in `docs/reference/` — those are user-managed
   and should be cited with standard backtick paths only.
5. When an `@`-referenced file itself contains `@`-references, load them
   recursively (up to 2 levels deep).
6. The markdown link format `[@path](path)` ensures clickable navigation
   in GitHub and IDEs.

## Revision History

- <YYYY-MM-DD>: Initial version
