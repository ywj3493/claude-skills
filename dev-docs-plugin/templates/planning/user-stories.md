> [← Requirements](requirements.md) | [Use Case →](use-case.md)

# User Stories

> **Classification note**: this document is a **planning/WHAT** document —
> stories and acceptance criteria are written in stakeholder language.
> Implementation technology belongs in the `../design/` documents.

---

## Table of Contents

1. [Overview](#overview)
2. [User Stories](#user-stories)
3. [Story-Requirement Traceability](#story-requirement-traceability)

---

## Overview

This document captures user stories for the system. Each story follows the format:

> **As a** [role], **I want to** [capability], **So that** [benefit].

Acceptance criteria use **Given/When/Then** format. Each acceptance criterion has an **AC-USNN-NN** ID for traceability to the test specification.

User stories trace back to functional requirements in [requirements.md](requirements.md).

---

## User Stories

### US-01: <Story Name>

#### Story

**As a** <!-- Role (e.g., End User, Admin) -->
**I want to** <!-- Capability -->
**So that** <!-- Benefit -->

#### Acceptance Criteria

**Normal Cases:**

- [ ] **AC-US01-01**: **Given** <!-- precondition -->, **When** <!-- action -->, **Then** <!-- expected result -->
- [ ] **AC-US01-02**: **Given** <!-- precondition -->, **When** <!-- action -->, **Then** <!-- expected result -->
- [ ] **AC-US01-03**: **Given** <!-- precondition -->, **Then** <!-- expected state -->

**Error Cases:**

- [ ] **AC-US01-04**: **Given** <!-- error precondition -->, **When** <!-- action -->, **Then** <!-- error handling -->
- [ ] **AC-US01-05**: **Given** <!-- error precondition -->, **When** <!-- action -->, **Then** <!-- error handling -->

#### Non-Functional Requirements

<!-- Measurable targets in user-observable terms (e.g., "results appear
within 2 seconds") — not implementation choices. -->

| Item | Requirement | Target |
|------|-------------|--------|
| **Security** | <!-- Security concern --> | <!-- Target --> |
| **Performance** | <!-- Performance concern --> | <!-- Target --> |

**Related**: FR-<AREA>-01, FR-<AREA>-02, UC-<AREA>-01

---

### US-02: <Story Name>

#### Story

**As a** <!-- Role -->
**I want to** <!-- Capability -->
**So that** <!-- Benefit -->

#### Acceptance Criteria

**Normal Cases:**

- [ ] **AC-US02-01**: **Given** <!-- precondition -->, **When** <!-- action -->, **Then** <!-- expected result -->
- [ ] **AC-US02-02**: **Given** <!-- precondition -->, **When** <!-- action -->, **Then** <!-- expected result -->

**Error Cases:**

- [ ] **AC-US02-03**: **Given** <!-- error precondition -->, **When** <!-- action -->, **Then** <!-- error handling -->

#### Non-Functional Requirements

| Item | Requirement | Target |
|------|-------------|--------|
| **Performance** | <!-- Performance concern --> | <!-- Target --> |

**Related**: FR-<AREA>-NN, UC-<AREA>-NN

---

<!-- Repeat ### US-NN: <Story Name> for each user story -->

---

## Story-Requirement Traceability

| User Story | AC Count | Requirements | Use Cases |
|------------|----------|--------------|-----------|
| **US-01** (Name) | AC-US01-01..05 | FR-<AREA>-01, FR-<AREA>-02, NFR-SEC-01 | UC-<AREA>-01 |
| **US-02** (Name) | AC-US02-01..03 | FR-<AREA>-03 | UC-<AREA>-02 |

---

## Sources Read

<!--
Populated by dev-reverse-docs only — omitted entirely for forward planning
(dev-planning). List every file/line-range actually opened while inferring
these stories from code, and note at the top of this document that the
stories are inferred, not confirmed intent, when this section is present.
[REF] citations are provenance markers, not design content — they are
allowed even though this is a non-technical planning document.
-->

---

## Related Documents

### Supporting References

- [Architecture](../../architecture.md) — Architecture structure and layer rules

---

## Document Information

| Field | Value |
|-------|-------|
| **Created** | YYYY-MM-DD |
| **Last Modified** | YYYY-MM-DD |
| **Status** | Draft |
| **Reference Documents** | <!-- list @-references from document discovery --> |

**Version History**:

- 1.0.0 (YYYY-MM-DD): Initial user stories document

---
> **All Documents**
> <!-- Keep only the design/*.md entries actually generated for this domain; current document in bold, not linked -->
> [Requirements](requirements.md) |
> **User Stories** |
> [Use Case](use-case.md) |
> [User Flows](../design/user-flows.md) |
> [Sequence Diagrams](../design/sequence-diagram.md) |
> [API Spec](../design/api-spec.md) |
> [Data Model](../design/data-model.md) |
> [Component Diagram](../design/component-diagram.md) |
> [Domain State Machine](../design/domain-state-machine.md) |
> [Client Store](../design/client-store.md) |
> [Infra Spec](../design/infra-spec.md) |
> [Test Spec](../verification/test-spec.md)
