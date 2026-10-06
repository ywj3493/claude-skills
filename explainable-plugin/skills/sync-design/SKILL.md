---
name: sync-design
version: 0.0.1
description: 스토리보드와 외부 디자인의 파일 교환, 기준 버전·Figma 매핑·변환 손실·3방향 변경 비교를 수행한다. Figma 반영과 디자이너 수정의 검토에 사용한다.
---

# sync-design

**시작 전에 로드한다**:
[@explainable-plugin/references/common-rules.md](explainable-plugin/references/common-rules.md)
· [@explainable-plugin/references/storyboard-rules.md](explainable-plugin/references/storyboard-rules.md).
실행 시 경로는 ${CLAUDE_PLUGIN_ROOT} 기준으로 해석한다.

## 내보내기
1. 승인 버전과 HTML을 check --require-html로 확인한다. 사용할 실제 연결 도구와
   Figma 파일 ID를 확인한다. BSS Sync나 특정 MCP가 설치되어 있다고 가정하지 않는다.
2. python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" export-sync <domain>
   --figma-file <file-id> --output <domain>/storyboard/sync/<version>-baseline.json
3. 실제 연결 도구가 있으면 HTML→렌더링→디자인 변환을 도구의 지원 범위 안에서 수행하고
   화면 SCR·요소 ELM·Figma 노드 ID를 기록한다. 변환기 없는 경우 HTML과 패키지를 수동
   전달한다. 화면에서 만든 기준 노드 매핑은 별도 불변 기준 패키지로 확정한다.
   작업한 기준 파일·변환 도구 버전·지원 capability·손실을 기록한다.

## 가져오기와 검토
1. 선택 노드의 변경을 교환 JSON으로 확보한다. storyboard-rules의 동일 annotations
   계약, baseVersion, figmaFileId, capabilities, losses를 사용한다. 원시 Figma JSON은
   실제 연결 도구로 정규화한다. HTML만 돌아오면 기능 의미를 추론하지 않고 비교 제안과
   매핑 미확인 사항을 기록한다.
2. python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" compare-sync <domain>
   <baseline.json> <incoming.json> --output <new-report.json>
3. 텍스트/스타일, 동작/권한/검증, 추가/삭제, 양쪽 동시 수정, 매핑 손실을 구분하여
   사람에게 검토받는다. 충돌·손실·미지원이 있으면 동기화 완료로 표시하지 않는다.
4. 채택된 변경은 revise-planning으로 반영하고 HTML을 재생성한다. Figma 모습은 코드
   사실이 아니므로 reverse-planning의 코드 근거로 사용하지 않는다. 디자이너 수정을
   조용히 덮어쓰지 않는다. 새 승인 버전으로 기준 패키지를 다시 만든다.

## 검증과 완료
실제 도구가 확보되면 텍스트/스타일 변경, 요소 추가/삭제, 동시 수정 샘플을 왕복하고
매핑/손실/충돌 결과를 기록한다. 파일 교환·비교 검사가 통과해도 실제 Figma 왕복은
실행한 경우만 검증됨으로 보고한다. 최종 완료는 사람이 해당 버전을 확인한 뒤다.

## 공통 검사

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" check <domain>`과
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/check-docs.sh" <specifications>`를 실행한다.
생성/갱신 파일, 생략 이유, 미결 사항, 승인 대상 버전, 다음 단계를 보고한다.

