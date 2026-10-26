# 로컬 이슈의 Orca 연동 계약

이 문서는 `issue-orca-worktree`만 읽는다. 이슈 관리·상태 전이는 `issue-local`의
책임이다. 원본 파일·frontmatter·번역·git 공용 이슈 등록을 이 연동에서 고치지
않는다. git 브랜치와 Orca 메타데이터만 쓴다.

## §1. 입력과 식별

필수 입력은 로컬 이슈 ID와 원본 이슈 디렉터리 절대 경로다. 경로를 안 받았으면
`local-issues.py locate --repo <현재 checkout>`으로 등록 원본을 찾는다. 미등록이면
`issue-local`로 원본을 확정하도록 안내하거나 사용자가 준 절대 경로를 읽는다.
이 단계에서 Orca의 `linkedIssue`를 로컬 ID로 바꾸지 않는다.

`local-issues.py check --root <원본>`의 errors가 있거나 대상이 legacy면 생성하지
않고 보고한다. 대상 frontmatter의 type·parent와 실제 제목을 읽는다. Done 또는
Cancelled면 계속할지 묻는다. Blocked여도 워크스페이스는 만들 수 있으나 작업
에이전트는 띄우지 않고 선행 목록을 보고한다.

CLI는 실행 시 환경과 설치된 도움말을 기준으로 선택한다. `ORCA_CLI_COMMAND`가
있으면 그 실행 파일, 없고 `ORCA_DEV_REPO_ROOT`가 있으면 `orca-dev`, Linux의
Orca 밖이면 `orca-ide`, 그 밖에는 `orca`다. 선택한 실행 파일의
`skills get orca-cli --json` 안내를 읽는다. 명령이 없는 구버전이면 `--help`로
읽기 계약만 확인하고 지원하지 않는 쓰기 옵션을 추측하지 않는다. 설치·런타임
오류를 보고하고 멈춘다. 이 스킬이 Orca를 설치·시작·재시작하지 않는다.

## §2. 조회·부모·중복

선택한 CLI를 아래 `ORCA` 자리에 대입한다.

```text
ORCA worktree current --json
ORCA worktree list --repo id:<repoId> --json
ORCA worktree show --worktree id:<worktreeId> --json
```

현재 checkout의 repoId와 hostId를 기준으로 같은 저장소·실행 호스트의 보관되지
않은 항목만 본다. current 조회가 실패하면 `ORCA repo list --json`에서 현재 git
저장소 경로와 일치하는 항목을 찾고, 모호하면 선택받는다. GitHub projectId나
원격 URL이 있다는 가정으로 저장소를 찾지 않는다.
목록의 제한·truncation·호스트 coverage를 확인한다. 잘린 경우 한 번만 더 큰
limit으로 조회한다. 그래도 불완전하면 중복/부모 부재를 확정하지 않고 멈춘다.

새 워크스페이스의 comment는 고정 접두사 `explainable-local-issue:` 뒤 JSON이다.

```text
explainable-local-issue:{"id":"issue012","root":"/absolute/project/docs/ko/issue"}
```

원본 root는 resolve한 절대 경로다. 이슈 ID와 root 둘 다 같아야 같은 이슈다.
comment는 이 연동의 식별 정보이므로 상태 메모로 덮어쓰지 않는다. 사람이
수정해 식별 정보가 사라졌다면 아래 브랜치 후보 확인으로 복구를 제안한다.

- 대상과 같은 메타데이터가 1개면 재사용하고 에이전트를 추가 실행하지 않는다.
  표시 이름이 다르면 제목에 맞출지 묻는다. 2개 이상이면 후보를 보고하고 선택을
  기다린다. 자동으로 하나를 고르거나 새로 만들지 않는다.
- 메타데이터가 없지만 `(^|[/-])issueNNN-` 브랜치가 일치하는 항목은 후보일
  뿐이다. GitHub 번호와 겹칠 수 있으므로 이슈 원본 연결을 확인받는다. 기존
  comment와 linkedIssue를 덮어쓰지 않고, 충돌 시 기존 연결을 어떻게 처리할지 묻는다.
- 대상에 parent가 있으면 같은 방식으로 부모 워크스페이스를 찾는다. 없으면
  생성하지 않고 부모를 먼저 만들지, 이번에는 독립으로 만들지 묻는다.
- 생성 시 최상위·독립은 `--no-parent`, 부모가 있으면 `--parent-worktree
  id:<부모 전체 id>`를 명시한다. 이슈 계층과 Orca 계층은 같게 하되, git base는
  부모 브랜치가 아니라 저장소의 기본 브랜치다.

## §3. 생성·에이전트

base는 Orca 저장소 설정과 git ref를 읽어 확정한다. 원격이 없으면 존재하는
로컬 기본 브랜치를 사용한다. 기본 브랜치를 판별하지 못하면 선택받는다.
선택한 ref는 `git rev-parse --verify <ref>^{commit}`으로 검증한다. ref가 없으면
다른 브랜치로 자동 대체하거나 원격을 만들지 않는다. 자동 fetch·push는 없다.

브랜치용 name은 `<type>/issueNNN-<english-slug>`다. 제목이 fix/docs로 시작하면
그 type, 아니면 feat를 기본값으로 쓴다. slug는 제목에서 영어 kebab-case로
2–5단어를 제안하고 생성 전에 보여 준다. 표시 이름은 문서의 제목이다.

에이전트는 **사용자가 지정했을 때만** 실행한다. 기본값은 `없음`이다. 종류에
따라 Claude/Teams를 자동 선택하지 않는다. 사용자가 주지 않은 작업 지시를
지어내지 않는다. 초기 프롬프트에는 지정한 작업 지시와 이슈 ID·공용 원본 경로를
전달하여 새 checkout의 사본을 원본으로 오해하지 않게 한다.

> **생성 확인**: 이슈 ID, 공용 원본, 표시 이름, 브랜치 name, base ref, 부모,
> 에이전트 또는 없음, 전달 프롬프트를 한 번에 보인다. 미확정인 선택이 있으면
> 답을 기다린다. 이미 같은 내용으로 생성·실행을 요청했다면 중복 확인하지 않는다.

다음 명령은 **개념적 인자 목록**이다. 실제 값은 subprocess 인자 배열 등으로
넘겨 제목·본문 안의 따옴표/달러/역따옴표가 셸에서 실행되지 않게 한다.

```text
ORCA worktree create --repo id:<repoId> --name <name> --base-branch <ref>
  (--no-parent | --parent-worktree id:<parentId>) --comment <marker+JSON>
  [--agent <requested-agent> --prompt <task+issue-context>] --json
ORCA worktree set --worktree id:<createdId> --display-name <title> --json
```

`--issue`, `--pr`, `--reference`는 넣지 않는다. 로컬 이슈를 외부 provider에
연결하지 않기 위해서다. `--activate`도 요청받은 경우에만 쓴다.
`claude-teams`를 명시적으로 요청한 경우는 `--agent` 값이 아니므로 워크스페이스를
에이전트 없이 만든 뒤, 설치된 `orca-cli`의 Teams 실행 방법을 확인한다.
방법을 확인하지 못하면 워크스페이스만 보고하고 실행 실패를 알린다.

## §4. 검증·실패

생성 결과에서 전체 worktree id를 얻고 `worktree show`로 표시 이름·comment의
ID/root·parentWorktreeId·branch를 확인한다. 에이전트를 요청한 경우 최신 CLI는
`result.launch.outcome.kind/handle`과 `result.launch.prompt.outcome`을 확인한다.
구버전 핸들은 `result.agentTerminalHandle` 또는 `result.startupTerminal.handle`이다.
핸들은 시작 증거이며 작업 완료 증거가 아니다. 프롬프트 전달을 확인하지 못하면
그 사실을 보고한다.

생성·실행 실패에 자동 재시도는 **0회**다. 먼저 목록을 읽어 같은 ID/root가
생성됐는지 확인하고 현재 상태와 남은 작업을 보고한다. 응답 유실 뒤 무작정
재생성하거나 에이전트를 다시 실행하면 중복이 생긴다. 워크스페이스 삭제·터미널
닫기·다른 호스트 재실행으로 복구하지 않는다. 이후 터미널 제어·실행 재개는
사용자가 요청한 범위에서 설치된 `orca-cli` 안내를 따른다.
