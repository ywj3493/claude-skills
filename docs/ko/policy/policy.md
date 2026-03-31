# 프로젝트 정책

## 문서화

- 모든 문서는 `docs/`에 위치하며 단일 진실 공급원(source of truth)으로 취급한다
- 영어 문서는 `docs/en/`에 위치한다
- 한국어 번역본은 동일한 파일명으로 `docs/ko/`에 위치한다
- `docs/reference/`는 사용자가 직접 관리하며, Claude는 해당 디렉토리의 파일을 생성하거나 수정하지 않는다

## 워크플로우

- 모든 작업은 이슈로 시작한다 — git remote가 있으면 GitHub Issue, 없으면
  `docs/en/issue/`의 로컬 문서를 사용한다
- GitHub Issues는 GitHub이 자동으로 번호를 부여한다
- 로컬 이슈 파일(fallback)은 순차적으로 번호를 부여한다: issue001.md, issue002.md, ...
- 이슈가 없으면 구현을 시작하지 않는다 (GitHub Issue 또는 로컬 문서)
- 코드 변경과 같은 커밋 또는 PR에 관련 문서를 함께 업데이트한다

## 정책 업데이트

- 정책 파일 변경은 사전에 사용자와 협의해야 한다
- 정책 변경 시 영어 버전과 한국어 버전을 모두 업데이트한다

## 관련 정책 파일

- [@docs/en/policy/commit-message-rule.md](docs/en/policy/commit-message-rule.md) — 커밋 메시지 형식
- [@docs/en/policy/naming-conventions.md](docs/en/policy/naming-conventions.md) — 파일, 코드, 브랜치 명명 규칙
- [@docs/en/policy/reference-convention.md](docs/en/policy/reference-convention.md) — 문서 참조 컨벤션
