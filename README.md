# claude — Claude Code 스킬 팩토리

재사용 가능한 Claude Code 스킬 모음입니다.
모든 프로젝트에서 일관된 문서 구조와 작업 흐름을 유지하기 위해 만들어졌습니다.

## 목적

새 프로젝트를 시작할 때마다 반복되는 작업 — docs 구조 설정, 정책 문서 작성, 이슈 추적,
한국어 번역 동기화 — 을 Claude Code 스킬로 표준화합니다.

한 번 설치하면 모든 프로젝트에서 동일한 명령어로 동일한 품질의 문서 시스템을 구축할 수 있습니다.

## 스킬 목록

| 스킬 | 명령어 | 용도 |
| --- | --- | --- |
| init-docs | `/init-docs` | 새 프로젝트에 표준 `docs/` 구조를 생성한다 |
| new-issue | `/new-issue` | 다음 번호의 이슈 문서와 한국어 번역을 생성한다 |
| sync-translations | `/sync-translations` | `docs/ko/`의 한국어 번역 누락 및 구식 항목을 감지하고 동기화한다 |
| new-policy | `/new-policy` | 새 정책 문서와 한국어 번역을 추가한다 |
| frontend-planning | `/frontend-planning` | 프론트엔드 프로젝트의 6단계 기획 문서를 순차 생성한다 |

## 설치

```bash
npx skills add https://github.com/ywj3493/claude-skills.git
```

해당 명령어 사용 후 가이드에 따라 선택

## 사용법

스킬 설치 후, Claude Code 세션에서 다음 명령어를 호출합니다.

```text
/init-docs           ← 새 프로젝트 시작 시 최초 1회 실행
/new-issue           ← 새 작업을 시작할 때마다 실행
/sync-translations   ← 한국어 번역 동기화가 필요할 때 실행
/new-policy          ← 새 규칙을 공식화할 때 실행
/frontend-planning   ← 프론트엔드 프로젝트 기획 문서 6단계 생성
```

## 전형적인 작업 흐름

```text
새 프로젝트
  └─ /init-docs              docs/ 구조 + 정책 파일 + CLAUDE.md 생성
      └─ /new-issue          issue001.md + 한국어 번역 생성, 작업 시작
          └─ 구현 작업...
              └─ /new-issue          이후 작업마다 반복
              └─ /new-policy         새 규칙이 필요할 때
              └─ /sync-translations  번역 누락이 생겼을 때
              └─ /frontend-planning  프론트엔드 기획 문서가 필요할 때
```

## 저장소 구조

```text
templates/              # 재사용 가능한 파일 템플릿
  CLAUDE.md             # 새 프로젝트 루트에 배치하는 표준 CLAUDE.md (루트와 동일)
skills/                 # Claude Code 스킬 정의
  init-docs/            # /init-docs 스킬
  new-issue/            # /new-issue 스킬
  sync-translations/    # /sync-translations 스킬
  new-policy/           # /new-policy 스킬
  frontend-planning/    # /frontend-planning 스킬
docs/                   # 이 저장소 자체의 문서 (init-docs로 생성됨)
  en/                   # 영어 문서
    policy/             # 작업 규칙
    issue/              # 작업 추적 이슈
    specifications/     # 설계 문서
  ko/                   # 한국어 번역
    policy/
    issue/
    specifications/
  reference/            # 참조 자료 (언어 무관, 사용자 관리)
```

## 템플릿

`templates/CLAUDE.md`는 루트 `CLAUDE.md`와 동일한 내용입니다.
이 저장소 자체가 스킬과 템플릿의 동작을 검증하는 기준이 됩니다.

새 프로젝트에 수동으로 복사할 수도 있습니다:

```bash
cp /path/to/this/repo/templates/CLAUDE.md /path/to/new-project/CLAUDE.md
```

## 스킬 개발 가이드

### 기존 스킬 수정

1. `SKILL.md`를 편집한다 — YAML 프론트매터(`name`, `description`)를 정확하게 유지한다
2. 스킬이 의존하는 `scripts/` 또는 `references/`를 업데이트한다

### 새 스킬 추가

1. `skills/<skill-name>/SKILL.md`를 YAML 프론트매터와 마크다운 지시사항으로 작성한다
2. 필요한 경우 `scripts/` 또는 `references/` 하위 디렉토리를 추가한다
3. 이 README에 스킬을 문서화한다
