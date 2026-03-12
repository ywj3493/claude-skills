# Issue 006: frontend-planning 스킬 개선 — 프로젝트 문서 탐색 및 @-reference 링크 자동 연결

**상태**: 완료

## 배경

현재 `frontend-planning` 스킬은 기존 프로젝트 문서 참조 방식이 미흡하다:
- Step 1, 6에서 "기존 백엔드 문서를 확인하라"는 모호한 지시만 존재
- 하드코딩된 경로(`docs/en/specifications/api-spec.md`)만 언급하여, 중첩 디렉토리 구조(예: `auth/requirements/api-spec.md`)를 처리 못 함
- 백틱 경로만 사용하여 `@`-reference 컨벤션([@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md))을 따르지 않음

auth-gateway 프로젝트처럼 풍부한 문서 체계를 가진 프로젝트에서 스킬을 실행할 때, 기존 문서를 자동 탐색하고 적절한 `@`-reference 링크를 생성하도록 개선한다.

## 완료 기준

- [x] SKILL.md Step 0.5에 도메인 분석 후 "Document Discovery" 포함
- [x] Pipeline overview에 "Domain analysis & document discovery" 반영
- [x] Steps 1-4, 6, 7이 문서 탐색 결과를 문서 유형별로 참조
- [x] SKILL.md에 "Document Discovery Rules" 섹션 추가
- [x] 6개 템플릿 파일의 선행 문서 경로를 `@`-reference 형식으로 변환
- [x] 6개 템플릿 파일에 `**Reference Documents**` placeholder 필드 추가
- [x] `requirements-template.md` 섹션 6의 하드코딩 경로를 placeholder로 교체
- [x] `state-api-integration-template.md` 엔드포인트 테이블에 Source 열 추가

## 작업 목록

1. [x] 이슈 문서 생성 (en + ko)
2. [x] `skills/frontend-planning/SKILL.md` 수정
   - Step 0.5에 문서 탐색 기능 추가 (항목 6-10)
   - Pipeline overview 업데이트
   - Steps 1-4, 6에 문서 유형 참조 지시 추가
   - Step 7에 관련 프로젝트 문서 섹션 추가
   - Document Discovery Rules 섹션 추가
3. [x] 6개 템플릿 파일 수정
   - 백틱 경로 → `@`-reference 변환
   - `**Reference Documents**` placeholder 추가
   - `requirements-template.md` 섹션 6 수정
   - `state-api-integration-template.md` 엔드포인트 테이블에 Source 열 추가

## 비고

- 문서 유형 분류: `requirements`, `user-stories`, `use-cases`, `api-spec`, `sequence-diagram`, `architecture`, `config`, `infrastructure`, `deployment`, `policy`, `other`
- 스캔 대상: `README.md`, `CLAUDE.md`, `docs/en/specifications/` (재귀), `docs/en/policy/`
- `docs/reference/` 파일은 reference-convention.md에 따라 절대 `@`-prefix 사용 금지
- 번호 충돌 방지를 위해 기존 Step 0.5 (Domain Analysis)에 문서 탐색 기능을 통합
