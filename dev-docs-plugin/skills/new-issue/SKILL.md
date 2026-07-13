---
name: new-issue
version: 0.3.1
description: Creates a new issue for tracking work. When a git remote exists, creates a GitHub Issue via `gh` CLI, sets up a working branch, and (optionally) opens a draft PR linked to the issue. When no remote is configured, falls back to creating local issue documents in the source-language issue directory (per docs/config.yml, default docs/en/issue/) with translation mirrors. Use this whenever starting new work — features, bug fixes, tasks, or investigations. The user may say "create an issue", "new issue", "이슈 만들어줘", or simply describe work they want to start.
---

# new-issue

Creates a properly tracked issue for a unit of work, using GitHub Issues when
available or local docs as fallback.

## When to Use

- User says "create an issue", "new issue", "start an issue", "이슈 만들기"
- Beginning a new feature, bug fix, investigation, or task
- User describes work that should be formally tracked

## Execution Requirements

These rules are part of the skill contract. They make the expected working
discipline explicit so the result does not depend on which model executes the
skill. Follow them exactly — do not rely on implicit judgment.

1. **Decide mode from real output.** Run the Step 1 detection commands and
   base the mode decision only on their actual output. Never assume the
   remote or authentication state.
2. **Never invent identifiers.** Issue numbers, URLs, and branch names must
   come from command output or directory listings. If the issue number cannot
   be parsed from the `gh issue create` URL, recover it with
   `gh issue list --limit 1` — do not guess it.
3. **Check before writing.** In docs mode, confirm `docs/en/issue/issue<NNN>.md`
   does not already exist before writing. If it does, re-derive the next
   number from a fresh listing — never overwrite an existing issue.
4. **Handle failures explicitly.** When a `gh` or `git` command fails, read
   the error output, apply the documented recovery (e.g., empty commit before
   retrying `gh pr create`), and retry once. If it still fails, report the
   exact error and stop. Never report success for a step that failed or was
   skipped.
5. **Verify before reporting.** Before the final report, confirm each artifact
   actually exists: the issue URL and PR URL returned by `gh`, the branch
   shown by `git branch --show-current`, or the files on disk in docs mode.
   The report may contain only verified URLs and paths.
6. **Keep structural parity.** The draft PR body (GitHub mode) and the
   translation mirrors (docs mode) must mirror the issue's structure exactly —
   same sections and the same number of checklist items.
7. **Ask only at defined gates.** The single confirmation point is the drafted
   issue content (Step 2G / 3D), which also settles whether to create the
   branch and draft PR. All other steps proceed without asking.

## Step-by-Step Instructions

### Step 1: Detect Mode

Determine whether to use GitHub Issues or local docs:

1. Check for a git remote:
   ```bash
   git remote -v 2>/dev/null
   ```
2. If output is non-empty, verify `gh` CLI is available and authenticated:
   ```bash
   command -v gh >/dev/null 2>&1 && gh auth status 2>/dev/null
   ```
3. Decision:
   - **GitHub mode**: remote exists AND `gh` is available and authenticated
   - **Docs mode (fallback)**: no remote, OR `gh` is missing/unauthenticated

If falling back from GitHub to docs mode due to `gh` issues, inform the user:

> No `gh` CLI found or not authenticated. Falling back to local docs mode.
> Run `gh auth login` to enable GitHub Issues mode.

---

## GitHub Mode

### Step 2G: Gather Issue Details

If the user has already described the work in their message, draft the issue
content from that description and **ask for confirmation** before creating.

Otherwise, ask the user for:

1. **Title** — one-line summary of the work
2. **Background** — why is this needed? what problem does it solve?
3. **Acceptance Criteria** — what does "done" look like?
4. **Initial Tasks** — what are the first known steps?

When presenting the draft for confirmation, also state the follow-up plan so
the user can opt out in the same reply:

> After creating the issue I'll set up a working branch and open a draft PR
> linked to it. Say "issue only" (or similar) to skip the draft PR.

Default (no objection) = create the branch and draft PR. Remember the choice
for Steps 4G–6G.

### Step 3G: Create GitHub Issue

Run `gh issue create` with the gathered details:

```bash
gh issue create --title "<Title>" --body "$(cat <<'EOF'
## Background

<Why this work is needed and what problem it solves>

## Acceptance Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>

## Tasks

- [ ] 1. <Task 1>
- [ ] 2. <Task 2>

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->
EOF
)"
```

Capture the output URL. Extract the issue number from the URL (the trailing
integer, e.g., `https://github.com/owner/repo/issues/42` → `#42`).

### Step 4G: Create Branch

Create a working branch for this issue — unless the current working directory
is already on a dedicated branch (e.g., created via `git worktree`).

1. Check the current branch:
   ```bash
   git branch --show-current
   ```
2. If on `main` (or the repo's default branch), create and switch to a new branch:
   ```bash
   git checkout -b feat/issue<number>-<short-description>
   ```
   Use the naming convention from policy: `feat/`, `fix/`, or `docs/` prefix
   depending on the issue type.
3. If already on a feature branch (e.g., a worktree), skip branch creation and
   inform the user that the existing branch will be used.

### Step 5G: Create Draft PR

**Skip this step if the user opted out in Step 2G** — report the issue and
branch only.

Create a draft pull request linked to the issue. The PR title and body should
be written in the **same language** as the GitHub Issue (paired language).

```bash
gh pr create --draft \
  --title "<Same title as the issue>" \
  --body "$(cat <<'EOF'
## Summary

Resolves #<number>

## Changes

<!-- Describe changes as work progresses -->

## Test Plan

<!-- How to verify the changes -->
EOF
)"
```

The `Resolves #<number>` link ensures the issue is automatically closed when
the PR is merged.

If the branch has no commits yet beyond the base branch, `gh pr create` may
fail. In that case, create an empty commit first:

```bash
git commit --allow-empty -m "chore: start work on issue #<number>"
git push -u origin HEAD
```

Then retry the PR creation.

### Step 6G: Confirm and Report

Tell the user:

> Created:
> - GitHub Issue #\<number\>: \<issue URL\>
> - Draft PR: \<PR URL\>  (omit if skipped in Step 2G)
> - Branch: `feat/issue<number>-<short-description>`
>
> Reference this issue in commit messages with `Refs: #<number>`.

---

## Docs Mode (Fallback)

Docs mode uses the languages configured in `docs/config.yml`
(`source_language` + `translation_languages`; infer from the `docs/` layout if
the file is missing). The examples below show the default `en` → `ko` pairing.

If the source-language issue directory does not exist, stop and tell the user:

> No documentation structure found. Run `/dev-docs:init-docs` to set it up first.

### Step 2D: Determine the Next Issue Number

Check what issue numbers already exist:

```bash
ls docs/en/issue/ 2>/dev/null | grep -E '^issue[0-9]+\.md$' | sort
```

Take the highest number found and add 1. If no issues exist yet, start at `001`.
Format as zero-padded 3 digits: `001`, `002`, ..., `099`, `100`, `101`, ...

### Step 3D: Gather Issue Details

If the user has already described the work in their message, draft the issue
content from that description and **ask for confirmation** before writing.

Otherwise, ask the user for:

1. **Title** — one-line summary of the work
2. **Background** — why is this needed? what problem does it solve?
3. **Acceptance Criteria** — what does "done" look like?
4. **Initial Tasks** — what are the first known steps?

### Step 4D: Create the Source-Language Issue Document

Create `docs/<source>/issue/issue<NNN>.md` (shown here for the default `en`):

```markdown
# Issue <NNN>: <Title>

**Status**: Open
**Created**: <YYYY-MM-DD>

## Background

<Why this work is needed and what problem it solves>

## Acceptance Criteria

- [ ] <Criterion 1>
- [ ] <Criterion 2>

## Tasks

- [ ] 1. <Task 1>
- [ ] 2. <Task 2>

## Notes

<!-- Record decisions, discoveries, and blockers here as work progresses -->
```

See `references/issue-template.md` for the raw template.

### Step 5D: Create Translation Mirrors

**Skip this step if the project has no translation languages.**

For each configured translation language, create
`docs/<target>/issue/issue<NNN>.md` with the same structure in that language
(shown here for the default `ko`). Code blocks, file paths, commands, and
technical identifiers remain in English.

```markdown
# 이슈 <NNN>: <한국어 제목>

**상태**: 열림
**생성일**: <YYYY-MM-DD>

## 배경

<이 작업이 필요한 이유와 해결하려는 문제>

## 완료 기준

- [ ] <기준 1>
- [ ] <기준 2>

## 작업 목록

- [ ] 1. <작업 1>
- [ ] 2. <작업 2>

## 참고 사항

<!-- 작업 진행 중 결정 사항, 발견 사항, 차단 사항을 여기에 기록하세요 -->
```

### Step 6D: Confirm and Report

Tell the user:

> Created:
> - `docs/en/issue/issue<NNN>.md`
> - `docs/ko/issue/issue<NNN>.md`  (one line per translation language)
>
> Reference this issue in commit messages with `Refs: issue<NNN>`.

---

## Updating Issues During Work

### GitHub Mode

- Edit the issue body or add comments: `gh issue edit <number>` or `gh issue comment <number>`
- Check off tasks directly in the issue body on GitHub
- Close the issue: `gh issue close <number>` or use `Closes #<number>` in a commit message

### Docs Mode

- Check off completed tasks: `- [x] 1. Task 1`
- Update **Status** from `Open` → `In Progress` → `Done`
- Record key decisions in the **Notes** section
- Update the translation mirrors when significant changes are made
