<!--
NAV NOTE: design/ is a dynamic set. At generation time, replace the
prev-link below with the previous document actually generated for this
domain (or ../planning/use-case.md if this is the first design document),
and apply the same substitution to the Related Documents and All Documents
blocks at the bottom. Never link a design/*.md file that was not generated
for this domain.
-->
> [← Sequence Diagrams](sequence-diagram.md) | [Test Spec →](../verification/test-spec.md)

# API Specification

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft
> **Tech Stack**: (auto-detected)
> **Reference Documents**: <!-- list @-references from document discovery -->

> **Generation note**: this file is only produced when the codebase exposes
> REST/GraphQL endpoints. Request/response entity shapes belong in
> `data-model.md`, not duplicated here — link to it instead.

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
| POST | `/api/<resource>` | No | <!-- Summary --> | [UC-<AREA>-01](../planning/use-case.md#uc-area-01) | <!-- file.py --> |
| GET | `/api/<resource>` | Yes | <!-- Summary --> | [UC-<AREA>-02](../planning/use-case.md#uc-area-02) | <!-- file.py --> |
| GET | `/health` | No | Health check | - | <!-- file.py --> |

---

## API Endpoints

### METHOD /api/<path>

**Use Case**: [UC-<AREA>-01 (Name)](../planning/use-case.md#uc-area-01-name)

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

- **Previous**: [← Sequence Diagrams](sequence-diagram.md)
- **Next**: [Test Spec →](../verification/test-spec.md)
- **Data Models**: [Data Model](data-model.md)
- **Requirements**: [Requirements Analysis](../planning/requirements.md)
- **User Stories**: [User Stories](../planning/user-stories.md)
- **Use Case**: [Use Case](../planning/use-case.md)

---

**Version History**:

- 1.0.0 (YYYY-MM-DD): Initial API specification document

---
> **All Documents**
> <!-- list only the design/*.md files generated for this domain; current file in bold -->
> [Requirements](../planning/requirements.md) |
> [User Stories](../planning/user-stories.md) |
> [Use Case](../planning/use-case.md) |
> [Sequence Diagrams](sequence-diagram.md) |
> **API Spec** |
> [Test Spec](../verification/test-spec.md)
