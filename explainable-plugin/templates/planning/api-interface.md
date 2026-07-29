<!--
템플릿: 도메인 기획 문서 (api-interface.md)

내비게이션 규칙은 `${CLAUDE_PLUGIN_ROOT}/references/document-order.md` 참조.

**이 문서는 기술 중립성의 유일한 예외다.** 계약 문서이므로 구체적인 스키마를
담는다. 다만 예외인 것은 *구체성*이지 *특정 프로토콜 고정*이 아니다.

**REST/OpenAPI를 전제하지 않는다.** 문서 구조는 고정이고, `## 계약 정의`의
블록 형식만 `architecture.md`에 기록된 API 스타일에 따라 달라진다:

| API 스타일 | 계약 블록 형식 |
|---|---|
| REST/HTTP | OpenAPI 3.1 YAML |
| GraphQL | SDL 스키마 |
| gRPC | `.proto` 정의 발췌 |
| 메시지/이벤트 기반 | AsyncAPI 또는 메시지 스키마 표 |
| 그 외 / 혼합 | 오퍼레이션 표 + 요청·응답 스키마 |

해당하지 않는 형식의 예시 블록은 생성 시 **삭제**한다. 여러 스타일이 섞인
프로젝트만 블록을 여러 개 남긴다.

이 문서는 백엔드와 프론트엔드 설계 스킬 **양쪽의 공통 입력**이다. 설계
단계에서 만들면 두 스킬이 서로 다른 계약을 만들어 버리므로 기획 단계에 둔다.
-->

> [← 유저 스토리](user-stories.md) | [다음: 백엔드 설계 →](../design/backend/layered-architecture.md)

# 인터페이스 계약

> **도메인**: <!-- 도메인 이름 -->
>
> **API 스타일**: <!-- architecture.md의 스택 표에서 확정된 값 -->

---

## 목차

1. [오퍼레이션 카탈로그](#오퍼레이션-카탈로그)
2. [계약 정의](#계약-정의)
3. [오류 모델](#오류-모델)
4. [인증·인가](#인증인가)

---

## 오퍼레이션 카탈로그

<!--
"오퍼레이션"은 외부에서 호출 가능한 진입점 하나다 — REST 엔드포인트,
GraphQL 리졸버, gRPC 서비스 메서드, 메시지 컨슈머, 스케줄러 잡 중 무엇이든
된다.

`오퍼레이션 ID`는 프로토콜과 무관한 안정적인 식별자다. 계약 블록과 시퀀스
다이어그램이 이 ID로 서로를 참조한다.
-->

| 오퍼레이션 ID | 호출 주체 | 관련 스토리 | 한 줄 설명 | 흐름 키 |
|---|---|---|---|---|
| <!-- placeOrder --> | | US-NN | | <!-- FLOW-... 설계 후 채움 --> |

---

## 계약 정의

<!-- 아래 블록 중 이 프로젝트의 API 스타일에 해당하는 것만 남기고 나머지는
     통째로 삭제한다. -->

### REST/HTTP — OpenAPI 3.1

```yaml
openapi: 3.1.0
info:
  title: <!-- 도메인 이름 -->
  version: 1.0.0
paths:
  /<!-- 경로 -->:
    post:
      operationId: <!-- 카탈로그의 오퍼레이션 ID와 동일하게 -->
      summary: <!-- 한 줄 -->
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/<!-- 스키마명 -->'
      responses:
        '201':
          description: <!-- -->
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/<!-- 스키마명 -->'
        '400':
          $ref: '#/components/responses/BadRequest'
components:
  schemas:
    <!-- 스키마명 -->:
      type: object
      required: []
      properties: {}
  responses:
    BadRequest:
      description: <!-- -->
```

### GraphQL — SDL

```graphql
type Mutation {
  """<!-- 한 줄 설명 -->"""
  placeOrder(input: PlaceOrderInput!): PlaceOrderPayload!
}

input PlaceOrderInput {
  <!-- 필드 -->
}

type PlaceOrderPayload {
  <!-- 필드 -->
}
```

### gRPC — Protocol Buffers

```protobuf
service OrderService {
  // <!-- 한 줄 설명 -->
  rpc PlaceOrder(PlaceOrderRequest) returns (PlaceOrderResponse);
}

message PlaceOrderRequest {
  // <!-- 필드 -->
}

message PlaceOrderResponse {
  // <!-- 필드 -->
}
```

### 메시지/이벤트 기반

| 메시지 | 채널·토픽 | 방향 | 페이로드 스키마 | 전달 보장 |
|---|---|---|---|---|
| | | <!-- 발행 / 구독 --> | | <!-- at-least-once 등 --> |

```yaml
# 페이로드 스키마 (AsyncAPI 또는 JSON Schema)
```

---

## 오류 모델

<!--
오류를 어떻게 표현하는지 한 번만 정의하고, 위의 계약 블록은 이 표를
참조한다. 오퍼레이션마다 오류 구조를 다르게 정의하지 않는다.

`재시도 가능` 열은 호출하는 쪽이 재시도해도 되는지를 뜻한다. 프론트엔드
설계가 이 값으로 재시도·에러 경계 동작을 정한다.
-->

### 오류 응답 구조

```json
{
  "code": "<!-- 기계가 읽는 오류 코드 -->",
  "message": "<!-- 사람이 읽는 설명 -->",
  "details": {}
}
```

### 오류 코드

| 코드 | 발생 조건 | 프로토콜 상태 | 재시도 가능 | 관련 인수 기준 |
|---|---|---|---|---|
| | | <!-- HTTP 409, gRPC ABORTED 등 --> | | AC-USNN-NN |

---

## 인증·인가

### 인증

| 항목 | 값 |
|---|---|
| **방식** | <!-- 토큰 / 세션 / mTLS / 서명 등 --> |
| **전달 위치** | |
| **만료·갱신** | |

### 인가

<!--
오퍼레이션별 접근 권한. 역할 이름은 용어집의 영문 식별자를 따른다.
공개 오퍼레이션도 "인증 불필요"로 명시한다 — 빈 칸은 미확인과 구분되지
않는다.
-->

| 오퍼레이션 ID | 필요 권한 | 추가 조건 | 근거 |
|---|---|---|---|
| | | <!-- 예: 본인 소유 자원만 --> | |

---

## 읽은 소스

<!-- 역방향 스킬 전용. 순방향 생성 시 제목까지 통째로 삭제한다. -->

---

## 관련 문서

- [유저 스토리](user-stories.md) — 이 오퍼레이션들이 실현하는 스토리
- [추적성 매트릭스](traceability.md)

### 참고 문서

- [아키텍처](../../architecture.md) — 확정된 API 스타일
- [도메인 지도](../../domain-map.md) — 다른 도메인과의 통합 계약
- [용어집](../../glossary.md)

---

## 문서 정보

| 항목 | 값 |
|---|---|
| **작성일** | YYYY-MM-DD |
| **최종 수정일** | YYYY-MM-DD |
| **상태** | 초안 |
| **분석 기준 커밋** | |
| **참고 문서** | |

**버전 이력**:

- 1.0.0 (YYYY-MM-DD): 최초 작성

---
> **전체 문서**
> [요구사항](requirements.md) |
> [유저 스토리](user-stories.md) |
> **인터페이스 계약** |
> [백엔드 설계](../design/backend/layered-architecture.md) |
> [프론트엔드 설계](../design/frontend/fsd-structure.md) |
> [추적성](traceability.md) |
> [테스트 명세](../verification/test-spec.md)
