# 이슈 008: frontend-planning 스킬 파이프라인 및 템플릿 구조 변경

**상태**: 대체됨
**생성일**: 2026-03-16
**대체 이슈**: [@docs/en/issue/issue010.md](docs/en/issue/issue010.md)

## 배경

현재 frontend-planning 스킬은 6단계 문서 파이프라인으로 구성되어 있으며,
`user-flows`가 `workflows/` 하위에 위치합니다. 현재 디렉터리 구조는 기획
(requirements/design) 문서와 구현(development) 문서를 명확히 구분하지 못합니다.
또한 `architecture.md`와 `infrastructure.md` 템플릿이 없고, 도메인 문서 간
네비게이션 링크도 없습니다.

이 이슈는 스킬을 다음과 같이 재구성합니다:

1. Mermaid 다이어그램을 포함한 `architecture.md` 및 `infrastructure.md` 템플릿 추가
2. 기획 문서(`user-flows`, `ui-spec`)를 `requirements/` 하위로 이동
3. 모든 도메인 문서에 네비게이션 헤더 추가

## 제안 디렉터리 구조

```text
docs/en/specifications/
├── architecture.md              # 프로젝트 디렉터리 구조 (Mermaid)
├── infrastructure.md            # 배포 & 인프라 (Mermaid) — 도메인 바깥
├── config.md
├── README.md
└── <domain>/
    ├── requirements/
    │   ├── requirements.md      # Step 1: 기능/비기능 요구사항
    │   ├── user-flows.md        # Step 2: 사용자 여정 플로차트 (기존 workflows/)
    │   └── ui-spec.md            # Step 3: UI 명세 (page-spec에서 이름 변경)
    └── workflows/
        ├── use-cases.md         # Step 4: 액터-시스템 상호작용
        ├── component-tree.md    # Step 5: 컴포넌트 계층 & props
        └── state-api-integration.md  # Step 6: 상태 관리 & API 계층
```

## 변경 세부 사항

### 1. architecture.md & infrastructure.md 템플릿

- `architecture.md`: 프로젝트 디렉터리 구조, 모듈 경계, 주요 파일 관계를 보여주는
  Mermaid 그래프. `docs/en/specifications/`에 위치 (도메인 비특정, 횡단 문서).
- `infrastructure.md`: 배포 토폴로지, CI/CD 파이프라인, 외부 서비스, 환경을
  보여주는 Mermaid 다이어그램. `docs/en/specifications/`에 위치 (도메인 비특정,
  횡단 문서).
- 두 템플릿 모두 Mermaid를 통한 시각적 표현을 강조합니다.

### 2. 기획 vs 구현 문서 재구성

- `user-flows.md`를 `workflows/`에서 `requirements/`로 이동 — 사용자 흐름은
  계획된 사용자 여정을 설명하며 요구사항과 함께 있어야 합니다.
- `page-spec.md`를 `ui-spec.md`로 이름 변경 후 `workflows/`에서 `requirements/`로
  이동 — UI 명세는 레이아웃 구조, 반응형 규칙, 인터랙션 패턴을 정의하며, 이는
  기획 단계 결정 사항입니다. "ui-spec"이라는 이름은 페이지 기반 앱, 디자인 시스템,
  컴포넌트 라이브러리 모두를 포괄합니다. 컴포넌트 매핑 세부사항은
  `component-tree.md`에서 다룹니다.
- `requirements/` = 기획/설계 문서 (무엇을 만들 것인가)
- `workflows/` = 구현 문서 (어떻게 만들 것인가)

### 3. 도메인 문서 네비게이션

도메인 내 모든 문서는 두 개의 네비게이션 블록을 가집니다:

**상단 네비게이션** — 순차 읽기를 위한 이전/다음 링크:

```markdown
> [← Requirements](requirements/requirements.md) | [User Flows →](requirements/user-flows.md)
```

**하단 네비게이션** — 모든 문서로 이동할 수 있는 전체 인덱스:

```markdown
---
> **All Documents**
> [Requirements](requirements/requirements.md) |
> [User Flows](requirements/user-flows.md) |
> [UI Spec](requirements/ui-spec.md) |
> [Use Cases](workflows/use-cases.md) |
> [Component Tree](workflows/component-tree.md) |
> [State & API](workflows/state-api-integration.md)
```

문서 순서:
1. Requirements → 2. User Flows → 3. UI Spec → 4. Use Cases → 5. Component Tree → 6. State & API

첫 번째 문서는 "←" 링크를 생략하고, 마지막 문서는 "→" 링크를 생략합니다.
링크는 현재 파일 기준 상대 경로를 사용하여 GitHub과 IDE에서 모두 작동합니다.

## 완료 기준

- [ ] Mermaid 다이어그램 포함 `architecture.md` 템플릿 `references/`에 추가
- [ ] Mermaid 다이어그램 포함 `infrastructure.md` 템플릿 `references/`에 추가
- [ ] `user-flows` 출력 경로를 `<domain>/requirements/user-flows.md`로 변경
- [ ] `page-spec`을 `ui-spec`으로 이름 변경 후 출력 경로를 `<domain>/requirements/ui-spec.md`로 변경
- [ ] 모든 도메인 문서 템플릿에 네비게이션 헤더 포함
- [ ] 새로운 파이프라인 구조를 반영하여 SKILL.md 업데이트
- [ ] SKILL.md 가능한 부분 간략화
- [ ] 기존 템플릿을 새 경로 및 네비게이션에 맞게 업데이트

## 작업 목록

- [ ] 1. `references/`에 `architecture-template.md` 추가
- [ ] 2. `references/`에 `infrastructure-template.md` 추가
- [ ] 3. `user-flows-template.md` 업데이트 — 네비게이션 헤더 추가
- [ ] 4. `page-spec-template.md`를 `ui-spec-template.md`로 이름 변경 — 내용 업데이트 및 네비게이션 헤더 추가
- [ ] 5. `use-cases-template.md` 업데이트 — 네비게이션 헤더 추가
- [ ] 6. `component-tree-template.md` 업데이트 — 네비게이션 헤더 추가
- [ ] 7. `state-api-integration-template.md` 업데이트 — 네비게이션 헤더 추가
- [ ] 8. `requirements-template.md` 업데이트 — 네비게이션 헤더 추가
- [ ] 9. 새 구조를 반영하고 간략화하여 SKILL.md 재작성
- [ ] 10. 모든 템플릿 상호 참조가 올바른 상대 경로를 사용하는지 확인

## 참고 사항

<!-- 작업 진행 중 결정 사항, 발견 사항, 차단 사항을 여기에 기록하세요 -->

- **page-spec → ui-spec 이름 변경**: 페이지 기반 앱, 디자인 시스템, 컴포넌트
  라이브러리 모두를 포괄하기 위해 `ui-spec`으로 이름 변경. `requirements/`로 이동.
  내용(레이아웃, 반응형 규칙, 인터랙션 패턴)이 기획 결정 사항이기 때문. 컴포넌트
  수준 세부사항은 `workflows/`의 `component-tree.md`에서 처리.
- 파이프라인 스텝 번호는 1~6으로 유지하되 출력 경로가 변경됨.
- `architecture.md`와 `infrastructure.md`는 Step 0에서 생성되거나 별도 선택적
  스텝으로 처리. 도메인 비특정 횡단 문서이기 때문.
