<!--
템플릿: 횡단 문서 (specifications/README.md)

내비게이션 없음, 도메인 태그 없음. 병합 전용.

**각 스킬은 자기가 다룬 도메인의 행만 갱신한다.** "마지막에 실행한 스킬이
전체를 다시 쓴다"는 방식은 실행 순서에 따라 결과가 달라지므로 쓰지 않는다.

생성되지 않은 문서는 링크하지 않는다. 링크가 없는 칸은 `—`로 둔다.
-->

<!-- GENERATED-BY: <스킬명>; commit: <sha>; root: <스캔 경로>; date: <YYYY-MM-DD> -->

# 명세 문서 인덱스

<!-- 이 프로젝트가 무엇인지 2~3문장. 상세는 architecture.md가 소유한다. -->

---

## 횡단 문서

| 문서 | 내용 |
|---|---|
| [아키텍처](architecture.md) | 코드베이스 구조, 스택, 레이어·슬라이스 매핑, 허용 의존성 |
| [인프라](infrastructure.md) | 런타임, 배포 토폴로지, 환경, CI/CD, 외부 서비스 |
| [도메인 지도](domain-map.md) | 도메인 간 관계, 컨텍스트 맵, 슬라이스 의존, 횡단 흐름 |
| [용어집](glossary.md) | 한국어 용어와 영문 식별자 대응 |

---

## 도메인

<!--
도메인 하나당 한 행. `계층` 열은 백엔드 / 프론트엔드 / 양쪽.
`생성 방식` 열은 순방향 / 역방향 — 역방향 재실행 시 폐기 대상을 판단하는
근거가 된다.
-->

| 도메인 | 계층 | 생성 방식 | 기획 | 설계 | 검증 |
|---|---|---|---|---|---|
| <!-- order --> | | | [요구사항](order/planning/requirements.md) | [백엔드](order/design/backend/layered-architecture.md) · [프론트엔드](order/design/frontend/fsd-structure.md) | [테스트 명세](order/verification/test-spec.md) |

---

## 도메인별 문서 구성

각 도메인 디렉터리는 다음 구조를 따릅니다. 증거가 없거나 해당하지 않는
문서는 생성되지 않습니다.

```text
<domain>/
├── planning/
│   ├── requirements.md      요구사항 (FR/NFR/제약)
│   ├── user-stories.md      유저 스토리와 인수 기준
│   ├── information-architecture.md  화면 목록·계층·내비게이션 (UI가 있을 때만)
│   ├── user-flows.md        화면 사이를 지나가는 과업 흐름 (UI가 있을 때만)
│   ├── api-interface.md     인터페이스 계약
│   └── traceability.md      FR ↔ US/AC ↔ SCR/UF ↔ FLOW ↔ T 매트릭스
├── design/
│   ├── backend/             레이어 매핑, 도메인 모델, ERD, 시퀀스 다이어그램
│   └── frontend/            FSD 구조, 라우팅, UI 구성, 렌더링·상태 흐름
└── verification/
    └── test-spec.md         테스트 매트릭스와 추적성
```

---

## 문서를 읽는 순서

**기획 의도를 알고 싶다면**: 도메인의 `requirements.md` → `user-stories.md` →
`information-architecture.md` → `user-flows.md` → `api-interface.md`

**구현 구조를 알고 싶다면**: `architecture.md` → 도메인의
`design/backend/layered-architecture.md` 또는
`design/frontend/fsd-structure.md`

**특정 기능이 어떻게 동작하는지 알고 싶다면**: `user-stories.md`에서 해당
`US-NN`을 찾고, `traceability.md`에서 그 스토리에 연결된 `FLOW-` 키를 확인한
뒤, 해당 시퀀스 다이어그램으로 간다.

**도메인이 서로 어떻게 엮이는지 알고 싶다면**: `domain-map.md`

---

## 관련 프로젝트 문서

<!-- 이 저장소의 다른 문서(루트 README, 기여 가이드 등) 링크. 없으면 삭제. -->

---

## 문서 정보

| 항목 | 값 |
|---|---|
| **작성일** | YYYY-MM-DD |
| **최종 수정일** | YYYY-MM-DD |
| **상태** | 초안 |

**버전 이력**:

- 1.0.0 (YYYY-MM-DD): 최초 작성
