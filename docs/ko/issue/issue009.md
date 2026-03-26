# Issue 009: 스킬 버전 관리 체계 도입

**Status**: Done
**Created**: 2026-03-19

## Background

이 프로젝트의 스킬들은 `npx skills add`를 통해 외부에서 설치되며 활발히
수정되고 있지만, 공식적인 버전 관리가 이루어지지 않고 있다. 변경 사항은
git 커밋 히스토리를 통해서만 암묵적으로 추적된다. 이로 인해 설치된 스킬의
버전을 파악하거나, 호환성이 깨지는 변경이 있었는지, 릴리즈 간에 무엇이
바뀌었는지 확인하기 어렵다.

## Requirements

1. **스킬별 버전 관리** — 각 스킬이 버전 식별자를 가지고, 스킬 변경 시
   업데이트되어야 한다.
2. **Git tag 연동** — 스킬 버전이 git tag와 연동되어 저장소 히스토리에서
   릴리즈가 명확히 표시되어야 한다.
3. **최신순 변경 기록** — 변경 이력은 가장 최근 항목이 상단에 오도록
   기록되어야 한다.

## Acceptance Criteria

- [ ] 각 SKILL.md의 frontmatter에 `version` 필드 포함
- [ ] `docs/en/policy/`에 버전 관리 정책 문서 존재 (한국어 번역 포함)
- [ ] Git tag가 스킬 버전에 대한 정의된 명명 규칙을 따름
- [ ] 프로젝트 루트에 최신순 정렬의 CHANGELOG.md 존재
- [ ] 모든 기존 스킬에 초기 버전 번호 부여 완료
- [ ] 버전 관리 정책에 major, minor, patch 버전 업 기준 정의

## Tasks

1. [ ] 버전 관리 정책 정의 (시맨틱 버전 규칙, 태그 명명 규칙, 변경 기록 형식)
2. [ ] `docs/en/policy/skill-versioning.md` 및 한국어 번역 생성
3. [ ] 모든 기존 SKILL.md frontmatter에 `version` 필드 추가
4. [ ] 프로젝트 레벨 CHANGELOG.md를 최신순 형식으로 생성
5. [ ] 현재 상태를 초기 릴리즈로 git tag 지정
6. [ ] CLAUDE.md에 새 버전 관리 정책 참조 추가

## Design Decisions

### 태그 명명 규칙

하나의 저장소에 여러 스킬이 있으므로, 태그에 스킬 이름을 포함한다:

```text
<skill-name>/v<major>.<minor>.<patch>
```

예시:
- `backend-planning/v1.0.0`
- `new-issue/v1.0.0`
- `frontend-planning/v1.1.0`

프로젝트 전체 릴리즈에는 일반 버전 태그를 사용한다:

```text
v<major>.<minor>.<patch>
```

### 시맨틱 버전 규칙

- **v0.x.y** — 초기 개발 단계; 스킬은 v0.0.1부터 시작
- **v1.0.0** — 스킬이 안정적이고 의도대로 동작함이 확인된 후에만 승격
- **Major (1+)** — 스킬 동작, 출력 형식, 필수 입력의 호환성이 깨지는 변경
- **Minor** — 새 기능, 템플릿, 호환성을 유지하는 개선
- **Patch** — 버그 수정, 오타 수정, 사소한 문구 변경

### CHANGELOG 형식

```markdown
# Changelog

## [skill-name/v1.1.0] - 2026-03-17

### Added
- architecture.md용 새 템플릿 추가

### Changed
- 파이프라인 단계 구조 변경

## [skill-name/v1.0.0] - 2026-03-10

### Added
- 최초 릴리즈
```

## Notes

- 모든 기존 스킬은 v0.0.1부터 시작
- 향후 스킬 수정 시 반드시 버전 업과 변경 기록 항목을 포함해야 함
