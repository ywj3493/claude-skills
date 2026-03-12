# State & API Integration

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft / Review / Final
> **Tech Stack**: (auto-detected)
> **Prerequisites**: `<domain>/requirements/requirements.md` through `<domain>/workflows/component-tree.md`

## 1. State Management Strategy

### 1.1 Rationale

| Category | Decision |
|----------|----------|
| State Management Library | (e.g., Zustand / Redux Toolkit / Pinia) |
| Server State Management | (e.g., TanStack Query / SWR) |
| Global vs Local Criteria | (e.g., shared across 2+ pages → global) |

### 1.2 State Classification

| Category | Description | Management | Examples |
|----------|-------------|------------|----------|
| Server State | Data fetched from APIs | TanStack Query | User list, posts |
| Client State | UI state | Zustand / useState | Modal open, sidebar toggle |
| Auth State | Authentication info | Zustand (persist) | Token, user profile |
| Form State | Form input state | React Hook Form | Input values, validation errors |

## 2. Store Definitions

### 2.1 Auth Store

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

interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}
```

### 2.2 (Next Store Name)

```typescript
interface SomeState {
  // define state
}

interface SomeActions {
  // define actions
}
```

---

## 3. API Endpoints

### 3.1 Endpoint List

| # | Method | Path | Description | Auth | Related UC |
|---|--------|------|-------------|------|------------|
| 1 | POST | `/auth/login` | Login | Not required | UC-002 |
| 2 | POST | `/auth/signup` | Sign up | Not required | UC-001 |
| 3 | GET | `/users/me` | Get current user info | Required | UC-003 |
| 4 | | | | | |

### 3.2 Request / Response DTOs

#### POST `/auth/login`

```typescript
// Request
interface LoginRequest {
  email: string;
  password: string;
}

// Response (200 OK)
interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
}

// Error Response (401)
interface AuthErrorResponse {
  code: 'INVALID_CREDENTIALS' | 'ACCOUNT_LOCKED';
  message: string;
}
```

#### (Next Endpoint)

```typescript
// Request
interface SomeRequest {
  // define fields
}

// Response
interface SomeResponse {
  // define fields
}
```

---

## 4. Caching Strategy

| Data | staleTime | gcTime | Revalidation Trigger |
|------|-----------|--------|---------------------|
| User profile | 5 min | 30 min | On page focus |
| List data | 1 min | 10 min | On page navigation |
| Static data | 1 hour | 24 hours | Manual invalidation |

## 5. Error Handling Patterns

| HTTP Status | Handling |
|-------------|----------|
| 401 Unauthorized | Attempt token refresh → on failure, redirect to login page |
| 403 Forbidden | Display "Permission denied" toast |
| 404 Not Found | Navigate to 404 error page |
| 422 Validation | Display per-field error messages |
| 500 Server Error | Display "Server error occurred" toast + retry button |
| Network Error | Display "Please check your network connection" toast |

## 6. API Client Configuration

```typescript
// Base configuration
interface ApiClientConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

// Interceptors
// - Request: Automatically attach token to Authorization header
// - Response: Token refresh logic on 401
// - Error: Call common error handler
```
