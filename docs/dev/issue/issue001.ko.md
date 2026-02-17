# 이슈 001: 저장소 문서 시스템 초기화

**상태**: 완료
**생성일**: 2026-02-17

## 배경

스킬 팩토리 저장소는 스킬과 템플릿을 갖추고 있었지만, 저장소 자체의 `docs/` 구조가 없었습니다.
이 이슈는 `init-docs` 스킬을 이 팩토리 저장소 자체에 적용하는 작업을 추적합니다.
이를 통해 스킬과 템플릿 CLAUDE.md가 실제로 올바르게 동작하는지 검증합니다.

## 완료 기준

- [x] `create-structure.sh`를 통해 `docs/` 디렉토리 구조 생성
- [x] 루트 `CLAUDE.md`를 `templates/CLAUDE.md` 내용으로 통일 (교체)
- [x] 영어로 초기 정책 파일 3개 생성
- [x] `docs/dev/policy/`에 한국어 미러 생성
- [x] `README.md`를 팩토리 개발 가이드 포함하여 한국어로 재작성

## 작업 목록

- [x] 1. `skills/init-docs/scripts/create-structure.sh` 실행
- [x] 2. 루트 `CLAUDE.md`를 `templates/CLAUDE.md` 내용으로 교체
- [x] 3. `docs/policy/policy.md` 생성
- [x] 4. `docs/policy/commit-message-rule.md` 생성
- [x] 5. `docs/policy/naming-conventions.md` 생성
- [x] 6. `docs/dev/policy/`에 한국어 미러 생성
- [x] 7. `README.md`를 팩토리 개발 가이드 포함하여 한국어로 재작성

## 참고 사항

이 이슈는 저장소 자체 문서 시스템의 초기 설정을 기록하고, 스킬과 템플릿이 실제 프로젝트에
적용했을 때 올바르게 동작함을 검증하기 위해 작성된 부트스트랩 이슈입니다.

루트 `CLAUDE.md`와 `templates/CLAUDE.md`가 이제 동일하므로, 다른 프로젝트에서도
해당 템플릿을 신뢰하고 도입할 수 있습니다.
