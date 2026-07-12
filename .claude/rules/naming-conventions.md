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
