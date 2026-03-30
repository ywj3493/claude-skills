> [← Domain Spec](./)

# Test Specification

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft
> **Tech Stack**: (auto-detected)
> **Reference Documents**: <!-- list @-references from document discovery -->

---

## Table of Contents

1. [Overview](#overview)
2. [Test Matrix](#test-matrix)
3. [Mocking Boundaries](#mocking-boundaries)
4. [Test File Structure](#test-file-structure)
5. [Test-Requirement Traceability](#test-requirement-traceability)
6. [Agent Guidelines](#agent-guidelines)

---

## 1. Overview

This document is the single source of truth for all test definitions. It references
IDs from earlier specification documents (FR-XXX, AC-XXX, UC-XXX) to derive test
cases. Test type classification, mocking strategy, and priority assignment are
defined here — not in the planning/design documents.

### Test Type Definitions

| Type | Description | Scope |
|------|-------------|-------|
| **E2E** | End-to-end tests verifying complete user flows | User action -> final result |
| **Integration** | Tests verifying component interactions | Multiple modules together |
| **Unit** | Tests verifying isolated logic | Single function/class |
| **Contract** | Tests verifying API contracts | Request/response schema |

---

## 2. Test Matrix

| Test ID | Source | Reference | Type | Description | Priority | Status |
|---------|--------|-----------|------|-------------|----------|--------|
| T-001 | US-01 | AC-US01-01 | E2E | <!-- Test description --> | P0 | - |
| T-002 | US-01 | AC-US01-02 | E2E | <!-- Test description --> | P0 | - |
| T-003 | UC-<AREA>-01 | Main Flow | Integration | <!-- Test description --> | P0 | - |
| T-004 | UC-<AREA>-01 | Alt Flow A1 | Unit | <!-- Test description --> | P1 | - |
| T-005 | UC-<AREA>-01 | Alt Flow A2 | Unit | <!-- Test description --> | P1 | - |

**Priority Legend**:

- **P0**: Must pass before merge — covers core happy paths and critical error cases
- **P1**: Should pass — covers alternative flows and edge cases
- **P2**: Nice to have — covers optimization and minor edge cases

---

## 3. Mocking Boundaries

Define where test doubles are inserted when running tests at each level.

### Unit Test Boundaries

| Test Target | Mock Target | Mock Strategy |
|-------------|-------------|---------------|
| <!-- e.g., AuthService --> | <!-- e.g., UserRepository --> | Interface stub |
| <!-- e.g., LoginUseCase --> | <!-- e.g., AuthService, TokenService --> | Dependency injection |
| <!-- e.g., LoginController --> | <!-- e.g., LoginUseCase --> | Mock return values |

### Integration Test Boundaries

| Test Scope | Real | Mocked | Notes |
|------------|------|--------|-------|
| <!-- e.g., Auth flow --> | <!-- e.g., Controller, UseCase, Repository --> | <!-- e.g., External API --> | <!-- e.g., Use test DB --> |

### E2E Test Boundaries

| Test Scope | Real | Mocked | Notes |
|------------|------|--------|-------|
| <!-- e.g., Full login flow --> | <!-- e.g., All layers --> | <!-- e.g., Third-party OAuth --> | <!-- e.g., Use staging env --> |

---

## 4. Test File Structure

```text
tests/
├── e2e/
│   └── <area>/
│       └── <flow>.spec.ts        # T-001, T-002
├── integration/
│   └── <area>/
│       └── <flow>.integration.ts # T-003
└── unit/
    └── <area>/
        ├── <service>.spec.ts     # T-004
        └── <module>.spec.ts      # T-005
```

---

## 5. Test-Requirement Traceability

| Requirement | User Story | Use Case | Test IDs | Coverage |
|------------|------------|----------|----------|----------|
| FR-<AREA>-01 | US-01 | UC-<AREA>-01 | T-001, T-002, T-003 | Full |
| FR-<AREA>-02 | US-02 | UC-<AREA>-02 | T-004, T-005 | Partial |

**Coverage Legend**:

- **Full**: All acceptance criteria and main/alternative flows covered
- **Partial**: Main flow covered, some alternative flows pending
- **None**: No test coverage yet

---

## 6. Agent Guidelines

When writing test code based on this specification:

- Each `describe`/`test` block name must include the Test ID (e.g., `// T-001`)
- Tests derived from acceptance criteria (AC-XXX) must reference the AC ID in a comment
- If adding tests not in the matrix, add a comment explaining the rationale and source
- Do not duplicate test logic across test types — each Test ID maps to exactly one test
- Refer to the mocking boundaries table to determine what to mock at each test level

---

## Related Documents

- **Previous**: [← Domain Spec](./)
- **Requirements**: [Requirements Analysis](../requirements/requirements.md)
- **User Stories**: [User Stories](../requirements/user-stories.md)
- **Use Cases**: [Use Cases](use-cases.md)
- **Sequence Diagrams**: [Sequence Diagrams](sequence-diagram.md)

---

**Version History**:

- 1.0.0 (YYYY-MM-DD): Initial test specification document

---
> **All Documents**
> [Requirements](../requirements/requirements.md) |
> [User Stories](../requirements/user-stories.md) |
> [Use Cases](use-cases.md) |
> [Sequence Diagrams](sequence-diagram.md) |
> [Domain Spec](./) |
> **Test Spec**
