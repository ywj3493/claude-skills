---
id: "{{ID}}"
type: "epic"
status: "Open"
parent: {{PARENT_JSON}}
blocked_by: {{BLOCKED_BY_JSON}}
size: {{SIZE_JSON}}
---
# {{TITLE}}

{{SUMMARY}}

## 배경

{{BACKGROUND}}

## 수용 기준

{{ACCEPTANCE_CHECKLIST}}

## 작업

{{NUMBERED_TASK_CHECKLIST}}

## 하위 이슈

<!-- SUBISSUES:START -->
| 이슈 | 종류 | 상태 | Blocked | 선행 |
|---|---|---|---|---|
{{CHILD_ROWS}}
<!-- SUBISSUES:END -->

## 나눈 기준

{{SPLIT_RATIONALE}}

## 기록

{{CREATION_DATE_AND_DECISIONS}}
