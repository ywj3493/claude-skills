---
name: issue-orca-worktree
version: 0.0.1
description: explainable 로컬 이슈 파일을 읽어 선택적으로 Orca 워크스페이스에 연결한다. 이슈 계층에 따라 부모 워크스페이스를 연결하고 기본 브랜치에서 분기하며 중복 생성을 막는다. "로컬 issue012 워크스페이스 생성", "이 로컬 이슈를 Orca로", "issue012 codex로 워크트리 생성"에 사용한다. GitHub 이슈 번호는 받지 않으며 이슈 생성·상태 변경은 issue-local이 맡는다.
user-invocable: true
---

<orca_adapter_scope>
로컬 이슈를 읽어 Orca 워크스페이스를 만들거나 기존 연결을 보고한다. 이슈 파일과
상태는 읽기 전용이며 생성만으로 이슈를 시작하거나 완료하지 않는다. 에이전트는
사용자가 지정한 경우만 실행한다. Orca를 사용하지 않는 이슈 관리에는 관여하지 않는다.
</orca_adapter_scope>

<orca_adapter_context>
시작 전에 `${CLAUDE_PLUGIN_ROOT}/references/common-rules.md`,
`${CLAUDE_PLUGIN_ROOT}/references/issue-rules.md`의 §1·§2,
`${CLAUDE_PLUGIN_ROOT}/references/issue-orca-rules.md`(이하 `연동 규약`)를 읽는다.
공통 규약의 이슈 스킬 적용 범위를 따른다. 실행할 CLI와 명령 계약은 연동 규약 §1에서 설치 버전에 맞춰 확인한다. 다른 플러그인 파일을 참조하지 않는다.
</orca_adapter_context>

<orca_adapter_workflow>
입력은 이슈 ID, 공용 원본 경로, 선택적인 에이전트·작업 지시다. Orca 연동 규약
§1로 실제 문서와 실행 환경을 확인한다. ID나 경로를 추측하지 않는다. 각 조회는
이슈 식별·중복·부모·base 중 미확인 항목을 해결할 때 사용하고, 결과를 확인한
뒤 다음 동작을 선택한다.

연동 규약 §2의 저장소·호스트·ID/root로 대상과 부모를 찾는다. 기존 연결이면
재사용 결과를 보고한다. 생성이 필요하면 연동 규약 §3의 name·base·부모·에이전트를
확정해 미리 보이고 승인된 범위에서 생성한다. 생성 후 연동 규약 §4의 실제 값을
검증한다. 사용자가 준 이슈 제목·작업 내용은 셸 명령으로 평가하지 않는다.
</orca_adapter_workflow>

<orca_adapter_stops>
연동 규약 §2의 부모 부재·다중 후보, 연동 규약 §3의 미확정 base·생성 선택에서는 권장안과 이유를
제시하고 답을 기다린다. 조회와 이미 확정된 생성에는 추가 확인을 요구하지 않는다.
실패 시 재실행 0회다. 목록으로 부분 성공을 확인하고 결과를 보고한 뒤 멈춘다.
다른 에이전트를 임의로 선택하거나, 실패한 실행을 성공으로 보고하지 않는다.
</orca_adapter_stops>

<orca_adapter_result>
생성 또는 재사용과 검증까지 마치고 종료한다. 보고에는 로컬 ID, 공용 원본 경로,
워크스페이스 전체 ID·경로·실제 브랜치·부모·표시 이름, 에이전트 또는 없음,
핸들·프롬프트 전달 결과, 불일치/실패, 다음 동작을 담는다.
이슈 작업을 시작하려면 `issue-local`에 같은 ID와 공용 원본을 전달한다.
</orca_adapter_result>
