# explainable 플러그인

기획·개발설계 문서를 **한국어로** 만드는
[Claude Code 플러그인](https://docs.claude.com/en/docs/claude-code/plugins)입니다.
두 방향을 모두 지원합니다.

- **새 프로젝트에서 시작** — 참고자료·서비스 목적 → 요구사항·유저 스토리 →
  화면 기능정의·검토·HTML 목업을 만들고, 승인 후 기술 설정·API 계약과 개발 설계로 넘어갑니다.
  스택이 미정이어도 기획을 시작할 수 있습니다.
- **기존 코드베이스 분석** — 인프라 → 코드베이스 구조 → 도메인별 설계를 먼저
  뽑고, **그 결과물로부터** 요구사항과 유저 스토리를 역산합니다.

설계는 백엔드와 프론트엔드를 별도 스킬로 나눕니다. 백엔드는 4-Layered DDD,
프론트엔드는 FSD(Feature-Sliced Design)를 기준선으로 삼되, **프레임워크에는
중립**입니다 — 프론트엔드가 React라고 가정하지 않고, 백엔드도 특정 프레임워크에
의존적인 지시문을 넣지 않습니다.

## 구성

| 종류 | 명령어 / 이름 | 용도 |
| --- | --- | --- |
| 스킬 | `/explainable:prepare-planning` | 자료 등록·선택·불변 스냅샷·UI 패턴 HTML 3안 |
| 스킬 | `/explainable:init-planning` | 서비스 목적 → 요구사항·스토리 → IA·UF·화면 기능정의 → 검토·승인 |
| 스킬 | `/explainable:revise-planning` | 단일 화면·화면 유지·전체 재구성·자료 재선택과 영향 추적 |
| 스킬 | `/explainable:build-storyboard` | 승인된 화면의 배지·기능 설명 패널이 있는 정적 HTML |
| 스킬 | `/explainable:sync-design` | 디자인 교환·Figma 매핑·손실 기록·3방향 변경 비교 |
| 스킬 | `/explainable:prepare-design` | 승인된 기획의 기술 설정·인프라·API 계약 확정 |
| 스킬 | `/explainable:init-design-backend` | 4-Layered DDD 설계: 레이어 매핑 → 도메인 모델 → ERD(조건부) → 유저 스토리 기반 시퀀스 다이어그램 |
| 스킬 | `/explainable:init-design-frontend` | FSD 설계: 레이어/슬라이스 구조 → 라우팅 → UI 구성 → 렌더링 흐름 → 상태 흐름. 기획의 화면·요소를 구현 단위에 연결 |
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
  /explainable:prepare-planning           자료·스냅샷·패턴 선택
    └─ /explainable:init-planning          서비스·화면 기획·승인
        └─ /explainable:build-storyboard   정적 목업·설명 패널
        ↔ /explainable:revise-planning     반복 수정·자료 재선택
        ↔ /explainable:sync-design         외부 디자인 변경 검토
    └─ /explainable:prepare-design         기술 설정·API 계약
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
    ├── planning/            service-brief, reference-materials, decisions, requirements,
    │                        user-stories, information-architecture, user-flows, screen-spec,
    │                        state.json, snapshots/, revisions/, api-interface, traceability
    ├── storyboard/          annotations.json, <SCR>.html, sync/
    ├── design/backend/      layered-architecture, domain-model, erd, sequence-diagram
    ├── design/frontend/     fsd-structure, routing, component-tree, render-flow,
    │                        state-flow
    └── verification/        test-spec
```

`information-architecture.md`와 `user-flows.md`는 **UI가 있는 프로젝트에서만**
만들어집니다. 둘은 짝이며, 화면이 무엇이고 사용자가 그 사이를 어떻게 지나가는지를
기획 계층에서 정합니다. 화면 내부 기능·상태·배치 요구는 `screen-spec.md`,
구현 UI/FSD 구조는 `component-tree.md`, 실제 주소는 `routing.md`가 소유합니다.
page는 라우트에, overlay/state는 부모 page 라우트에 연결합니다. 설계 스킬은 두 문서를 **읽기만** 합니다.

`README.md`, `architecture.md`, `infrastructure.md`, `glossary.md`,
`domain-map.md`, `test-spec.md`는 여러 스킬이 공유하는 **병합 전용** 문서입니다.
각 스킬은 `<!-- OWNER: ... -->` 마커로 표시된 자기 섹션만 쓰고, 나머지는 바이트
단위로 보존합니다.

## 공유 규약 (`references/`)

여러 스킬이 지키는 규칙은 스킬마다 반복하지 않고 `references/` 아래 한 곳에
둡니다. 각 스킬은 본문 상단에서 필요한 것만 로드합니다 — 주제별로 잘게
쪼개는 대신 **대상 스킬 묶음으로 이름을 지어**, 스킬 하나가 읽는 파일이
1~3개를 넘지 않게 했습니다.

| 파일 | 담는 것 | 읽는 스킬 |
| --- | --- | --- |
| `common-rules.md` | 문서 환경 감지, 실행 규약 9항목, 검증 루프, 완료 리포트, 문서 규칙, 공통 경계 규칙 | 12종 전부 |
| `reverse-rules.md` | 인용 계약, Source-Linked 시퀀스 규약, 재실행·폐기 정책, 탐색 에이전트 호출 규약 | `reverse-*` 3종 |
| `frontend-rules.md` | 프레임워크 중립 어휘, FSD 기준선, 문서 간 책임 경계 | `*-design-frontend` 2종 |
| `planning-rules.md` | ID 체계, 스왑 테스트, 인수 기준 형식, 계약 블록 선택 | 기획·개발 설계 준비 |
| `storyboard-rules.md` | 자료·결정·버전·화면/요소·수정 모드·목업·디자인 교환 계약 | 자료 기반 순방향 체인 |
| `document-order.md` | 문서 정규 순서와 내비게이션 링크 규칙 | `common-rules.md`가 참조 |

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

순방향 문서는 코드 인용 대신 자료 원장·SHA-256 스냅샷·판단/결정 기록을 사용합니다.
생성 모드는 state와 GENERATED-BY로 판별하고 기존 문서의 모호한 출처는 검토합니다.
`scripts/check-docs.sh`는 기존 문서 검사와 새 자료/화면/목업 검사를 함께 실행합니다.
보관본과 자료 복사본은 현재 문서 검사에서 제외합니다.

## 재실행

역방향 문서는 특정 커밋의 코드를 기술한 스냅샷입니다. 코드가 바뀐 뒤 부분
갱신하면 낡은 인용과 새 인용이 섞이므로, 해당 도메인의 역방향 산출물을
**폐기하고 다시 만듭니다**. 삭제 전에 대상 목록을 보여주고 확인을 받으며,
횡단 문서와 용어집은 폐기하지 않고 해당 도메인 섹션만 갱신합니다.

순방향 문서는 **절대 폐기하지 않습니다.** 수정 전 버전을 보관하고 사람의 결정과
기존 ID를 보존합니다. 폐기 ID는 재사용하지 않으며 목업·Figma·개발 설계의 기준
버전과 갱신 필요 상태를 추적합니다.

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

## 실행 도구와 지원 범위

Python 3.9 이상과 Bash가 필요합니다. 설치할 Python 패키지는 없습니다.

```bash
python3 explainable-plugin/scripts/planning-tools.py snapshot <domain> <materials.json> --id <snapshot-id>
python3 explainable-plugin/scripts/planning-tools.py check <domain>
python3 explainable-plugin/scripts/planning-tools.py approve <domain> --version <version> --reviewer <name>
python3 explainable-plugin/scripts/planning-tools.py build <domain>
python3 explainable-plugin/scripts/planning-tools.py restore <domain> --from-version <old-version> --version <new-version> --reason <reason>
python3 explainable-plugin/scripts/planning-tools.py ready-design <domain> --version <version>
python3 explainable-plugin/scripts/planning-tools.py export-sync <domain> --figma-file <file-id> --output <baseline.json>
python3 explainable-plugin/scripts/planning-tools.py compare-sync <domain> <baseline.json> <incoming.json> --output <report.json>
```

승인은 사람이 정확한 버전을 확인한 뒤 실행합니다. JSON 형식과 수정 명령은
[storyboard-rules.md](references/storyboard-rules.md)를 따릅니다.
목업은 로컬 CSS로 제공하는 Tailwind 유틸리티 부분집합이며 JS/CDN을 사용하지 않습니다.
임베딩 검색, 자체 Figma 플러그인, 범용 HTML/CSS↔Figma 변환기는 포함하지 않습니다.
Figma는 실제 연결 도구 또는 수동 교환으로 진행하며 텍스트·스타일·배치·아이콘·배지·
어노테이션의 손실과 미지원 항목을 기록합니다. 파일 교환 검사를 실제 왕복 성공으로
보고하지 않습니다. 최종 완료는 사람의 승인 버전에 연결합니다.
