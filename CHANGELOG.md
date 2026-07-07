# Changelog

All notable changes to skills in this project are documented here.
Entries are ordered newest first. Format follows [Keep a Changelog](https://keepachangelog.com/).

## [init-docs/v0.2.0] - 2026-07-07

### Added
- Configurable languages: Step 1 asks for a source language and translation languages, recorded in docs/config.yml; create-structure.sh accepts language arguments
- CLAUDE.md template bundled at references/CLAUDE-template.md so installed copies are self-contained

### Changed
- architecture and infrastructure templates upgraded to the richer format from the removed frontend-planning skill (module boundaries, key files, deployment topology, CI/CD pipeline, external services)

### Changed
- Directory, policy, and mirror creation follows the configured languages instead of hardcoded en/ko; projects may configure zero translation languages
- Planning-skill note references dev-planning instead of deprecated frontend-planning

## [new-issue/v0.3.0] - 2026-07-07

### Added
- Docs mode verifies the docs structure exists and guides to /init-docs when missing

### Changed
- Draft PR creation is optional — settled at the issue-content confirmation gate ("issue only" skips it)
- Docs-mode mirrors follow the translation languages in docs/config.yml instead of hardcoded Korean

## [dev-planning/v0.3.0] - 2026-07-07

### Added
- Review mode choice at Step 0: step-by-step (default) or continuous generation with one consolidated review at the end
- Optional Step 3.5 (frontend only): user-flows document restored from the removed frontend-planning skill as references/frontend/user-flows-template.md; exception/alternative paths feed E2E scenarios in the test spec

### Changed
- Output paths documented as source-language-relative (docs/config.yml) instead of hardcoded docs/en

## [new-policy/v0.2.0] - 2026-07-07

### Added
- Docs-structure precondition check with guidance to /init-docs when missing

### Changed
- Translation mirrors follow the configured translation languages; source-only projects skip mirrors

## [sync-translations/v0.2.0] - 2026-07-07

### Added
- Step 0 loads docs/config.yml (with directory-layout inference fallback) and stops with guidance when no docs structure exists

### Changed
- Generalized from hardcoded en → ko to the configured source and translation languages

## [backend-planning] - 2026-07-07

### Removed
- Skill removed from the repository (deprecated since v0.0.2; superseded by dev-planning)

## [frontend-planning] - 2026-07-07

### Removed
- Skill removed from the repository (deprecated since v0.0.2; superseded by dev-planning)

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
