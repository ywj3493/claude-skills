# Skill Versioning Policy

## Purpose

Defines how skills in this repository are versioned, tagged, and how
changes are recorded.

## Versioning Scheme

Skills follow [Semantic Versioning](https://semver.org/) with a v0.x.y
development phase:

- **v0.x.y** — initial development. The skill is not yet confirmed stable.
  All new skills start at `v0.0.1`.
- **v1.0.0** — promoted only when the skill is confirmed stable and working
  as intended.
- After v1.0.0:
  - **Major** — breaking changes to skill behavior, output format, or
    required input
  - **Minor** — new features, templates, or non-breaking enhancements
  - **Patch** — bug fixes, typo corrections, minor wording changes

## SKILL.md Version Field

Every SKILL.md must include a `version` field in its YAML frontmatter:

```yaml
---
name: my-skill
version: 0.0.1
description: What this skill does
---
```

## Git Tag Convention

Since multiple skills share one repository, tags include the skill name:

```text
<skill-name>/v<major>.<minor>.<patch>
```

Examples:
- `backend-planning/v0.0.1`
- `new-issue/v0.1.0`
- `frontend-planning/v1.0.0`

For project-wide releases, use a plain version tag:

```text
v<major>.<minor>.<patch>
```

## Changelog

A single `CHANGELOG.md` lives at the project root. Entries are ordered
**newest first**. Each entry follows this format:

```markdown
## [skill-name/v0.1.0] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Changed behavior description

### Fixed
- Bug fix description
```

Allowed section headers: `Added`, `Changed`, `Fixed`, `Removed`.

## When to Bump Versions

- Every skill modification must include a version bump in SKILL.md and a
  corresponding CHANGELOG.md entry.
- Tag the commit after merging to main.

## Related Documents

- [@docs/en/policy/policy.md](docs/en/policy/policy.md) — General working rules
- [@docs/en/policy/commit-message-rule.md](docs/en/policy/commit-message-rule.md) — Commit message format
