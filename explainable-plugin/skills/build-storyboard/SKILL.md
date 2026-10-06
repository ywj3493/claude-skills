---
name: build-storyboard
version: 0.0.1
description: 승인된 화면 기능정의를 배지와 기능 설명 패널이 있는 정적 HTML 목업으로 만든다. 구현 컴포넌트 설계 전에 스토리보드를 검토할 때 사용한다.
---

# build-storyboard

**시작 전에 로드한다**:
[@explainable-plugin/references/common-rules.md](explainable-plugin/references/common-rules.md)
· [@explainable-plugin/references/storyboard-rules.md](explainable-plugin/references/storyboard-rules.md).
실행 시 경로는 ${CLAUDE_PLUGIN_ROOT} 기준으로 해석한다.

## 절차
1. planning/state.json, screen-spec.md, storyboard/annotations.json, 선택 패턴과
   자료 스냅샷을 다시 읽는다. 승인된 정확한 버전이고 unresolved가 없는지 확인한다.
2. templates/storyboard/annotations.json과 storyboard-rules를 읽는다. screen-spec의
   섹션/컴포넌트/요소/동작과 annotations의 대응을 검토한다. 내용 변경은 revise-planning으로
   돌아간다. 패턴/디자인 시스템 배치를 허용 class로 표현하고 미지원 표현을 보고한다.
3. python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" build <domain>
   화면별 HTML을 생성한다. 배지와 설명 표는 같은 데이터에서 생성하며 외부 JS/CDN을
   사용하지 않는다. HTML은 designHtml에 대응하고 annotations는 에이전트용 중간 산출물이다.
4. check <domain> --require-html과 check-docs를 실행한다. 브라우저/렌더링 도구가
   있으면 데스크톱과 모바일 폭에서 배지 가독성·설명 대응·빈/오류 상태를 확인한다.
   도구가 없으면 사람의 시각 검토가 필요한 것으로 보고한다. 검사 성공을 시각 승인으로 간주하지 않는다.
5. 검토자가 만족한 화면/버전을 기록한다. Figma 전달 요청은 sync-design으로 이어간다.
   기획 변경은 revise-planning으로 돌아간다. 기존 수동 수정 충돌은 비교 후 채택한다.

## 공통 검사

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" check <domain>`과
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/check-docs.sh" <specifications>`를 실행한다.
생성/갱신 파일, 생략 이유, 미결 사항, 승인 대상 버전, 다음 단계를 보고한다.

