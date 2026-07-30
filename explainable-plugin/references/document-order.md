# 문서 정규 순서

이 파일은 `explainable` 플러그인이 만드는 문서들의 **읽는 순서**를 정의하는
단일 출처다. 모든 스킬은 내비게이션 링크(문서 1행의 이전/다음, 문서 하단의
`전체 문서` 인덱스)를 만들기 전에 이 파일을 읽는다.

템플릿마다 순서 규칙을 복제하지 않는 이유: 규칙이 여러 곳에 흩어지면 문서를
하나 추가하거나 뺄 때마다 모든 템플릿을 고쳐야 하고, 실제로 링크가 어긋난다.

---

## 1. 횡단 문서 (내비게이션 없음)

아래 문서들은 파이프라인에 속하지 않는다. **이전/다음 링크도, `전체 문서`
인덱스도 붙이지 않는다.** 도메인 태그도 없다.

```text
docs/<source>/specifications/README.md
docs/<source>/specifications/architecture.md
docs/<source>/specifications/infrastructure.md
docs/<source>/specifications/glossary.md
docs/<source>/specifications/domain-map.md
```

이 문서들은 `## 관련 문서` 섹션에서 서로를 링크하고, 도메인 문서를 링크한다.
도메인 문서 쪽에서는 `## 관련 문서`의 `### 참고 문서` 항목으로만 이들을
가리킨다 — 이전/다음 체인에 끼워 넣지 않는다.

---

## 2. 도메인 문서의 정규 순서

`docs/<source>/specifications/<domain>/` 아래 문서들의 순서다.

```text
planning/requirements.md
  → planning/user-stories.md
  → planning/information-architecture.md   (조건부)
  → planning/user-flows.md                 (조건부)
  → planning/api-interface.md
  → [ design/backend/*  또는  design/frontend/*  — 아래 3절 ]
  → planning/traceability.md
  → verification/test-spec.md
```

`information-architecture.md`와 `user-flows.md`는 **사용자 인터페이스가 있는
프로젝트에서만** 만든다. 둘은 짝이다 — 유저 플로우의 노드가 정보 구조의
`SCR-` 키를 참조하므로 한쪽만 만들지 않는다.

두 문서가 `api-interface.md` **앞에** 오는 이유: 한 화면이 한 번에 보여줘야
하는 범위가 오퍼레이션의 응답 범위를 결정한다. 두 문서는 인터페이스 계약의
**입력**이지 출력이 아니다.

`traceability.md`가 설계 문서 **뒤에** 오는 이유: FR ↔ US/AC ↔ FLOW ↔ T를
조인하려면 설계 단계에서 부여한 `FLOW-` 키가 이미 있어야 하기 때문이다.
기획 단계에서 먼저 만들어 두고 설계 단계에서 갱신하되, **읽는 순서는 설계
뒤**다. `## 스토리 → 화면·플로우` 표만은 예외로 기획 단계에서 전부 채운다 —
`SCR-`과 `UF-`는 설계 전에 부여되기 때문이다.

---

## 3. 설계 문서 내부 순서

백엔드와 프론트엔드 설계 문서는 **서로 다른 체인**이다. 한 도메인에 둘 다
있으면 두 체인이 나란히 존재하며, 각각의 첫 문서는
`../../planning/api-interface.md`를 이전 문서로, 각각의 마지막 문서는
`../../planning/traceability.md`를 다음 문서로 가리킨다.

### 백엔드

```text
design/backend/layered-architecture.md
  → design/backend/domain-model.md
  → design/backend/erd.md               (조건부)
  → design/backend/sequence-diagram.md
```

### 프론트엔드

```text
design/frontend/fsd-structure.md
  → design/frontend/routing.md
  → design/frontend/component-tree.md
  → design/frontend/render-flow.md
  → design/frontend/state-flow.md
```

유저 플로우는 이 체인에 없다 — 기획 문서(`planning/user-flows.md`)다. 설계
문서는 그것을 **입력으로 읽을 뿐 다시 그리지 않는다.** `routing.md`가 `SCR-`
키에 라우트를 대응시키는 것이 두 계층의 유일한 접점이다.

---

## 4. 링크 생성 규칙

1. **생성된 문서만 체인에 넣는다.** 증거가 없어 만들지 않은 문서(`erd.md`,
   프론트엔드 문서 일부)는 이전/다음 링크에도, `전체 문서` 인덱스에도
   등장하지 않는다. 존재하지 않는 파일을 가리키는 링크는 만들지 않는다.
2. **문서 대 문서로만 링크한다.** `../design/` 같은 디렉터리를 가리키지
   않는다.
3. **체인의 첫 문서는 이전 링크가 없고, 마지막 문서는 다음 링크가 없다.**
4. **문서를 새로 끼워 넣을 때는 양쪽 이웃의 링크도 함께 고친다.** 체인은
   양방향으로 이어져 있어야 한다.
5. `전체 문서` 인덱스에서 **현재 문서는 굵게 표시하고 링크하지 않는다.**
6. 문서 내부의 ID 참조는 GitHub 제목 앵커를 쓴다.
   예: `### US-01: 주문 생성` → `user-stories.md#us-01-주문-생성`

---

## 5. 상대 경로 기준표

| 출발 | 목적지 | 상대 경로 |
| --- | --- | --- |
| `<domain>/planning/*.md` | 같은 폴더 | `user-stories.md` · `information-architecture.md` · `user-flows.md` |
| `<domain>/planning/*.md` | 백엔드 설계 | `../design/backend/layered-architecture.md` |
| `<domain>/planning/*.md` | 프론트엔드 설계 | `../design/frontend/routing.md` |
| `<domain>/planning/*.md` | 검증 | `../verification/test-spec.md` |
| `<domain>/planning/*.md` | 횡단 문서 | `../../architecture.md` |
| `<domain>/design/backend/*.md` | 기획 | `../../planning/api-interface.md` |
| `<domain>/design/backend/*.md` | 프론트엔드 설계 | `../frontend/routing.md` |
| `<domain>/design/backend/*.md` | 횡단 문서 | `../../../architecture.md` |
| `<domain>/design/frontend/*.md` | 기획 | `../../planning/information-architecture.md` · `../../planning/user-flows.md` |
| `<domain>/verification/test-spec.md` | 기획 | `../planning/traceability.md` |
| `<domain>/verification/test-spec.md` | 백엔드 설계 | `../design/backend/sequence-diagram.md` |
| `<domain>/verification/test-spec.md` | 프론트엔드 설계 | `../design/frontend/state-flow.md` |
| 횡단 문서 | 도메인 문서 | `<domain>/planning/requirements.md` |
