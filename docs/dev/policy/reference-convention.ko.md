# 문서 참조 컨벤션

## 목적

필수로 읽거나 로드해야 하는 문서를 일관되게 표시하는 방법을 정의하여,
예시나 설명용으로 언급된 경로와 구분한다.

## 문법

**필수 컨텍스트**를 표시하려면 `@` 접두사가 포함된 마크다운 링크를 사용한다:

```markdown
[@docs/policy/policy.md](docs/policy/policy.md)
```

`@` 없이 백틱으로 감싼 경로는 정보 제공 또는 예시용이다:

```markdown
`docs/issue/issue003.md`
```

## 규칙

1. `@`-reference는 "이 파일을 반드시 로드한 후 진행하라"는 의미이다.
2. CLAUDE.md, 정책 파일, 이슈 문서, 스킬 정의에서 선행 파일이 있을 때
   `@`-reference를 사용한다.
3. `@`-reference는 프로젝트 루트 상대 경로를 사용한다 (앞에 `/` 없음).
4. `docs/reference/`의 파일은 `@`-reference 대상에서 제외한다
   — 해당 디렉토리는 사용자가 관리하며 표준 백틱 경로로만 인용한다.
5. `@`-reference된 파일 내에 추가 `@`-reference가 있으면 재귀적으로
   로드한다 (최대 2단계).
6. `[@경로](경로)` 마크다운 링크 형태로 GitHub 및 IDE에서 클릭 가능한
   탐색을 보장한다.

## AI 에이전트를 위한 안내

작업을 시작하기 전에 로드된 CLAUDE.md와 현재 이슈 문서에서
`@`-reference를 스캔한다. 참조된 모든 파일을 로드한 후, 해당 파일들에서
추가 `@`-reference를 스캔하여 로드한다 (최대 2단계).

모든 참조를 프로그래밍적으로 추출:

```bash
grep -rn '\[@docs/' CLAUDE.md docs/
```

## 사람을 위한 안내

`@`-reference는 현재 문서의 범위에서 작업하기 전에 읽어야 할 파일을
나타낸다. "필수 읽기" 목록이다. GitHub과 대부분의 IDE에서 클릭 가능한
링크로 렌더링되어 쉽게 탐색할 수 있다.

## 형식 예시

**목록 형태 (CLAUDE.md 및 정책 파일에서 주로 사용):**

```markdown
- [@docs/policy/policy.md](docs/policy/policy.md) — General working rules
- [@docs/policy/commit-message-rule.md](docs/policy/commit-message-rule.md) — Commit message format
```

**인라인 형태 (이슈 문서에서 주로 사용):**

```markdown
This issue implements the requirements in
[@docs/specifications/auth.md](docs/specifications/auth.md).
```

**메타 참조 (컨벤션 자체를 논의할 때):**

`@`-reference 컨벤션을 논의할 때는 백틱을 사용한다:
`` `[@docs/policy/policy.md](docs/policy/policy.md)` ``

## 개정 이력

- 2026-02-19: 최초 작성
