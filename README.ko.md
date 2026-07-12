# claude-skills — Claude Code 스킬 팩토리

문서 주도 개발 워크플로우를 위한 재사용 가능한
[Claude Code](https://claude.com/claude-code) 스킬 모음입니다: 표준화된
`docs/` 구조, 이슈 우선 작업 추적, 정책 문서, 기획 파이프라인, 번역 미러를
제공합니다.

English documentation: [README.md](README.md)

## 목적

새 프로젝트를 시작할 때마다 반복되는 작업 — docs 구조 설정, 정책 문서 작성,
이슈 추적, 번역 동기화 — 을 Claude Code 스킬로 표준화합니다.

한 번 설치하면 모든 프로젝트에서 동일한 명령어로 동일한 품질의 문서 시스템을
구축할 수 있습니다. 각 스킬에는 명시적인 **실행 요구사항(Execution
Requirements)** 이 포함되어 있어, 어떤 모델이 실행하든 결과 품질이 달라지지
않습니다.

## 스킬 목록

| 스킬 | 명령어 | 용도 |
| --- | --- | --- |
| init-docs | `/init-docs` | 표준 `docs/` 구조, 언어 설정, 정책 파일, CLAUDE.md를 생성한다 |
| new-issue | `/new-issue` | GitHub Issue와 작업 브랜치, (선택) 드래프트 PR을 생성한다 — 원격 저장소가 없으면 로컬 이슈 문서로 대체 |
| new-policy | `/new-policy` | 번역 미러와 함께 정책 문서를 추가한다 |
| sync-translations | `/sync-translations` | 누락되거나 구식이 된 번역 미러를 감지하고 동기화한다 |

각 스킬의 현재 버전은 `SKILL.md` 프론트매터에 있으며, 변경 사항은
[CHANGELOG.md](CHANGELOG.md)에 기록됩니다.

## 플러그인

| 플러그인 | 스킬 | 용도 |
| --- | --- | --- |
| dev-docs | `/dev-docs:dev-planning`, `/dev-docs:dev-reverse-docs` | 새 기능에 대한 사전 기획(`dev-planning`)과, 기존 코드에 대한 근거 기반·검증된 문서화(`dev-reverse-docs`)를 모두 제공하며 동일한 `planning/`/`design/`/`verification/` 문서 구조를 생성한다. `dev-reverse-docs`가 작성한 모든 주장을 실제 소스와 대조하는 읽기 전용 `doc-verifier` 서브에이전트를 포함한다. |

이 저장소의 마켓플레이스
([.claude-plugin/marketplace.json](.claude-plugin/marketplace.json))에서
설치할 수 있습니다:

```bash
claude
/plugin marketplace add ywj3493/claude-skills
/plugin install dev-docs@claude-skills
```

또는 로컬 개발 용도로 직접 불러올 수 있습니다:

```bash
claude --plugin-dir ./dev-docs-plugin
```

자세한 내용은 [dev-docs-plugin/README.md](dev-docs-plugin/README.md)를 참조하세요. 위의
스킬들과 달리 플러그인 스킬은 네임스페이스가 붙습니다
(`/dev-docs:dev-planning`, `/dev-planning`이 아님) — 여러 플러그인이
서로 충돌하지 않도록 하기 위함입니다.

## 설치

```bash
npx skills add https://github.com/ywj3493/claude-skills.git
```

명령어 실행 후 안내에 따라 설치할 스킬을 선택합니다.

## 스킬 간 의존성

`init-docs`가 다른 스킬들이 사용하는 구조를 만듭니다. `new-policy`,
`sync-translations`, `new-issue`(docs 모드)는 그 구조가 없으면 먼저
`/init-docs` 실행을 안내합니다. GitHub 모드의 `new-issue`와 `dev-docs`
플러그인의 스킬들은 독립적으로 사용할 수 있습니다.

## 언어 설정

문서 시스템은 하나의 **원본 언어**와 0개 이상의 **번역 언어**를 지원합니다.
`/init-docs` 실행 시 선택하며 `docs/config.yml`에 기록됩니다:

```yaml
source_language: en
translation_languages:
  - ko
```

모든 스킬은 언어 쌍을 가정하는 대신 이 파일을 읽습니다.
`translation_languages: []`인 프로젝트는 미러 부담 없이 단일 언어 문서
트리를 유지합니다. 기본 설정은 `en` → `ko`입니다.

## 전형적인 작업 흐름

```text
새 프로젝트
  └─ /init-docs                     docs/ 구조 + 언어 설정 + 정책 파일 + CLAUDE.md
      └─ /new-issue                 GitHub Issue + 브랜치 + 드래프트 PR (또는 로컬 이슈 문서)
          └─ /dev-docs:dev-planning      새 기능의 기획 문서 (구조화된 설계)
          └─ /dev-docs:dev-reverse-docs  이미 존재하는 코드의 근거 기반 문서화
          └─ 구현 작업...
              └─ /new-issue          작업 단위마다 반복
              └─ /new-policy         새 규칙을 공식화할 때
              └─ /sync-translations  번역 미러가 어긋났을 때
```

## 저장소 구조

```text
skills/                   # Claude Code 스킬 정의
  init-docs/              # /init-docs (+ scripts/, references/ — CLAUDE.md 템플릿 포함)
  new-issue/              # /new-issue
  new-policy/             # /new-policy
  sync-translations/      # /sync-translations
.claude-plugin/
  marketplace.json        # 플러그인 마켓플레이스 매니페스트 (dev-docs 등록)
dev-docs-plugin/          # dev-docs 플러그인 (.claude-plugin/plugin.json)
  skills/dev-planning/         # /dev-docs:dev-planning
  skills/dev-reverse-docs/     # /dev-docs:dev-reverse-docs
  agents/doc-verifier.md       # 읽기 전용 근거-코드 대조 검증기
  templates/              # 두 스킬이 공유: planning/, design/, verification/
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
(예: `new-issue/v0.3.0`), 모든 스킬 수정은 `SKILL.md`의 `version` 필드
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

1. `skills/<skill-name>/SKILL.md`를 YAML 프론트매터(`version: 0.0.1`부터
   시작)와 마크다운 지시사항으로 작성한다
2. 필요한 경우 `scripts/` 또는 `references/` 하위 디렉토리를 추가한다 —
   설치본이 자체 완결적이도록 스킬에 필요한 모든 파일을 스킬 디렉토리 안에
   둔다
3. 이 README(두 언어 버전 모두)에 스킬을 문서화하고 `CHANGELOG.md` 항목을
   추가한다
