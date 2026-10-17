# 명령

스킬과 규약은 명령을 직접 적지 않고 아래 **이름**으로 부른다. 여러 줄 본문은
스크래치패드의 임시 파일에 쓴 뒤 `--body-file`로 넘긴다.

표기: `{o}/{r}` = `저장소 조회`의 `nameWithOwner`, `{N}` 이슈 번호, `{P}` PR
번호, `{id}` 이슈 내부 id, `{B}` 기본 브랜치.

**sub-issue와 의존성 API는 이슈 번호가 아니라 내부 id를 받는다.** 번호를
넘기면 다른 이슈가 연결되거나 404가 난다.

---

## 저장소

| 이름 | 명령 |
|---|---|
| 저장소 조회 | `gh repo view --json nameWithOwner,defaultBranchRef --jq '.nameWithOwner + " " + .defaultBranchRef.name'` |
| 쓰기 권한 | `gh api repos/{o}/{r} --jq .permissions.push` — 계정 목록은 `gh auth status` |
| 머지 방식 | `gh api repos/{o}/{r} --jq '{merge: .allow_merge_commit, squash: .allow_squash_merge, rebase: .allow_rebase_merge}'` — `null`이면 모르는 것으로 보고 묻는다 |
| 라벨 목록 | `gh label list --limit 200 --json name --jq '.[].name'` |
| 라벨 생성 | `gh label create <이름> --color <색>` |

## 이슈

| 이름 | 명령 |
|---|---|
| 이슈 조회 | `gh issue view {N} --json number,title,body,state,stateReason,labels,assignees,url` |
| 이슈 id | `gh api repos/{o}/{r}/issues/{N} --jq .id` |
| 이슈 생성 | `gh issue create --title "<제목>" --body-file <파일> --label <라벨> ...` — 출력 마지막 줄 URL의 끝 조각이 번호 |
| 이슈 본문 갱신 | `gh issue view {N} --json body --jq .body > <파일>` → 표식 사이만 고침 → `gh issue edit {N} --body-file <파일>` |
| 라벨 붙이기 / 떼기 | `gh issue edit {N} --add-label <라벨>` / `--remove-label <라벨>` |
| 담당 지정 | `gh issue edit {N} --add-assignee @me` |
| 이슈 닫기 | `gh issue close {N} --reason completed` |
| 부모 조회 | `gh api repos/{o}/{r}/issues/{N}/parent --jq .number 2>&1` — `No parent issue found`·`HTTP 404`면 최상위. 그 밖의 오류는 실패 |
| 하위 이슈 목록 | 아래 |
| 하위 이슈 연결 | `gh api -X POST repos/{o}/{r}/issues/{N}/sub_issues -F sub_issue_id={자식 id}` |
| 선행 지정 | `gh api -X POST repos/{o}/{r}/issues/{N}/dependencies/blocked_by -F issue_id={선행 id}` |
| 선행 목록 | `gh api --paginate repos/{o}/{r}/issues/{N}/dependencies/blocked_by --jq '.[] \| {number, state}'` — `open`이 열린 선행 |

하위 이슈 목록 — `sub_issues`는 그 하위 이슈가 거느린 하위 이슈 수다(규약 §2의 7).

```bash
gh api --paginate repos/{o}/{r}/issues/{N}/sub_issues \
  --jq '.[] | {number, title, state, state_reason, labels: [.labels[].name], assignees: [.assignees[].login], sub_issues: .sub_issues_summary.total}'
```

수용 기준 개수 — 규약 §6.

```bash
gh issue view {N} --json body --jq .body \
  | awk '/^## /{in_ac = ($0 ~ /^## (수용 기준|Acceptance Criteria)/)} in_ac && /^[[:space:]]*- \[[ xX]\]/{n++} END{print n+0}'
```

## PR과 브랜치

| 이름 | 명령 |
|---|---|
| PR 본문 읽기 / 쓰기 | `gh pr view {P} --json body --jq .body > <파일>` / `gh pr edit {P} --body-file <파일>` |
| PR 상태 | `gh pr view {P} --json isDraft,mergeable,baseRefName,headRefName` — `CONFLICTING`이면 머지하지 않는다 |
| PR 머지 | `gh pr ready {P}` → `gh pr merge {P} --squash` (또는 사용자가 고른 `--merge` / `--rebase`) |
| PR 닫기 | `gh pr close {P} --comment "<이유>"` |
| PR 파일 | `gh pr view {P} --json files --jq '.files[].path'` |
| epic 변경 범위 | `git fetch origin {B} <epic 브랜치>` → `git log --oneline origin/{B}..origin/<epic 브랜치>` |

PR 목록 — 한 동작에서 한 번만 받아 파일에 두고, 이슈마다 그 파일을 거른다.

```bash
gh api --paginate "repos/{o}/{r}/pulls?state=all&per_page=100" \
  --jq '.[] | {number, headRefName: .head.ref, baseRefName: .base.ref, state, isDraft: .draft, mergedAt: .merged_at, url: .html_url}' \
  > <스크래치>/prs.jsonl
jq -c 'select(.headRefName | test("(^|[/-])issue{N}-"))' <스크래치>/prs.jsonl   # 이슈 {N}의 후보
```

Draft PR 열기 — 순서대로.

```bash
git status --porcelain                          # 출력이 있으면 멈춘다
git fetch origin {B}
git merge-base --is-ancestor origin/{B} HEAD    # 실패하면 아래 참고
git commit --allow-empty -m "chore: start #{N}"
git push -u origin HEAD
gh pr create --draft --base {B} --head "$(git rev-parse --abbrev-ref HEAD)" --title "<이슈 제목>" --body-file <파일>
```

`--is-ancestor`가 실패하면 main이 앞서 나간 것이다. 브랜치가 아직 원격에 없을
때만 `git rebase origin/{B}`로 맞춘다. 이미 원격에 있으면 멈춘다(force push 금지).
현재 브랜치가 이슈 브랜치가 아닐 때 새로 만드는 명령은
`git switch -c <type>/issue{N}-<slug> origin/{B}`다.

## Orca

**워크스페이스 선택자는 `id:<id>`다.** `<id>`는 `워크스페이스 목록`의 `id`
(`<repo-id>::<절대 경로>`) 그대로다. `orca worktree set`은 `worktree:<id>`
형식을 받지 않는다(`selector_not_found`). `--parent-worktree`·`--worktree` 모두
`id:`로 통일한다.

| 이름 | 명령 |
|---|---|
| 워크스페이스 목록 | `orca worktree list --json` — `result.worktrees[]`에서 `projectId`(`github:<owner>/<repo>`, 대소문자 무시), `linkedIssue`, `branch`(`refs/heads/` 떼고), `id`, `path`, `displayName`, `parentWorktreeId`, `isArchived`(true면 없는 것으로 본다)를 쓴다 |
| 현재 워크스페이스 | `orca worktree current --json` — Orca 밖이면 실패. 연결 이슈는 `linkedIssue` |
| 표시 이름 | `orca worktree set --worktree id:<id> --display-name "<이슈 제목 그대로>" --json` |
| Teams 실행 | `orca terminal create --worktree id:<id> --title "claude-teams" --command "orca claude-teams" --json` — 초기 프롬프트가 있으면 `--command "orca claude-teams '<프롬프트>'"`(프롬프트 안의 `'`는 `'\''`로). 핸들은 `result.terminal.handle` |

워크스페이스 생성 — `--repo`는 `현재 워크스페이스`가 실패할 때만 붙인다.
`[...]`의 에이전트 옵션은 `issue-orca-worktree` Step 4에서 정한 값이 Orca
에이전트 ID일 때만 붙인다(`claude-teams`·`없음`이면 뺀다).

```bash
git fetch origin {B}
# 최상위 이슈
orca worktree create [--repo path:<toplevel>] --issue {N} --no-parent \
  --base-branch origin/{B} --name <type>/issue{N}-<slug> \
  [--agent <ID> [--prompt "<초기 프롬프트>"]] --json
# 부모가 있는 이슈
orca worktree create [--repo path:<toplevel>] --issue {N} --parent-worktree id:<부모 id> \
  --base-branch origin/{B} --name <type>/issue{N}-<slug> \
  [--agent <ID> [--prompt "<초기 프롬프트>"]] --json
```

- `--no-parent`를 빼면 Orca가 호출 위치로 부모를 추론한다. 최상위에는 꼭 넣는다
- 부모는 `issue:<번호>`가 아니라 고른 워크스페이스의 `id:<id>`로 지정한다.
  `issue:`는 보관됐거나 다른 저장소의 워크스페이스를 고를 수 있다
- `--name`은 표시 이름과 브랜치를 함께 정하므로 이슈 제목을 넣지 않는다.
  표시 이름은 생성 뒤 `표시 이름`으로 맞춘다
- `--agent`를 붙이면 첫 터미널에서 그 에이전트가 뜬다. 핸들은
  `result.agentTerminalHandle`(구버전 Orca는 `result.startupTerminal.handle`)
- `orca claude-teams`는 Orca 에이전트 ID가 아니라 Orca 터미널 안에서만 실행되는
  명령이어서 `--agent`로 넘길 수 없다. 에이전트 없이 만든 워크스페이스의 생성
  결과에는 첫 터미널 핸들이 없으므로, `Teams 실행`으로 새 Orca 터미널을 열어
  실행한다. `orca terminal create`로 연 터미널은 Orca 터미널이다
  (`ORCA_TERMINAL_HANDLE`이 설정됨)
