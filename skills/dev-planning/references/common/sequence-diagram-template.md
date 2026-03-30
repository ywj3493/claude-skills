> [← Use Cases](use-cases.md) | [Domain Spec →](./)

# Sequence Diagrams

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft
> **Tech Stack**: (auto-detected)
> **Reference Documents**: <!-- list @-references from document discovery -->

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture Layer Structure](#architecture-layer-structure)
3. [Core Flows](#core-flows)
4. [Error Handling Flows](#error-handling-flows)
5. [Performance Optimization Points](#performance-optimization-points)

---

## Overview

This document represents all major flows as sequence diagrams, explicitly showing architecture layer interactions.

### Purpose

- **Implementation Traceability**: Code tracing possible using actual file names and methods
- **Architecture Understanding**: Visualize interactions between architecture layers
- **Debugging Support**: Understand entire request flow at a glance

### Related Documents

- [Requirements Analysis](../requirements/requirements.md) - Functional/non-functional requirements
- [Use Case Specification](use-cases.md) - Detailed use case specifications
- [User Stories](../requirements/user-stories.md) - User stories

---

## Architecture Layer Structure

### Layer Overview

<!-- Adapt the layer structure to match the project's architecture pattern -->

```text
+---------------------------------------------------------+
|                  Presentation Layer (HTTP)               |
|              controllers/ or routes/                     |
|              (Framework Controllers/Handlers)            |
+------------------------+--------------------------------+
                         | uses
                         v
+---------------------------------------------------------+
|          Application Layer (Use Cases / Services)        |
|              use_cases/ or services/                     |
|  - Use Case classes or Service methods                   |
+----------+-------------------------+--------------------+
           | uses                    | uses
           v                         v
+----------------------+   +------------------------------+
|   Domain Layer       |   |  Infrastructure Layer        |
|  entities/models/    |   |  repositories/ or adapters/  |
|  - Domain Entities   |   |  - Repository Implementations|
|  - Value Objects     |   |  - External Service Clients  |
+----------------------+   +------------------------------+
```

### Participant Notation

In sequence diagrams, each participant is displayed in the following format:

```text
[FileName]<br/>(Layer)
```

**Examples**:

- `controller.py<br/>(Presentation)` - HTTP Controller
- `CreateUseCase<br/>(Application)` - Use Case (business workflow)
- `Service<br/>(Application)` - Application Service (shared logic)
- `ExternalClient<br/>(Infrastructure)` - External Service Adapter
- `Repository<br/>(Infrastructure)` - Data Storage Adapter

---

## Core Flows

### <Flow Name> Flow

**Use Case**: [UC-<AREA>-01 (Name)](use-cases.md#uc-area-01-name)

**Description**: <!-- Brief description of the flow -->

```mermaid
sequenceDiagram
    participant F as Client
    participant C as controller.py<br/>(Presentation)
    participant UC as UseCase<br/>(Application)
    participant EXT as ExternalClient<br/>(Infrastructure)
    participant ExtSys as External System<br/>(External)
    participant R as Repository<br/>(Infrastructure)
    participant DB as Database<br/>(External)

    Note over F,DB: UC-<AREA>-01: <Flow Name>

    F->>C: METHOD /api/path<br/>{request_body}
    Note over C: handler() endpoint<br/>(controller.py)

    C->>UC: execute(params)
    Note over UC: Business logic<br/>(use_case.py)

    UC->>EXT: external_call(data)
    Note over EXT: External adapter<br/>(external_client.py)
    EXT->>ExtSys: API call
    ExtSys-->>EXT: Response data
    EXT-->>UC: Processed result

    UC->>UC: Internal processing
    Note over UC: Domain logic

    UC->>R: save(entity)
    Note over R: Storage adapter<br/>(repository.py)
    R->>DB: Data operation
    DB-->>R: OK
    R-->>UC: Save complete

    UC-->>C: result

    C-->>F: 200 OK<br/>ResponseBody
```

**Key Steps**:

1. <!-- Key step 1 -->
2. <!-- Key step 2 -->
3. <!-- Key step 3 -->

**Related Code**:

- <!-- [controller.py](path) - endpoint -->
- <!-- [use_case.py](path) - method -->
- <!-- [repository.py](path) - method -->

---

### <Another Flow Name> Flow

**Use Case**: [UC-<AREA>-02 (Name)](use-cases.md#uc-area-02-name)

**Description**: <!-- Brief description -->

```mermaid
sequenceDiagram
    participant F as Client
    participant C as controller.py<br/>(Presentation)
    participant UC as UseCase<br/>(Application)
    participant R as Repository<br/>(Infrastructure)
    participant DB as Database<br/>(External)

    Note over F,DB: UC-<AREA>-02: <Flow Name>

    F->>C: METHOD /api/path
    C->>UC: execute(params)
    UC->>R: find(id)
    R->>DB: Query
    DB-->>R: Result
    R-->>UC: entity
    UC-->>C: result
    C-->>F: 200 OK<br/>ResponseBody
```

**Key Steps**:

1. <!-- Key step 1 -->
2. <!-- Key step 2 -->

**Related Code**:

- <!-- [file](path) - method -->

---

### Conditional Flow (with alt block)

**Use Case**: <!-- UC reference -->

**Description**: <!-- Flow with conditional branching -->

```mermaid
sequenceDiagram
    participant F as Client
    participant C as controller.py<br/>(Presentation)
    participant UC as UseCase<br/>(Application)
    participant SVC as Service<br/>(Application)
    participant R as Repository<br/>(Infrastructure)
    participant DB as Database<br/>(External)
    participant EXT as ExternalClient<br/>(Infrastructure)
    participant ExtSys as External System<br/>(External)

    Note over F,ExtSys: Conditional Flow

    F->>C: METHOD /api/path
    C->>UC: execute(params)

    UC->>R: find(id)
    R->>DB: Query
    DB-->>R: Result
    R-->>UC: entity

    UC->>UC: Check condition
    Note over UC: Evaluate business rule

    alt Condition met
        Note over UC,ExtSys: Execute additional logic
        UC->>SVC: process(entity)
        SVC->>EXT: external_call(data)
        EXT->>ExtSys: API call
        ExtSys-->>EXT: Response
        EXT-->>SVC: Result

        SVC->>R: save(updated_entity)
        R->>DB: Update
        DB-->>R: OK
        R-->>SVC: Complete

        SVC-->>UC: updated_result
    else Condition not met
        Note over UC: Skip additional logic
    end

    UC-->>C: result
    C-->>F: 200 OK<br/>ResponseBody
```

**Conditional Branch (alt)**:

- **Condition met**: <!-- Description of what happens -->
- **Condition not met**: <!-- Description of what happens -->

**Related Code**:

- <!-- [file](path) - method -->

---

<!-- Repeat ### <Flow Name> Flow for each major flow -->

---

## Error Handling Flows

### <Error Scenario Name> Error Flow

**Scenario**: <!-- Brief description of the error scenario -->

```mermaid
sequenceDiagram
    participant F as Client
    participant C as controller.py<br/>(Presentation)
    participant UC as UseCase<br/>(Application)
    participant R as Repository<br/>(Infrastructure)
    participant DB as Database<br/>(External)

    Note over F,DB: Error Scenario: <Error Name>

    F->>C: METHOD /api/path
    C->>UC: execute(params)
    UC->>R: find(id)
    R->>DB: Query
    DB-->>R: nil (not found)
    R-->>UC: None

    UC->>UC: raise NotFoundError
    Note over UC: Domain exception<br/>(use_case.py)

    UC--xC: NotFoundError

    C->>C: raise HTTPException(404, "Resource not found")
    Note over C: Convert to HTTP error<br/>(controller.py)

    C--xF: 404 Not Found<br/>{detail: "Resource not found"}
    Note over F: Handle error
```

**Error Propagation Flow**:

1. **Data Layer Failure**: <!-- Database returns empty/error -->
2. **Domain Exception**: <!-- Application layer raises exception -->
3. **HTTP Exception**: <!-- Presentation layer converts to HTTP error -->
4. **Client Handling**: <!-- Client handles the error -->

---

### External Service Failure Flow

**Scenario**: <!-- External service communication failure -->

```mermaid
sequenceDiagram
    participant F as Client
    participant C as controller.py<br/>(Presentation)
    participant UC as UseCase<br/>(Application)
    participant EXT as ExternalClient<br/>(Infrastructure)
    participant ExtSys as External System<br/>(External)

    Note over F,ExtSys: Error Scenario: External Service Failure

    F->>C: METHOD /api/path<br/>{request_data}
    C->>UC: execute(params)
    UC->>EXT: external_call(data)
    EXT->>ExtSys: API call
    ExtSys--xEXT: Connection Timeout
    Note over EXT: Connection failure detected

    EXT->>EXT: raise ServiceError("Service unreachable")
    Note over EXT: Convert to domain exception

    EXT--xUC: ServiceError
    UC--xC: ServiceError

    C->>C: raise HTTPException(500, "Service unavailable")
    Note over C: Convert to HTTP 500

    C--xF: 500 Internal Server Error<br/>{detail: "Service unavailable"}
    Note over F: Display error or retry
```

**Error Propagation Flow**:

1. **Network Error**: <!-- External service timeout/error -->
2. **Domain Exception**: <!-- Infrastructure layer raises exception -->
3. **HTTP Exception**: <!-- Presentation layer converts to HTTP error -->
4. **Client Handling**: <!-- Client handles the error -->

---

## Performance Optimization Points

### <Optimization Area>

```mermaid
graph LR
    A[Controller] --> B[Use Cases]
    B --> C[Repository]
    C --> D[Connection Pool]
    D --> E1[Connection 1]
    D --> E2[Connection 2]
    D --> E3[Connection N]
    E1 --> F[Database]
    E2 --> F
    E3 --> F
```

**Optimizations**:

- <!-- Optimization 1 (e.g., Connection pooling) -->
- <!-- Optimization 2 (e.g., Timeout settings) -->

**Related Requirement**: <!-- e.g., NFR-PERF-01 -->

---

### <Another Optimization Area>

```mermaid
graph TD
    A[Request] --> B{Condition Check}
    B -->|Condition A| C[Expensive Path]
    B -->|Condition B| D[Fast Path]
    C --> E[External Call]
    C --> F[Data Update]
    D --> G[Return Cached]
```

**Optimizations**:

- <!-- Optimization 1 -->
- <!-- Optimization 2 -->

**Related Requirement**: <!-- e.g., NFR-PERF-02 -->

---

## Related Documents

- **Previous**: [← Use Cases](use-cases.md)
- **Next**: [Domain Spec →](./)
- **Requirements**: [Requirements Analysis](../requirements/requirements.md)
- **User Stories**: [User Stories](../requirements/user-stories.md)
- **Architecture**: [Architecture](../../architecture.md)

---

**Version History**:

- 1.0.0 (YYYY-MM-DD): Initial sequence diagram document

---
> **All Documents**
> [Requirements](../requirements/requirements.md) |
> [User Stories](../requirements/user-stories.md) |
> [Use Cases](use-cases.md) |
> **Sequence Diagrams** |
> [Domain Spec](./) |
> [Test Spec](test-spec.md)
