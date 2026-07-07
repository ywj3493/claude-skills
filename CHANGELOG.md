# Changelog

All notable changes to skills in this project are documented here.
Entries are ordered newest first. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [dev-planning/v0.2.0] - 2026-07-07

### Added
- Execution Requirements section: mandatory template loading, disk-based input re-reading, sequential ID assignment, pre-completion traceability validation, link/diagram verification, literal review gates, verified-path reporting

## [new-issue/v0.2.0] - 2026-07-07

### Added
- Execution Requirements section: output-based mode detection, no invented identifiers, overwrite protection for local issue numbers, explicit failure recovery, pre-report artifact verification, structural parity between issue/PR/mirror

## [init-docs/v0.1.0] - 2026-07-07

### Added
- Execution Requirements section: pre-creation survey with overwrite protection, verbatim template copying, real-date placeholders, post-creation tree verification, translation parity, verified-facts-only reporting

## [new-policy/v0.1.0] - 2026-07-07

### Added
- Execution Requirements section: kebab-case filename validation with collision check, real-date revision history, paired-language creation in one run, explicit policy.md gate, pre-report verification

## [sync-translations/v0.1.0] - 2026-07-07

### Added
- Execution Requirements section: exhaustive audit coverage, content-level stale confirmation over timestamp heuristics, full-source translation from disk, structural parity verification, docs/ko-only write scope, per-file reporting

## [new-issue/v0.1.0] - 2026-03-31

### Added
- GitHub Issues mode via `gh issue create` when git remote exists
- Automatic branch creation for new issues
- Draft PR creation linked to the issue (`Resolves #N`)
- Automatic mode detection (`git remote -v` + `gh auth status`)
- GitHub-native issue references (`Refs: #N`, `Closes #N`)

### Changed
- Local docs-based issue creation is now fallback for repos without a remote
- Korean mirror step skipped in GitHub mode
## [dev-planning/v0.1.0] - 2026-03-30

### Added
- Unified planning pipeline: requirements -> user stories -> use cases -> sequence diagrams -> domain spec -> test spec
- Domain type branching: backend (api-spec), frontend (component-spec), infra (infra-spec placeholder)
- ID-based test traceability (FR-XXX, AC-XXX, UC-XXX) with dedicated test-spec document
- Common templates shared across all domain types
- Document navigation (prev/next and all-documents index) on every template

## [backend-planning/v0.0.2] - 2026-03-30

### Deprecated
- Superseded by dev-planning. Use dev-planning instead.

## [frontend-planning/v0.0.2] - 2026-03-30

### Deprecated
- Superseded by dev-planning. Use dev-planning instead.

## [backend-planning/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- 5-step backend planning pipeline (requirements → user stories → API spec → use cases → sequence diagrams)

## [frontend-planning/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- 6-step frontend planning pipeline (requirements → user flows → UI spec → use cases → component tree → state/API integration)

## [new-issue/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Issue document creation with Korean translation

## [new-policy/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Policy document creation with Korean translation

## [sync-translations/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Audit and sync Korean translations for docs/en/

## [init-docs/v0.0.1] - 2026-03-19

### Added
- Initial versioned release
- Standard docs/ directory structure initialization
