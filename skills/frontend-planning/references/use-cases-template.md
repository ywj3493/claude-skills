> [← UI Spec](../requirements/ui-spec.md) | [Component Tree →](component-tree.md)

# Use Cases

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft / Review / Final
> **Tech Stack**: (auto-detected)
> **Prerequisites**: [@<domain>/requirements/requirements.md](<domain>/requirements/requirements.md), [@<domain>/requirements/user-flows.md](<domain>/requirements/user-flows.md), [@<domain>/requirements/ui-spec.md](<domain>/requirements/ui-spec.md)
> **Reference Documents**: <!-- list @-references from document discovery -->

## 1. Actors

| Actor | Description | Permission Level |
|-------|-------------|------------------|
| e.g., End User | Registered user of the service | CRUD own data |
| e.g., Admin | System operator | Full data management |
| e.g., System | Automated background process | Internal operations |

## 2. Use Case List

| ID | Use Case | Primary Actor | Related Feature | Related View |
|----|----------|---------------|-----------------|--------------|
| UC-001 | e.g., Sign Up | End User | FR-001 | Sign Up |
| UC-002 | e.g., Login | End User | FR-002 | Login |
| UC-003 | | | | |

## 3. Use Case Details

### UC-001: (Use Case Name)

**Actor**: (e.g., End User)
**Related Feature**: (e.g., FR-001)
**Related View**: (e.g., Sign Up)

#### Preconditions

- (e.g., User has navigated to the sign-up page)
- (e.g., User does not have an existing account)

#### Postconditions

- (e.g., User account is created)
- (e.g., Welcome email is sent)

#### Main Flow

| # | Actor | System |
|---|-------|--------|
| 1 | Navigates to sign-up page | Displays sign-up form |
| 2 | Enters email and password | Performs real-time validation |
| 3 | Clicks "Sign Up" button | Sends POST /auth/signup request |
| 4 | | On success, redirects to login page |

#### Alternative Flow

- **A1**: Sign up with social account
  1. User clicks social login button
  2. System redirects to OAuth provider page
  3. After authentication, callback processes and creates account

#### Exception Flow

- **E1**: Email already registered
  1. System displays "This email is already registered" message
  2. Provides link to login page
- **E2**: Network error
  1. System displays "A network error occurred. Please try again." message

---

### UC-002: (Next Use Case Name)

<!-- Repeat the same structure as above -->

---

## 4. Use Case Relationships

<!-- Document include and extend relationships between use cases -->

| Relationship | Use Case A | Use Case B | Description |
|-------------|------------|------------|-------------|
| include | UC-002 Login | UC-010 Token Refresh | Token issuance included in login |
| extend | UC-001 Sign Up | UC-011 Email Verification | Extends when email verification is required |

---
> **All Documents**
> [Requirements](../requirements/requirements.md) |
> [User Flows](../requirements/user-flows.md) |
> [UI Spec](../requirements/ui-spec.md) |
> **Use Cases** |
> [Component Tree](component-tree.md) |
> [State & API](state-api-integration.md)
