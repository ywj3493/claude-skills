# 이슈 004: npx를 통한 frontend-planning 스킬 배포 문제 수정

**상태**: 열림
**생성일**: 2026-03-01

## 배경

이슈 003에서 `frontend-planning` 스킬을 도입하였다. 해당 이슈의 완료 기준과 참고 사항에는
스킬의 설치 대상 경로를 `.agents/skills/frontend-planning/SKILL.md`로 명시하고 있다.
이는 설치 완료 후 *사용자 프로젝트* 내에서 스킬이 위치하는 경로다.

그런데 스킬 소스 파일이 이 *저장소* 내에서 `skills/` 대신 `.agents/skills/` 아래에 배치되었다
(또는 배치될 계획이었다). `npx skills add` 설치 도구는 스킬 정의 파일을 `skills/` 디렉토리에서
읽어 대상 프로젝트의 `.agents/skills/` 디렉토리로 복사한다. `frontend-planning`이 `skills/`에
없으면 설치 도구가 이를 찾거나 배포할 수 없다.

기존의 네 가지 스킬(`init-docs`, `new-issue`, `new-policy`, `sync-dev`)은 모두 이 저장소의
`skills/<name>/SKILL.md` 아래에 위치하여 `npx skills add`를 통해 정상 설치된다.
`frontend-planning` 스킬도 동일한 배포 방식을 따르려면 같은 패턴을 적용해야 한다.

## 완료 기준

- [ ] `skills/frontend-planning/SKILL.md`가 올바른 YAML front matter와 함께 이 저장소에 존재
- [ ] `skills/frontend-planning/references/`에 6개의 참조 템플릿 존재
- [ ] `npx skills add` 실행 시 `frontend-planning`이 대상 프로젝트의 `.agents/skills/frontend-planning/`에 정상 설치
- [ ] README 스킬 목록에 `frontend-planning` 항목 추가
- [ ] 이슈 003 완료 기준이 소스 경로를 `skills/frontend-planning/`으로 반영하도록 수정
- [ ] 이 이슈의 한국어 미러가 `docs/dev/issue/issue004.ko.md`에 존재

## 작업 목록

- [ ] 1. 이슈 문서 생성 (영문 + 한국어 미러)
- [ ] 2. YAML front matter와 전체 스킬 지시사항을 포함한 `skills/frontend-planning/SKILL.md` 생성
- [ ] 3. `skills/frontend-planning/references/`에 6개 참조 템플릿 생성
- [ ] 4. `npx skills add`가 대상 프로젝트에 스킬을 올바르게 설치하는지 검증
- [ ] 5. `README.md` 스킬 목록에 `frontend-planning` 항목 추가
- [ ] 6. 이슈 003 완료 기준을 소스 경로 `skills/frontend-planning/`으로 수정

## 참고 사항

<!-- 작업 진행 중 결정 사항, 발견 사항, 차단 사항을 여기에 기록하세요 -->

- **근본 원인**: 이슈 003에서 설치 도구가 읽는 *소스* 경로(`skills/frontend-planning/`)가 아닌
  *대상* 경로(`.agents/skills/frontend-planning/`)로 기술하여, 스킬이 배포에 적합하지 않은
  위치에 생성되는 문제가 발생하였다.
- **수정 방향**: 다른 모든 스킬과 일관되게 `skills/frontend-planning/`에 스킬 소스를 생성한다.
  그러면 `npx skills add` 설치 도구가 이를 대상 프로젝트의 `.agents/skills/frontend-planning/`에
  복사하여 의도한 설치 경로를 충족한다.
- **설치 도구 수정 불필요**: 기존 설치 도구 로직이 이 패턴을 이미 처리하고 있으므로 스킬 소스
  위치만 수정하면 된다.
