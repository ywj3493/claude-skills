---
name: prepare-design
version: 0.0.1
description: 승인된 기획을 개발 설계로 넘기기 전에 기술 스택·인프라·아키텍처·인터페이스 계약을 확정한다. 스택 미정 기획의 개발 설계 준비에 사용한다.
---

# prepare-design

**시작 전에 로드한다**:
[@explainable-plugin/references/common-rules.md](explainable-plugin/references/common-rules.md)
· [@explainable-plugin/references/storyboard-rules.md](explainable-plugin/references/storyboard-rules.md).
실행 시 경로는 ${CLAUDE_PLUGIN_ROOT} 기준으로 해석한다.

## 절차
1. 기획 문서·state·결정 기록을 읽고 승인된 버전을 확인한다. 오래된 기획이나 미결
   상태이면 개발 설계 준비 완료로 보고하지 않는다. 기존 JSON 없는 기획은 사람이
   최신 문서를 검토한 뒤 forward 상태를 초기화한다.
2. templates/overview/{architecture,infrastructure}.md와 templates/planning/api-interface.md를
   읽는다. 계약 작성 시 references/planning-rules.md §6을 로드한다.
   기술 중립 업무 요구와 구현 선택을 구분한다.
3. 백엔드/프론트엔드 필요 여부, 언어·런타임·프레임워크·API 스타일·영속성·라우팅·
   상태 관리·렌더링·배포·환경·CI/CD를 확인한다. 결정된 항목은 다시 묻지 않는다.
   미정 값은 임의 확정하지 않는다. 백엔드 4-Layered DDD와 프론트엔드 FSD를 제안하되 사용자 선택을 따른다.
4. architecture의 스택·디렉터리 매핑·의존성 표와 infrastructure의 필요한 섹션을
   자기 OWNER 영역에 작성한다. 자료가 없는 섹션은 만들지 않는다.
   기존 순방향 init-planning 소유의 기술 설정 영역은 결정을 보존하면서 prepare-design으로
   소유권을 승계하고 변경 기록을 남긴다. 다른 스킬 소유 영역은 그대로 보존한다.
5. 요구사항·스토리·IA·UF·screen-spec을 읽고 API 스타일별 계약 블록을 작성한다.
   화면의 정보·행동은 입도 검토 입력이며 화면 하나에 API 하나를 강제하지 않는다.
   권한·검증·오류·재시도 계약과 도메인 간 통합 계약을 연결한다.
6. 입력 planningVersion을 문서 정보와 artifacts에 기록한다. stale 설계의 재설계
   범위를 보고하고 check-docs를 실행한다. 기술 설정/API 계약을 사용자가 확인하면
   `ready-design <domain> --version <version>`을 실행하여 designReadyVersion과 실제 입력
   해시를 기록한 뒤 init-design-backend/frontend로 이어간다. API가 불필요하면
   api-interface에 해당 없음의 근거를 기록한다. 기획의 SCR/UF/요소 의미는 변경하지 않는다.

## 공통 검사

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" check <domain>`과
`bash "${CLAUDE_PLUGIN_ROOT}/scripts/check-docs.sh" <specifications>`를 실행한다.
생성/갱신 파일, 생략 이유, 미결 사항, 승인 대상 버전, 다음 단계를 보고한다.
