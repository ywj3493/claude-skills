# Document Reference Convention

## Purpose

Establishes a consistent way to mark documents that must be read or loaded
as prerequisite context, distinguishing them from paths mentioned as
examples or illustrations.

## Syntax

Use a markdown link with an `@` prefix to indicate **required context**:

```markdown
[@docs/en/policy/policy.md](docs/en/policy/policy.md)
```

A bare backtick path without `@` is informational or illustrative only:

```markdown
`docs/en/issue/issue003.md`
```

## Rules

1. An `@`-reference means "this file MUST be loaded before proceeding."
2. Use `@`-references in issue documents and skill/plugin definitions where
   prerequisite files exist.
3. `@`-references use project-root-relative paths (no leading slash).
4. Do not `@`-reference files in `docs/reference/` — those are user-managed
   and should be cited with standard backtick paths only.
5. When an `@`-referenced file itself contains `@`-references, load them
   recursively (up to 2 levels deep).
6. The markdown link format `[@path](path)` ensures clickable navigation
   in GitHub and IDEs.

## For AI Agents

Policy rules no longer need this scan-and-load procedure — every file in
`.claude/rules/` loads automatically every session. The `@`-reference
convention now primarily governs **issue documents** and **skill/plugin
definitions**: before starting work on one, scan it for `@`-references,
load all referenced files, then scan those for further `@`-references and
load those as well (up to 2 levels).

Extract all references programmatically:

```bash
grep -rn '\[@docs/' docs/
```

## For Humans

`@`-references indicate files you should read before working on the
current document's scope. They are the "required reading" list. In
GitHub and most IDEs, they render as clickable links for easy navigation.

## Format Examples

**In a list (common in issue documents):**

```markdown
- [@docs/en/specifications/architecture.md](docs/en/specifications/architecture.md) — Architecture structure
```

**Inline (common in issue documents):**

```markdown
This issue implements the requirements in
[@docs/en/specifications/auth.md](docs/en/specifications/auth.md).
```

**Meta-references (discussing the convention itself):**

When discussing the `@`-reference convention, use backticks:
`` `[@docs/en/policy/policy.md](docs/en/policy/policy.md)` ``

## Revision History

- 2026-02-19: Initial version
- 2026-03-11: Update all example paths to docs/en/ structure
- 2026-07-10: Relocated from `docs/en/policy/reference-convention.md` to
  `.claude/rules/reference-convention.md`; narrowed scope to issue
  documents and skill/plugin definitions now that policy rules auto-load
  instead of relying on `@`-scanning
