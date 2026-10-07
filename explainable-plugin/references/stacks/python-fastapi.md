# 스택 프로파일: Python + FastAPI

`backend-implementation` 스킬이 `architecture.md` 스택 표의 백엔드 언어가
Python이고 프레임워크가 FastAPI일 때 로드한다. 프레임워크 중립 규칙은
`${CLAUDE_PLUGIN_ROOT}/references/backend-implementation-rules.md`(이하
`구현 규약`)가 소유하며, 이 문서는 그 규칙을 **이 스택에서 어떻게 쓰는가**만
담는다.

이 프로파일은 FastAPI + Redis 기반 4-Layer DDD로 운영 중인 인증 세션 서비스의
관례를 원형으로 삼고, 그 서비스가 구현 규약에서 벗어난 지점을 보정했다
(§10). 아래 코드 조각은 프로파일 작성 시 실제 프로젝트로 조립해
`pytest`·`lint-imports`·`ruff`를 통과시킨 것이다.

**우선순위** (`구현 규약` §1): 이름·폴더·도구 같은 관용구는 호스트
프로젝트에 이미 있는 관례가 이 프로파일보다 앞선다. 예를 들어 기존 코드가
`routers/`를 쓰면 `controllers/`로 바꾸지 않는다. 원칙(불변 값 객체, 의존
방향 등)은 기존 코드가 달라도 새 코드에서 지킨다.

---

## 1. 도구 기준

| 구분 | 기본값 | 비고 |
|---|---|---|
| Python | 3.11 이상 | 3.9·3.10이면 `X \| None` 대신 `Optional[X]` |
| 패키지 관리 | `uv` | 기존 `poetry`·`pip` 프로젝트면 그것을 따른다 |
| 웹 | FastAPI + pydantic 2 | |
| 설정 | pydantic-settings | |
| 테스트 | pytest + pytest-asyncio(`asyncio_mode = "auto"`) + pytest-describe + httpx | |
| 린트·포맷 | ruff | |
| 의존 방향 | import-linter | `구현 규약` §2.3 |
| 타입 검사 | mypy (선택) | |
| 주석·독스트링 | 한국어 | 식별자는 영어. 호스트 프로젝트 규칙이 있으면 그것을 따른다 |

새 의존성을 추가하면 매니페스트 변경을 완료 리포트에 남긴다.

---

## 2. 디렉터리

**컨텍스트 먼저, 그다음 계층, 그다음 종류.** `architecture.md`의 계층 ↔
디렉터리 매핑이 다르게 정했으면 그것을 따른다.

```text
app/
├── main.py                       # FastAPI 앱, lifespan, 오류 처리기 등록, 라우터 포함
├── config.py                     # Settings (pydantic-settings)
├── shared/                       # 컨텍스트 공용 커널 (필요할 때만)
│   ├── domain/errors.py          # DomainError 기반 타입
│   └── application/errors.py     # ApplicationError, NotFoundError
└── <context>/
    ├── dependencies.py           # 컴포지션 루트
    ├── domain/
    │   ├── entities/             # 애그리거트 루트·엔티티
    │   ├── value_objects/
    │   ├── services/             # 도메인 서비스 (있을 때만)
    │   ├── repositories/         # 리포지토리 포트 (ABC)
    │   ├── clients/              # 외부 연동 포트 (ABC, 있을 때만)
    │   └── exceptions/
    ├── application/
    │   ├── use_cases/
    │   ├── dtos/                 # Command / Query / Result
    │   ├── queries/              # 조회 전용 포트 (CQRS, 있을 때만)
    │   ├── services/             # 유스케이스 간 조율 (있을 때만)
    │   └── exceptions/
    ├── infrastructure/
    │   ├── repositories/         # 어댑터 + 레코드 매퍼
    │   ├── clients/
    │   └── queries/
    └── presentation/http/
        ├── controllers/          # APIRouter
        ├── schemas/              # 요청·응답 pydantic 모델
        └── error_handlers.py
tests/
├── conftest.py                   # 페이크로 유스케이스를 조립하는 픽스처
├── doubles/                      # 포트 페이크
└── app/<context>/{domain,application,infrastructure,presentation}/
```

1. **파일 하나에 클래스 하나**, 파일 이름은 클래스의 snake_case.
2. 하위 패키지의 `__init__.py`는 공개 이름을 `__all__`로 다시 내보낸다.
   import는 패키지 경로로 한다 (`from app.order.domain.entities import Order`).
3. 응용 DTO는 `application/dtos/`, HTTP 스키마는 `presentation/http/schemas/`
   — 이름이 겹치지 않게 `dtos`를 표현 계층에서 쓰지 않는다.
4. 비어 있을 디렉터리는 만들지 않는다.

---

## 3. 도메인 계층

### 3.1 값 객체 — `frozen` dataclass

```python
@dataclass(frozen=True)
class Money:
    """원 단위 금액. 음수가 될 수 없다."""

    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise InvalidMoneyError(self.amount)

    def add(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)
```

- 검증은 `__post_init__`. 연산은 새 인스턴스를 돌려준다.
- 식별자도 값 객체로 감싼다 (`OrderId(value: str)`). 컬렉션 필드는 `tuple`.
- 상태 열거는 `class OrderStatus(str, Enum)` — 도메인 언어로 값을 짓는다
  (`STEP1`이 아니라 `PAYMENT_WAITING`).
- pydantic `BaseModel`을 도메인에 쓰지 않는다 (§9 계약이 막는다).

### 3.2 애그리거트 루트 — 일반 클래스 + 비공개 필드 + 프로퍼티

```python
class Order:
    """주문 애그리거트 루트. 상태는 행위 메서드로만 바뀐다."""

    def __init__(self, order_id: OrderId, orderer_id: str,
                 lines: tuple[OrderLine, ...], status: OrderStatus,
                 placed_at: datetime) -> None:
        # 재구성 경로 — 저장소 어댑터가 호출한다. 새 주문은 place()로 만든다.
        self._id = order_id
        self._lines = lines
        self._status = status
        ...

    @classmethod
    def place(cls, order_id: OrderId, orderer_id: str,
              lines: list[OrderLine], now: datetime) -> "Order":
        """새 주문을 만든다. 불변식: 항목이 하나 이상"""
        if not lines:
            raise EmptyOrderError()
        return cls(order_id, orderer_id, tuple(lines), OrderStatus.PAYMENT_WAITING, now)

    def cancel(self) -> None:
        if self._status not in _CANCELLABLE:
            raise OrderNotCancellableError(self._status.value)
        self._status = OrderStatus.CANCELED

    @property
    def status(self) -> OrderStatus:
        return self._status

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Order) and other._id == self._id

    def __hash__(self) -> int:
        return hash(self._id)
```

- **애그리거트에 `@dataclass`를 쓰지 않는다** — 공개 필드가 곧 setter가 된다.
  필드는 `_` 접두어, 읽기는 `@property`, 쓰기는 행위 메서드뿐.
- **`__init__`은 재구성 경로**, 생성은 `@classmethod` 팩토리
  (`구현 규약` §3.1.3–4). 팩토리는 식별자와 현재 시각을 **인자로** 받는다.
- 허용 전이 집합은 모듈 상수(`_CANCELLABLE = frozenset({...})`)로 둔다.

### 3.3 포트 — `ABC`

```python
class OrderRepository(ABC):
    """주문 애그리거트의 영속성 포트"""

    @abstractmethod
    def next_id(self) -> OrderId:
        """새 주문 식별자를 발급한다"""

    @abstractmethod
    async def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        """완전한 애그리거트를 돌려준다. 없으면 None"""

    @abstractmethod
    async def save(self, order: Order) -> None: ...
```

- I/O 메서드는 `async`. CPU만 쓰는 메서드(`next_id`)는 동기로 둔다.
- 식별자 발급을 리포지토리의 `next_id()`로 두면 유스케이스가 UUID를
  만들지 않아도 된다.
- 반환 타입은 도메인 타입. `tuple[User, str, str, int]` 같은 익명 튜플 대신
  값 객체를 정의한다.

### 3.4 도메인 예외

```python
# app/shared/domain/errors.py
class DomainError(Exception):
    """도메인 규칙 위반. 전송 계층 정보(HTTP 상태 등)를 갖지 않는다."""

# app/order/domain/exceptions/order_errors.py
class OrderNotCancellableError(DomainError):
    def __init__(self, status: str) -> None:
        super().__init__(f"취소할 수 없는 상태: {status}")
```

컨텍스트가 하나뿐이면 `shared/` 대신 `<context>/domain/exceptions/`에 기반
타입을 둔다.

---

## 4. 응용 계층

```python
class CancelOrderUseCase:
    """FLOW-order-cancel-order: 주문 취소"""

    def __init__(self, order_repository: OrderRepository) -> None:
        self._order_repository = order_repository

    async def execute(self, order_id: str) -> OrderResult:
        order = await self._order_repository.find_by_id(OrderId(order_id))
        if order is None:
            raise OrderNotFoundError(order_id)
        order.cancel()
        await self._order_repository.save(order)
        return OrderResult.from_aggregate(order)
```

1. 클래스 이름 `<Verb><Noun>UseCase`, 공개 메서드는 `async def execute(...)`
   하나. 독스트링 첫 줄에 `FLOW-` 키를 적는다.
2. 의존성은 생성자에서 **포트 타입으로** 받아 `self._<name>`에 둔다.
3. 시계는 `clock: Callable[[], datetime]`으로 주입한다. 테스트는 고정 시각을
   넣는다.
4. **`Settings`를 받지 않는다.** 만료 여유 시간 같은 값은 `int`나 정책 값
   객체로 받고, 컴포지션 루트가 `settings`에서 꺼내 넘긴다.
5. DTO는 `@dataclass(frozen=True)`. Result DTO는
   `from_aggregate(cls, aggregate)` 클래스 메서드 한 곳에서 변환한다.
6. 응용 예외는 `ApplicationError` 하위 (`NotFoundError` 등).
7. 관계형 DB로 여러 저장을 한 트랜잭션에 묶어야 하면 `UnitOfWork` 포트를
   응용 계층에 두고(`async with self._uow:`) 구현은 인프라에 둔다. Redis처럼
   단일 명령 저장소면 만들지 않는다.
8. 로거는 `logging.getLogger(__name__)`. 토큰·비밀번호·세션 ID 원문을
   어느 레벨로도 남기지 않는다.

---

## 5. 인프라 계층

```python
class RedisOrderRepository(OrderRepository):
    def __init__(self, redis_client: Redis) -> None:
        self._redis = redis_client

    async def find_by_id(self, order_id: OrderId) -> Optional[Order]:
        raw = await self._redis.get(f"order:{order_id.value}")
        return None if raw is None else from_record(order_id.value, json.loads(raw))

    async def save(self, order: Order) -> None:
        await self._redis.set(f"order:{order.id.value}", json.dumps(to_record(order)))
```

1. 클래스 이름은 기술 접두어 + 포트 이름 (`RedisOrderRepository`,
   `SqlAlchemyOrderRepository`, `HttpPaymentClient`).
2. **직렬화는 같은 디렉터리의 레코드 매퍼**(`order_record_mapper.py`의
   `to_record` / `from_record`)에 둔다. 엔티티에 `to_dict`를 두지 않는다.
   재구성은 애그리거트의 `__init__`을 호출한다.
3. 동기 SDK는 `await asyncio.to_thread(...)`로 감싼다.
4. SDK·드라이버 예외는 어댑터 안에서 잡아 도메인 예외로 바꾼다.
   **`app.<context>.application`을 import하지 않는다** (§9 계약이 막는다).
5. SDK 모델 → 도메인 타입 변환은 비공개 함수 하나로 모은다.

---

## 6. 표현 계층

```python
router = APIRouter(prefix="/api/orders", tags=["orders"])

@router.post("/{order_id}/cancel", response_model=OrderResponse,
             status_code=status.HTTP_200_OK)
async def cancel_order(
    order_id: str,
    use_case: CancelOrderUseCase = Depends(provide_cancel_order_use_case),
) -> OrderResponse:
    result = await use_case.execute(order_id)
    return OrderResponse.from_result(result)
```

1. 엔드포인트마다 `response_model`과 `status_code`를 명시한다. 값은
   `api-interface.md`와 일치해야 한다.
2. 요청 스키마는 `to_command()`, 응답 스키마는 `from_result()`로 응용 DTO와
   변환한다. 같은 매핑을 엔드포인트마다 복사하지 않는다.
3. 필드에는 `Field(..., description="한국어 설명")`과 값 범위 제약
   (`ge`, `min_length`)을 단다 — 형식 검증은 여기서, 업무 규칙은 도메인에서.
4. **엔드포인트 안에 try/except를 두지 않는다.** 오류 변환은
   `error_handlers.py` 한 곳에서 한다.

```python
ERROR_RESPONSES: dict[type[Exception], tuple[int, str]] = {
    OrderNotFoundError: (404, "ORDER_NOT_FOUND"),
    OrderNotCancellableError: (409, "ORDER_NOT_CANCELLABLE"),
}

def register_error_handlers(app: FastAPI) -> None:
    for exc_type, (status_code, code) in ERROR_RESPONSES.items():
        app.add_exception_handler(exc_type, _make_handler(status_code, code))
```

   `ERROR_RESPONSES`의 상태 코드와 오류 코드는 `api-interface.md`의
   `## 오류 모델`을 옮긴 것이다. 표에 없는 예외는 500으로 떨어지므로, 도메인 예외를
   추가하면 이 표에도 추가한다.
5. 쿠키·헤더·인증 확인은 `Depends` 함수로 만든다(예:
   `get_session_id_from_cookie`). 쿠키 설정과 삭제는 같은 속성(httponly,
   secure, samesite, domain)을 쓰는 비공개 헬퍼 하나로 한다.

---

## 7. 컴포지션 루트 — `<context>/dependencies.py`

```python
@lru_cache
def provide_redis_client() -> Redis: ...

def provide_order_repository(
    redis_client: Redis = Depends(provide_redis_client),
) -> OrderRepository:                      # 반환 타입은 포트
    return RedisOrderRepository(redis_client)

def provide_cancel_order_use_case(
    order_repository: OrderRepository = Depends(provide_order_repository),
) -> CancelOrderUseCase:
    return CancelOrderUseCase(order_repository)
```

1. 프로바이더 이름은 `provide_<snake_case 클래스명>`이다. `get_` 접두어는
   `GetSessionUseCase`에서 `get_get_session_use_case`가 되므로 쓰지 않는다.
2. 싱글톤 자원은 `@lru_cache`, 이벤트 루프 안에서 만들어야 하는 비동기
   클라이언트는 모듈 전역 + 지연 생성으로 하고 `main.py`의 `lifespan`에서
   닫는다.
3. 설정은 `from app.config import settings`를 여기서만 읽는다.
4. 테스트는 `app.dependency_overrides[provide_order_repository]`로 페이크를
   끼운다.

---

## 8. 테스트

```python
def describe_CancelOrderUseCase():
    def describe_execute():
        def context_when_order_not_exists(cancel_order_use_case):
            async def it_raises_order_not_found_error():
                """[T-103] 없는 주문이면 OrderNotFoundError"""
                # When & Then
                with pytest.raises(OrderNotFoundError):
                    await cancel_order_use_case.execute("missing")
```

1. **pytest-describe**: `describe_<ClassName>` → `describe_<method>` →
   `context_<조건>` → `it_<결과>`. 픽스처는 `context_` 함수의 인자로 받는다.
2. `it_` 독스트링은 한국어 한 문장이고, test-spec의 행을 구현한 테스트는
   **`[T-1NN]`으로 시작한다** (`구현 규약` §8.2). 본문은
   `# Given` / `# When` / `# Then`.
3. **페이크는 `tests/doubles/`**에 포트당 하나(`InMemoryOrderRepository`,
   `FakePaymentClient`). 테스트 보조 메서드(`add`, `count`)를 둘 수 있다.
   `tests/doubles/__init__.py` 독스트링에 "응용 계층은 목 대신 페이크"를 적는다.
4. `tests/conftest.py`가 유스케이스를 페이크로 조립하는 픽스처와 상태별
   시나리오 픽스처(`waiting_order`, `expired_session`)를 제공한다.
5. 인프라 테스트는 실물 Redis/DB가 가능하면 testcontainers, 아니면
   `AsyncMock` 클라이언트로 저장 형식과 예외 변환을 확인한다.
6. 표현 테스트는 `httpx.AsyncClient(transport=httpx.ASGITransport(app=app))`
   + `dependency_overrides`로 상태 코드와 오류 본문을 확인한다.
7. 테스트 트리는 `tests/app/<context>/<layer>/`로 계층을 그대로 비춘다.
   같은 대상의 테스트 파일을 두 곳에 만들지 않는다.

---

## 9. 설정 파일

`pyproject.toml`에 추가하거나, 이미 있는 섹션에 병합한다. 컨텍스트 이름은
와일드카드(`app.*.domain`)로 받으므로 컨텍스트가 늘어도 고칠 필요가 없다.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]

[tool.ruff.lint.per-file-ignores]
# pytest-describe의 describe_<ClassName> 관례
"tests/**" = ["N802"]

[tool.importlinter]
root_package = "app"
include_external_packages = true

[[tool.importlinter.contracts]]
name = "Domain은 다른 계층과 프레임워크를 import하지 않는다"
type = "forbidden"
source_modules = ["app.*.domain"]
forbidden_modules = [
    "app.*.application", "app.*.infrastructure", "app.*.presentation",
    "app.*.dependencies", "app.config",
    "fastapi", "pydantic", "pydantic_settings",
]

[[tool.importlinter.contracts]]
name = "Application은 Infrastructure·Presentation·설정을 import하지 않는다"
type = "forbidden"
source_modules = ["app.*.application"]
forbidden_modules = [
    "app.*.infrastructure", "app.*.presentation",
    "app.*.dependencies", "app.config", "fastapi",
]

[[tool.importlinter.contracts]]
name = "Infrastructure는 Application·Presentation을 import하지 않는다"
type = "forbidden"
source_modules = ["app.*.infrastructure"]
forbidden_modules = ["app.*.application", "app.*.presentation", "fastapi"]

[[tool.importlinter.contracts]]
name = "Presentation은 Infrastructure를 직접 import하지 않는다"
type = "forbidden"
source_modules = ["app.*.presentation"]
forbidden_modules = ["app.*.infrastructure"]
# 컨트롤러는 Depends로 컴포지션 루트를 거쳐 어댑터에 간접 의존한다 — 직접 import만 막는다
allow_indirect_imports = true
```

- 저장소 드라이버(`redis`, `sqlalchemy`)를 쓰면 Domain·Application 계약의
  `forbidden_modules`에 추가한다. `include_external_packages = true`이므로
  설치된 패키지 이름이면 된다.
- `allow_indirect_imports`는 Presentation 계약에만 둔다. 다른 계약에서
  간접 의존을 허용하면 계층 위반이 한 단계 우회로 숨는다.

**검증 명령** (스킬의 검증 단계가 실행한다):

```bash
uv run pytest
uv run ruff check .
uv run lint-imports
```

---

## 10. 원형 서비스 대비 보정 사항

원형 서비스의 관례 중 아래는 `구현 규약`과 충돌해 이 프로파일에서 바꿨다.
호스트 프로젝트가 원형과 같은 관례를 이미 쓰고 있어도 **새로 쓰는 코드는
오른쪽 열을 따른다** (`구현 규약` §1). 구현 범위 밖의 기존 코드는 고치지 않고
완료 리포트에 "기존 코드의 규약 이탈"로 남긴다. 단, 프로바이더 이름처럼
관용구에 해당하는 행은 기존 관례를 따른다.

| 원형 서비스 | 이 프로파일 | 근거 |
|---|---|---|
| 값 객체가 가변 `@dataclass`, `entities/`에 위치 | `frozen=True`, `value_objects/` | 구현 규약 §3.2 |
| 애그리거트가 `@dataclass`(공개 필드) | 비공개 필드 + 프로퍼티 + 행위 메서드 | 구현 규약 §3.1.1 |
| 유스케이스가 UUID·타임스탬프 조립 | 팩토리 + `next_id()` + 주입된 시계 | 구현 규약 §3.1.3 |
| 엔티티의 `to_dict`/`from_dict` | 인프라 레코드 매퍼 | 구현 규약 §5.2 |
| 포트가 익명 튜플 반환 | 값 객체 반환 | 구현 규약 §3.4.4 |
| 응용 예외만 있고 HTTP 상태를 보유 | 도메인 예외 + `ApplicationError`, 상태 코드는 표현 계층 표 | 구현 규약 §3.5, §6.3 |
| 엔드포인트별 try/except와 수동 매핑 반복 | `error_handlers.py` + `from_result()` | 구현 규약 §6.3, §4.3 |
| `Settings`를 유스케이스에 주입 | 컴포지션 루트가 값만 꺼내 주입 | 구현 규약 §4.5.1 |
| 인프라가 응용 예외를 import | import-linter 계약으로 금지 | 구현 규약 §2, §5.3 |
| `get_get_<x>_use_case` 프로바이더 이름 | `provide_<x>` | §7.1 |
| 토큰을 INFO 로그로 출력 | 비밀값 로그 금지 | 구현 규약 §4.7 |
| 의존 방향이 관례로만 유지 | import-linter 계약 | 구현 규약 §2.3 |
