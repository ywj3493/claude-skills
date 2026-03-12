# 이슈 005: init-docs 스킬의 스크립트 경로 수정

**상태**: 완료
**생성일**: 2026-03-12

## 배경

issue004에서 docs 구조를 리팩터링하면서 모든 스킬의 경로를 새로운 `docs/en/`,
`docs/ko/` 경로로 업데이트했다. 그러나 init-docs 스킬 내부의 자기 참조 스크립트
경로(`.skills/`, `~/.agents/skills/`)는 실제 디렉토리 구조와 일치하도록 수정되지
않았다.

`skills/init-docs/SKILL.md`에서 스크립트 실행 예시가
`.skills/init-docs/scripts/create-structure.sh`와
`~/.agents/skills/init-docs/scripts/create-structure.sh`를 참조하고 있으나,
실제 경로는 `skills/init-docs/scripts/create-structure.sh`이다.

## 완료 기준

- [x] `skills/init-docs/SKILL.md`의 스크립트 경로를 `skills/init-docs/scripts/create-structure.sh`로 수정
- [x] 폴백 경로 업데이트 또는 제거
- [x] 스킬 파일 내 모든 경로가 실제 파일 시스템과 일치

## 작업 목록

- [x] 1. issue005 문서 생성 (영문 + 한국어)
- [x] 2. `skills/init-docs/SKILL.md`의 스크립트 경로 수정
- [x] 3. 수정된 경로가 실제 파일 위치와 일치하는지 검증

## 참고 사항

- `skills/init-docs/scripts/create-structure.sh` 스크립트가 존재하며 올바른
  경로이다.
- `.skills/` 접두사는 더 이상 적용되지 않는 레거시 관례이다.
