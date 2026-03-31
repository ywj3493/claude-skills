# 명명 규칙

## 파일 및 디렉토리

- 모든 파일명: 소문자, 하이픈 구분 (kebab-case)
- 이슈 문서: `issue001.md`, `issue002.md` (3자리 0 패딩)
- 번역 문서는 `docs/<lang>/` 하위에 동일한 파일명을 사용한다
  - 영어: `docs/en/policy/policy.md` → 한국어: `docs/ko/policy/policy.md`
- 파일 및 디렉토리 이름에 공백 없음

## 코드 (언어 공통 기본값)

- 변수 및 함수: camelCase
- 상수: UPPER_SNAKE_CASE
- 클래스 및 타입: PascalCase
- 비공개 멤버: 밑줄 `_` 접두사

## 브랜치 이름

- 기능: `feat/issue<NNN>-<짧은-설명>`
  - GitHub Issues 사용 시: `feat/issue42-user-authentication` (0 패딩 없음)
  - 로컬 docs 이슈 사용 시: `feat/issue003-user-authentication` (0 패딩)
- 버그 수정: `fix/issue<NNN>-<짧은-설명>`
- 문서: `docs/issue<NNN>-<짧은-설명>`

## 참고

- 언어별 규칙이 이 기본값보다 우선한다
- 프로젝트가 발전함에 따라 언어별 규칙을 이 파일에 추가한다
