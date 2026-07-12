# Commit Message Rules

## Format

```text
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes only
- `style`: Formatting or whitespace (no logic change)
- `refactor`: Code restructuring (no feature or fix)
- `test`: Adding or updating tests
- `chore`: Build process, dependency updates, tooling

## Rules

- Subject line: 72 characters maximum
- Subject: imperative mood, lowercase, no trailing period
- Example: `feat(auth): add OAuth2 login flow`
- Reference the issue number in the body or footer:
  - GitHub Issues: `Refs: #42` (or `Closes #42` to auto-close)
  - Local docs issues: `Refs: issue003`
- Separate body from subject with a blank line
