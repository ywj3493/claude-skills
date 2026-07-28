#!/usr/bin/env bash
#
# check-docs.sh — explainable 플러그인이 만든 문서의 결정적 검사.
#
# LLM 판단이 필요 없는 것만 검사한다. 의미 검증은 citation-verifier의 일이다.
#
#   1. 자리표시자 잔존   — 안 채워진 <!-- --> 주석, 남아 있는 YYYY-MM-DD
#   2. mermaid 펜스 균형 — ``` 개수와 mermaid 블록 짝
#   3. 링크 무결성       — 상대 링크가 실존 파일을 가리키는지
#   4. REF 존재성        — [REF: 경로:줄]의 파일이 있고 그 줄이 존재하는지
#   5. ID 추적성         — FR/US/AC/T ID의 중복, 미커버, 고아 참조
#
# 사용법:
#   check-docs.sh <명세 디렉터리>
#   예: check-docs.sh docs/ko/specifications
#
# 종료 코드: 0 = 문제 없음, 1 = 문제 발견, 2 = 사용법 오류

set -uo pipefail

SPEC_DIR="${1:-}"

if [[ -z "$SPEC_DIR" ]]; then
  echo "사용법: $(basename "$0") <명세 디렉터리>" >&2
  echo "예:     $(basename "$0") docs/ko/specifications" >&2
  exit 2
fi

if [[ ! -d "$SPEC_DIR" ]]; then
  echo "오류: 디렉터리를 찾을 수 없습니다: $SPEC_DIR" >&2
  exit 2
fi

SPEC_DIR="${SPEC_DIR%/}"
PROBLEMS=0

note() { printf '  %s\n' "$1"; }
fail() { printf '  [문제] %s\n' "$1"; PROBLEMS=$((PROBLEMS + 1)); }

mapfile -t DOCS < <(find "$SPEC_DIR" -name '*.md' -type f | sort)

if [[ ${#DOCS[@]} -eq 0 ]]; then
  echo "오류: $SPEC_DIR 아래에 마크다운 문서가 없습니다." >&2
  exit 2
fi

echo "검사 대상: ${#DOCS[@]}개 문서 ($SPEC_DIR)"
echo

# ---------------------------------------------------------------------------
echo "1. 자리표시자 잔존"
# ---------------------------------------------------------------------------
for doc in "${DOCS[@]}"; do
  # 템플릿 지시 주석은 생성 시 지워져야 한다. 남아 있으면 채우다 만 것이다.
  if grep -qE '<!--[^>]*(TODO|채운다|적는다|삭제한다|여기 적|예: )' "$doc" 2>/dev/null; then
    n=$(grep -cE '<!--[^>]*(TODO|채운다|적는다|삭제한다|여기 적|예: )' "$doc")
    fail "$doc: 템플릿 지시 주석 ${n}건이 남아 있습니다"
  fi
  if grep -q 'YYYY-MM-DD' "$doc" 2>/dev/null; then
    n=$(grep -c 'YYYY-MM-DD' "$doc")
    fail "$doc: 채우지 않은 날짜 자리표시자 ${n}건"
  fi
  if grep -qE '<[가-힣]+>' "$doc" 2>/dev/null; then
    n=$(grep -cE '<[가-힣]+>' "$doc")
    fail "$doc: 채우지 않은 꺾쇠 자리표시자 ${n}건 (예: <도메인 이름>)"
  fi
done
[[ $PROBLEMS -eq 0 ]] && note "문제 없음"

# ---------------------------------------------------------------------------
echo
echo "2. mermaid 펜스 균형"
# ---------------------------------------------------------------------------
BEFORE=$PROBLEMS
for doc in "${DOCS[@]}"; do
  # grep -c 는 일치가 없어도 "0"을 출력하고 종료 코드 1을 낸다.
  # `|| echo 0` 을 덧붙이면 "0\n0" 이 되어 산술 평가가 깨지므로 쓰지 않는다.
  fences=$(grep -c '^```' "$doc" 2>/dev/null)
  if (( fences % 2 != 0 )); then
    fail "$doc: 코드 펜스 개수가 홀수입니다 (${fences}개) — 닫히지 않은 블록"
    continue
  fi
  opens=$(grep -c '^```mermaid' "$doc" 2>/dev/null)
  if (( opens > 0 )); then
    # mermaid 블록 안에 다이어그램 종류 선언이 있는지
    if ! grep -qE '^\s*(sequenceDiagram|flowchart|erDiagram|classDiagram|stateDiagram-v2|graph)' "$doc"; then
      fail "$doc: mermaid 블록 ${opens}개가 있으나 다이어그램 종류 선언이 없습니다"
    fi
  fi
done
[[ $PROBLEMS -eq $BEFORE ]] && note "문제 없음"

# ---------------------------------------------------------------------------
echo
echo "3. 링크 무결성"
# ---------------------------------------------------------------------------
BEFORE=$PROBLEMS
for doc in "${DOCS[@]}"; do
  dir=$(dirname "$doc")
  # 마크다운 상대 링크만. 외부 URL과 순수 앵커는 건너뛴다.
  grep -oE '\]\([^)#][^)]*\.md(#[^)]*)?\)' "$doc" 2>/dev/null \
    | sed -E 's/^\]\(//; s/\)$//; s/#.*$//' \
    | sort -u \
    | while IFS= read -r target; do
        [[ -z "$target" ]] && continue
        case "$target" in
          http*|/*) continue ;;
        esac
        if [[ ! -f "$dir/$target" ]]; then
          printf '  [문제] %s: 링크 대상이 없습니다 -> %s\n' "$doc" "$target"
        fi
      done
done
# 서브셸에서 센 문제는 PROBLEMS에 반영되지 않으므로 다시 센다.
BROKEN=$(
  for doc in "${DOCS[@]}"; do
    dir=$(dirname "$doc")
    grep -oE '\]\([^)#][^)]*\.md(#[^)]*)?\)' "$doc" 2>/dev/null \
      | sed -E 's/^\]\(//; s/\)$//; s/#.*$//' \
      | sort -u \
      | while IFS= read -r target; do
          [[ -z "$target" ]] && continue
          case "$target" in http*|/*) continue ;; esac
          [[ -f "$dir/$target" ]] || echo x
        done
  done | wc -l
)
PROBLEMS=$((PROBLEMS + BROKEN))
[[ $PROBLEMS -eq $BEFORE ]] && note "문제 없음"

# ---------------------------------------------------------------------------
echo
echo "4. [REF:] 인용 존재성"
# ---------------------------------------------------------------------------
BEFORE=$PROBLEMS
BAD_REFS=0
for doc in "${DOCS[@]}"; do
  while IFS= read -r ref; do
    [[ -z "$ref" ]] && continue
    path="${ref%%:*}"
    lines="${ref#*:}"
    start="${lines%%-*}"
    if [[ ! -f "$path" ]]; then
      fail "$doc: 인용 파일이 없습니다 -> $path"
      BAD_REFS=$((BAD_REFS + 1))
      continue
    fi
    if [[ "$start" =~ ^[0-9]+$ ]]; then
      total=$(grep -c '' "$path")
      if (( start > total )); then
        fail "$doc: 인용한 줄이 파일 범위를 넘습니다 -> $path:$start (총 ${total}줄)"
        BAD_REFS=$((BAD_REFS + 1))
      fi
    fi
  done < <(grep -oE '\[REF: [^]]+\]' "$doc" 2>/dev/null | sed -E 's/^\[REF: //; s/\]$//')
done
[[ $PROBLEMS -eq $BEFORE ]] && note "문제 없음 (인용 존재성만 검사 — 의미 검증은 citation-verifier의 일)"

# ---------------------------------------------------------------------------
echo
echo "5. ID 추적성"
# ---------------------------------------------------------------------------
BEFORE=$PROBLEMS

collect_ids() { # <파일 글롭 패턴> <ID 정규식>
  find "$SPEC_DIR" -name "$1" -type f -exec grep -ohE "$2" {} + 2>/dev/null | sort -u
}

# ID 중복 정의 — 제목(### ID: ...) 기준
for doc in "${DOCS[@]}"; do
  dupes=$(grep -oE '^#{2,4} (FR|NFR|US|UC)-[A-Z0-9-]+' "$doc" 2>/dev/null \
          | sed -E 's/^#+ //' | sort | uniq -d)
  if [[ -n "$dupes" ]]; then
    while IFS= read -r d; do
      fail "$doc: ID가 중복 정의되었습니다 -> $d"
    done <<< "$dupes"
  fi
done

# 정의되지 않은 ID를 참조하는 경우
DEFINED_FR=$(find "$SPEC_DIR" -name 'requirements.md' -exec grep -ohE '^#{2,4} (FR|NFR)-[A-Z0-9-]+' {} + 2>/dev/null | sed -E 's/^#+ //' | sort -u)
DEFINED_US=$(find "$SPEC_DIR" -name 'user-stories.md' -exec grep -ohE '^#{2,4} US-[0-9]+' {} + 2>/dev/null | sed -E 's/^#+ //' | sort -u)

if [[ -n "$DEFINED_FR$DEFINED_US" ]]; then
  REFERENCED=$(find "$SPEC_DIR" -name 'traceability.md' -exec grep -ohE '\b(FR|NFR|US)-[A-Z0-9-]+' {} + 2>/dev/null | sort -u)
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    if ! grep -qxF "$id" <<< "$DEFINED_FR
$DEFINED_US"; then
      fail "traceability.md: 정의되지 않은 ID를 참조합니다 -> $id"
    fi
  done <<< "$REFERENCED"

  # 추적성 매트릭스에서 빠진 요구사항
  while IFS= read -r id; do
    [[ -z "$id" ]] && continue
    if ! find "$SPEC_DIR" -name 'traceability.md' -exec grep -qF "$id" {} + 2>/dev/null; then
      fail "추적성 매트릭스에 없는 요구사항입니다 -> $id"
    fi
  done <<< "$DEFINED_FR"
else
  note "요구사항·스토리 ID가 아직 없습니다 — 추적성 검사를 건너뜁니다"
fi

# T-ID 대역 규칙: 백엔드 T-1NN, 프론트엔드 T-2NN, E2E T-3NN
while IFS= read -r spec; do
  [[ -z "$spec" ]] && continue
  bad=$(grep -oE '\bT-[0-9]+' "$spec" 2>/dev/null | sed -E 's/^T-//' \
        | awk 'length($0) != 3 || $0 < 100 || $0 >= 400' | sort -u)
  if [[ -n "$bad" ]]; then
    while IFS= read -r b; do
      fail "$spec: T-ID가 대역을 벗어납니다 -> T-$b (백엔드 1NN / 프론트 2NN / E2E 3NN)"
    done <<< "$bad"
  fi
done < <(find "$SPEC_DIR" -name 'test-spec.md' -type f)

[[ $PROBLEMS -eq $BEFORE ]] && note "문제 없음"

# ---------------------------------------------------------------------------
echo
if [[ $PROBLEMS -eq 0 ]]; then
  echo "결과: 문제 없음 (${#DOCS[@]}개 문서)"
  exit 0
else
  echo "결과: 문제 ${PROBLEMS}건 (${#DOCS[@]}개 문서)"
  exit 1
fi
