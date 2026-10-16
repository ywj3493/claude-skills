---
name: issue-orca-worktree
version: 0.0.1
description: GitHub 이슈 번호 하나로 Orca 워크스페이스를 만든다. 최상위 이슈는 독립 워크스페이스로, 부모가 있는 이슈는 부모 이슈 워크스페이스의 하위로 만들고, 브랜치는 언제나 main에서 분기한다. 표시 이름은 이슈 제목 그대로다. 부모 워크스페이스가 없으면 만들지 않고 묻는다. "#61 워크스페이스 만들어줘", "이슈로 워크트리 생성"에 반응한다. 이슈 생성·시작은 issue-epic/issue-leaf, 에이전트 실행·터미널 제어는 orca-cli가 맡는다.
user-invocable: true
allowed-tools: Bash(gh repo view*), Bash(gh issue view*), Bash(gh api*), Bash(git fetch*), Bash(git rev-parse*), Bash(orca worktree list*), Bash(orca worktree current*), Bash(orca worktree create*), Bash(orca worktree set*), Bash(jq*)
---

## 개요

이슈 하나에 Orca 워크스페이스 하나를 만든다. 워크스페이스의 부모·자식이 이슈의
부모·자식(sub-issue)과 같아지게 하고, 표시 이름을 이슈 제목과 같게 맞춘다.

시작 전에 읽는다:

- `${CLAUDE_PLUGIN_ROOT}/references/issue-rules.md` (이하 `규약`)
- `${CLAUDE_PLUGIN_ROOT}/references/commands.md` — 특히 `## Orca`

---

## 절대 금지

- GitHub에 쓰지 않는다. 그래서 쓰기 권한은 확인하지 않는다(규약 §10)
- 이슈 하나에 워크스페이스를 둘 만들지 않는다
- `--name`에 이슈 제목을 넣지 않는다 — 브랜치에서 `issue<N>`이 사라진다(규약 §3)
- base를 찾지 못했다고 다른 ref로 바꿔 다시 만들지 않는다
- 에이전트 실행(`--agent`), 터미널 제어, 삭제, 화면 전환(`--activate`)은 하지
  않는다. 요청받으면 생성 뒤 `orca-cli`로 이어 가라고 안내한다

---

## Step 0: 진입 조건

1. `저장소 조회`가 되는가. 아니면 멈춘다
2. `워크스페이스 목록`이 되는가. 아니면 멈춘다

   > "Orca CLI를 쓸 수 없습니다. Orca가 설치·실행 중인지 확인하세요."

3. 이슈 번호가 없으면 묻는다

## Step 1: 이슈 확인

`이슈 조회`. 종류(규약 §1)는 보고에만 쓴다 — 명령은 부모 유무로만 갈린다.
닫힌 이슈면 묻는다.

> "#<N>은 닫힌 이슈입니다. 그래도 워크스페이스를 만들까요?"

## Step 2: 중복 확인

`워크스페이스 목록`에서 같은 저장소이고 `linkedIssue`가 이 이슈인 항목이 있으면
새로 만들지 않는다. `displayName`이 이슈 제목과 같으면 경로·브랜치를 보고하고
끝낸다. 다르면 묻는다.

> "#<N>의 워크스페이스가 이미 있습니다. 표시 이름 `<displayName>`을 이슈 제목 `<제목>`으로 바꿀까요?"

승인하면 `표시 이름`을 실행하고 끝낸다.

## Step 3: 부모 워크스페이스

`부모 조회`. 최상위면 Step 4로 간다.

부모가 있으면 `워크스페이스 목록`에서 같은 저장소이고 `linkedIssue`가 부모 번호인
항목을 찾는다. 부모가 시작됐는지는 따지지 않는다 — 브랜치를 부모에서 따오지
않는다.

- 1개 — 그 `worktree:<id>`가 부모다
- 2개 이상 — 묻는다

  > "부모 #<P>의 워크스페이스가 여럿입니다. 어느 것을 부모로 할까요? 1. `<displayName>` — `<branch>` 2. …"

- 0개 — 만들지 않고 묻는다

  > "부모 #<P>의 워크스페이스가 없습니다. 1. 중단 — 이 스킬로 #<P>를 먼저 만든 뒤 #<N>으로 다시 실행 (권장 — 이슈 계층이 워크스페이스 계층으로 보인다) 2. 부모 없이 독립 워크스페이스로 만든다"

## Step 4: 미리보기

`--name`은 `<type>/issue<N>-<slug>`(규약 §3), 표시 이름은 이슈 제목 그대로다.

> "워크스페이스를 만들까요? 표시 이름 `<이슈 제목>`, `--name` `<type>/issue<N>-<slug>`(브랜치는 `<사용자>/<type>-issue<N>-<slug>` 꼴이 된다), 부모 `<부모 displayName 또는 없음>`, base `origin/<기본 브랜치>`"

## Step 5: 생성

`워크스페이스 생성` → 이어서 `표시 이름`(Step 4에서 승인받았으므로 다시 묻지
않는다). 실패하면 규약 §10.

## Step 6: 결과 확인

결과 JSON(키를 알 수 없으면 `워크스페이스 목록`)에서 넷을 확인한다. 어긋나면
고치지 않고 보고의 `불일치`에 다음 단계와 함께 적는다.

| 확인 | 어긋날 때 안내 |
|---|---|
| `linkedIssue` = N | `orca worktree set --worktree worktree:<id> --issue <N>` |
| `parentWorktreeId` = 부모 id (최상위·독립이면 `null`) | `orca worktree set --worktree worktree:<id> --parent-worktree worktree:<부모 id>` |
| `displayName` = 이슈 제목 | `표시 이름`을 한 번 다시 |
| 브랜치가 `(^|[/-])issue<N>-`에 맞음 | 시작 동작이 이슈 브랜치로 못 알아본다. 실제 브랜치를 적고 규약 §3을 고쳐야 할 수 있다고 알린다 |

## 보고

```markdown
## issue-orca-worktree 결과

| 이슈 | 종류 | 표시 이름 | 경로 | 브랜치 | 부모 워크스페이스 |
|---|---|---|---|---|---|
| #<N> | epic / leaf / 종류 미정 | <displayName> | <path> | <실제 브랜치> | <부모 또는 없음> |

- 불일치: <Step 6에서 어긋난 것과 안내. 없으면 생략>
- 다음 단계: 이 워크스페이스에서 `issue-epic` 또는 `issue-leaf`의 `시작`
```
