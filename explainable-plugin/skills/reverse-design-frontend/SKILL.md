---
name: reverse-design-frontend
version: 0.1.0
description: 이미 있는 프론트엔드 코드베이스에서 설계 문서를 한국어로 역추출한다. 인프라 탐색 → 프레임워크 감지 → FSD 적합도 판정 → 앱 셸 1회 추적 → 라우트별 코드·렌더링 흐름 추적 순서로 진행하며, 모든 주장에 [REF: 경로:줄번호] 인용을 붙이고 citation-verifier로 검증한다. "프론트엔드 분석해줘", "화면 구조 파악해줘", "렌더링 흐름 문서화"에 반응한다. React를 가정하지 않는다. 코드가 없는 새 화면 설계에는 쓰지 않는다 — 그건 init-design-frontend의 일이다.
---

# reverse-design-frontend

이미 동작하는 프론트엔드 코드에서 **코드 흐름과 렌더링 흐름**을 근거와 함께
문서로 만든다.

**순서가 이 스킬의 핵심이다.** 인프라 → 프레임워크 감지 → FSD 적합도 판정 →
앱 셸 → 라우트. 프레임워크가 무엇인지 모르는 채로 파일을 읽기 시작하면
라우트 정의조차 찾지 못한다.

**시작 전에 로드한다**:
`${CLAUDE_PLUGIN_ROOT}/references/common-rules.md` ·
`${CLAUDE_PLUGIN_ROOT}/references/reverse-rules.md` ·
`${CLAUDE_PLUGIN_ROOT}/references/frontend-rules.md`

## 사용 시점

- 인수인계받은 프론트엔드를 파악해야 할 때
- "프론트엔드 분석해줘", "화면 구조 파악해줘", "렌더링 흐름 문서화"
- 어느 상태가 어디서 바뀌는지 추적해야 할 때

## 사용하지 않는 경우

- **코드가 아직 없는 경우** — `init-design-frontend`
- **프론트엔드가 없는 프로젝트** — `common-rules.md` §6.1
- **백엔드 분석** — `reverse-design-backend`
- **요구사항·유저 스토리가 필요한 경우** — 이 스킬을 먼저 돌리고
  `reverse-planning`을 실행한다.

## 실행 규약

`common-rules.md` 실행 규약 1~9, `reverse-rules.md`, `frontend-rules.md`를
전부 따른다. 이 스킬 고유 항목:

1. **프레임워크를 추측하지 않는다.** 단계 2에서 감지한 값만 쓰고, 그 값을
   모든 에이전트 호출에 입력으로 넘긴다.
2. **FSD는 대조 기준일 뿐이다** (`frontend-rules.md` §2). 코드가 FSD를 따르지
   않으면 실제 구조를 기록하고 대비표만 붙인다. 억지로 재분류하거나
   리팩터링을 제안하지 않는다.
3. **에이전트의 `state.scope`가 문서 배분을 결정한다** (`frontend-rules.md`
   §3).

## 산출물

```text
docs/<원본 언어>/specifications/
├── infrastructure.md            # 단계 1 (프론트엔드 관련 부분 병합)
├── architecture.md              # 단계 2 (프론트엔드 구조 섹션)
├── glossary.md
├── domain-map.md                # 단계 8 (프론트엔드 슬라이스 의존 맵)
└── <도메인>/design/frontend/
    ├── fsd-structure.md
    ├── routing.md
    ├── component-tree.md
    ├── render-flow.md
    ├── state-flow.md
    └── user-flows.md
```

## 단계별 지침

### 단계 0: 환경 감지와 재실행 판단

1. `common-rules.md` §1 — 문서 환경 감지, 분석 기준 커밋 확정, 리뷰 모드.
2. `reverse-rules.md` §3 — 재실행 판단. **폐기 범위는
   `<도메인>/design/frontend/**`**이며, 횡단 문서와 `glossary.md`는 폐기하지
   않는다.

### 단계 1: 인프라 탐색

**산출** `specifications/infrastructure.md` ·
**템플릿** `templates/overview/infrastructure.md`

1. **`infrastructure.md`가 이미 있고 `분석 기준 커밋`이 현재 HEAD와 같으면
   건너뛴다** — `reverse-design-backend`가 방금 만들었을 수 있다. 그 사실을
   완료 리포트에 남긴다.
2. 그렇지 않으면 **`infra-explorer` 에이전트를 호출한다.**
3. 반환된 `INFRA` 블록에서 **프론트엔드 관련 항목**을 병합한다: 빌드 도구,
   번들러, 정적 자산 배포 대상, 클라이언트에 노출되는 환경 변수, CDN 설정.
4. **환경 변수의 값을 절대 적지 않는다.** 클라이언트 번들에 들어가는 변수는
   특히 주의해서 이름만 적는다.
5. 백엔드가 쓴 섹션은 바이트 단위로 보존한다 (계약 6).

### 단계 2: 프레임워크 감지와 코드베이스 구조

**산출** `specifications/architecture.md`의 `## 프론트엔드 구조`와
`## 아키텍처 규약` 표의 프론트엔드 행

이 단계의 산출물이 **이후 모든 에이전트 호출의 입력**이 된다.

1. **프론트엔드가 있는지 확인한다.** 없으면 멈춘다:

   > 이 저장소에서 프론트엔드 코드를 찾지 못했습니다.
   > 확인한 경로: `<경로들>`
   > 백엔드 분석은 `/explainable:reverse-design-backend`를 사용하세요.

2. **감지된 프레임워크 환경 표를 채운다.** 각 항목에 인용을 붙인다.

   | 항목 | 어디서 확인하나 |
   |---|---|
   | 프레임워크 | 패키지 매니페스트와 잠금 파일 |
   | **라우트 정의 파일 패턴** | 라우터 설정 또는 파일 기반 라우팅 규칙 |
   | 상태 관리 | 매니페스트의 의존성과 실제 사용처 |
   | 데이터 조회 계층 | 서버 통신 코드의 공통 패턴 |
   | 렌더링 모드 | 프레임워크 설정과 페이지별 지시 |

   **라우트 정의 파일 패턴이 특히 중요하다** — 이것이 없으면 에이전트가
   라우트 경계를 찾지 못한다.

3. **FSD 레이어 ↔ 디렉터리 매핑을 시도한다.** 대응되지 않는 디렉터리는
   `미분류`로 둔다.
4. **`## 아키텍처 규약`의 스택 표와 레이어 매핑 표에 프론트엔드 행을
   채운다.** 백엔드 행은 보존한다.

### 단계 3: FSD 적합도 판정

**산출** `<도메인>/design/frontend/fsd-structure.md` ·
**템플릿** `templates/design/frontend/fsd-structure.md`

1. **FSD 준수 여부를 판정한다**: 준수 / 부분 준수 / 따르지 않음.
2. **따르지 않으면 실제 구조를 먼저 기록하고** FSD 대비표를 붙인다. 개요에
   그 사실과 실제 구조를 쓴다.
3. 대응되지 않는 레이어는 "대응 없음"으로 두고, 그것이 정보다.
4. 슬라이스 목록과 공개 API를 인용과 함께 기록한다.
5. 세그먼트 구성 표의 `이 프로젝트의 이름` 열에 실제 이름을 적고 표준
   세그먼트와 대응시킨다.
6. **의존 규칙 위반을 이 도메인 범위에서 기록한다** (`reverse-rules.md` §5).
7. `domain-model.md`가 있으면 `entities` 슬라이스와 애그리거트를 용어집을
   매개로 대응시킨다. 없으면 그 섹션을 삭제한다.

### 단계 4: 라우트·도메인 식별 — 리뷰 게이트 ①·②

1. **라우트를 전부 나열한다.** 단계 2에서 확정한 라우트 정의 파일 패턴으로
   찾고, 각 라우트의 진입점 `경로:줄번호`를 기록한다.
2. **도메인에 매핑한다.** 백엔드가 이미 도메인을 정했으면 그것을 따르고,
   프론트엔드 전용 프로젝트면 라우트 그룹과 슬라이스로 제안한다.
3. **사용자에게 제시하고 확인받는다:**

   > 라우트 `<N>`개를 찾았습니다. 도메인 매핑은 다음과 같습니다:
   >
   > | 도메인 | 라우트 | 근거 |
   > |---|---|---|
   >
   > 이대로 진행할까요?

4. 20개 상한은 `common-rules.md` §6.3, 모노레포 앱 경계는 §6.2를 따른다.

### 단계 5: 앱 셸 추적 (1회)

**산출** `<도메인>/design/frontend/render-flow.md`의 `## 앱 셸` 섹션 ·
**템플릿** `templates/design/frontend/render-flow.md`

1. **`render-flow-tracer`를 `mode: shell`로 한 번만 호출한다.**

2. **에이전트에 넘기는 입력:**

   | 입력 | 출처 |
   |---|---|
   | 저장소 루트 | 단계 0 |
   | `mode: shell` | — |
   | 애플리케이션 진입점 `경로:줄번호` | 단계 2 |
   | 감지된 프레임워크·라우터·상태 라이브러리·데이터 조회 계층 | 단계 2 |
   | 라우트 정의 파일 패턴 | 단계 2 |
   | FSD 레이어 ↔ 디렉터리 매핑 | 단계 2·3 |
   | 용어집 항목 | 현재까지 확정된 것 |

3. 반환된 `RENDER_TRACE`에서 진입점부터 라우터 해석까지의 시퀀스
   다이어그램, 단계 표, 전역 가드 표를 만든다.
4. **셸 추적 요약을 보관한다.** 단계 6의 모든 라우트 호출에 입력으로 넘긴다.

### 단계 6: 라우트별 흐름 추적

**산출** `<도메인>/design/frontend/{render-flow,component-tree,state-flow,routing}.md` ·
**템플릿** `templates/design/frontend/` 아래 각 파일

호출 방식·`PARTIAL` 처리·별칭 재배정은 `reverse-rules.md` §4가 소유한다.

1. **입력은 단계 5와 같되 다음을 추가한다:** `mode: route`, 대상 라우트
   패턴과 진입점 `경로:줄번호`, 그리고 **셸 추적 요약** — 이것이 있어야
   에이전트가 셸을 다시 훑지 않는다.

2. **반환 데이터를 네 문서로 배분한다.**

   | 에이전트 필드 | 가는 문서 |
   |---|---|
   | `route`, `guards` | `routing.md` |
   | `ui_tree` | `component-tree.md` |
   | `participants`, `edges`, `branches` | `render-flow.md`의 시퀀스 다이어그램 |
   | `entry`, `render_mode`, `data_sources`, `render_boundaries`, `rerender_triggers` | `render-flow.md` |
   | `state` (`scope: local`) | `render-flow.md` |
   | `state` (`scope: shared` 또는 `server`) | `state-flow.md` |
   | `navigation` | `routing.md`의 라우트 전환 표 |

   **`edges`와 `ui_tree`를 섞지 않는다.** `edges`는 시퀀스 다이어그램의
   원료이고 `ui_tree`는 구조 문서의 원료다.

3. **`render-flow.md`의 라우트 섹션**을 만든다. 제목은
   `### FLOW-<도메인>-<라우트 슬러그>: <라우트 이름>`이다. 각 `RENDER_TRACE`의
   데이터 하나에서 시퀀스 다이어그램·`Note`·`CALLGRAPH`를 함께 렌더링한다.
   **앱 셸 부분은 다시 그리지 않는다.**

4. `state-flow.md`의 캐시 키·무효화 계기와 `routing.md`의 접근 제어는
   `frontend-rules.md` §4.4~4.5를 따른다. 코드에서 무효화 계기를 찾지 못하면
   `[ASSUMED: ...]`로 표시한다.

### 단계 7: 유저 플로우 역추출

**산출** `<도메인>/design/frontend/user-flows.md` ·
**템플릿** `templates/design/frontend/user-flows.md`

1. `routing.md`의 라우트 전환 표와 각 라우트의 UI 단위에서 사용자 여정을
   조립한다.
2. `flowchart TD`로 그린다. **노드는 사용자가 보는 것**, **간선은 사용자
   행동**이다.
3. **서버 처리는 노드 하나로 뭉뚱그리고 `FLOW-` 키를 링크만 한다**
   (`frontend-rules.md` §4.1).
4. 예외 경로를 반드시 채우고 `render-flow.md`의 오류 경계와 대응시킨다.
5. **의도를 추론한 부분에는 배너를 넣는다** (`reverse-rules.md` §1.4) —
   사용자 여정의 "왜"는 코드에 없다.

### 단계 8: 슬라이스 의존 맵

**산출** `specifications/domain-map.md`의 `## 프론트엔드 슬라이스 의존 맵`

1. **슬라이스 간 import를 전부 수집한다.** 각 간선에 인용을 붙인다.
2. **정상 의존과 규칙 위반을 구분해 그린다.** 정상은 실선, 위반은 점선에
   위반 스타일 (`reverse-rules.md` §5).
3. 다른 스킬이 쓴 섹션은 바이트 단위로 보존한다 (계약 6).

### 단계 9: 검증과 수정 루프

`common-rules.md` §3의 인용 검증과 결정적 검사를 실행한다.
`render-flow.md`는 시퀀스 다이어그램을 담으므로 `Note` ↔ `CALLGRAPH` 양방향
교차 검증까지 받는다.

### 단계 10: 완료 리포트 — 리뷰 게이트 ③

`common-rules.md` §4에 다음을 더한다: 추적하지 않은 라우트와 그 이유,
FSD 준수 판정 결과와 발견한 규칙 위반 개수.

> 프론트엔드 설계 문서화가 끝났습니다.
>
> - 요구사항과 유저 스토리를 역산하려면 `/explainable:reverse-planning`
> - 백엔드가 아직이면 `/explainable:reverse-design-backend`
> - 번역 미러가 필요하면 `/explainable:translate-docs`

## 문서 규칙

`common-rules.md` §5와 `frontend-rules.md` §1의 중립 어휘를 따른다.
**`분석 기준 커밋`을 반드시 채운다.**
