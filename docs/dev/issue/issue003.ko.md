# 이슈 003: frontend-planning 스킬 추가

**상태**: 열림
**생성일**: 2026-02-25

## 배경

프로젝트는 이미 백엔드 기획 파이프라인(requirements → user-stories → use-cases →
sequence-diagram → api-spec)을 사용하여 구현 전에 구조화된 설계 문서를 작성하고 있다.

프론트엔드 프로젝트에도 UI 관점에 맞게 조정된 동등한 파이프라인이 필요하다:
requirements → user-flows → page-spec → use-cases → component-tree →
state-api-integration (6단계).

이 이슈는 `docs/specifications/`에 6개의 기획 문서를 순차적으로 생성하며, 각
단계마다 사용자 검토와 피드백을 거치도록 안내하는 `frontend-planning` 스킬 생성을
추적한다.

모든 기획 문서는 사용자의 프론트엔드 설계 문서 선호에 따라 한국어로 작성하되,
기술 용어는 영어를 병기한다.

## 완료 기준

- [ ] `.agents/skills/frontend-planning/SKILL.md`가 올바른 YAML front matter와 함께 존재
- [ ] `.agents/skills/frontend-planning/references/`에 6개 참조 템플릿 존재
- [ ] 스킬이 `docs/specifications/`에 문서 생성 (01~06)
- [ ] 각 단계가 이전 모든 단계의 결과물을 참조
- [ ] 각 단계 완료 후 다음 단계 진행 전 사용자 검토 요청
- [ ] `package.json` / `tsconfig.json`에서 기술 스택 자동 감지
- [ ] `docs/specifications/`에 기존 백엔드 문서가 있는 경우 참조
- [ ] 모든 문서에 메타 정보 포함 (생성일, 최종 수정일, 상태)
- [ ] user-flows와 component-tree에 Mermaid 다이어그램 포함
- [ ] component-tree와 state-api-integration에 TypeScript 인터페이스 포함
- [ ] 6단계 완료 후 `docs/specifications/README.md` 목차 생성
- [ ] 올바른 트리거 구문 (한국어 및 영어) 문서화
- [ ] 비트리거 조건 문서화
- [ ] 이 이슈의 한국어 미러가 `docs/dev/issue/issue003.ko.md`에 존재

## 작업 목록

- [ ] 1. 이슈 문서 생성 (영문 + 한국어)
- [ ] 2. `.agents/skills/frontend-planning/SKILL.md` 생성
- [ ] 3. `.agents/skills/frontend-planning/references/`에 6개 참조 템플릿 생성

## 참고 사항

<!-- 작업 진행 중 결정 사항, 발견 사항, 차단 사항을 여기에 기록하세요 -->

- **파이프라인**: 6단계 — requirements → user-flows → page-spec → use-cases →
  component-tree → state-api-integration
- **출력 디렉토리**: `docs/specifications/` (다른 설계 문서와 동일 위치)
- **언어**: 한국어 + 영어 기술 용어 (영어 우선 + 한국어 미러 방식 아님)
- **배포 방식**: git + `add skill` (수동 `skills/` 복사나 심볼릭 링크 불필요)
