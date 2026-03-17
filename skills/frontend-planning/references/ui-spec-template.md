> [← User Flows](user-flows.md) | [Use Cases →](../workflows/use-cases.md)

# UI Specification

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft / Review / Final
> **Tech Stack**: (auto-detected)
> **Prerequisites**: [@<domain>/requirements/requirements.md](<domain>/requirements/requirements.md), [@<domain>/requirements/user-flows.md](<domain>/requirements/user-flows.md)
> **Reference Documents**: <!-- list @-references from document discovery -->

## 1. UI Overview

| # | View | URL / Trigger | Access | Related Flow |
|---|------|---------------|--------|--------------|
| 1 | e.g., Login | `/login` | Public | Login Flow |
| 2 | e.g., Dashboard | `/dashboard` | Authenticated | Dashboard View |
| 3 | | | | |

## 2. View Details

### 2.1 (View Name)

**URL / Trigger**: `/path` or (e.g., triggered by button click)
**Access**: (e.g., Authenticated / Public)
**Related Flow**: (reference to the relevant flow)

#### Layout

<!-- Describe the layout structure using ASCII art or text description -->

```text
┌─────────────────────────────────┐
│           Header / Nav          │
├─────────┬───────────────────────┤
│ Sidebar │     Main Content      │
│         │                       │
│         │  ┌─────────────────┐  │
│         │  │   Component A   │  │
│         │  └─────────────────┘  │
│         │  ┌─────────────────┐  │
│         │  │   Component B   │  │
│         │  └─────────────────┘  │
├─────────┴───────────────────────┤
│             Footer              │
└─────────────────────────────────┘
```

#### Key Components

| Component | Role | Data |
|-----------|------|------|
| e.g., LoginForm | Login form input and submission | email, password |
| e.g., SocialLoginButtons | Social login button group | provider list |

#### Responsive Behavior

| Viewport | Changes |
|----------|---------|
| Desktop (≥1024px) | Default layout |
| Tablet (768–1023px) | Sidebar hidden, hamburger menu |
| Mobile (<768px) | Single column, bottom navigation |

#### SEO (if applicable)

| Property | Value |
|----------|-------|
| `<title>` | (e.g., Login - Service Name) |
| `<meta description>` | (e.g., Log in to your account) |
| OG Image | (e.g., /og/login.png) |

---

### 2.2 (Next View Name)

<!-- Repeat the same structure as above -->

---

## 3. Shared Layout

### 3.1 Header

- Logo, navigation menu, user menu
- Display items change based on authentication state

### 3.2 Footer

- Copyright information, link collections

### 3.3 Error Views

| Status Code | View | Description |
|-------------|------|-------------|
| 404 | `/404` | Not found |
| 500 | `/500` | Server error |

---
> **All Documents**
> [Requirements](requirements.md) |
> [User Flows](user-flows.md) |
> **UI Spec** |
> [Use Cases](../workflows/use-cases.md) |
> [Component Tree](../workflows/component-tree.md) |
> [State & API](../workflows/state-api-integration.md)
