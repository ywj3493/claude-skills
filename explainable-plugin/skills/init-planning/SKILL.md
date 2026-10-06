---
name: init-planning
version: 0.3.0
description: 기술 스택 미정인 새 서비스나 기능의 기획을 한국어로 작성한다. 서비스 목적·참고자료에서 요구사항, 유저 스토리, IA, 유저 플로우, 화면 기능정의와 추적성을 만들고 검토 버전을 관리한다. 기존 기획 수정은 revise-planning, 기술 설정과 API 계약은 prepare-design, 기존 코드의 사실 역산은 reverse-planning이 담당한다.
---

# init-planning

코드가 없는 기능의 목적·사용자 과업·화면 의미를 정한다. 기술 선택은 기획 진입
조건이 아니다. 스택 미정이어도 UI가 필요하면 화면 문서를 만든다.

**시작 전에 로드한다**:
${CLAUDE_PLUGIN_ROOT}/references/common-rules.md ·
${CLAUDE_PLUGIN_ROOT}/references/planning-rules.md ·
${CLAUDE_PLUGIN_ROOT}/references/storyboard-rules.md

## 산출물

`planning/service-brief.md`, `decisions.md`, `requirements.md`,
`user-stories.md`, `traceability.md`, `state.json`,
`storyboard/annotations.json`, 공유 `glossary.md`, `README.md`,
도메인이 여러 개면 `domain-map.md`를 만든다.
UI가 있으면 `information-architecture.md`, `user-flows.md`,
`screen-spec.md`를 함께 만든다. UI가 없으면 annotations의 screens는 빈 배열이다.
참고자료는 prepare-planning의 스냅샷을 읽는다. 자료가 없으면 snapshotId는 null이며
대화에서 확정한 근거를 decisions에 기록한다.
architecture/infrastructure/api-interface는 prepare-design이 작성한다.
verification은 개발 설계 스킬의 소유다.

## 단계 0: 환경과 입력

common-rules의 문서 환경·리뷰 모드를 적용한다. 기존 기획은 덮어쓰지 않고
revise-planning으로 이어간다. 기존 코드의 사실 문서화는 reverse-design-* →
reverse-planning으로 안내한다. 기존 코드가 있어도 새 기능의 기획은 이 스킬로 가능하다.
서비스 이름·설명·대상 사용자·핵심 문제·UI 필요 여부·화면 수(고정/목표)·범위를 확인한다.
도메인을 구획하고 필요 자료가 있으면 prepare-planning을 실행한다. 자료 등록은
별도 재진입 가능 작업이며 기술 스택을 먼저 묻지 않는다.

## 단계 1: 서비스 개요·결정·상태

templates/planning/{service-brief,decisions}.md와 state.json,
templates/storyboard/annotations.json을 읽는다. 목적·성공 기준·포함/범위 밖·제약을
작성하고 사용자 결정과 AI 가정을 분리한다. state의 mode는 forward, status는 draft,
approvedVersion은 null이다. 실제 snapshotId와 같은 planningVersion을 annotations에 넣는다.
기획 문서에 GENERATED-BY의 mode: forward와 기획 버전을 표시한다.
사람의 결정은 DEC ID로 연결하고 충돌·미결은 unresolved에 기록한다.
화면 수 제약을 충족할 수 없으면 기능을 누락하지 않고 충돌을 보고한다.

## 단계 2: 용어집

templates/overview/glossary.md를 읽고 핵심 개념의 한국어 정의와 영문 식별자를
정한다. 한 개념의 영문 식별자는 하나다. 공유 OWNER 섹션만 병합한다.
처음부터 구현 심볼이나 테이블 이름을 기획 요구에 강제하지 않는다.

## 단계 3: 요구사항

templates/planning/requirements.md와 planning-rules §3을 적용한다. 액터·FR·측정
가능한 NFR·제약·범위 밖을 작성한다. 자료와 결정 ID를 근거로 연결한다.
목표값이 미정인 성능 요구는 임의 수치로 확정하지 않고 미결 사항으로 기록한다.
기술 중립 스왑 테스트를 수행한다.

## 단계 4: 유저 스토리·인수 기준

templates/planning/user-stories.md를 읽고 액터·능력 단위 US와 Given/When/Then AC를
작성한다. 정상·실패·경계 경로를 포함하고 모든 FR의 US 커버리지를 확인한다.
다중 액터 UC는 필요할 때만 만든다. 구현 FLOW와 테스트 연결은 설계 대기다.

## 단계 5: 정보 구조 (UI 조건부)

templates/planning/information-architecture.md를 읽는다. 사용자 과업을 화면으로
묶고 SCR을 부여한다. 화면 유형 page/overlay/state와 부모 화면은 screen-spec에서
정의하고 IA에서 참조한다. 주소·FSD 구조는 쓰지 않는다.
UI 없는 US는 사유를 기록하고 불필요한 화면을 만들지 않는다.

## 단계 6: 유저 플로우 (UI 조건부)

templates/planning/user-flows.md를 읽고 과업별 UF를 만든다. 노드는 SCR과 사용자
결정, 간선은 사용자 행동이다. 서버 처리는 노드로 요약하며 FLOW는 설계 대기로 둔다.
모든 SCR의 도달 경로를 확인한다. 화면 내부 동작 상세는 screen-spec이 소유한다.

## 단계 7: 화면 기능정의 (UI 조건부)

templates/planning/screen-spec.md와 templates/storyboard/annotations.json을 읽는다.
화면 → 섹션 → 사용자 관점 컴포넌트 → 요소 → 동작으로 구체화한다.
정상·로딩·빈 결과·오류·권한 부족과 미적용 사유, 검증·권한·입력·출력·반응형
요구를 정의한다. SEC/CMP/ELM과 FR/US/AC/SCR/UF를 연결한다.
장식은 기능 배지 대상에서 제외하고 기능 요소마다 고유 ELM과 화면 내 배지를 부여한다.
동일 단계에서 annotations를 갱신하고 선택 패턴·자료 출처를 sourceIds로 연결한다.
사용자 관점 구성과 구현 컴포넌트를 혼합하지 않는다.

## 단계 8: 도메인 통합·추적성

templates/overview/domain-map.md는 도메인이 여러 개일 때만 작성한다. 도메인 목록과
과업 연결·통합 필요를 기록한다. 구체 통합 계약은 prepare-design이 채운다.
templates/planning/traceability.md의 요구사항→스토리, 스토리→화면·플로우를 채우고
화면→요소→목업 대응을 별도 표로 추가한다. 기존 파싱 대상 표 열은 바꾸지 않는다.
FLOW/테스트는 설계 대기로 명시하고 가짜 ID를 만들지 않는다.

## 단계 9: 검토·승인과 다음 단계

공유 README의 해당 도메인 OWNER 영역과 실제 생성 문서의 내비게이션을 갱신한다.
planning-tools.py check <domain>과 check-docs.sh <specifications>를 실행한다.
스왑 테스트, 상태 누락, 사람 결정 보존, 자료 근거와 화면 의미를 검토한다.
state를 in-review로 두고 사람이 정확한 버전을 승인하면
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/planning-tools.py" approve <domain> --version <version> --reviewer <name>`
을 실행한다. 미결 사항이 있으면 승인하지 않는다.

기획 버전·근거 스냅샷·결정/미결·검사 결과·생성/생략 파일을 보고한다.
화면 검토는 build-storyboard, 반복 수정은 revise-planning, 디자인 왕복은 sync-design,
개발 설계 진입은 prepare-design → init-design-backend/frontend로 이어간다.
기획 승인과 개발 설계 준비 완료를 구분한다.
