# Project Policy

## Documentation

- All documentation lives in `docs/` and is the source of truth
- Source-language documents live in `docs/en/`
- Translation mirrors (if configured in `docs/config.yml`) live in
  `docs/<lang>/` with the same filename
- `docs/reference/` is user-managed only — never create or edit files there

## Workflow

- Every task begins with an issue — either a GitHub Issue (when a git remote
  exists) or a document in `docs/en/issue/` (when no remote is configured)
- GitHub Issues are numbered automatically by GitHub
- Local issue files (fallback) are numbered sequentially: issue001.md, issue002.md, ...
- Do not begin implementation before an issue exists (GitHub Issue or local document)
- Update documentation in the same commit as the code change

## Policy Updates

- Changes to the rule files in `.claude/rules/` must be discussed with the
  user first

See also: `commit-message-rule.md`, `naming-conventions.md`,
`reference-convention.md` — in this same directory, loaded automatically
alongside this file.
