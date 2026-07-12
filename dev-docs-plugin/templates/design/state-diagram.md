<!--
NAV NOTE: design/ is a dynamic set. At generation time, replace the
prev-link below with the previous document actually generated for this
domain (or ../planning/use-case.md if this is the first design document),
and apply the same substitution to the Related Documents and All Documents
blocks at the bottom. Never link a design/*.md file that was not generated
for this domain.
-->
> [← Sequence Diagrams](sequence-diagram.md) | [Test Spec →](../verification/test-spec.md)

# State Diagram

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft
> **Tech Stack**: (auto-detected)
> **Reference Documents**: <!-- list @-references from document discovery -->

> **Generation note**: this file is only produced when the codebase has
> explicit state management — either a state machine worth diagramming
> (e.g. an order/workflow status field with transitions) or a
> client-side store (Redux/Vuex/Pinia/Zustand/etc.). Use whichever of the
> two sections below applies; both may apply.

---

## Table of Contents

1. [Overview](#overview)
2. [State Machine](#state-machine)
3. [Store Strategy](#store-strategy)
4. [Store Definitions](#store-definitions)

---

## Overview

<!-- One paragraph: what is stateful here — a domain entity's lifecycle, a
client-side store, or both — and why it's significant enough to diagram -->

---

## State Machine

<!-- Use when a domain entity/workflow has explicit states and transitions
(e.g. Order: pending -> paid -> shipped -> delivered). Omit this section
entirely if the codebase has no such state machine. -->

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Paid: payment confirmed
    Paid --> Shipped: fulfillment starts
    Shipped --> Delivered: delivery confirmed
    Pending --> Cancelled: user cancels
    Paid --> Cancelled: refund issued
    Delivered --> [*]
    Cancelled --> [*]
```

### Transition Table

| From | To | Trigger | Guard/Condition |
|------|----|---------|------------------|
| <!-- Pending --> | <!-- Paid --> | <!-- payment webhook --> | <!-- amount matches --> |

---

## Store Strategy

<!-- Use when the codebase has a client-side state management layer.
Omit this section entirely if there is none. -->

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
(dev-planning). List every file/line-range actually opened; the states,
transitions, and store shapes above must trace back to a file listed here,
or be tagged [ASSUMED: ...] if inferred rather than confirmed.
-->

---

## Related Documents

- **Previous**: [← Sequence Diagrams](sequence-diagram.md)
- **Next**: [Test Spec →](../verification/test-spec.md)
- **Component Diagram**: [Component Diagram](component-diagram.md)
- **Requirements**: [Requirements Analysis](../planning/requirements.md)
- **Use Case**: [Use Case](../planning/use-case.md)

---

**Version History**:

- 1.0.0 (YYYY-MM-DD): Initial state diagram document

---
> **All Documents**
> <!-- list only the design/*.md files generated for this domain; current file in bold -->
> [Requirements](../planning/requirements.md) |
> [User Stories](../planning/user-stories.md) |
> [Use Case](../planning/use-case.md) |
> [Sequence Diagrams](sequence-diagram.md) |
> **State Diagram** |
> [Test Spec](../verification/test-spec.md)
