# claude-skills — Claude Code 플러그인 팩토리

문서 주도 개발 워크플로우를 위한 재사용 가능한
[Claude Code](https://claude.com/claude-code) 스킬 모음입니다 — 표준화된
`docs/` 구조, 기획 파이프라인, 근거 기반 역문서화, 번역 미러를 두 개의
플러그인으로 배포합니다 — **dev-docs**(영어)와 **explainable**(한국어,
프론트엔드와 백엔드 설계를 분리).

English documentation: [README.md](README.md)

## 목적

새 프로젝트를 시작할 때마다 반복되는 작업 — docs 구조 설정, 기능 기획,
기존 코드 문서화, 번역 동기화 — 을 하나의 Claude Code 플러그인으로
표준화합니다.

한 번 설치하면 모든 프로젝트에서 동일한 명령어로 동일한 품질의 문서 시스템을
구축할 수 있습니다. 각 스킬에는 명시적인 **실행 요구사항(Execution
Requirements)** 이 포함되어 있어, 어떤 모델이 실행하든 결과 품질이 달라지지
않습니다.

## dev-docs 플러그인

명령어에 네임스페이스가 붙어(`/dev-docs:init-docs`) 다른 플러그인과
충돌하지 않습니다:

| 스킬 / 에이전트 | 명령어 / 이름 | 용도 |
| --- | --- | --- |
| init-docs | `/dev-docs:init-docs` | 표준 `docs/` 구조, 원본 언어 설정, 설정 질문으로 선택하는 `.claude/rules/` 작업 규칙, CLAUDE.md를 생성한다 |
| dev-planning | `/dev-docs:dev-planning` | 새 기능의 사전 기획 파이프라인: 요구사항 → 유저 스토리 → 유스케이스 → 설계 문서 → 테스트 명세, ID 기반 테스트 추적성 포함 |
| dev-reverse-docs | `/dev-docs:dev-reverse-docs` | 기존 코드에 대한 근거 기반·검증된 문서화 (모든 주장에 `[REF: path:line]` 인용) |
| domain-overview | `/dev-docs:domain-overview` | 도표 중심의 DDD 도메인 개요: 바운디드 컨텍스트, 애그리거트 루트, 패턴 라벨이 붙은 관계를 담은 Mermaid 컨텍스트 맵 |
| flow-diagram | `/dev-docs:flow-diagram` | 구현 직후: 방금 만들거나 변경한 흐름 하나에 대한 Source-Linked 시퀀스 다이어그램을 작성하거나 병합한다 |
| sync-translations | `/dev-docs:sync-translations` | 번역 미러링을 옵트인하고 원본 문서와 미러를 동기화한다 |
| doc-verifier | `doc-verifier` (에이전트) | `dev-reverse-docs`의 모든 인용을 실제 소스와 대조하는 읽기 전용 서브에이전트 |

## explainable 플러그인

한국어 기획·설계 파이프라인입니다
([explainable-plugin/](explainable-plugin/)). `dev-docs`와 목적은 같되 네
가지를 다르게 갑니다: 모든 프롬프트와 템플릿이 한국어이고, 프론트엔드와
백엔드 설계가 별도 스킬이며, 역방향 파이프라인이 설계부터 시작하고, 탐색
서브에이전트마다 목적이 하나씩 좁게 정해져 있습니다.

| 스킬 / 에이전트 | 명령어 / 이름 | 용도 |
| --- | --- | --- |
| init-planning | `/explainable:init-planning` | 새 프로젝트: 인프라·프로젝트 설정을 먼저 확정한 뒤 용어집 → 요구사항 → 유저 스토리 → 정보 구조 → 유저 플로우 → 인터페이스 계약 → 추적성 |
| init-design-backend | `/explainable:init-design-backend` | 4-Layered DDD: 레이어 매핑 → 도메인 모델 → ERD → 유저 스토리 기반 시퀀스 다이어그램 |
| init-design-frontend | `/explainable:init-design-frontend` | FSD: 레이어·슬라이스 구조 → 라우팅 → UI 구성 → 렌더링 흐름 → 상태 흐름. 기획의 화면 목록을 읽고 유저 플로우에 흐름 키를 되먹임 |
| reverse-design-backend | `/explainable:reverse-design-backend` | 기존 백엔드: 인프라 → 코드베이스 → 도메인 → 오퍼레이션별 Source-Linked 시퀀스 다이어그램 → 도메인 모델·ERD |
| reverse-design-frontend | `/explainable:reverse-design-frontend` | 기존 프론트엔드: 인프라 → 프레임워크 감지 → FSD 적합도 → 앱 셸 → 라우트별 코드·렌더링 흐름 |
| reverse-planning | `/explainable:reverse-planning` | 설계 문서와 코드 근거로 요구사항·유저 스토리·화면 목록·유저 플로우를 역산. 순방향으로 쓴 기획 문서는 덮어쓰지 않음 |
| translate-docs | `/explainable:translate-docs` | 번역 미러 감사·동기화, 또는 미러링 옵트인 |
| infra-explorer | `infra-explorer` (에이전트) | 읽기 전용: 배포·CI/CD·환경·외부 서비스 사실을 근거와 함께 수집 |
| operation-tracer | `operation-tracer` (에이전트) | 읽기 전용: 백엔드 오퍼레이션 하나의 호출 체인 추적, 프로토콜 중립 |
| render-flow-tracer | `render-flow-tracer` (에이전트) | 읽기 전용: 라우트 하나의 코드 흐름과 렌더링 흐름, 프레임워크 중립 |
| citation-verifier | `citation-verifier` (에이전트) | 읽기 전용: 모든 인용을 소스와 대조. `doc-verifier`와 검증 계약 동일 |

백엔드는 4-Layered DDD, 프론트엔드는 FSD를 기준선으로 삼지만 **프레임워크에는
중립**입니다 — React를 가정하지 않으며, 구체 프레임워크는 감지된 사실이나
사용자 결정으로 `architecture.md`에 기록될 때만 등장합니다.

각 스킬의 현재 버전은 `SKILL.md` 프론트매터에 있으며, 변경 사항은
[CHANGELOG.md](CHANGELOG.md)에 기록됩니다.

## 설치

이 저장소의 마켓플레이스
([.claude-plugin/marketplace.json](.claude-plugin/marketplace.json))에서
설치할 수 있습니다:

```bash
claude
/plugin marketplace add ywj3493/claude-skills
/plugin install dev-docs@claude-skills
/plugin install explainable@claude-skills
```

둘은 독립적이므로 하나만 설치해도 됩니다. 또는 로컬 개발 용도로 직접
불러올 수 있습니다:

```bash
claude --plugin-dir ./dev-docs-plugin
claude --plugin-dir ./explainable-plugin
```

자세한 내용은 [dev-docs-plugin/README.md](dev-docs-plugin/README.md)와
[explainable-plugin/README.md](explainable-plugin/README.md)를 참조하세요.

## 어느 플러그인을 쓸까

| | `dev-docs` | `explainable` |
| --- | --- | --- |
| 언어 | 영어 | 한국어 |
| 설계 분리 | 하나의 파이프라인 | 프론트엔드·백엔드 별도 스킬 |
| 역방향 순서 | 기획 → 설계 | **설계 → 기획** |
| 아키텍처 기준선 | 없음 | 백엔드 4-Layered DDD, 프론트엔드 FSD |
| 이슈 관리 | 정책으로 포함 | 범위 제외 |
| 출력 티어 | Lite / Full | 없음 (오퍼레이션 선별 게이트로 대체) |
| `docs/` 스캐폴딩 | `init-docs` | 출력 경로만 최소 생성 |

한 프로젝트에서 함께 쓸 수 있습니다. `explainable`은 `docs/` 트리 전체를
스캐폴딩하지 않으므로, `issue/`·`reference/`·`.claude/rules/`를 포함한 완전한
구조가 필요하면 `/dev-docs:init-docs`를 먼저 실행하세요.

## 스킬 간 의존성

`init-docs`가 다른 스킬들이 사용하는 구조를 만듭니다. `sync-translations`는
그 구조가 없으면 먼저 `/dev-docs:init-docs` 실행을 안내합니다.
`dev-planning`과 `dev-reverse-docs`는 그 구조 안에서 가장 잘 동작하지만
구조 없이도 실행할 수 있습니다.

`explainable`에서는 순방향일 때 기획이 설계로, 역방향일 때 설계가 기획으로
이어집니다. 모든 스킬이 문서 환경을 스스로 감지하고 필요한 출력 경로만
만들므로, 구조가 없다고 멈추는 스킬은 없습니다.

## 언어 설정

문서 시스템은 하나의 **원본 언어**(문서를 작성하는 기준 언어)와 0개 이상의
**번역 언어**를 지원하며 `docs/config.yml`에 기록됩니다.
`/dev-docs:init-docs`는 원본 언어만 설정합니다:

```yaml
source_language: en
translation_languages: []
```

미러링은 옵트인이며 나중에 이루어집니다: 첫 `/dev-docs:sync-translations`
실행이 번역 언어(예: `ko`) 추가를 제안하고, 수락하면 `docs/config.yml`에
기록한 뒤 미러 디렉토리를 만들고 기존 문서를 번역합니다. 모든 스킬은 언어
쌍을 가정하는 대신 이 파일을 읽습니다. 옵트인하지 않은 프로젝트는 미러 부담
없이 단일 언어 문서 트리를 유지합니다.

## 전형적인 작업 흐름

```text
새 프로젝트
  └─ /dev-docs:init-docs            docs/ 구조 + 원본 언어 + .claude/rules + CLAUDE.md
      └─ 이슈 생성                   GitHub Issue (또는 docs/<lang>/issue/issue001.md)
          └─ /dev-docs:dev-planning      새 기능의 기획 문서 (구조화된 설계)
          └─ /dev-docs:dev-reverse-docs  이미 존재하는 코드의 근거 기반 문서화
          └─ /dev-docs:domain-overview   전체 도메인을 담는 도표 중심 DDD 컨텍스트 맵
          └─ 구현 작업...
              └─ /dev-docs:flow-diagram       방금 변경한 흐름에 대한 Source-Linked 시퀀스 다이어그램 1장
              └─ /dev-docs:sync-translations  번역 미러 옵트인 / 미러가 어긋났을 때 재동기화
```

`explainable` 플러그인에서는 코드가 이미 있는지에 따라 기획과 설계의 순서가
반대입니다:

```text
새 프로젝트 (기획 먼저)
  └─ /explainable:init-planning            인프라·프로젝트 설정, 그다음 기획 문서
      └─ /explainable:init-design-backend      4-Layered DDD
      └─ /explainable:init-design-frontend     FSD
          └─ /explainable:translate-docs       번역 미러

기존 코드베이스 (설계 먼저)
  └─ /explainable:reverse-design-backend   인프라 → 코드베이스 → 도메인 → 오퍼레이션
  └─ /explainable:reverse-design-frontend  인프라 → 프레임워크 → 앱 셸 → 라우트
      └─ /explainable:reverse-planning         설계로부터 요구사항·스토리 역산
          └─ /explainable:translate-docs       번역 미러
```

역방향이 설계부터인 이유는, 코드가 무엇을 강제하는지 확인하기 전에
요구사항을 쓰면 추측이 되기 때문입니다. 설계 단계가 검증·가드·분기·타임아웃
설정을 드러내고, 요구사항은 그것으로부터 도출됩니다.

## 저장소 구조

```text
.claude-plugin/
  marketplace.json        # 플러그인 마켓플레이스 매니페스트 (dev-docs, explainable 등록)
dev-docs-plugin/          # dev-docs 플러그인 (.claude-plugin/plugin.json)
  skills/init-docs/            # /dev-docs:init-docs (+ scripts/, references/ — CLAUDE.md 템플릿 포함)
  skills/dev-planning/         # /dev-docs:dev-planning
  skills/dev-reverse-docs/     # /dev-docs:dev-reverse-docs
  skills/domain-overview/      # /dev-docs:domain-overview (+ references/ — 전용 템플릿 포함)
  skills/flow-diagram/         # /dev-docs:flow-diagram
  skills/sync-translations/    # /dev-docs:sync-translations
  agents/doc-verifier.md       # 읽기 전용 근거-코드 대조 검증기
  templates/              # 기획 스킬들이 공유: planning/, design/, verification/
explainable-plugin/       # explainable 플러그인 (한국어; .claude-plugin/plugin.json)
  skills/init-planning/            # /explainable:init-planning
  skills/init-design-backend/      # /explainable:init-design-backend
  skills/init-design-frontend/     # /explainable:init-design-frontend
  skills/reverse-design-backend/   # /explainable:reverse-design-backend
  skills/reverse-design-frontend/  # /explainable:reverse-design-frontend
  skills/reverse-planning/         # /explainable:reverse-planning
  skills/translate-docs/           # /explainable:translate-docs
  agents/                 # infra-explorer, operation-tracer, render-flow-tracer, citation-verifier
  templates/              # overview/, planning/, design/{backend,frontend}/, verification/
  references/             # 스킬이 로드하는 공유 규약: common-, reverse-,
                          # frontend-, planning-rules.md + document-order.md
  scripts/check-docs.sh   # ID·링크·자리표시자·펜스 결정적 검사
templates/
  CLAUDE.md               # 새 프로젝트용 표준 CLAUDE.md (init-docs 번들 템플릿과 동일)
docs/                     # 이 저장소 자체의 문서 (시스템 자체 검증용)
  config.yml              # 언어 설정 (en → ko)
  en/                     # 원본 문서 (policy/, issue/, specifications/)
  ko/                     # 한국어 미러
  reference/              # 사용자 관리 참조 자료
CHANGELOG.md              # 전체 스킬/플러그인의 변경 이력 (최신순)
```

## 버저닝

스킬은 v0.x 개발 단계를 포함한 시맨틱 버저닝을 따릅니다 —
[.claude/rules/skill-versioning.md](.claude/rules/skill-versioning.md)
참조 (이 저장소 자체의 정책 규칙은 `.claude/rules/`에 영어로만 존재하며
`docs/ko/` 이중언어 미러 대상이 아닙니다). Git 태그는
`<skill-name>/v<major>.<minor>.<patch>` 형식을 사용하며
(예: `init-docs/v0.3.0`), 모든 스킬 수정은 `SKILL.md`의 `version` 필드
갱신과 `CHANGELOG.md` 항목 추가를 동반합니다. 플러그인(예: `dev-docs`)은
`<plugin-name>/v<version>` 형식으로 하나의 단위로 버전이 관리되며, 이는
플러그인에 포함된 각 스킬/에이전트가 개별적으로 유지하는 `version` 필드와는
별개입니다.

## 스킬 개발 가이드

### 기존 스킬 수정

1. `SKILL.md`를 편집한다 — YAML 프론트매터(`name`, `version`, `description`)를
   정확하게 유지한다
2. 스킬이 의존하는 `scripts/` 또는 `references/`를 업데이트한다
3. `version` 필드를 올리고 `CHANGELOG.md` 항목을 추가한다

### 새 스킬 추가

1. `dev-docs-plugin/skills/<skill-name>/SKILL.md`를 YAML
   프론트매터(`version: 0.0.1`부터 시작)와 마크다운 지시사항으로 작성한다
2. 필요한 경우 `scripts/` 또는 `references/` 하위 디렉토리를 추가한다 —
   설치본이 자체 완결적이도록 스킬에 필요한 모든 파일을 스킬 디렉토리 안에
   두고, 지시사항의 경로는 `${CLAUDE_PLUGIN_ROOT}`를 사용한다
3. 이 README(두 언어 버전 모두)와 플러그인 README에 스킬을 문서화하고
   `CHANGELOG.md` 항목을 추가한다; 패키징 변경이므로
   `dev-docs-plugin/.claude-plugin/plugin.json`의 플러그인 버전을 올린다
