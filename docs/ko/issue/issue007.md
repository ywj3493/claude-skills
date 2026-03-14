# Issue 007: backend-planning 스킬 생성

**Status**: Done
**Created**: 2026-03-12

## 배경

프로젝트에 프론트엔드 프로젝트용 6단계 기획 문서 파이프라인을 생성하는
`frontend-planning` 스킬이 있습니다. `auth-gateway` 프로젝트의 명세 문서
형식(요구사항, 사용자 스토리, API 명세, 유스케이스, 시퀀스 다이어그램)을 따르는
백엔드 프로젝트용 유사 스킬이 필요합니다.

## 완료 기준

- [x] `~/.agents/skills/backend-planning/` 스킬 디렉토리 존재
- [x] `SKILL.md`에 기술 스택 감지 및 도메인 분석이 포함된 5단계 파이프라인 정의
- [x] `references/` 하위에 5개 참조 템플릿 존재:
  - `requirements-template.md`
  - `user-stories-template.md`
  - `api-spec-template.md`
  - `use-cases-template.md`
  - `sequence-diagram-template.md`
- [x] 각 템플릿에 문서 탐색 링크(Previous/Next) 포함
- [x] 템플릿이 auth-gateway 문서 형식 사용 (메타 헤더, 목차, Mermaid 다이어그램, 교차 참조)
- [x] README 생성 단계에서 클릭 가능한 링크가 포함된 목차 생성
- [x] `docs/en/issue/`와 `docs/ko/issue/` 모두에 이슈 문서 생성

## 작업

1. [x] 이슈 문서 생성 (EN + KO)
2. [x] `~/.agents/skills/backend-planning/SKILL.md` 생성
3. [x] `references/requirements-template.md` 생성
4. [x] `references/user-stories-template.md` 생성
5. [x] `references/api-spec-template.md` 생성
6. [x] `references/use-cases-template.md` 생성
7. [x] `references/sequence-diagram-template.md` 생성
8. [x] 모든 파일 및 탐색 링크 검증

## 참고 사항

- backend-planning 스킬은 5개 콘텐츠 문서 생성 (프론트엔드의 6개 대비)
- 탐색 체인: requirements -> user-stories -> api-spec -> use-cases -> sequence-diagram
- 출력 위치: `docs/en/specifications/<domain>/requirements/` 및 `docs/en/specifications/<domain>/workflows/`
- 템플릿은 `auth-gateway` 프로젝트의 실제 명세 문서에서 일반화

Refs: issue007
