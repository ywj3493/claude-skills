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

- This rule applies to ad-hoc documents created under `docs/*/policy/` (e.g.
  via the `new-policy` skill) for downstream-style, project-specific rules —
  not to the files in this `.claude/rules/` directory itself, which are
  English-only Claude Code configuration, not part of the bilingual docs
  product.
- Changes to `docs/*/policy/` documents must be discussed with the user first
- Such changes require updating both the English and Korean versions

See also: `commit-message-rule.md`, `naming-conventions.md`,
`reference-convention.md`, `skill-versioning.md` — all in this same
directory, loaded automatically alongside this file.
