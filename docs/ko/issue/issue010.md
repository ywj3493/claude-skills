# 이슈 010: 기획 스킬을 dev-planning으로 통합 및 테스트 추적성 추가

**상태**: 진행 중
**생성일**: 2026-03-30

## 배경

현재 저장소에는 `backend-planning`과 `frontend-planning` 두 개의 기획 스킬이
별도로 존재하며, 파이프라인 구조가 서로 다릅니다. 실제로 앞 4단계(requirements,
user stories, use cases, sequence diagrams)는 도메인에 무관하게 동일한 성격입니다.
마지막 명세 단계만 도메인 유형에 따라 달라집니다.

이 이슈는 두 스킬을 하나의 `dev-planning` 스킬로 통합합니다:

1. 공통 4단계 파이프라인 + 도메인별 명세 단계
2. 문서 간 ID 기반 연결 (FR-XXX, AC-XXX, UC-XXX)
3. 새로운 `test-spec.md` 최종 단계 — 앞 단계의 ID를 참조하여 테스트 매트릭스를
   생성하는 테스트 정의 전담 문서

이슈 008(frontend-planning 재구성)의 목표를 이번 통합에 흡수하여 대체합니다.

## 통합 파이프라인

```text
Step 0:   기술 스택 감지 + 도메인 유형 (backend/frontend/infra)
Step 0.5: 도메인 분석 & 문서 탐색
Step 1:   Requirements          → <domain>/requirements/requirements.md   [공통, FR-XXX]
Step 2:   User Stories           → <domain>/requirements/user-stories.md   [공통, US-XXX, AC-XXX]
Step 3:   Use Cases              → <domain>/workflows/use-cases.md         [공통, UC-XXX]
Step 4:   Sequence Diagrams      → <domain>/workflows/sequence-diagram.md  [공통]
Step 5:   도메인별 명세           → <domain>/workflows/<spec>.md           [분기]
             백엔드:    api-spec.md
             프론트엔드: component-spec.md
             인프라:    infra-spec.md
Step 6:   Test Specification     → <domain>/workflows/test-spec.md         [공통]
Step 7:   README (목차)
```

## 스킬 디렉토리 구조

```text
skills/dev-planning/
├── SKILL.md                          # v0.1.0
└── references/
    ├── common/
    │   ├── requirements-template.md
    │   ├── user-stories-template.md
    │   ├── use-cases-template.md
    │   ├── sequence-diagram-template.md
    │   └── test-spec-template.md
    ├── backend/
    │   └── api-spec-template.md
    ├── frontend/
    │   └── component-spec-template.md
    └── infra/
        └── infra-spec-template.md
```

## 완료 기준

- [ ] `skills/dev-planning/` 생성 — SKILL.md 및 9개 템플릿 포함
- [ ] 공통 템플릿(Steps 1-4)에는 ID만 포함, 테스트 정의 없음
- [ ] `test-spec-template.md`가 앞 단계 ID(FR, AC, UC)를 참조
- [ ] `component-spec-template.md`가 component-tree + state-api + ui-spec 통합
- [ ] `infra-spec-template.md`가 placeholder로 존재
- [ ] `backend-planning`과 `frontend-planning`이 deprecated 표시 (v0.0.2)
- [ ] CHANGELOG.md에 모든 버전 항목 업데이트
- [ ] 이슈 008이 Superseded로 표시

## 작업 목록

- [ ] 1. 이슈 문서 생성 (영문/한국어)
- [ ] 2. 이슈 008을 Superseded로 변경
- [ ] 3. `skills/dev-planning/` 디렉토리 구조 생성
- [ ] 4. 공통 템플릿 생성 (requirements, user-stories, use-cases, sequence-diagram)
- [ ] 5. `backend/api-spec-template.md` 생성 (기존에서 이동)
- [ ] 6. `frontend/component-spec-template.md` 생성 (3개 템플릿 병합)
- [ ] 7. `infra/infra-spec-template.md` 생성 (placeholder)
- [ ] 8. `common/test-spec-template.md` 생성
- [ ] 9. `dev-planning/SKILL.md` 작성
- [ ] 10. `backend-planning`과 `frontend-planning` deprecated 처리 (v0.0.2)
- [ ] 11. CHANGELOG.md 업데이트

## 참고 사항

- `backend-planning`과 `frontend-planning` 디렉토리는 마이그레이션 경로 제공을
  위해 삭제하지 않고 deprecated 처리합니다.
- `infra-spec-template.md`는 placeholder입니다 — 전체 인프라 지원은 향후 작업입니다.
- 기획/설계 문서(Steps 1-5)에는 테스트 관련 내용(테스트 타입, 모킹 경계)을 넣지
  않습니다. 모든 테스트 정의는 test-spec에서만 다룹니다.
- 이슈 008의 목표(네비게이션 헤더, 디렉토리 재구성)는 이번 통합 접근에 흡수됩니다.
