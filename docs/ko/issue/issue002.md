# 이슈 002: 문서 탐색을 위한 @-reference 컨벤션 도입

**상태**: 열림
**생성일**: 2026-02-19

## 배경

현재 문서 시스템은 예시용 경로와 필수 참조 경로 모두에 백틱 표기를 사용하고
있어, 사람과 AI 에이전트가 한눈에 구분하기 어렵다.

예를 들어, CLAUDE.md에서:

- 33행: `docs/issue/issue003.md` — 예시용 (읽을 필요 없음)
- 48행: `docs/policy/policy.md` — 필수 참조 (반드시 로드해야 함)

두 경우 모두 동일한 백틱 표기를 사용하므로, 어떤 파일이 필수 컨텍스트인지
알려주는 시각적·의미적 신호가 없다. 이로 인해 사람과 에이전트 모두의
온보딩과 컨텍스트 로딩이 느려진다.

## 완료 기준

- [ ] `reference-convention.md` 정책이 `@`-reference 문법을 정의함
- [ ] CLAUDE.md가 모든 필수 컨텍스트 파일에 `[@경로](경로)` 형태를 사용함
- [ ] `templates/CLAUDE.md`가 업데이트된 루트 `CLAUDE.md`와 일치함
- [ ] `docs/policy/policy.md`가 "Related Policy Files"에서 `@`-reference를 사용함
- [ ] 기존 스킬(`new-policy`, `init-docs`)이 `@`-reference를 출력하도록 업데이트됨
- [ ] 모든 한국어 미러가 생성 또는 업데이트됨
- [ ] 깨진 `@`-reference가 없음 (참조된 모든 파일이 존재함)
- [ ] 예시/설명용 백틱 경로는 변경 없이 유지됨

## 작업 목록

- [ ] 1. issue002 문서 생성 (영문 + 한국어)
- [ ] 2. `docs/policy/reference-convention.md` 및 한국어 미러 생성
- [ ] 3. CLAUDE.md 구조 개선: "Policy Files"를 "Required Context"로 변경, `@`-reference 적용
- [ ] 4. `templates/CLAUDE.md`를 동일하게 업데이트
- [ ] 5. `docs/policy/policy.md` "Related Policy Files"에 `@`-reference 적용
- [ ] 6. `skills/new-policy/SKILL.md`에서 `@`-reference 형태 안내로 수정
- [ ] 7. `skills/init-docs/SKILL.md` 내장 템플릿 업데이트
- [ ] 8. 모든 한국어 미러 동기화

## 참고 사항

<!-- 작업 진행 중 결정 사항, 발견 사항, 차단 사항을 여기에 기록하세요 -->

- **문법 선택**: `[@docs/policy/policy.md](docs/policy/policy.md)` 형태 선택.
  GitHub/IDE에서 클릭 가능한 링크로 렌더링되며, `@` 접두사가 사람과 에이전트
  모두에게 "필수 컨텍스트"임을 알려준다.
- **grep 추출**: `grep -rn '\[@docs/' CLAUDE.md`로 모든 필수 참조 목록 추출 가능.
