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
