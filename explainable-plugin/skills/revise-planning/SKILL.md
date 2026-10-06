---
name: revise-planning
version: 0.0.1
description: 기존 기획을 단일 화면 수정, 화면 유지 전체 수정, 전체 재구성, 자료 재선택 모드로 갱신한다. 사람의 결정과 ID를 보존하고 파생물 영향을 추적할 때 사용한다.
---

# revise-planning

**시작 전에 로드한다**:
[@explainable-plugin/references/common-rules.md](explainable-plugin/references/common-rules.md)
· [@explainable-plugin/references/storyboard-rules.md](explainable-plugin/references/storyboard-rules.md).
실행 시 경로는 ${CLAUDE_PLUGIN_ROOT} 기준으로 해석한다.

## 절차
1. 디스크에서 기획 문서, state.json, annotations.json, 최신 accepted 결정, 관련
   파생물을 읽는다. 기존 문서에 state가 없으면 common-rules의 출처 판별을 적용하고
   현재 문서를 보존한 상태로 JSON 계약을 초기화한다. 역방향 사실을 순방향 결정으로 바꾸지 않는다.
2. storyboard-rules의 네 수정 모드 중 요청에 맞는 하나를 정한다. 단일 화면은 SCR을
   확인하고 변경 범위·영향받는 FR/US/AC/UF·목업·디자인·개발 설계를 제시한다.
   화면 집합 보존과 완전 재구성을 혼동하지 않는다.
3. 후보 annotations를 별도 파일에 만든다. templates/storyboard/annotations.json의
   계약을 따른다. 기존 ID와 accepted 결정을 보존한다. 신규 ID는 이전 최대 번호 뒤에
   부여하며 폐기 ID는 재사용하지 않는다. 버전을 올리고, 구조 변경은 대체 관계 JSON을 만든다.
4. python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" revise <domain> <candidate.json>
   --mode <screen|preserve|restructure|references> --version <new-version> --reason <reason>
   단일 화면은 --screen <SCR>, 대체 관계는 --replacements <json>을 추가한다.
   자료 재선택은 먼저 prepare-planning으로 새 스냅샷을 만든다.
5. 같은 단계에서 화면 기능정의·IA·UF·요구사항·스토리·추적성·결정 기록의 실제 영향
   부분을 갱신한다. 변경 없는 부분과 사람의 결정은 보존한다. 기존 accepted 결정 변경은
   이전 결정과 대체 결정을 기록하고 사용자 확인을 받는다. 미결과 충돌은 unresolved에 남긴다.
6. 영향받는 개발 설계도 artifacts에 등록하여 stale로 둔다. 이전 버전 보관 경로,
   추가/변경/폐기/대체 ID, 관련 없는 화면 보존 여부, 파생물 상태를 보고한다.
7. check와 check-docs를 실행하고 의미 차이를 검토받는다. 사람이 정확한 새 버전을
   승인하면 approve --reviewer <name> --version <version>을 실행한다. build-storyboard
   재생성은 별도이며 수동/디자이너 수정이 남은 HTML을 덮어쓰지 않는다.

## 공통 검사

이전 버전 복원 요청은 storyboard-rules의 restore 계약을 따른다. 보관본을 그대로
덮어써 승인 상태를 되돌리지 않고 새 검토 버전을 만든다. 최신 사람 결정과 복원한
화면의 충돌을 decisions/unresolved에 기록하고 정확한 버전을 다시 승인받는다.

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" check <domain>`과
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/check-docs.sh" <specifications>`를 실행한다.
생성/갱신 파일, 생략 이유, 미결 사항, 승인 대상 버전, 다음 단계를 보고한다.
