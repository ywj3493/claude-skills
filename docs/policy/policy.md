# Project Policy

## Documentation

- All documentation lives in `docs/` and is the source of truth
- All `docs/` content (except `docs/dev/`) is written in English
- `docs/dev/` contains Korean translations with `.ko.md` suffix
- `docs/reference/` is user-managed only — never create or edit files there

## Workflow

- Every task begins with an issue document in `docs/issue/`
- Issue files are numbered sequentially: issue001.md, issue002.md, ...
- Do not begin implementation before an issue document exists
- Update documentation in the same commit as the code change

## Policy Updates

- Changes to policy files must be discussed with the user first
- Policy changes require updating both the English and Korean versions

## Related Policy Files

- [@docs/policy/commit-message-rule.md](docs/policy/commit-message-rule.md) — Commit message format
- [@docs/policy/naming-conventions.md](docs/policy/naming-conventions.md) — Naming conventions for files, code, and branches
- [@docs/policy/reference-convention.md](docs/policy/reference-convention.md) — Document linking convention
