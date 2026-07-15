<!--
NAV NOTE: design/ is a dynamic set. The canonical order of the full
pipeline is: requirements → user-stories → use-case → [user-flows →
sequence-diagram → api-spec → data-model → component-diagram →
state-diagram → infra-spec] → test-spec. At generation time, re-chain the
prev/next links below through only the design documents actually generated
for this domain, keeping that order: the first generated design document's
prev is ../planning/use-case.md, and the last generated design document's
next is ../verification/test-spec.md. Apply the same substitution to the
All Documents index at the bottom. Always link document to document —
never a folder — and never link a design/*.md file that was not generated
for this domain.
-->
> [← Use Case](../planning/use-case.md) | [Sequence Diagrams →](sequence-diagram.md)

# User Flows

> **Generation note**: this file is only produced when the feature has
> multi-step user-facing journeys (screen-to-screen navigation, wizards,
> checkout-style funnels). It shows HOW the UI moves the actor through the
> feature — the actor-level WHAT stays in `../planning/use-case.md`, and
> component structure lives in `component-diagram.md`. The **Exception
> Path** entries below feed the E2E scenarios in
> `../verification/test-spec.md`.

---

## Table of Contents

1. [Flow Overview](#flow-overview)
2. [Flow Details](#flow-details)
3. [Flow Relationships](#flow-relationships)

---

## 1. Flow Overview

<!-- List all user flows covered in this document -->

| # | Flow | Related Requirement | Related Use Case | Primary Actor |
|---|------|---------------------|------------------|---------------|
| 1 | e.g., Sign Up Flow | FR-AUTH-01 | UC-AUTH-01 | End User |
| 2 | e.g., Dashboard View Flow | FR-DASH-01 | UC-DASH-01 | Admin |

---

## 2. Flow Details

### 2.1 (Flow Name)

**Entry Condition**: (e.g., User navigates to the login page)
**Exit Condition**: (e.g., User is redirected to the main page)

#### Happy Path

```mermaid
flowchart TD
    A[Start: Navigate to login page] --> B[Enter email/password]
    B --> C{Validation}
    C -->|Pass| D[API: POST /auth/login]
    D --> E{Auth Result}
    E -->|Success| F[Store token & redirect to main page]
    E -->|Failure| G[Display error message]
    C -->|Fail| H[Show field validation errors]
    G --> B
    H --> B
```

#### Alternative Path

- (e.g., User selects social login)

#### Exception Path

<!-- Each entry here becomes an E2E test candidate in test-spec.md -->

- (e.g., Network error occurs)
- (e.g., Server is under maintenance)

---

### 2.2 (Next Flow Name)

<!-- Repeat the same structure as above -->

**Entry Condition**:
**Exit Condition**:

#### Happy Path

```mermaid
flowchart TD
    A[Start] --> B[...]
```

#### Alternative Path

#### Exception Path

---

## 3. Flow Relationships

<!-- Document relationships between flows if they connect to each other -->

```mermaid
flowchart LR
    F1[Sign Up] --> F2[Login]
    F2 --> F3[Dashboard]
    F3 --> F4[Detail View]
```

---

## Sources Read

<!--
Populated by dev-reverse-docs only — omitted entirely for forward planning
(dev-planning). List every route/page/navigation file/line-range actually
opened; the flows above must trace back to a file listed here.
-->

---

## Related Documents

### Supporting References

- [Requirements Analysis](../planning/requirements.md) — Functional and non-functional requirements
- [User Stories](../planning/user-stories.md) — Stories and acceptance criteria
- [Test Specification](../verification/test-spec.md) — E2E scenarios derived from the exception paths above

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

- 1.0.0 (YYYY-MM-DD): Initial user flows document

---
> **All Documents**
> <!-- Keep only the design/*.md entries actually generated for this domain; current document in bold, not linked -->
> [Requirements](../planning/requirements.md) |
> [User Stories](../planning/user-stories.md) |
> [Use Case](../planning/use-case.md) |
> **User Flows** |
> [Sequence Diagrams](sequence-diagram.md) |
> [API Spec](api-spec.md) |
> [Data Model](data-model.md) |
> [Component Diagram](component-diagram.md) |
> [State Diagram](state-diagram.md) |
> [Infra Spec](infra-spec.md) |
> [Test Spec](../verification/test-spec.md)
