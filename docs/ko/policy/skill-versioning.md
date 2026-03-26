# 스킬 버전 관리 정책

## Purpose

이 저장소의 스킬들이 어떻게 버전 관리되고, 태그되며, 변경 사항이 어떻게
기록되는지 정의한다.

## Versioning Scheme

스킬은 v0.x.y 개발 단계를 포함한
[Semantic Versioning](https://semver.org/)을 따른다:

- **v0.x.y** — 초기 개발 단계. 스킬이 아직 안정적으로 확인되지 않은 상태.
  모든 새 스킬은 `v0.0.1`부터 시작한다.
- **v1.0.0** — 스킬이 안정적이고 의도대로 동작함이 확인된 후에만 승격.
- v1.0.0 이후:
  - **Major** — 스킬 동작, 출력 형식, 필수 입력의 호환성이 깨지는 변경
  - **Minor** — 새 기능, 템플릿, 호환성을 유지하는 개선
  - **Patch** — 버그 수정, 오타 수정, 사소한 문구 변경

## SKILL.md Version Field

모든 SKILL.md는 YAML frontmatter에 `version` 필드를 포함해야 한다:

```yaml
---
name: my-skill
version: 0.0.1
description: What this skill does
---
```

## Git Tag Convention

하나의 저장소에 여러 스킬이 있으므로, 태그에 스킬 이름을 포함한다:

```text
<skill-name>/v<major>.<minor>.<patch>
```

예시:
- `backend-planning/v0.0.1`
- `new-issue/v0.1.0`
- `frontend-planning/v1.0.0`

프로젝트 전체 릴리즈에는 일반 버전 태그를 사용한다:

```text
v<major>.<minor>.<patch>
```

## Changelog

단일 `CHANGELOG.md`가 프로젝트 루트에 위치한다. 항목은 **최신순**으로
정렬된다. 각 항목은 다음 형식을 따른다:

```markdown
## [skill-name/v0.1.0] - YYYY-MM-DD

### Added
- 새 기능 설명

### Changed
- 변경된 동작 설명

### Fixed
- 버그 수정 설명
```

허용되는 섹션 헤더: `Added`, `Changed`, `Fixed`, `Removed`.

## When to Bump Versions

- 모든 스킬 수정에는 SKILL.md의 버전 업과 해당하는 CHANGELOG.md 항목이
  포함되어야 한다.
- main에 머지한 후 커밋에 태그를 지정한다.

## Related Documents

- [@docs/en/policy/policy.md](docs/en/policy/policy.md) — 일반 작업 규칙
- [@docs/en/policy/commit-message-rule.md](docs/en/policy/commit-message-rule.md) — 커밋 메시지 형식
