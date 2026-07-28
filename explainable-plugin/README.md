# explainable 플러그인

기획·개발설계 문서를 **한국어로** 만드는
[Claude Code 플러그인](https://docs.claude.com/en/docs/claude-code/plugins)입니다.
두 방향을 모두 지원합니다.

- **새 프로젝트에서 시작** — 인프라·프로젝트 설정을 먼저 확정하고, 요구사항 →
  유저 스토리 → 인터페이스 계약 순으로 기획한 뒤 설계로 넘어갑니다.
- **기존 코드베이스 분석** — 인프라 → 코드베이스 구조 → 도메인별 설계를 먼저
  뽑고, **그 결과물로부터** 요구사항과 유저 스토리를 역산합니다.

설계는 백엔드와 프론트엔드를 별도 스킬로 나눕니다. 백엔드는 4-Layered DDD,
프론트엔드는 FSD(Feature-Sliced Design)를 기준선으로 삼되, **프레임워크에는
중립**입니다 — 프론트엔드가 React라고 가정하지 않고, 백엔드도 특정 프레임워크에
의존적인 지시문을 넣지 않습니다.

## 구성

| 종류 | 명령어 / 이름 | 용도 |
| --- | --- | --- |
| 스킬 | `/explainable:init-planning` | 새 프로젝트 기획: 인프라·프로젝트 설정 → 용어집 → 요구사항(FR/NFR) → 유저 스토리(US/AC) → 인터페이스 계약 → 도메인 간 통합 → 추적성 매트릭스 |
| 스킬 | `/explainable:init-design-backend` | 4-Layered DDD 설계: 레이어 매핑 → 도메인 모델 → ERD(조건부) → 유저 스토리 기반 시퀀스 다이어그램 |
| 스킬 | `/explainable:init-design-frontend` | FSD 설계: 레이어/슬라이스 구조 → 라우팅 → UI 구성 → 렌더링 흐름 → 상태 흐름 → 유저 플로우 |
| 스킬 | `/explainable:reverse-design-backend` | 기존 백엔드 분석: 인프라 → 코드베이스 → 도메인 식별 → 오퍼레이션별 Source-Linked 시퀀스 다이어그램 → 도메인 모델·ERD 역추출 |
| 스킬 | `/explainable:reverse-design-frontend` | 기존 프론트엔드 분석: 인프라 → 프레임워크 감지 → FSD 적합도 판정 → 앱 셸 + 라우트별 코드·렌더링 흐름 추적 |
| 스킬 | `/explainable:reverse-planning` | 설계 문서와 코드 근거로부터 요구사항·유저 스토리를 역산. 순방향 기획 문서는 덮어쓰지 않고 차이 리포트를 만든다 |
| 스킬 | `/explainable:translate-docs` | 번역 미러 감사 및 동기화. 번역 언어가 없으면 미러링 옵트인을 제안 |
| 에이전트 | `infra-explorer` | 배포·CI/CD·환경변수·외부 서비스 사실 수집 (읽기 전용) |
| 에이전트 | `operation-tracer` | 오퍼레이션 1개의 호출 체인을 진입점부터 어댑터까지 추적 (읽기 전용) |
| 에이전트 | `render-flow-tracer` | 앱 셸 또는 라우트 1개의 코드 흐름과 렌더링 흐름 추적 (읽기 전용) |
| 에이전트 | `citation-verifier` | 문서의 모든 인용을 실제 소스와 대조 (읽기 전용) |

## 워크플로

```text
새 프로젝트
  /explainable:init-planning              인프라·설정 + 기획 문서
    └─ /explainable:init-design-backend       4-Layered DDD 설계
    └─ /explainable:init-design-frontend      FSD 설계
        └─ /explainable:translate-docs        번역 미러

기존 코드베이스
  /explainable:reverse-design-backend     인프라 → 코드베이스 → 도메인별 설계
  /explainable:reverse-design-frontend    인프라 → 프레임워크 감지 → 라우트별 흐름
    └─ /explainable:reverse-planning          설계로부터 기획 역산
        └─ /explainable:translate-docs        번역 미러
```

역방향은 **설계가 먼저**입니다. 코드가 이미 있는 상태에서 요구사항을 먼저
쓰려고 하면 근거 없이 추측하게 되기 때문입니다. 설계 문서에서 코드가 실제로
강제하는 것(검증, 권한 체크, 분기, 타임아웃 설정)을 확인한 뒤에야 요구사항을
말할 수 있습니다.

## 산출 문서

```text
docs/<source>/specifications/
├── README.md                # 도메인 인덱스
├── architecture.md          # 코드베이스 구조 + 아키텍처 규약
├── infrastructure.md        # 인프라·배포·환경
├── glossary.md              # 한국어 용어 ↔ 영문 식별자
├── domain-map.md            # 도메인 간 관계 (컨텍스트 맵, 슬라이스 의존, 횡단 흐름)
└── <domain>/
    ├── planning/            requirements, user-stories, api-interface, traceability
    ├── design/backend/      layered-architecture, domain-model, erd, sequence-diagram
    ├── design/frontend/     fsd-structure, routing, component-tree, render-flow,
    │                        state-flow, user-flows
    └── verification/        test-spec
```

`README.md`, `architecture.md`, `infrastructure.md`, `glossary.md`,
`domain-map.md`, `test-spec.md`는 여러 스킬이 공유하는 **병합 전용** 문서입니다.
각 스킬은 `<!-- OWNER: ... -->` 마커로 표시된 자기 섹션만 쓰고, 나머지는 바이트
단위로 보존합니다.

## 프레임워크 중립성

스킬과 템플릿에는 레이어·슬라이스의 **역할**과 **의존성 방향 규칙**만 담고,
특정 프레임워크의 API·데코레이터·훅 이름은 담지 않습니다. 프레임워크 구체
사항은 두 경로로만 문서에 들어옵니다.

1. **감지된 사실** — 매니페스트·설정 파일에서 읽어 `[REF: path:line]`과 함께
   `architecture.md` / `infrastructure.md`에 기록
2. **사용자가 정한 결정** — 인프라·프로젝트 설정 단계에서 사용자가 고른 값

`api-interface.md`도 REST/OpenAPI를 전제하지 않습니다. 문서 구조는 고정이고,
계약 블록 형식만 확정된 API 스타일에 따라 달라집니다 — REST면 OpenAPI 3.1,
GraphQL이면 SDL, gRPC면 `.proto`, 이벤트 기반이면 AsyncAPI.

## 근거와 검증

역방향 스킬이 만드는 모든 문서는 인용 계약을 따릅니다.

- 모든 주장에 `[REF: path:line]` 또는 `[ASSUMED: <추론>; basis: <근거>]`
- 문서마다 `## 읽은 소스` 원장
- `citation-verifier`가 인용을 실제 소스와 대조하고, 시퀀스 다이어그램은
  보이는 `Note`와 숨김 `CALLGRAPH` 블록을 양방향으로 교차 검증
- 미해결 `MISMATCHED`/`UNSUPPORTED`가 남아 있으면 완료를 보고하지 않음

순방향 문서는 코드가 없어 인용할 대상이 없으므로 `## 읽은 소스`를 넣지 않고,
대신 `scripts/check-docs.sh`가 ID 추적성·링크 무결성·자리표시자 잔존·mermaid
펜스 균형을 결정적으로 검사합니다.

## 재실행

역방향 문서는 특정 커밋의 코드를 기술한 스냅샷입니다. 코드가 바뀐 뒤 부분
갱신하면 낡은 인용과 새 인용이 섞이므로, 해당 도메인의 역방향 산출물을
**폐기하고 다시 만듭니다**. 삭제 전에 대상 목록을 보여주고 확인을 받으며,
횡단 문서와 용어집은 폐기하지 않고 해당 도메인 섹션만 갱신합니다.

순방향 문서는 **절대 폐기하지 않습니다.** 사람이 결정한 기획을 스킬이 지울 수는
없습니다.

## 설치

이 저장소 루트의 마켓플레이스에서:

```bash
claude
/plugin marketplace add ywj3493/claude-skills
/plugin install explainable@claude-skills
```

로컬/팀 사용을 위해 직접 로드하려면:

```bash
claude --plugin-dir ./explainable-plugin
```

## 호스트 프로젝트 전제

이 플러그인은 `docs/` 구조를 **전체 스캐폴딩하지 않습니다.** `docs/config.yml`이
있으면 그 `source_language`를 따르고, 없으면 디렉터리 구조에서 추론하며,
`docs/` 자체가 없으면 출력 경로만 최소로 만들고 진행합니다. 전체 초기화
(`issue/`, `reference/`, `.claude/rules/`, 루트 `CLAUDE.md`)가 필요하면
`dev-docs` 플러그인의 `/dev-docs:init-docs`를 안내합니다.

동의 없이 `docs/config.yml`, 루트 `CLAUDE.md`, `.claude/rules/`를 쓰지 않습니다.

## `dev-docs` 플러그인과의 관계

같은 저장소의 `dev-docs`와 목적이 겹치지만 별개의 플러그인입니다.

| | `dev-docs` | `explainable` |
| --- | --- | --- |
| 언어 | 영어 | 한국어 |
| 설계 분리 | 하나의 파이프라인 | 백엔드/프론트엔드 별도 스킬 |
| 역방향 순서 | 기획 → 설계 | **설계 → 기획** |
| 아키텍처 기준선 | 없음 | 백엔드 4-Layered DDD, 프론트엔드 FSD |
| 이슈 관리 | 정책으로 포함 | 범위 제외 |
| 출력 티어 | Lite / Full | 없음 (오퍼레이션 선별 게이트로 대체) |

`citation-verifier`는 `dev-docs`의 `doc-verifier`를 이식한 것으로 **검증 계약이
동일**합니다. 두 플러그인에서 같은 이름의 에이전트가 서로 다르게 진화하는 것을
막기 위해 이름만 다르게 두었습니다.

도메인이 여러 개인 저장소에서 영어 DDD 컨텍스트 맵이 필요하면
`/dev-docs:domain-overview`가 별도로 있습니다. 이 플러그인의 `domain-map.md`는
프론트엔드 슬라이스 축과 도메인 횡단 흐름까지 다루므로 범위가 다릅니다.

## 버전 관리

플러그인은 하나의 단위로 버전을 매기고(`plugin.json`의 `version`, git 태그
`explainable/v<x.y.z>`), 번들된 각 스킬과 에이전트는 자체 `version` 필드를
독립적으로 유지합니다. 변경 사항은 저장소 루트의
[CHANGELOG.md](../CHANGELOG.md)에 기록됩니다.
