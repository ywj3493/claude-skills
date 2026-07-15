<!--
NAV NOTE: the prev-link below points at the last design document in
canonical order (infra-spec.md by default). At generation time, replace it
with the last design/*.md file actually generated for this domain — never
link the ../design/ folder or a design file that was not generated. Apply
the same substitution to the All Documents index at the bottom. This is
the last document in the pipeline, so it has no next-link.
-->
> [← Infra Spec](../design/infra-spec.md)

# Test Specification

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
| T-006 | User Flows §2.1 | Exception Path | E2E | <!-- Test description --> | P1 | - |

<!--
The T-006 row applies only when design/user-flows.md was generated for
this domain: derive one E2E test candidate from each Exception Path (and
notable Alternative Path) entry there. Drop the row otherwise.
-->


**Priority Legend**:

- **P0**: Must pass before merge — covers core happy paths and critical error cases
- **P1**: Should pass — covers alternative flows and edge cases
- **P2**: Nice to have — covers optimization and minor edge cases

<!--
dev-reverse-docs mode: when describing existing test coverage rather than
defining tests to be written, add a "Source" column citing where each test
actually lives, e.g. [REF: tests/unit/order_test.py:12], and mark rows with
no corresponding test file as Status "Missing" rather than "-".
-->

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

## Sources Read

<!--
Populated by dev-reverse-docs only — omitted entirely for forward planning
(dev-planning). List every test file/line-range actually opened when
describing existing coverage; every Source-column citation above must
trace back to a file listed here.
-->

---

## Related Documents

### Supporting References

- [Specification](../planning/spec.md) — Requirements, user stories, and multi-actor flows

---

## Document Information

| Field | Value |
|-------|-------|
| **Created** | YYYY-MM-DD |
| **Last Modified** | YYYY-MM-DD |
| **Status** | Draft |
| **Tech Stack** | (auto-detected) |
| **Reference Documents** | <!-- list @-references from document discovery --> |

**Version History**:

- 1.0.0 (YYYY-MM-DD): Initial test specification document

---
> **All Documents**
> <!-- Keep only the design/*.md entries actually generated for this domain; current document in bold, not linked -->
> [Specification](../planning/spec.md) |
> [User Flows](../design/user-flows.md) |
> [Sequence Diagrams](../design/sequence-diagram.md) |
> [API Spec](../design/api-spec.md) |
> [Data Model](../design/data-model.md) |
> [Component Diagram](../design/component-diagram.md) |
> [Domain State Machine](../design/domain-state-machine.md) |
> [Client Store](../design/client-store.md) |
> [Infra Spec](../design/infra-spec.md) |
> **Test Spec**
