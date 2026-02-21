# Document Reference Convention

## Purpose

Establishes a consistent way to mark documents that must be read or loaded
as prerequisite context, distinguishing them from paths mentioned as
examples or illustrations.

## Syntax

Use a markdown link with an `@` prefix to indicate **required context**:

```markdown
[@docs/policy/policy.md](docs/policy/policy.md)
```

A bare backtick path without `@` is informational or illustrative only:

```markdown
`docs/issue/issue003.md`
```

## Rules

1. An `@`-reference means "this file MUST be loaded before proceeding."
2. Use `@`-references in CLAUDE.md, policy files, issue documents, and
   skill definitions where prerequisite files exist.
3. `@`-references use project-root-relative paths (no leading slash).
4. Do not `@`-reference files in `docs/reference/` — those are user-managed
   and should be cited with standard backtick paths only.
5. When an `@`-referenced file itself contains `@`-references, load them
   recursively (up to 2 levels deep).
6. The markdown link format `[@path](path)` ensures clickable navigation
   in GitHub and IDEs.

## For AI Agents

Before starting any task, scan the loaded CLAUDE.md and current issue
document for `@`-references. Load all referenced files. Then scan those
files for further `@`-references and load those as well (up to 2 levels).

Extract all references programmatically:

```bash
grep -rn '\[@docs/' CLAUDE.md docs/
```

## For Humans

`@`-references indicate files you should read before working on the
current document's scope. They are the "required reading" list. In
GitHub and most IDEs, they render as clickable links for easy navigation.

## Format Examples

**In a list (common in CLAUDE.md and policy files):**

```markdown
- [@docs/policy/policy.md](docs/policy/policy.md) — General working rules
- [@docs/policy/commit-message-rule.md](docs/policy/commit-message-rule.md) — Commit message format
```

**Inline (common in issue documents):**

```markdown
This issue implements the requirements in
[@docs/specifications/auth.md](docs/specifications/auth.md).
```

**Meta-references (discussing the convention itself):**

When discussing the `@`-reference convention, use backticks:
`` `[@docs/policy/policy.md](docs/policy/policy.md)` ``

## Revision History

- 2026-02-19: Initial version
