---
name: issue-orca-worktree
version: 0.1.0
description: GitHub 이슈 번호 하나로 Orca 워크스페이스를 만들고 에이전트를 띄운다. 최상위 이슈는 독립 워크스페이스로, 부모가 있는 이슈는 부모 이슈 워크스페이스의 하위로 만들고, 브랜치는 언제나 main에서 분기한다. 표시 이름은 이슈 제목 그대로다. 사용자가 에이전트를 말하지 않으면 epic은 Claude Code Agent Teams(orca claude-teams), leaf는 Claude Code(claude)를 띄운다. 부모 워크스페이스가 없으면 만들지 않고 묻는다. "#61 워크스페이스 만들어줘", "이슈로 워크트리 생성", "#61 codex로 워크스페이스"에 반응한다. 이슈 생성·시작은 issue-epic/issue-leaf, 띄운 뒤의 터미널 제어는 orca-cli가 맡는다.
user-invocable: true
allowed-tools: Bash(gh repo view*), Bash(gh issue view*), Bash(gh api*), Bash(git fetch*), Bash(git rev-parse*), Bash(orca worktree list*), Bash(orca worktree current*), Bash(orca worktree create*), Bash(orca worktree set*), Bash(orca terminal create*), Bash(jq*)
---

## 개요

이슈 하나에 Orca 워크스페이스 하나를 만들고, 그 워크스페이스에서 에이전트를 한
번 띄운다. 워크스페이스의 부모·자식이 이슈의 부모·자식(sub-issue)과 같아지게
하고, 표시 이름을 이슈 제목과 같게 맞춘다.

시작 전에 읽는다:

- `${CLAUDE_PLUGIN_ROOT}/references/issue-rules.md` (이하 `규약`)
- `${CLAUDE_PLUGIN_ROOT}/references/commands.md` — 특히 `## Orca`

---

## 절대 금지

- GitHub에 쓰지 않는다. 그래서 쓰기 권한은 확인하지 않는다(규약 §10)
- 이슈 하나에 워크스페이스를 둘 만들지 않는다
- `--name`에 이슈 제목을 넣지 않는다 — 브랜치에서 `issue<N>`이 사라진다(규약 §3)
- base를 찾지 못했다고 다른 ref로 바꿔 다시 만들지 않는다
- 에이전트는 Step 6에서 **한 번만** 띄운다. 이미 있던 워크스페이스(Step 2)에는
  띄우지 않는다. 띄운 뒤의 터미널 읽기·보내기·대기·닫기, 워크스페이스 삭제,
  화면 전환(`--activate`)은 하지 않는다. 요청받으면 `orca-cli`로 이어 가라고
  안내한다
- 에이전트 실행이 실패해도 워크스페이스를 지우거나 다시 만들지 않는다

---

## Step 0: 진입 조건

1. `저장소 조회`가 되는가. 아니면 멈춘다
2. `워크스페이스 목록`이 되는가. 아니면 멈춘다

   > "Orca CLI를 쓸 수 없습니다. Orca가 설치·실행 중인지 확인하세요."

3. 이슈 번호가 없으면 묻는다

## Step 1: 이슈 확인

`이슈 조회`. 종류(규약 §1)는 Step 4의 기본 에이전트와 보고에 쓴다 — 워크스페이스
생성 명령은 부모 유무로만 갈린다. 닫힌 이슈면 묻는다.

> "#<N>은 닫힌 이슈입니다. 그래도 워크스페이스를 만들까요?"

## Step 2: 중복 확인

`워크스페이스 목록`에서 같은 저장소이고 `linkedIssue`가 이 이슈인 항목이 있으면
새로 만들지 않고 에이전트도 띄우지 않는다. `displayName`이 이슈 제목과 같으면
경로·브랜치를 보고하고 끝낸다. 다르면 묻는다.

> "#<N>의 워크스페이스가 이미 있습니다. 표시 이름 `<displayName>`을 이슈 제목 `<제목>`으로 바꿀까요?"

승인하면 `표시 이름`을 실행하고 끝낸다. 보고의 다음 단계에 "에이전트가 필요하면
`orca-cli`로 띄운다"를 적는다.

## Step 3: 부모 워크스페이스

`부모 조회`. 최상위면 Step 4로 간다.

부모가 있으면 `워크스페이스 목록`에서 같은 저장소이고 `linkedIssue`가 부모 번호인
항목을 찾는다. 부모가 시작됐는지는 따지지 않는다 — 브랜치를 부모에서 따오지
않는다.

- 1개 — 그 항목의 `id`가 부모다 (선택자는 `id:<id>`)
- 2개 이상 — 묻는다

  > "부모 #<P>의 워크스페이스가 여럿입니다. 어느 것을 부모로 할까요? 1. `<displayName>` — `<branch>` 2. …"

- 0개 — 만들지 않고 묻는다

  > "부모 #<P>의 워크스페이스가 없습니다. 1. 중단 — 이 스킬로 #<P>를 먼저 만든 뒤 #<N>으로 다시 실행 (권장 — 이슈 계층이 워크스페이스 계층으로 보인다) 2. 부모 없이 독립 워크스페이스로 만든다"

## Step 4: 에이전트 결정

위에서부터 처음 해당하는 것으로 정한다.

| 순위 | 조건 | 에이전트 |
|---|---|---|
| 1 | 사용자가 이번 요청에서 에이전트를 말했다 ("codex로", "claude-teams로") | 그 값 |
| 2 | 사용자가 띄우지 말라고 했다 ("에이전트 없이", "워크스페이스만") | `없음` |
| 3 | 이슈가 epic | `claude-teams` |
| 4 | 이슈가 leaf | `claude` |
| 5 | 종류 미정 | 묻는다 (아래) |

> "#<N>은 종류 미정입니다(`epic`/`leaf` 라벨이 없거나 둘 다 있음). 어떤 에이전트를 띄울까요? 1. `claude` (권장 — 단일 작업의 기본값) 2. `claude-teams` 3. 띄우지 않음"

- `claude-teams`는 Orca 에이전트 ID가 아니라 `orca claude-teams` 명령이다.
  그 밖의 값(`claude`, `codex`, `opencode` 등)은 Orca 에이전트 ID로
  `--agent`에 넘긴다. ID가 맞는지 미리 검사하지 않는다 — 틀리면 Orca가 거부하고
  Step 7에서 보고된다
- 초기 프롬프트는 사용자가 이번 요청에서 작업 지시를 함께 준 때만 넘긴다.
  스킬이 지어내지 않는다

## Step 5: 미리보기

`--name`은 `<type>/issue<N>-<slug>`(규약 §3), 표시 이름은 이슈 제목 그대로다.

> "워크스페이스를 만들까요? 표시 이름 `<이슈 제목>`, `--name` `<type>/issue<N>-<slug>`(브랜치는 `<사용자>/<type>-issue<N>-<slug>` 꼴이 된다), 부모 `<부모 displayName 또는 없음>`, base `origin/<기본 브랜치>`, 에이전트 `<claude-teams / claude / 지정 값 / 없음>`(<결정 근거: 사용자 지정 / epic 기본 / leaf 기본>), 초기 프롬프트 `<내용 또는 없음>`. 에이전트를 바꾸려면 함께 말해 주세요."

답에서 에이전트를 바꾸면 그 값으로 다시 이 미리보기를 보인다.

## Step 6: 생성과 에이전트 실행

에이전트에 따라 명령이 다르다(`commands.md` `## Orca`).

| 에이전트 | 순서 |
|---|---|
| `claude`·지정 ID | `워크스페이스 생성`에 `--agent <ID>`(초기 프롬프트가 있으면 `--prompt`)를 붙여 실행 → `표시 이름` |
| `claude-teams` | `워크스페이스 생성`(에이전트 없이) → `표시 이름` → `Teams 실행` |
| `없음` | `워크스페이스 생성` → `표시 이름` |

Step 5에서 승인받았으므로 사이사이 다시 묻지 않는다.

실패 처리:

- `워크스페이스 생성`이 실패하면 다시 실행하기 **전에** `워크스페이스 목록`에서
  `linkedIssue`가 N인 항목을 찾는다. 있으면 워크스페이스는 만들어진 것이다 —
  다시 만들지 않고 그 항목의 `id`로 나머지 순서(`표시 이름`, `claude-teams`면
  `Teams 실행`)를 이어 간다. `--agent`를 붙였던 경우는 에이전트가 떴는지 알 수
  없으므로 다시 띄우지 않고 에이전트 실패로 본다. 항목이 없을 때만 규약 §10
  실패 1을 따른다
- `Teams 실행`과 `--agent` 실행은 다시 실행하지 않는다(규약 §10 실패 1의 예외).
  앞선 시도가 실제로는 떴을 수 있어서, 다시 실행하면 같은 워크스페이스에
  에이전트가 둘 뜬다. 보고에 수동 실행 명령을 적는다

## Step 7: 결과 확인

결과 JSON(키를 알 수 없으면 `워크스페이스 목록`)에서 확인한다. 어긋나면
고치지 않고 보고의 `불일치`에 다음 단계와 함께 적는다. `<id>`는 결과의
`result.worktree.id`다.

| 확인 | 어긋날 때 안내 |
|---|---|
| `linkedIssue` = N | `orca worktree set --worktree id:<id> --issue <N> --json` |
| `parentWorktreeId` = 부모 id (최상위·독립이면 `null`) | `orca worktree set --worktree id:<id> --parent-worktree id:<부모 id> --json` |
| `displayName` = 이슈 제목 | `표시 이름`을 한 번 다시 |
| 브랜치가 `(^|[/-])issue<N>-`에 맞음 | 시작 동작이 이슈 브랜치로 못 알아본다. 실제 브랜치를 적고 규약 §3을 고쳐야 할 수 있다고 알린다 |
| 에이전트 핸들이 있음 (`없음`이면 확인하지 않는다) | 아래 수동 실행 명령 |

에이전트 핸들 위치: `--agent`는 `result.agentTerminalHandle`(구버전은
`result.startupTerminal.handle`), `Teams 실행`은 `result.terminal.handle`.
핸들이 없으면 수동 실행 명령을 안내한다.

- `claude`·지정 ID: `orca terminal create --worktree id:<id> --command "<ID>" --json`
- `claude-teams`: `Teams 실행`과 같은 명령

## 보고

```markdown
## issue-orca-worktree 결과

| 이슈 | 종류 | 표시 이름 | 경로 | 브랜치 | 부모 워크스페이스 | 에이전트 |
|---|---|---|---|---|---|---|
| #<N> | epic / leaf / 종류 미정 | <displayName> | <path> | <실제 브랜치> | <부모 또는 없음> | <claude-teams / claude / 지정 값 / 없음> — <터미널 핸들 또는 실패> |

- 불일치: <Step 7에서 어긋난 것과 안내. 없으면 생략>
- 다음 단계: 이 워크스페이스에서 `issue-epic` 또는 `issue-leaf`의 `시작`. 띄운 에이전트의 터미널 제어는 `orca-cli`
```
