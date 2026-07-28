---
name: translate-docs
version: 0.0.1
description: docs/config.yml에 설정된 원본 언어 문서 디렉터리를 감사해 번역이 없는 문서나 원본보다 오래된 번역을 찾아 생성·갱신한다. 번역 언어가 아직 설정되지 않았으면 미러링을 켤지 제안하고, 선택한 언어를 docs/config.yml에 기록한 뒤 미러 디렉터리를 만들고 동기화한다. "번역 동기화", "문서 번역해줘", "미러 맞춰줘", "번역 언어 추가"에 반응한다.
---

# translate-docs

`docs/config.yml`에 설정된 언어 쌍에 따라 번역 미러 디렉터리를 원본 문서와
동기화한다. 아래 예시는 기본 쌍인 `ko` → `en`을 기준으로 한다.

## 사용 시점

- 사용자가 "번역 동기화", "문서 번역해줘", "미러 맞춰줘"라고 말할 때
- 프로젝트가 미러링을 **시작**하려 할 때: 문서가 원본 언어만으로 초기화되어
  있고(`translation_languages: []`) 이제 번역 언어를 추가하려는 경우
- 문서를 여러 개 갱신한 뒤 번역이 빠졌을 수 있을 때
- 주기적으로 번역 완성도를 감사할 때

## 범위 디렉터리

설정된 번역 언어마다 (여기서는 `en`을 예로 든다):

| 원본 (`docs/<원본>/`) | 번역 (`docs/<대상>/`) |
|---|---|
| `docs/ko/specifications/` | `docs/en/specifications/` |

`specifications/` 아래를 **재귀적으로** 훑는다. `<도메인>/design/backend/`
같은 깊은 경로도 포함된다.

`docs/reference/`는 **제외한다** — 사용자가 관리하고 언어 중립이므로 번역이
필요 없다. `.claude/rules/`도 제외한다 — 영어 전용 Claude Code 설정이며
번역 대상이 아니다. 이 플러그인은 이슈를 다루지 않으므로 `issue/`도 범위에
없다.

## 실행 규약

이 규칙들은 스킬 계약의 일부다. 어느 모델이 실행하든 번역 품질이 같도록
작업 방식을 명시한다.

1. **빠짐없이 감사한다.** 누락·노후 목록은 실제 `find` 출력에서 도출해야
   하며 설정된 모든 번역 언어의 모든 원본 파일을 포함한다. 표본 추출도,
   "대표적인 일부"도 없다. 정확한 개수를 보고한다.

2. **타임스탬프는 어림짐작이다.** git 커밋 날짜 비교는 오탐을 만든다(예:
   원본 파일만 건드린 서식 수정 커밋). 노후로 표시된 기존 번역을 다시
   쓰기 전에 실제 내용을 비교하고, 번역이 이미 원본을 반영하고 있으면
   건너뛴다 — 그리고 그 사실을 리포트에 적는다.

3. **디스크에서 읽어 전부 번역한다.** 번역 직전에 원본 문서를 통째로 다시
   읽는다. 기억으로, 요약으로, 앞선 대화의 발췌로 번역하지 않는다. 긴
   파일도 전부 번역한다 — "..." 나 "(이하 동일)"로 자르지 않는다.

4. **구조 동등성을 검증한다.** 각 번역을 쓴 뒤 원본과 대조한다: 제목 수,
   코드 블록 수, **mermaid 블록 수**, 표 행 수, 체크박스 항목 수가 같은
   순서로 일치해야 한다. 어긋나면 다음 파일로 넘어가기 전에 고친다.

5. **번역 디렉터리 아래에만 쓴다.** 원본 언어 문서와 `docs/reference/`는
   이 스킬에게 읽기 전용이다. 번역 중에 원본 파일의 오류를 발견해도
   "고쳐 주지" 않는다 — 리포트에 보고한다.

6. **파일마다 보고한다.** 최종 리포트는 생성·갱신·건너뜀 파일을 전부
   나열하고, 건너뛴 것은 이유를 적는다. 실제로 쓰고 검증하지 않은 파일을
   동기화됨으로 보고하지 않는다.

7. **설정 변경은 동의를 받고만 한다.** `docs/config.yml`은 사용자가 어떤
   번역 언어를 추가할지 명시적으로 확인한 뒤에만 갱신한다(단계 0). 언어
   선택을 가정하고 번역 언어를 추가하거나, 미러 디렉터리를 만들거나,
   무언가를 번역하지 않는다.

## 단계별 지침

### 단계 0: 언어 설정 로드

1. `docs/config.yml`에서 `source_language`와 `translation_languages`를 읽는다.

2. 파일이 없으면 디렉터리 배치에서 설정을 추론한다: `docs/` 아래의 언어
   코드 디렉터리(`reference/` 제외). `ko/`가 있으면 원본으로, 나머지를 번역
   대상으로 본다. 추론했다는 사실을 최종 리포트에 밝히고
   `docs/config.yml`에 기록할 것을 제안한다.

3. `docs/`가 없거나 언어 디렉터리가 하나도 없으면 멈추고 사용자에게 알린다:

   > 문서 구조를 찾지 못했습니다. `/explainable:init-planning`으로 기획
   > 문서를 먼저 만들거나, `/dev-docs:init-docs`로 전체 문서 구조를
   > 초기화해 주세요.

4. `translation_languages`가 비어 있으면(원본 언어만 초기화한 경우의 기본값)
   멈추지 말고 미러링을 켤지 제안한다:

   > 번역 언어가 아직 설정되지 않았습니다(`docs/config.yml`의
   > `translation_languages: []`). 지금 추가할까요?
   > 미러링은 `specifications/` 전체의 번역본을 원본 언어와 동기화된
   > 상태로 유지합니다 — 예를 들어 영어 미러라면 `en`입니다.

   - 사용자가 **거절하면** 멈춘다 — 프로젝트는 원본 언어만 유지한다.
   - 사용자가 **언어를 하나 이상 지정하면**, 각 대상 언어 `<대상>`에 대해:

     1. `docs/config.yml`을 갱신한다: `translation_languages: []`를 선택한
        언어 코드 목록으로 바꾼다. 파일의 나머지(주석, `source_language`)는
        그대로 둔다.
     2. 미러 디렉터리를 `.gitkeep`과 함께 만든다:

        ```bash
        mkdir -p docs/<대상>/specifications
        touch docs/<대상>/specifications/.gitkeep
        ```

     3. 단계 1로 진행한다 — 감사에서 모든 원본 문서가 누락으로 잡히고,
        평소 흐름대로 번역된다.

설정된 번역 언어마다 단계 1~4를 한 번씩 실행한다. 아래 명령은 기본 쌍인
`ko` → `en`을 보여준다. 실제 언어 코드로 바꿔 쓴다.

### 단계 1: 감사 — 누락된 번역 찾기

범위 디렉터리의 모든 원본 파일을 나열한다:

```bash
find docs/ko/specifications \
  -name "*.md" ! -name ".gitkeep" 2>/dev/null | sort
```

찾은 파일마다(예: `docs/ko/specifications/order/planning/requirements.md`)
대응하는 번역이 있는지 확인한다(예:
`docs/en/specifications/order/planning/requirements.md`).

번역이 없는 파일들로 **누락** 목록을 만든다.

### 단계 2: 감사 — 노후된 번역 찾기

번역이 있는 파일은 git으로 수정 시각을 비교한다:

```bash
git log --follow -1 --format="%ai" -- docs/ko/specifications/order/planning/requirements.md
git log --follow -1 --format="%ai" -- docs/en/specifications/order/planning/requirements.md
```

원본 문서의 커밋이 번역보다 최근이면 **노후** 목록에 넣는다.

### 단계 3: 리포트와 확인

사용자에게 알린다:

> 동기화 감사를 마쳤습니다:
>
> **누락된 번역** (`<N>`개):
> - docs/ko/specifications/order/planning/requirements.md
> - docs/ko/specifications/architecture.md
>
> **노후 가능성** (`<N>`개):
> - docs/ko/specifications/glossary.md (원본 2026-07-20 수정, 번역 2026-07-12 수정)
>
> 전부 생성·갱신할까요?

파일을 쓰기 전에 확인을 기다린다.

### 단계 4: 번역 생성·갱신

누락 또는 노후 목록의 각 파일에 대해:

1. 원본 파일을 통째로 읽는다
2. 산문 내용을 대상 언어로 번역한다
3. 같은 파일명으로 대응하는 번역 경로에 쓴다

**명명 규칙**: `docs/<원본>/`을 `docs/<대상>/`으로 바꾸고 나머지 경로와
파일명은 그대로 둔다. `ko` → `en`의 예:

- `docs/ko/specifications/architecture.md` →
  `docs/en/specifications/architecture.md`
- `docs/ko/specifications/order/design/backend/sequence-diagram.md` →
  `docs/en/specifications/order/design/backend/sequence-diagram.md`

### 단계 5: 결과 보고

생성·갱신한 모든 파일을 경로와 함께 나열한다.

## 번역 규칙

**대상 언어로 번역할 것:**

- 모든 산문 문단과 문장
- 섹션 제목
- 목록 항목 설명
- 표의 셀 텍스트

**번역하지 않을 것** — 이 목록을 빠뜨리면 번역본에서 검증 루프와 후속
도구가 전부 깨진다:

- **코드 블록(``` ... ```) 내부** — 절대 내용을 번역하지 않는다
- **`mermaid` 블록 내부 전체** — 참여자 별칭, `Note`의 `경로:줄번호`,
  `link` 줄, 노드 라벨. 라벨 하나만 번역해도 `citation-verifier`의
  `Note` ↔ `CALLGRAPH` 교차 검증이 깨진다
- **숨김 `<!-- CALLGRAPH: ... -->` 블록** 전체
- **`api-interface.md`의 계약 블록** 전체 (OpenAPI / SDL / `.proto` /
  AsyncAPI 무엇이든) — 스키마·경로·오퍼레이션 ID는 계약이다. 번역 대상은
  설명 필드뿐이며 그것도 선택이다
- **근거 표시**: `[REF: 경로:줄번호]`,
  `[ASSUMED: <추론>; basis: <근거>]`
- **검증 판정 어휘**: `MATCHED`, `MISMATCHED`, `UNSUPPORTED`, `EXCLUDED`
- **모든 ID**: `FR-`, `NFR-`, `US-`, `AC-`, `UC-`, `T-`, `FLOW-` 접두사와
  그 뒤의 식별자 전체
- **구조 마커**: `<!-- OWNER: ... -->`, `<!-- GENERATED-BY: ... -->`
- 파일 경로 (`docs/ko/specifications/architecture.md`)
- 함수명, 변수명, 클래스명
- 브랜치명과 명령줄 예시
- 기술 약어: API, URL, HTTP, JSON, Git 등
- 체크박스 표시: `- [ ]`, `- [x]`

**기술 약어의 첫 등장 시**에는 괄호로 대상 언어 설명을 덧붙일 수 있고,
이후로는 약어만 쓴다.

**마크다운 구조를 정확히 보존한다:**

- 같은 제목 수준 (`#`, `##`, `###`)
- 같은 목록·체크박스 서식
- 같은 굵게·기울임 표시
- 같은 수평선과 표 구조
- **같은 개수의 mermaid 블록**
