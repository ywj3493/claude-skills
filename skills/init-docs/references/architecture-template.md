# Architecture

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft / Review / Final
> **Tech Stack**: (auto-detected)

## 1. Overview

<!-- High-level description of the project architecture -->

## 2. Project Structure

```mermaid
graph TD
    Root[Project Root]
    Root --> Src[src/]
    Root --> Docs[docs/]
    Root --> Config[Configuration Files]

    Src --> App[app/ or pages/]
    Src --> Components[components/]
    Src --> Lib[lib/ or utils/]
    Src --> Types[types/]
    Src --> Api[api/ or services/]
```

<!-- Replace with the actual project structure -->

## 3. Module Boundaries

```mermaid
graph LR
    UI[UI Layer] --> State[State Layer]
    UI --> Hooks[Logic Layer]
    Hooks --> State
    Hooks --> API[API Layer]
    State --> API
    API --> External[External Services]
```

<!-- Define the dependency rules between modules -->

| Layer | Allowed Dependencies | Description |
|-------|---------------------|-------------|
| UI | Logic, State, Types | Presentation and interaction |
| Logic | State, API, Types | Reusable business logic |
| State | API, Types | Application state management |
| API | Types | External communication |
| Types | None | Shared type definitions |

## 4. Key Files

| File | Purpose |
|------|---------|
| | |

## 5. References

- [@docs/en/specifications/infrastructure.md](docs/en/specifications/infrastructure.md) — Deployment and infrastructure
- [@docs/en/specifications/config.md](docs/en/specifications/config.md) — Environment variables and configuration
