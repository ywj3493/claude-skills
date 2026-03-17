> [← Back to README](../README.md)

# Architecture

> **Created**: YYYY-MM-DD
> **Last Modified**: YYYY-MM-DD
> **Status**: Draft / Review / Final
> **Tech Stack**: (auto-detected)

## 1. Project Structure

```mermaid
graph TD
    Root[Project Root]
    Root --> Src[src/]
    Root --> Public[public/]
    Root --> Docs[docs/]
    Root --> Config[Configuration Files]

    Src --> App[app/ or pages/]
    Src --> Components[components/]
    Src --> Lib[lib/ or utils/]
    Src --> Hooks[hooks/]
    Src --> Stores[stores/ or state/]
    Src --> Types[types/]
    Src --> Styles[styles/]
    Src --> Api[api/ or services/]

    Components --> Shared[shared/]
    Components --> Features[features/]

    App --> Routes[Route Modules]
```

<!-- Replace with the actual project structure -->

## 2. Module Boundaries

```mermaid
graph LR
    UI[UI Layer<br/>components/] --> State[State Layer<br/>stores/]
    UI --> Hooks[Hook Layer<br/>hooks/]
    Hooks --> State
    Hooks --> API[API Layer<br/>api/]
    State --> API
    API --> External[External Services]
```

<!-- Define the dependency rules between modules -->

| Layer | Allowed Dependencies | Description |
|-------|---------------------|-------------|
| UI (components/) | Hooks, State, Types | Presentation and interaction |
| Hooks (hooks/) | State, API, Types | Reusable logic |
| State (stores/) | API, Types | Application state management |
| API (api/) | Types | External communication |
| Types (types/) | None | Shared type definitions |

## 3. Key Files

| File | Purpose |
|------|---------|
| `src/app/layout.tsx` | Root layout |
| `src/app/page.tsx` | Home page |
| `src/lib/api-client.ts` | API client configuration |
| `src/stores/auth.ts` | Authentication state |

## 4. References

- [@docs/en/specifications/infrastructure.md](docs/en/specifications/infrastructure.md) — Deployment and infrastructure
