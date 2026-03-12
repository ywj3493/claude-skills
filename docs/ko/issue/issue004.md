# 이슈 004: docs/ 디렉토리를 언어 코드 기반 구조로 재구성

**상태**: 완료
**생성일**: 2026-03-09

## 배경

현재 `docs/` 구조는 영어 문서가 루트에 위치하고 한국어 번역이 `docs/dev/`에
`.ko.md` 접미사로 존재한다. 이 구조는 언어 간 비대칭적이며 새 언어를 추가할 때
일관성을 유지하기 어렵다.

`docs/en/`, `docs/ko/` 패턴을 도입하여 각 언어를 동등하게 취급하고 구조의
확장성을 확보하는 것이 목표이다.

## 완료 기준

- [x] 영어 문서를 `docs/en/{specifications,issue,policy}/`로 이동
- [x] 한국어 문서를 `docs/ko/{specifications,issue,policy}/`로 이동 (`.ko.md` 접미사 제거)
- [x] `docs/reference/`는 루트 레벨 유지 (언어 무관)
- [x] `docs/dev/` 디렉토리 제거
- [x] CLAUDE.md 및 `templates/CLAUDE.md`를 새 경로로 업데이트
- [x] 모든 정책 파일의 경로 참조 업데이트
- [x] 모든 스킬을 새 경로로 업데이트
- [x] `skills/sync-dev/`를 `skills/sync-translations/`로 이름 변경
- [x] README.md 업데이트
- [x] 이전 경로(`docs/dev/`, `docs/policy/`, 스킬 내 `.ko.md`) 잔여 참조 없음

## 작업 목록

- [x] 1. 이전 구조에서 issue004 문서 생성 (영문 + 한국어)
- [x] 2. `git mv`로 새 디렉토리 레이아웃에 파일 마이그레이션
- [x] 3. CLAUDE.md 및 `templates/CLAUDE.md` 업데이트
- [x] 4. 정책 파일 업데이트 (영문 및 한국어)
- [x] 5. 모든 스킬을 새 경로로 업데이트
- [x] 6. `skills/sync-dev/`를 `skills/sync-translations/`로 이름 변경
- [x] 7. README.md 업데이트
- [x] 8. 이전 경로 잔여 참조 확인

## 참고 사항

- 기존 이슈(001–003)는 작성 당시의 구조를 반영하므로 그대로 유지한다.
- `reference/` 디렉토리는 참조 자료가 언어 무관하고 사용자가 관리하므로
  `docs/reference/`에 그대로 둔다.
