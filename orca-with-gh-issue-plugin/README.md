# orca-with-gh-issue 플러그인

GitHub 이슈를 **epic / leaf** 계층으로 관리하고, 이슈 하나당 Orca
워크스페이스 하나에서 작업하는
[Claude Code 플러그인](https://docs.claude.com/en/docs/claude-code/plugins)입니다.
프롬프트와 템플릿은 한국어입니다.

- **epic**은 기획·설계를 맡고 하위 이슈(GitHub sub-issue)를 거느립니다.
  구현 코드는 쓰지 않습니다.
- **leaf**는 구현을 맡습니다. 수용 기준이 6개를 넘으면 leaf로 만들지 않고
  epic으로 나눕니다.
- 모든 이슈는 **Draft PR**로 시작합니다. Draft PR이 열려 있다는 것이 "누군가
  맡았다"는 표시입니다.
- 이슈마다 **Orca 워크스페이스**를 하나씩 두고, 워크스페이스의 부모·자식
  관계를 이슈의 부모·자식 관계와 맞춥니다.

규칙은 [references/issue-rules.md](references/issue-rules.md) 한 곳에만
있습니다. 세 스킬은 그 규칙을 실행하는 순서만 정합니다.

## 구성

| 종류 | 명령어 / 이름 | 용도 |
| --- | --- | --- |
| 스킬 | `/orca-with-gh-issue:issue-epic` | 생성(하위 이슈 계획을 세워 sub-issue로 함께 등록) · 하위 이슈 추가 · 시작(Draft PR) · 동기화(체크리스트, `blocked` 라벨) · 마무리(누락·보강 점검 → 정리 작업이 있으면 머지, 없으면 닫기) |
| 스킬 | `/orca-with-gh-issue:issue-leaf` | 생성(부모 epic 연결, 크기 라벨, 선행 이슈) · 시작(기본 브랜치를 base로 Draft PR, `Closes #N`) |
| 스킬 | `/orca-with-gh-issue:issue-orca-worktree` | 이슈 번호로 Orca 워크스페이스 생성. 최상위 이슈는 독립, 부모가 있으면 부모 워크스페이스의 하위. 표시 이름은 이슈 제목 그대로 |
| 규약 | `references/issue-rules.md` | 용어, 계층, Draft PR 시작, 순서·Blocked, epic 추적과 마무리, 규모, 사전 점검, 확인 게이트, 라벨, 실패 처리 |
| 명령 | `references/commands.md` | 스킬이 이름으로 부르는 gh · git · orca 명령 (예: `PR 목록`, `워크스페이스 생성`) |
| 예시 | `references/examples.md` | epic 1개와 leaf 2개의 가상 예시, 실제로 본 문제와 처리 방법 |
| 템플릿 | `templates/` | epic/leaf 이슈 본문, epic/leaf Draft PR 본문 |

## 워크플로

```text
/orca-with-gh-issue:issue-epic        생성        epic #60 + 하위 leaf #61, #62 등록 (#62는 #61에 Blocked)
/orca-with-gh-issue:issue-orca-worktree #60      독립 워크스페이스
/orca-with-gh-issue:issue-epic        시작        Draft PR #70 (base: main)

/orca-with-gh-issue:issue-orca-worktree #61      #60 워크스페이스의 하위 (main에서 분기)
/orca-with-gh-issue:issue-leaf        시작        Draft PR #71 (base: main, Closes #61)
  … 구현, 리뷰, #71을 main에 머지 → #61 자동으로 닫힘 …

/orca-with-gh-issue:issue-epic        동기화      #62 Blocked 해제, 체크리스트 갱신
  … #62도 같은 흐름 …
/orca-with-gh-issue:issue-epic        마무리      누락·보강 점검 → 정리 작업이 있으면 #70 머지, 없으면 #70 닫고 #60 닫기
```

## 꼭 알아둘 점

- **모든 PR은 기본 브랜치에 바로 머지됩니다.** epic 브랜치로 모으지 않으므로
  main이 늘 최신이고 `Closes #N`이 그대로 동작합니다. 대신 epic 단위로 한꺼번에
  내보내지 않으니, 미완성 기능을 숨겨야 하면 기능 플래그를 씁니다.
- **epic은 하위 이슈를 등록한 상태로만 만듭니다.** 나눌 계획을 본문에만 적은
  epic은 진행이 추적되지 않습니다. epic 생성은 하위 이슈 계획(설계·계약 leaf
  먼저, BE·FE 분리, 실제로 막는 것만 선행)과 한 묶음이며, 하위 이슈가 없는
  epic이나 하위 이슈를 거느린 leaf는 동기화가 `이상`으로 알려 줍니다.
- **leaf가 읽을 설계 문서는 문서 leaf로 먼저 머지합니다.** epic PR은 마무리
  때까지 머지되지 않아 거기 둔 문서는 leaf가 볼 수 없습니다. 구현 leaf는 문서
  leaf를 선행 이슈로 둡니다.
- **Blocked 해제도 자동이 아닙니다.** epic 동기화나 이슈 시작을 실행할 때
  판정합니다.
- **쓰기 권한이 필요합니다.** GitHub에 쓰는 동작 전에 활성 gh 계정의 push
  권한을 확인하고, 없으면 아무것도 쓰지 않고 멈춥니다. 계정은 직접 바꿉니다
  (`gh auth switch -u <계정>`).
- **필요한 라벨**: `epic`, `leaf`, `blocked`, `size/XS`·`S`·`M`·`L`·`XL`·`XXL`.
  없으면 처음 쓸 때 만들지 묻습니다.
- GitHub sub-issue와 이슈 의존성(blocked by) API를 씁니다. gh 2.87.3 기준으로
  `gh issue create`에는 부모 지정 옵션이 없어 `gh api`로 연결합니다.

## 요구 사항

- `gh` CLI (로그인된 계정에 대상 저장소 push 권한)
- Orca CLI (`orca worktree create`가 `--issue`, `--parent-worktree`,
  `--no-parent`, `--base-branch`를 지원하는 버전) — `issue-orca-worktree`에만
  필요합니다
