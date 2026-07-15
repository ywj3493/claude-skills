<!--
NAV NOTE: design/ is a dynamic set. The canonical order of the full
pipeline is: spec → [user-flows → sequence-diagram → api-spec →
data-model → component-diagram → domain-state-machine → client-store →
infra-spec] → test-spec. At generation time, re-chain the prev/next
links below through only the design documents actually generated for
this domain, keeping that order: the first generated design document's
prev is ../planning/spec.md, and the last generated design document's
next is ../verification/test-spec.md. Apply the same substitution to
the All Documents index at the bottom. Always link document to document
— never a folder — and never link a design/*.md file that was not
generated for this domain.
-->
> [← Sequence Diagrams](sequence-diagram.md) | [Data Model →](data-model.md)

# API Specification

> **Generation note**: this file is only produced when the codebase exposes
> REST/GraphQL endpoints. Request/response entity shapes belong in
> `data-model.md`, not duplicated here — link to it instead.
>
> **Domain**: Backend-only

---

## Table of Contents

1. [Overview](#overview)
2. [Endpoint Catalog](#endpoint-catalog)
3. [API Endpoints](#api-endpoints)
4. [Authentication](#authentication)
5. [Error Responses](#error-responses)

---

## Overview

### API Basic Information

| Item | Value |
|------|-------|
| **Base URL** | `http://localhost:<port>` (development), `https://api.example.com` (production) |
| **Protocol** | HTTP/1.1, HTTPS |
| **Data Format** | JSON (Content-Type: application/json) |
| **Authentication Method** | <!-- e.g., Bearer Token, Cookie, API Key --> |
| **CORS** | <!-- CORS policy --> |
| **Documentation** | <!-- e.g., Swagger UI (`/docs`), ReDoc (`/redoc`) --> |

### Authentication Mechanism

<!-- Describe the authentication method used by the API -->

**Related Requirements**: <!-- e.g., NFR-SEC-01, NFR-SEC-03 -->

---

## Endpoint Catalog

### Complete Endpoint List

| HTTP Method | Path | Auth Required | Summary | Related Use Case | Implementation |
|-------------|------|--------------|---------|------------------|----------------|
| POST | `/api/<resource>` | No | <!-- Summary --> | [UC-<AREA>-01](../planning/spec.md#uc-area-01) | <!-- file.py --> |
| GET | `/api/<resource>` | Yes | <!-- Summary --> | [UC-<AREA>-02](../planning/spec.md#uc-area-02) | <!-- file.py --> |
| GET | `/health` | No | Health check | - | <!-- file.py --> |

---

## API Endpoints

### METHOD /api/<path>

**Use Case**: [UC-<AREA>-01 (Name)](../planning/spec.md#uc-area-01-name)

**Description**: <!-- What this endpoint does -->

#### Request

**HTTP Method**: `METHOD`
**Path**: `/api/<path>`

**Headers**:

```text
Content-Type: application/json
```

**Body Schema** (JSON):

```json
{
  "field1": "string (required)",
  "field2": "number (optional)"
}
```

| Field | Type | Required | Description | Validation Rules |
|-------|------|----------|-------------|------------------|
| `field1` | string | Yes | <!-- Description --> | <!-- Rules --> |
| `field2` | number | No | <!-- Description --> | <!-- Rules --> |

**Entity Reference**: <!-- link the request/response body to its model in [data-model.md](data-model.md#modelname) when one is generated -->

#### Response

**Success (200 OK)**:

**Headers**:

```text
Content-Type: application/json
```

**Body Schema** (JSON):

```json
{
  "id": "string",
  "field1": "string",
  "created_at": "string (ISO 8601)"
}
```

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `id` | string | Unique identifier | `"abc123"` |
| `field1` | string | <!-- Description --> | `"value"` |
| `created_at` | string | Creation timestamp (ISO 8601) | `"2025-12-10T12:00:00Z"` |

#### Error Responses

**400 Bad Request** - Invalid input:

```json
{
  "detail": "Invalid input"
}
```

**401 Unauthorized** - Authentication required:

```json
{
  "detail": "Not authenticated"
}
```

**500 Internal Server Error** - Server failure:

```json
{
  "detail": "Internal server error"
}
```

#### Examples

**curl**:

```bash
curl -X METHOD http://localhost:<port>/api/<path> \
  -H "Content-Type: application/json" \
  -d '{"field1": "value"}' \
  -v
```

**JavaScript (Fetch)**:

```javascript
const response = await fetch('http://localhost:<port>/api/<path>', {
  method: 'METHOD',
  headers: { 'Content-Type': 'application/json' },
  credentials: 'include',
  body: JSON.stringify({ field1: 'value' })
});

if (response.ok) {
  const data = await response.json();
  console.log('Success:', data);
}
```

#### Sequence Diagram

See [Flow Name Sequence Diagram](sequence-diagram.md#flow-name)

---

<!-- Repeat ### METHOD /api/<path> for each endpoint -->

---

## Authentication

### Authentication Flow

<!-- Describe the authentication flow if applicable -->

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database

    C->>S: Authentication request
    S->>DB: Validate credentials
    DB-->>S: Validation result
    S-->>C: Authentication response
```

---

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message"
}
```

### HTTP Status Codes

| Code | Name | Meaning | Occurrence Scenario | Client Handling |
|------|------|---------|---------------------|-----------------|
| **200** | OK | Request successful | Normal response | Use data |
| **201** | Created | Resource created | Successful creation | Confirm and use |
| **400** | Bad Request | Invalid request | Malformed input, validation failure | Display error message |
| **401** | Unauthorized | Authentication failure | Missing or invalid credentials | Redirect to login |
| **403** | Forbidden | Access denied | Insufficient permissions | Display access denied |
| **404** | Not Found | Resource not found | Non-existent resource or endpoint | Display not found |
| **422** | Unprocessable Entity | Validation error | Business rule violation | Display validation errors |
| **500** | Internal Server Error | Server error | Unexpected failure | Retry or error page |

---

## Sources Read

<!--
Populated by dev-reverse-docs only — omitted entirely for forward planning
(dev-planning). List every file/line-range actually opened; every
[REF: path:line] citation above must trace back to a file listed here.
-->

---

## Related Documents

### Supporting References

- [Data Model](data-model.md) — Entity shapes referenced by request/response bodies
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

- 1.0.0 (YYYY-MM-DD): Initial API specification document

---
> **All Documents**
> <!-- Keep only the design/*.md entries actually generated for this domain; current document in bold, not linked -->
> [Specification](../planning/spec.md) |
> [User Flows](user-flows.md) |
> [Sequence Diagrams](sequence-diagram.md) |
> **API Spec** |
> [Data Model](data-model.md) |
> [Component Diagram](component-diagram.md) |
> [Domain State Machine](domain-state-machine.md) |
> [Client Store](client-store.md) |
> [Infra Spec](infra-spec.md) |
> [Test Spec](../verification/test-spec.md)
