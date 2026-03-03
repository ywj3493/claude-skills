---
name: frontend-planning
description: 프론트엔드 프로젝트의 6단계 기획 문서(요구사항 → 사용자 플로우 → 화면 명세 → 유스케이스 → 컴포넌트 트리 → 상태/API 연동)를 docs/specifications/에 순차 생성한다. 각 단계마다 사용자 검토를 거치며, 기술 스택을 자동 감지하고, 한국어로 작성한다.
---

# frontend-planning

프론트엔드 프로젝트를 위한 6단계 기획 문서 파이프라인.

## When to Use

- User says "프론트엔드 기획", "frontend planning", "UI 설계", "화면 설계"
- User says "프론트엔드 문서", "기획 문서 만들어줘", "plan frontend"
- Starting a new frontend project that needs structured design documents
- Adding a major frontend feature that requires multi-page planning

## When NOT to Use

- Backend-only projects (use the backend planning pipeline instead)
- Fixing a single component or small UI tweak
- Editing or updating existing specification documents
- Non-UI work such as CI/CD, infrastructure, or tooling

## Pipeline Overview

```text
Step 0: Tech stack detection
Step 1: Requirements (요구사항 정의서)
Step 2: User Flows (사용자 플로우)
Step 3: Page Spec (화면 명세서)
Step 4: Use Cases (유스케이스)
Step 5: Component Tree (컴포넌트 트리)
Step 6: State & API Integration (상태/API 연동 명세)
Step 7: Table of Contents (목차 생성)
```

## Step-by-Step Instructions

### Step 0: Detect Tech Stack

Before generating any documents, detect the project's tech stack:

1. Read `package.json` — check for React, Vue, Next.js, Nuxt, Svelte, Angular, etc.
2. Read `tsconfig.json` — check if TypeScript is used
3. Scan directory structure — `src/`, `app/`, `pages/`, `components/`
4. Check for styling solutions — Tailwind, styled-components, CSS Modules, etc.
5. Check for state management — Redux, Zustand, Recoil, Pinia, etc.

Summarize the detected stack and confirm with the user:

> 감지된 기술 스택:
> - Framework: Next.js 14 (App Router)
> - Language: TypeScript
> - Styling: Tailwind CSS
> - State: Zustand
>
> 이 스택을 기반으로 기획 문서를 작성합니다. 맞나요?

Wait for confirmation before proceeding.

### Step 1: Requirements (요구사항 정의서)

**Output**: `docs/specifications/01-requirements.md`

1. Load the reference template: `references/01-requirements-template.md`
2. Check `docs/specifications/` for existing backend documents — reference them if present
3. Ask the user to describe:
   - Project purpose and target users
   - Core features and functionality
   - Non-functional requirements (performance, accessibility, etc.)
4. Generate the document following the template structure
5. Present the document to the user and wait for review

> Step 1/6 완료: 요구사항 정의서를 작성했습니다.
> 검토 후 수정 사항이 있으면 말씀해 주세요. 다음 단계로 진행할까요?

### Step 2: User Flows (사용자 플로우)

**Output**: `docs/specifications/02-user-flows.md`

1. Load the reference template: `references/02-user-flows-template.md`
2. Load Step 1 output: `docs/specifications/01-requirements.md`
3. For each major feature, create:
   - **Mermaid flowchart** diagram showing the happy path
   - Alternative paths and error/exception flows
   - Entry and exit conditions
4. Generate the document and wait for review

> Step 2/6 완료: 사용자 플로우를 작성했습니다.
> 검토 후 수정 사항이 있으면 말씀해 주세요. 다음 단계로 진행할까요?

### Step 3: Page Spec (화면 명세서)

**Output**: `docs/specifications/03-page-spec.md`

1. Load the reference template: `references/03-page-spec-template.md`
2. Load previous outputs: Steps 1–2
3. For each page/screen, define:
   - URL / route path
   - Layout structure and sections
   - Key components on the page
   - Responsive behavior (mobile / tablet / desktop)
   - SEO considerations (title, meta, OG tags)
4. Generate the document and wait for review

> Step 3/6 완료: 화면 명세서를 작성했습니다.
> 검토 후 수정 사항이 있으면 말씀해 주세요. 다음 단계로 진행할까요?

### Step 4: Use Cases (유스케이스)

**Output**: `docs/specifications/04-use-cases.md`

1. Load the reference template: `references/04-use-cases-template.md`
2. Load previous outputs: Steps 1–3
3. For each use case, define:
   - Actor (user role)
   - Preconditions and postconditions
   - Main flow (step-by-step actor-system interaction)
   - Alternative flows
   - Exception flows
4. Generate the document and wait for review

> Step 4/6 완료: 유스케이스를 작성했습니다.
> 검토 후 수정 사항이 있으면 말씀해 주세요. 다음 단계로 진행할까요?

### Step 5: Component Tree (컴포넌트 트리)

**Output**: `docs/specifications/05-component-tree.md`

1. Load the reference template: `references/05-component-tree-template.md`
2. Load previous outputs: Steps 1–4
3. Define the component hierarchy:
   - **Mermaid graph TD** diagram showing parent-child relationships
   - Separate sections for shared/common components and page-specific components
   - **TypeScript interface** for each component's props
4. Generate the document and wait for review

> Step 5/6 완료: 컴포넌트 트리를 작성했습니다.
> 검토 후 수정 사항이 있으면 말씀해 주세요. 다음 단계로 진행할까요?

### Step 6: State & API Integration (상태/API 연동 명세)

**Output**: `docs/specifications/06-state-api-integration.md`

1. Load the reference template: `references/06-state-api-integration-template.md`
2. Load previous outputs: Steps 1–5
3. Check `docs/specifications/` for existing backend API specs — reference endpoints if available
4. Define:
   - State management strategy and rationale
   - **TypeScript interface** for each store/slice
   - API endpoints table with method, path, description
   - **TypeScript interface** for request/response DTOs
   - Caching strategy and error handling patterns
5. Generate the document and wait for review

> Step 6/6 완료: 상태/API 연동 명세를 작성했습니다.
> 검토 후 수정 사항이 있으면 말씀해 주세요.

### Step 7: Generate Table of Contents

**Output**: `docs/specifications/README.md`

After all 6 documents are approved, generate a table of contents:

```markdown
# Specifications

## Frontend Planning Documents

| # | Document | Description |
|---|----------|-------------|
| 01 | [Requirements](01-requirements.md) | 요구사항 정의서 |
| 02 | [User Flows](02-user-flows.md) | 사용자 플로우 |
| 03 | [Page Spec](03-page-spec.md) | 화면 명세서 |
| 04 | [Use Cases](04-use-cases.md) | 유스케이스 |
| 05 | [Component Tree](05-component-tree.md) | 컴포넌트 트리 |
| 06 | [State & API Integration](06-state-api-integration.md) | 상태/API 연동 명세 |
```

If `docs/specifications/README.md` already exists, append the frontend section
rather than overwriting.

Report completion:

> 프론트엔드 기획 문서 6개를 모두 생성했습니다:
> - `docs/specifications/01-requirements.md`
> - `docs/specifications/02-user-flows.md`
> - `docs/specifications/03-page-spec.md`
> - `docs/specifications/04-use-cases.md`
> - `docs/specifications/05-component-tree.md`
> - `docs/specifications/06-state-api-integration.md`
> - `docs/specifications/README.md` (목차)

## Document Rules

- **Language**: Korean with English technical terms in parentheses
- **Meta block**: Every document includes creation date, last modified date, status, tech stack, and prerequisite documents
- **Mermaid**: Use `flowchart TD` for user flows, `graph TD` for component trees
- **TypeScript**: Use `interface` declarations for props, store shapes, and API DTOs
- **References**: Each step must load all previous step outputs before generating
- **Review gate**: Never proceed to the next step without user approval
