<!--
NAV NOTE: design/ is a dynamic set. The canonical order of the full
pipeline is: requirements → user-stories → use-case → [user-flows →
sequence-diagram → api-spec → data-model → component-diagram →
domain-state-machine → client-store → infra-spec] → test-spec. At
generation time, re-chain the prev/next links below through only the
design documents actually generated for this domain, keeping that order:
the first generated design document's prev is ../planning/use-case.md,
and the last generated design document's next is
../verification/test-spec.md. Apply the same substitution to the All
Documents index at the bottom. Always link document to document — never
a folder — and never link a design/*.md file that was not generated for
this domain.
-->
> [← Domain State Machine](domain-state-machine.md) | [Infra Spec →](infra-spec.md)

# Client Store

> **Generation note**: this file is only produced when the codebase has a
> client-side state management layer (Redux/Vuex/Pinia/Zustand/etc.).
> Domain entity/workflow state machines are a different axis and live in
> `domain-state-machine.md`.
>
> **Domain**: Frontend-only

---

## Table of Contents

1. [Overview](#overview)
2. [Store Strategy](#store-strategy)
3. [Store Definitions](#store-definitions)

---

## Overview

<!-- One paragraph: what client-side state exists here and why it's
significant enough to document -->

---

## Store Strategy

| Category | Decision |
|----------|----------|
| State Management Library | (e.g., Zustand / Redux Toolkit / Pinia) |
| Server State Management | (e.g., TanStack Query / SWR) |
| Global vs Local Criteria | (e.g., shared across 2+ pages -> global) |

### State Classification

| Category | Description | Management | Examples |
|----------|-------------|------------|----------|
| Server State | Data fetched from APIs | TanStack Query | User list, posts |
| Client State | UI state | Zustand / useState | Modal open, sidebar toggle |
| Auth State | Authentication info | Zustand (persist) | Token, user profile |
| Form State | Form input state | React Hook Form | Input values, validation errors |

---

## Store Definitions

#### Auth Store

```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

interface AuthActions {
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}
```

#### <Next Store Name>

```typescript
interface SomeState {
  // define state
}

interface SomeActions {
  // define actions
}
```

---

## Sources Read

<!--
Populated by dev-reverse-docs only — omitted entirely for forward planning
(dev-planning). List every file/line-range actually opened; the store
shapes above must trace back to a file listed here, or be tagged
[ASSUMED: ...] if inferred rather than confirmed.
-->

---

## Related Documents

### Supporting References

- [Component Diagram](component-diagram.md) — Components that read and mutate these stores
- [Requirements Analysis](../planning/requirements.md) — Functional and non-functional requirements
- [Use Case](../planning/use-case.md) — Actor-level flows that drive the state changes

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

- 1.0.0 (YYYY-MM-DD): Initial client store document

---
> **All Documents**
> <!-- Keep only the design/*.md entries actually generated for this domain; current document in bold, not linked -->
> [Requirements](../planning/requirements.md) |
> [User Stories](../planning/user-stories.md) |
> [Use Case](../planning/use-case.md) |
> [User Flows](user-flows.md) |
> [Sequence Diagrams](sequence-diagram.md) |
> [API Spec](api-spec.md) |
> [Data Model](data-model.md) |
> [Component Diagram](component-diagram.md) |
> [Domain State Machine](domain-state-machine.md) |
> **Client Store** |
> [Infra Spec](infra-spec.md) |
> [Test Spec](../verification/test-spec.md)
