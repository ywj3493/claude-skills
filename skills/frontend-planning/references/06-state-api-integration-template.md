# 상태/API 연동 명세 (State & API Integration)

> **생성일**: YYYY-MM-DD
> **최종 수정일**: YYYY-MM-DD
> **상태**: 초안 / 검토 중 / 확정
> **기술 스택**: (자동 감지 결과 기입)
> **선행 문서**: `docs/en/specifications/01-requirements.md` ~ `docs/en/specifications/05-component-tree.md`

## 1. 상태 관리 전략 (State Management Strategy)

### 1.1 선택 근거

| 항목 | 결정 |
|------|------|
| 상태 관리 라이브러리 | (예: Zustand / Redux Toolkit / Pinia) |
| 서버 상태 관리 | (예: TanStack Query / SWR) |
| 전역 vs 로컬 기준 | (예: 2개 이상 페이지에서 공유하면 전역) |

### 1.2 상태 분류

| 분류 | 설명 | 관리 방식 | 예시 |
|------|------|----------|------|
| Server State | API에서 가져오는 데이터 | TanStack Query | 사용자 목록, 게시글 |
| Client State | UI 상태 | Zustand / useState | 모달 열림, 사이드바 토글 |
| Auth State | 인증 정보 | Zustand (persist) | 토큰, 사용자 프로필 |
| Form State | 폼 입력 상태 | React Hook Form | 입력값, 유효성 에러 |

## 2. Store 정의

### 2.1 Auth Store

```typescript
interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

interface AuthActions {
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

interface User {
  id: string;
  email: string;
  name: string;
  role: 'user' | 'admin';
}
```

### 2.2 (다음 Store 이름)

```typescript
interface SomeState {
  // 상태 정의
}

interface SomeActions {
  // 액션 정의
}
```

---

## 3. API 엔드포인트 (API Endpoints)

### 3.1 엔드포인트 목록

| # | Method | Path | 설명 | 인증 | 관련 UC |
|---|--------|------|------|------|---------|
| 1 | POST | `/auth/login` | 로그인 | 불필요 | UC-002 |
| 2 | POST | `/auth/signup` | 회원가입 | 불필요 | UC-001 |
| 3 | GET | `/users/me` | 내 정보 조회 | 필요 | UC-003 |
| 4 | | | | | |

### 3.2 Request / Response DTO

#### POST `/auth/login`

```typescript
// Request
interface LoginRequest {
  email: string;
  password: string;
}

// Response (200 OK)
interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
}

// Error Response (401)
interface AuthErrorResponse {
  code: 'INVALID_CREDENTIALS' | 'ACCOUNT_LOCKED';
  message: string;
}
```

#### (다음 엔드포인트)

```typescript
// Request
interface SomeRequest {
  // 필드 정의
}

// Response
interface SomeResponse {
  // 필드 정의
}
```

---

## 4. 캐싱 전략 (Caching Strategy)

| 데이터 | staleTime | gcTime | 재검증 시점 |
|--------|-----------|--------|------------|
| 사용자 프로필 | 5분 | 30분 | 페이지 포커스 시 |
| 목록 데이터 | 1분 | 10분 | 페이지 이동 시 |
| 정적 데이터 | 1시간 | 24시간 | 수동 무효화 |

## 5. 에러 처리 패턴 (Error Handling)

| HTTP 상태 | 처리 방식 |
|-----------|----------|
| 401 Unauthorized | 토큰 갱신 시도 → 실패 시 로그인 페이지 리다이렉트 |
| 403 Forbidden | "권한이 없습니다" Toast 표시 |
| 404 Not Found | 404 에러 페이지로 이동 |
| 422 Validation | 필드별 에러 메시지 표시 |
| 500 Server Error | "서버 오류가 발생했습니다" Toast + 재시도 버튼 |
| Network Error | "네트워크 연결을 확인해 주세요" Toast |

## 6. API 클라이언트 설정

```typescript
// Base configuration
interface ApiClientConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

// Interceptors
// - Request: Authorization 헤더에 토큰 자동 첨부
// - Response: 401 시 토큰 갱신 로직
// - Error: 공통 에러 핸들러 호출
```
