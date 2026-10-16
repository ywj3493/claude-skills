---
name: issue-leaf
version: 0.0.1
description: 구현 단위 leaf 이슈를 다룬다. 부모 epic 아래 sub-issue로 leaf를 만들면서 수용 기준 개수로 크기 라벨을 정하고(상한을 넘으면 epic으로 안내), 선행 이슈를 걸면 blocked로 표시하고, 시작할 때 main을 base로 Draft PR과 작업 계획을 올린다. 머지하면 Closes로 이슈가 닫힌다. "leaf 만들어줘", "구현 이슈 추가", "이슈 시작", "Draft PR 올려줘"에 반응한다. epic은 issue-epic, 워크스페이스는 issue-orca-worktree가 맡는다.
user-invocable: true
allowed-tools: Bash(gh repo view*), Bash(gh auth status*), Bash(gh api*), Bash(gh issue*), Bash(gh label*), Bash(gh pr view*), Bash(gh pr create*), Bash(git status*), Bash(git fetch*), Bash(git merge-base*), Bash(git rev-parse*), Bash(git switch*), Bash(git rebase*), Bash(git commit*), Bash(git push*), Bash(orca worktree current*), Bash(jq*), Bash(awk*)
---

## 개요

leaf는 구현을 맡는다. 하위 이슈가 없고, 크기는 규약 §6의 leaf 상한 안이다.
PR은 main에 바로 머지되고 `Closes`로 이슈가 닫힌다. 부모 epic의 체크리스트와
Blocked 해제는 `issue-epic`의 동기화가 맡는다.

시작 전에 읽는다:

- `${CLAUDE_PLUGIN_ROOT}/references/issue-rules.md` (이하 `규약`)
- `${CLAUDE_PLUGIN_ROOT}/references/commands.md`
- 본문을 쓸 때만: `${CLAUDE_PLUGIN_ROOT}/references/examples.md`,
  `${CLAUDE_PLUGIN_ROOT}/templates/leaf-issue.md` · `leaf-pr.md`

---

## 절대 금지

- 수용 기준을 지어내지 않는다. 0개면 받을 때까지 만들지 않는다
- 상한을 넘는 leaf를 만들지 않는다
- 부모 유무를 추측하지 않는다 — 부모가 없으면 어느 epic에서도 추적되지 않는다
- Blocked인 이슈를 시작하지 않는다
- 이 스킬이 쓰는 다른 이슈는 부모 epic 본문의 `SUBISSUE-PLAN` 표 하나뿐이다

---

## Step 0: 진입 조건과 동작 고르기

1. 규약 §10의 진입 조건을 확인한다
2. 동작을 정한다. "만들고 바로 시작"이면 생성 → 시작으로 잇는다

| 동작 | 요청 예 |
|---|---|
| 생성 | "leaf 만들어줘", "#60 아래에 구현 이슈" |
| 시작 | "#61 시작", "Draft PR 올려줘" |

이슈 번호가 없으면 `현재 워크스페이스`의 `linkedIssue`를 후보로 묻는다.

---

## 생성

1. **입력** — 제목(규약 §8), 요약, 배경, 수용 기준, 작업, 부모 epic. 선택:
   선행 이슈. 부모를 말하지 않았으면 묻는다

   > "부모 epic이 있나요? 1. 있다 — 번호 2. 부모 없는 leaf로 만든다"

2. **크기** — 규약 §6. 상한을 넘으면 나눌 방법을 한두 줄 제안하고 묻는다

   > "수용 기준 <n>개는 leaf 상한을 넘습니다. 1. `issue-epic` 생성으로 넘어간다 (권장 — 규약 §6) 2. 수용 기준을 줄여 다시 입력한다 3. 중단"

3. **관계 확인** — 부모는 `이슈 조회`로 열린 epic인지 본다. leaf나 닫힌 이슈면
   멈추고 알린다. 라벨을 스스로 바꾸지 않는다. 선행은 규약 §4의 1
4. **본문** — `examples.md`로 형식을 맞추고 `leaf-issue.md`를 채운다. 부모가
   있으면 요약 첫 문장에 epic 번호와 역할(설계·계약 / BE / FE)을 적는다.
   라벨 점검을 여기서 한다(규약 §10)
5. **미리보기** — 제목, 본문, 라벨, 부모, 선행(열려 있으면 Blocked로 시작한다는
   것), 부모 epic 계획 표에 붙일 행

   > "위 내용으로 leaf를 만들까요?"

6. **쓰기** — 순서대로
   1. `이슈 생성` (라벨 `leaf` + `size/*`)
   2. 부모에 `하위 이슈 연결`
   3. `선행 지정`. 선행이 열려 있으면 `blocked`
   4. 부모 epic `SUBISSUE-PLAN` 표 끝에 행을 붙여 `이슈 본문 갱신`. 표식이
      없으면 고치지 않고 보고에 적는다

다음 단계 안내: `issue-orca-worktree` → 이 스킬의 `시작`. 부모 epic PR이 열려
있으면 그 epic의 `동기화`.

---

## 시작

1. **이슈 확인** — `이슈 조회`. 열린 leaf가 아니면 멈춘다. `하위 이슈 목록`이
   있으면 규약 §2의 7 `이상`으로 보고하고 epic 전환을 권한다(시작은 막지 않는다)
2. **Blocked 확인** — `선행 목록`. 열린 선행이 있으면 목록을 보고하고 멈춘다.
   없는데 `blocked`가 있으면 뗀다
3. **이미 시작했는가** — `PR 목록`. 열린 이슈 PR이 있으면 보고하고 멈춘다.
   머지된 이슈 PR만 있으면 묻는다

   > "#<N>의 이슈 PR #<P>가 이미 머지됐습니다. 1. 중단 (권장) 2. 새 Draft PR을 연다"

4. **브랜치 확인** — 현재 브랜치가 이슈 브랜치가 아니면 묻는다

   > "현재 브랜치 `<브랜치>`는 #<N>의 이슈 브랜치가 아닙니다. 1. `issue-orca-worktree`로 워크스페이스를 만들고 거기서 다시 시작 (권장) 2. 여기서 `<type>/issue<N>-<slug>`를 새로 만든다"

5. **PR 본문** — `leaf-pr.md`. 계획은 이슈의 작업과 수용 기준으로만 쓴다.
   수용 기준이 부족해 보이면 계획에 넣지 말고 보고에 적는다
6. **미리보기**

   > "빈 커밋 `chore: start #<N>`을 push하고 위 본문으로 Draft PR(base `<기본 브랜치>`)을 열까요?"

7. `Draft PR 열기` → `담당 지정`

---

## 보고

실제로 실행해 확인한 것만 적는다.

```markdown
## issue-leaf <동작> 결과

- leaf: #<N> <제목> (<URL>) — <size 라벨>, 부모 #<번호 또는 없음>
- 한 일: <만든 이슈, 연결, 의존성, 라벨, PR>
- 하지 않은 일: <멈춘 곳과 이유. 없으면 생략>
- 다음 단계: <한 줄>
```
