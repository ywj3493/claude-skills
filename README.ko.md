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
| dev-planning | `/dev-planning` | 6단계 기획 파이프라인(요구사항 → 유저 스토리 → 유스케이스 → 시퀀스 다이어그램 → 도메인 명세 → 테스트 명세)을 ID 기반 테스트 추적성과 함께 생성한다 |
| new-policy | `/new-policy` | 번역 미러와 함께 정책 문서를 추가한다 |
| sync-translations | `/sync-translations` | 누락되거나 구식이 된 번역 미러를 감지하고 동기화한다 |

각 스킬의 현재 버전은 `SKILL.md` 프론트매터에 있으며, 변경 사항은
[CHANGELOG.md](CHANGELOG.md)에 기록됩니다.

## 설치

```bash
npx skills add https://github.com/ywj3493/claude-skills.git
```

명령어 실행 후 안내에 따라 설치할 스킬을 선택합니다.

## 스킬 간 의존성

`init-docs`가 다른 스킬들이 사용하는 구조를 만듭니다. `new-policy`,
`sync-translations`, `new-issue`(docs 모드)는 그 구조가 없으면 먼저
`/init-docs` 실행을 안내합니다. GitHub 모드의 `new-issue`와 `dev-planning`은
독립적으로 사용할 수 있습니다.

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
  └─ /init-docs              docs/ 구조 + 언어 설정 + 정책 파일 + CLAUDE.md
      └─ /new-issue          GitHub Issue + 브랜치 + 드래프트 PR (또는 로컬 이슈 문서)
          └─ /dev-planning   구조화된 설계가 필요한 작업의 기획 문서
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
  dev-planning/           # /dev-planning (+ references/ — 도메인별 템플릿)
  new-policy/             # /new-policy
  sync-translations/      # /sync-translations
templates/
  CLAUDE.md               # 새 프로젝트용 표준 CLAUDE.md (init-docs 번들 템플릿과 동일)
docs/                     # 이 저장소 자체의 문서 (시스템 자체 검증용)
  config.yml              # 언어 설정 (en → ko)
  en/                     # 원본 문서 (policy/, issue/, specifications/)
  ko/                     # 한국어 미러
  reference/              # 사용자 관리 참조 자료
CHANGELOG.md              # 전체 스킬의 변경 이력 (최신순)
```

## 버저닝

스킬은 v0.x 개발 단계를 포함한 시맨틱 버저닝을 따릅니다 —
[docs/ko/policy/skill-versioning.md](docs/ko/policy/skill-versioning.md)
참조. Git 태그는 `<skill-name>/v<major>.<minor>.<patch>` 형식을 사용하며
(예: `dev-planning/v0.3.0`), 모든 스킬 수정은 `SKILL.md`의 `version` 필드
갱신과 `CHANGELOG.md` 항목 추가를 동반합니다.

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
