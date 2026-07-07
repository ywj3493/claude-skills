---
name: new-policy
version: 0.2.0
description: Creates a new policy document in the source-language policy directory (per docs/config.yml, default docs/en/policy/) with the standard format, and simultaneously creates its translation in each configured translation language (default docs/ko/policy/). Use this when the team needs to establish a new working rule or standard. Triggered by "add a policy", "create a policy for X", "새 정책 만들어줘", "규칙 문서화", or describing a convention that needs to be formalized.
---

# new-policy

Adds a new policy document to the project following the standard format, with
automatic translation mirrors in each translation language configured in
`docs/config.yml`. The examples below show the default `en` → `ko` pairing.

## When to Use

- User says "add a policy", "create a policy for X", "새 정책 추가", "규칙 만들어줘"
- A new convention needs to be formalized (branching strategy, review process, etc.)
- The user describes a working rule that isn't yet written down

## Execution Requirements

These rules are part of the skill contract. They make the expected working
discipline explicit so the result does not depend on which model executes the
skill.

1. **Require the docs structure.** Before anything else, read
   `docs/config.yml` (fall back to inferring languages from the `docs/`
   layout) and verify the source-language policy directory exists. If it does
   not, stop and tell the user to run `/init-docs` first — never create a
   partial structure ad hoc.
2. **Validate the filename.** The policy filename must match kebab-case
   (`^[a-z0-9]+(-[a-z0-9]+)*\.md$`). Check the source policy directory for an
   existing file with that name before writing — if it exists, this is a
   policy *change*, which must be discussed with the user first, not silently
   overwritten.
3. **Use the real date.** The Revision History date comes from `date +%F`,
   never from an assumed date.
4. **Create all configured languages in the same run.** Never finish with only
   the source file when translation languages are configured (skip mirrors
   only when `translation_languages` is empty). Each mirror must have the
   identical heading structure; code blocks, file paths, and technical
   identifiers stay in English.
5. **Do not edit `policy.md` automatically.** Show the suggested @-reference
   line and let the user decide (Step 4) — this is a deliberate gate, not an
   omission to fix.
6. **Verify before reporting.** Confirm every created file exists on disk and
   all have the same section count. The report lists only verified paths.

## Step-by-Step Instructions

### Step 1: Gather Information

Ask the user (or infer from context):

1. **Policy name** — becomes the filename in kebab-case
   - Example: "branching strategy" → `branching-strategy.md`
2. **Purpose** — what does this policy govern and why?
3. **Rules** — the actual rules (numbered or bulleted)
4. **Exceptions** — when, if ever, the rules may be bypassed

If the user has described the policy in their message, draft the content and
ask for confirmation before writing.

### Step 2: Create the Source-Language Policy Document

Create `docs/<source>/policy/<policy-name>.md` (shown here for the default
`en`):

```markdown
# <Policy Title>

## Purpose

<What this policy governs and why it exists>

## Rules

1. <Rule 1>
2. <Rule 2>

## Exceptions

<When the rules may be bypassed, or "None" if no exceptions apply>

## Revision History

- <YYYY-MM-DD>: Initial version
```

### Step 3: Create Translation Mirrors

**Skip this step if the project has no translation languages.**

For each configured translation language, create
`docs/<target>/policy/<policy-name>.md` with a full translation (shown here
for the default `ko`).

Translation rules (same as sync-translations):
- All prose and headings → target language
- Code blocks, file paths, technical identifiers → keep in English
- Checkbox and list markers → keep as-is

```markdown
# <정책 한국어 제목>

## 목적

<이 정책이 다루는 내용과 존재 이유>

## 규칙

1. <규칙 1>
2. <규칙 2>

## 예외

<규칙을 우회할 수 있는 경우, 또는 "없음">

## 개정 이력

- <YYYY-MM-DD>: 최초 작성
```

### Step 4: Reference in policy.md

After creating the files, remind the user:

> Consider adding an @-reference to this new policy in `docs/en/policy/policy.md`
> under the "Related Policy Files" section:
> `- [@docs/en/policy/<policy-name>.md](docs/en/policy/<policy-name>.md) — <description>`

Do **not** automatically edit `policy.md` — show the suggested line and let the
user decide.

### Step 5: Confirm and Report

Tell the user:

> Created:
> - `docs/en/policy/<policy-name>.md`
> - `docs/ko/policy/<policy-name>.md`  (one line per translation language)
>
> Add an @-reference to `docs/en/policy/policy.md` if appropriate.
