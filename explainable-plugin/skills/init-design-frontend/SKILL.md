---
name: init-design-frontend
version: 0.1.0
description: 기획 문서를 입력으로 프론트엔드 설계 문서를 한국어로 작성한다. FSD(Feature-Sliced Design)를 기준선으로 레이어·슬라이스 구조, 라우팅, UI 구성, 렌더링 흐름, 상태 흐름, 유저 플로우를 만들고 테스트 명세의 프론트엔드·E2E 섹션을 채운다. "프론트엔드 설계해줘", "화면 구조 잡아줘", "컴포넌트 설계", "라우팅 설계"에 반응한다. React를 가정하지 않으며 프레임워크는 architecture.md의 결정을 따른다. 이미 있는 코드를 문서화하는 데는 쓰지 않는다 — 그건 reverse-design-frontend의 일이다.
---

# init-design-frontend

기획 문서가 정한 **무엇을**을 화면 구조와 흐름으로 옮긴다. 프론트엔드만
다룬다.

**시작 전에 로드한다**:
`${CLAUDE_PLUGIN_ROOT}/references/common-rules.md` ·
`${CLAUDE_PLUGIN_ROOT}/references/frontend-rules.md`

## 사용 시점

- `init-planning`이 끝난 뒤
- "프론트엔드 설계해줘", "화면 구조 잡아줘", "라우팅 설계"
- 기획은 이미 있고 클라이언트 쪽 구조만 필요할 때

## 사용하지 않는 경우

- **기획 문서가 없는 경우** — `init-planning`을 먼저 실행한다.
- **이미 코드가 있는 경우** — `reverse-design-frontend`
- **프론트엔드가 없는 프로젝트** — `common-rules.md` §6.1에 따라 "해당 없음"을
  보고하고 멈춘다.
- **백엔드 설계** — `init-design-backend`

## 실행 규약

`common-rules.md`의 실행 규약 1~9와 `frontend-rules.md` 전체를 따른다.
이 스킬 고유 항목:

1. **입력을 디스크에서 읽는다** (계약 2): `requirements.md`,
   `user-stories.md`, `api-interface.md`, `architecture.md`, `glossary.md`.
2. **`FLOW-<도메인>-<라우트 슬러그>` 키를 라우트마다 부여한다.**
3. **`## 읽은 소스`를 생성하지 않는다** (계약 7). `분석 기준 커밋`은
   "해당 없음".

FSD 기준선, 프레임워크 중립 어휘, 문서 간 책임 경계는 `frontend-rules.md`가
소유한다.

## 산출물

```text
docs/<원본 언어>/specifications/<도메인>/
├── design/frontend/
│   ├── fsd-structure.md
│   ├── routing.md
│   ├── component-tree.md
│   ├── render-flow.md
│   ├── state-flow.md
│   └── user-flows.md
└── verification/test-spec.md     # 프론트엔드(T-2NN)·E2E(T-3NN) 섹션
```

## 단계별 지침

### 단계 0: 입력 확인

1. `common-rules.md` §1의 문서 환경 감지와 리뷰 모드 확인을 수행한다.
2. **선행 기획 문서를 확인한다.** 없으면 멈춘다:

   > `<도메인>/planning/`에 기획 문서가 없습니다.
   > `/explainable:init-planning`을 먼저 실행해 주세요.

3. **프론트엔드가 있는 프로젝트인지 확인한다.** 없으면:

   > 이 프로젝트에는 프론트엔드가 없습니다. 프론트엔드 설계 문서를 만들지
   > 않고 종료합니다.

4. **FSD 채택 여부를 확인한다.** `architecture.md`에 이미 기록되어 있으면
   그것을 따른다. 없으면 묻는다:

   > 프론트엔드 구조로 FSD(app / pages / widgets / features / entities /
   > shared)를 제안합니다. 이대로 갈까요, 아니면 다른 구조를 쓸까요?

   FSD를 쓰지 않기로 하면 `fsd-structure.md` 자리에 사용자가 정한 구조를
   기록하고, 이후 단계의 레이어 관련 표를 그 구조에 맞춘다.

5. **기존 설계 문서를 확인한다.** 있으면 덮어쓰지 않고 확인받는다.

### 단계 1: FSD 구조

**산출** `<도메인>/design/frontend/fsd-structure.md` ·
**템플릿** `templates/design/frontend/fsd-structure.md`

1. `architecture.md`의 레이어 ↔ 디렉터리 매핑에서 프론트엔드 행을 읽는다.
2. 레이어 구성 표를 채운다 (`frontend-rules.md` §4.6 — 안 쓰는 레이어의
   행을 지우지 않는다).
3. 슬라이스를 정한다. 이름은 `glossary.md`의 영문 식별자를 따른다.
4. 세그먼트 구성 표에서 실제로 쓸 세그먼트만 남긴다.
5. **`## 백엔드 도메인 모델과의 대응`** — `domain-model.md`가 있으면
   `entities` 슬라이스와 애그리거트를 용어집을 매개로 연결한다. 둘이 1:1일
   필요는 없다 — 다른 부분이 이 표의 정보다. 백엔드가 없으면 섹션을 삭제한다.

> **단계 1 완료**: FSD 구조를 작성했습니다. 검토 후 라우팅으로 진행할까요?

### 단계 2: 라우팅

**산출** `<도메인>/design/frontend/routing.md` ·
**템플릿** `templates/design/frontend/routing.md`

1. `user-stories.md`의 각 스토리가 어떤 화면을 필요로 하는지 도출한다.
2. 라우트 트리를 그린다. 동적 구간 표기는 `architecture.md`에 기록된 라우터의
   표기를 따른다.
3. `FLOW-<도메인>-<라우트 슬러그>` 키를 각 라우트에 부여한다.
4. `frontend-rules.md` §4.3~4.4 (관련 스토리 열, 접근 제어 명시)를 적용한다.
5. **라우트 전환 표에는 간선만 적는다** — 전체 여정 서술은 `user-flows.md`의
   일이다.

### 단계 3: UI 구성

**산출** `<도메인>/design/frontend/component-tree.md` ·
**템플릿** `templates/design/frontend/component-tree.md`

1. 라우트마다 UI 단위 트리를 그린다. 각 노드에 FSD 레이어·슬라이스를 괄호로
   표시해 슬라이스 경계가 보이게 한다.
2. 조건부는 `(조건부)`, 반복은 `(반복)`을 붙인다. 조건의 내용은
   `render-flow.md`의 일이다.
3. 공용 UI 단위는 두 개 이상의 화면에서 쓰이는 것만 적는다.
4. **입출력 계약은 공용 단위와 슬라이스 공개 API만 적는다.** 내부 구현
   단위까지 적으면 코드가 바뀔 때마다 문서가 틀린다.

> **단계 3 완료**: UI 구성을 작성했습니다. 검토 후 렌더링 흐름으로
> 진행할까요?

### 단계 4: 렌더링 흐름

**산출** `<도메인>/design/frontend/render-flow.md` ·
**템플릿** `templates/design/frontend/render-flow.md`

1. **`## 앱 셸`을 한 번만 기술한다** (`frontend-rules.md` §4.2).
2. **Source-Linked 모드 요소를 전부 생략한다** — 코드가 없다.
3. 라우트마다 한 섹션. 제목은
   `### FLOW-<도메인>-<라우트 슬러그>: <라우트 이름>`이며, **앱 셸 부분은
   다시 그리지 않고 라우트 경계 안쪽부터** 시작한다.
4. **데이터 조회 표** — `조회 시점`은 "라우트 진입 전 / 렌더 중 / 렌더 후 /
   사용자 행동 시" 중에서 정한다. `대상 오퍼레이션`은 `api-interface.md`의
   오퍼레이션 ID와 일치해야 한다.
5. **지역 상태 표** — 이 라우트를 벗어나면 사라지는 상태만.
6. **재렌더 유발 요인 표** — 무엇이 바뀌면 어떤 UI 단위가 다시 그려지는지.
   성능 문제의 근원이 여기서 보인다.
7. `## 로딩·오류 경계`의 재시도 정책은 `api-interface.md` 오류 모델의
   `재시도 가능` 열과 일치해야 한다.

### 단계 5: 상태 흐름

**산출** `<도메인>/design/frontend/state-flow.md` ·
**템플릿** `templates/design/frontend/state-flow.md`

1. **`## 상태 분류` 표를 먼저 채운다.** 이 표가 있어야 새 상태가 생겼을 때
   어디에 둘지 판단할 수 있다.
2. **서버 상태** — `frontend-rules.md` §4.5 (무효화 계기와 캐시 키 일치).
3. **클라이언트 공유 상태** — 저장소 단위로 나눠 적는다.
4. **낙관적 갱신을 쓴다면 실패 시 복구 방법이 반드시 있어야 한다.** 없으면
   낙관적 갱신을 설계하지 않는다.
5. **`## 상태 간 의존`에서 순환이 있으면 반드시 기록한다** — 무한 갱신의
   원인이 된다.

> **단계 5 완료**: 상태 흐름을 작성했습니다. 검토 후 유저 플로우로
> 진행할까요?

### 단계 6: 유저 플로우

**산출** `<도메인>/design/frontend/user-flows.md` ·
**템플릿** `templates/design/frontend/user-flows.md`

1. 유저 스토리 하나에 플로우 하나가 기본이다.
2. `flowchart TD`로 그린다. **노드는 사용자가 보는 화면이나 결정**, **간선은
   사용자 행동**이다.
3. **서버 처리는 노드 하나로 뭉뚱그리고 `FLOW-` 키를 링크만 한다**
   (`frontend-rules.md` §4.1).
4. 예외 경로 표를 반드시 채운다. 오류 코드는 `api-interface.md`를 링크하고
   여기서 정의하지 않는다.
5. `## 진입점` — 다른 도메인에서 넘어오는 경로는 `domain-map.md`의 횡단
   흐름과 일치해야 한다.

### 단계 7: 테스트 명세 프론트엔드·E2E 섹션

**산출** `<도메인>/verification/test-spec.md` ·
**템플릿** `templates/verification/test-spec.md`

1. 파일이 없으면 템플릿에서 만들고, 있으면 **프론트엔드·E2E 섹션만
   갱신한다.** 백엔드 섹션은 보존한다.
2. **테스트 ID 대역**: 프론트엔드 `T-2NN`, E2E `T-3NN`.
3. E2E는 유저 플로우 하나에 하나가 기본이다. **모든 인수 기준을 E2E로
   덮으려 하지 않는다** — 느리고 깨지기 쉽다. 정상 경로와 치명적 실패
   경로만 E2E로 두고 나머지는 아래 계층에 맡긴다.
4. 순방향이므로 `상태` 열은 전부 `미구현`, `근거` 열은 비운다.

### 단계 8: 도메인 지도와 추적성 갱신

1. **`domain-map.md`의 `## 프론트엔드 슬라이스 의존 맵`** — 슬라이스 간 참조
   그래프를 그린다. 정상 의존은 실선, 규칙 위반은 점선에 위반 스타일.
   **순방향에서 규칙 위반이 나오면 설계 결함이므로 기록만 하지 말고 설계를
   고친다.** 백엔드 컨텍스트 맵 섹션은 건드리지 않는다.
2. **`planning/traceability.md`** — `스토리 → 흐름`에 프론트엔드 `FLOW-` 키를
   `계층: 프론트엔드`로 추가하고(백엔드 행 보존), `인수 기준 → 테스트`에
   `T-2NN`·`T-3NN`을 채운다.
3. **`architecture.md`의 `## 프론트엔드 구조`** — "감지된 프레임워크 환경"
   표를 사용자 결정값으로, FSD 적합도 표를 채택한 구조로 채운다.
4. `common-rules.md` §3의 결정적 검사를 실행한다.

### 단계 9: 완료 리포트

`common-rules.md` §4에 다음을 더한다: 부여한 `FLOW-` 키 목록.

> 프론트엔드 설계가 끝났습니다.
>
> - 백엔드가 아직이면 `/explainable:init-design-backend`
> - 번역 미러가 필요하면 `/explainable:translate-docs`

## 문서 규칙

`common-rules.md` §5를 따른다. 이 스킬 고유 사항: 순방향이므로
`## 읽은 소스`를 생성하지 않고 `분석 기준 커밋`은 "해당 없음"이다.
