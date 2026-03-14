# 이슈 005: frontend-planning 및 init-docs 스킬 개선

**상태**: 진행 중
**생성일**: 2026-03-12

## 배경

`frontend-planning` 스킬(issue003)에 개선이 필요한 부분이 있습니다:

- 모든 프롬프트, 템플릿, 사용자 메시지가 한국어로 되어 있으나 `docs/en/` 규칙에
  따라 영어로 작성되어야 함
- 도메인 분석 단계가 없어 6개 문서가 `specifications/`에 논리적 그룹 없이
  평면적으로 생성됨
- 출력 파일명에 번호 접두사(`01-requirements.md`)가 사용되고 있어 제거 필요
- `init-docs` 스킬과 `CLAUDE.md`가 새로운 도메인 기반 디렉터리 구조를 반영해야 함

원래 스킬 생성 이슈는
[@docs/en/issue/issue003.md](docs/en/issue/issue003.md) 참조.

## 인수 기준

- [ ] `SKILL.md` 설명 및 모든 사용자 메시지가 영어로 작성됨
- [ ] 기술 스택 감지와 요구사항 사이에 새로운 Step 0.5(도메인 분석) 추가
- [ ] 출력 경로가 도메인 기반 구조 사용: `specifications/<domain>/requirements/` 및 `specifications/<domain>/workflows/`
- [ ] 최상위 공통 문서가 `specifications/` 루트에 위치: `architecture.md`, `config.md`, `infrastructure.md`
- [ ] 6개 참조 템플릿의 번호 접두사 제거 및 영어로 재작성
- [ ] 멀티 도메인 흐름: 다음 도메인으로 넘어가기 전에 한 도메인의 6단계 모두 완료
- [ ] Step 7에서 모든 도메인과 문서를 나열하는 `README.md` 생성
- [ ] `init-docs` SKILL.md에 새로운 구조 다이어그램 반영
- [ ] `create-structure.sh`에서 최상위 스펙 템플릿 파일 생성
- [ ] `CLAUDE.md` 문서 구조 섹션 업데이트
- [ ] 이전 번호 파일명에 대한 참조가 남아 있지 않음
- [ ] 한국어 텍스트는 "When to Use" 트리거 문구에만 유지

## 작업

- [ ] 1. issue005 문서 생성 (영어 + 한국어)
- [ ] 2. `skills/frontend-planning/SKILL.md` 재작성
- [ ] 3. 6개 참조 템플릿 이름 변경 및 영어로 재작성
- [ ] 4. init-docs용 최상위 스펙 참조 템플릿 생성
- [ ] 5. `skills/init-docs/SKILL.md` 및 `scripts/create-structure.sh` 업데이트
- [ ] 6. `CLAUDE.md` 문서 구조 섹션 업데이트
- [ ] 7. issue003에 교차 참조 메모 추가

## 메모

- 도메인 디렉터리는 단일 도메인 프로젝트에서도 항상 생성됨
- `skills/frontend-planning/references/`의 템플릿 파일은 번호 접두사 없이 이름 변경
- `skills/init-docs/references/`에 3개 새 템플릿 추가: `architecture-template.md`, `config-template.md`, `infrastructure-template.md`
