#!/usr/bin/env python3
"""Read-only issue validation and a git-common-dir store pointer; Python stdlib only."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ID = re.compile(r"issue([0-9]{3,})\Z")
FIELDS = {"id", "type", "status", "parent", "blocked_by", "size"}
TERMINAL = {"Done", "Cancelled"}
START = "<!-- SUBISSUES:START -->"
END = "<!-- SUBISSUES:END -->"


class IssueError(ValueError):
    pass


def git_common(repo):
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--path-format=absolute", "--git-common-dir"],
        capture_output=True, text=True,
    )
    if result.returncode:
        raise IssueError("git repository required for register/locate; otherwise pass --root to read commands")
    return Path(result.stdout.strip())


def store_pointer(repo):
    return git_common(repo) / "explainable-issue-store.json"


def locate(repo):
    pointer = store_pointer(repo)
    if not pointer.exists():
        raise IssueError("issue store is not registered; choose the source issue directory and run register --root PATH")
    try:
        root = Path(json.loads(pointer.read_text(encoding="utf-8"))["root"])
    except (ValueError, KeyError, TypeError) as exc:
        raise IssueError(f"invalid store pointer: {pointer}") from exc
    if not root.is_absolute() or not root.is_dir():
        raise IssueError(f"issue store is unavailable: {root}; restore it or explicitly choose a replacement")
    return root.resolve()


def register(repo, root):
    root = root.resolve()
    pointer = store_pointer(repo)
    if pointer.exists():
        existing = locate(repo)
        if existing != root:
            raise IssueError(f"store already registered at {existing}; no replacement performed")
        return existing
    root.mkdir(parents=True, exist_ok=True)
    # Exclusive create: two worktrees cannot silently register different stores.
    with pointer.open("x", encoding="utf-8") as stream:
        json.dump({"root": str(root)}, stream)
        stream.write("\n")
    return root


def size_for(count):
    if count < 1 or count > 6:
        raise IssueError(f"leaf acceptance criteria count must be 1..6, got {count}")
    return "XS" if count == 1 else "S" if count == 2 else "M" if count <= 4 else "L"


def criteria(body):
    active = False
    count = 0
    fence = None
    for line in body.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1][0]
            fence = None if fence == token else token if fence is None else fence
            continue
        if fence:
            continue
        if line.startswith("## "):
            active = line[3:].strip() in {"수용 기준", "Acceptance Criteria"}
        elif active and re.match(r"^\s*- \[[ xX]\] ", line):
            count += 1
    return count


def read_issue(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None  # A legacy issue is reserved, never implicitly migrated.
    chunks = text.split("\n---\n", 1)
    if len(chunks) != 2:
        raise IssueError("frontmatter closing delimiter missing")
    meta = {}
    for line in chunks[0].splitlines()[1:]:
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or key in meta or key not in FIELDS:
            raise IssueError(f"invalid/duplicate frontmatter field: {key}")
        try:
            meta[key] = json.loads(value.strip())
        except ValueError as exc:
            raise IssueError(f"{key}: expected a JSON value in YAML frontmatter") from exc
    if set(meta) != FIELDS:
        raise IssueError(f"required fields: {sorted(FIELDS - set(meta))}")
    issue_id = meta["id"]
    if not isinstance(issue_id, str) or not ID.fullmatch(issue_id) or path.stem != issue_id:
        raise IssueError("id must match the zero-padded filename")
    if issue_id != f"issue{int(ID.fullmatch(issue_id)[1]):03d}" or int(ID.fullmatch(issue_id)[1]) == 0:
        raise IssueError("id must be positive and use canonical padding (issue001, issue1000)")
    if meta["type"] not in ("epic", "leaf") or meta["status"] not in ("Open", "In Progress", "Done", "Cancelled"):
        raise IssueError("invalid type/status")
    parent = meta["parent"]
    if parent is not None and (not isinstance(parent, str) or not ID.fullmatch(parent)):
        raise IssueError("parent must be an issue id or null")
    deps = meta["blocked_by"]
    if not isinstance(deps, list) or any(not isinstance(dep, str) or not ID.fullmatch(dep) for dep in deps):
        raise IssueError("blocked_by must be an array of issue ids")
    if len(set(deps)) != len(deps):
        raise IssueError("duplicate prerequisite")
    if meta["type"] == "leaf":
        expected = size_for(criteria(chunks[1]))
        if meta["size"] != expected:
            raise IssueError(f"size must be {expected}")
    elif meta["size"] not in (None, "XL", "XXL"):
        raise IssueError("epic size must be null, XL or XXL")
    if not re.search(r"^# .+", chunks[1], re.M):
        raise IssueError("issue title missing")
    required = [("배경", "Background"), ("수용 기준", "Acceptance Criteria"), ("작업", "Tasks"), ("기록", "Notes")]
    for names in required:
        if not any(re.search(r"^## " + re.escape(name) + r"\s*$", chunks[1], re.M) for name in names):
            raise IssueError(f"required section missing: {names[1]}")
    if criteria(chunks[1]) == 0:
        raise IssueError("acceptance criteria missing")
    if meta["type"] == "epic" and (text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END)):
        raise IssueError("epic requires exactly one ordered SUBISSUES marker pair")
    return {**meta, "title": re.search(r"^# (.+)", chunks[1], re.M)[1], "path": str(path)}


def inspect(root):
    if not root.is_dir():
        raise IssueError(f"issue directory missing: {root}")
    issues, legacy, errors = {}, [], []
    for path in sorted(root.glob("issue*.md")):
        if not ID.fullmatch(path.stem):
            continue
        try:
            issue = read_issue(path)
            if issue is None:
                legacy.append(path.stem)
            else:
                issues[issue["id"]] = issue
        except (IssueError, TypeError, OSError) as exc:
            errors.append(f"{path.name}: {exc}")
    children = {key: [] for key in issues}
    for key, issue in issues.items():
        parent = issue["parent"]
        if parent is not None:
            if parent not in issues:
                errors.append(f"{key}: parent {parent} is missing or unmanaged")
            else:
                children[parent].append(key)
                if issues[parent]["type"] != "epic":
                    errors.append(f"{key}: parent {parent} is not epic")
                if issue["status"] not in TERMINAL and issues[parent]["status"] in TERMINAL:
                    errors.append(f"{key}: active child of terminal parent {parent}")
        for dep in issue["blocked_by"]:
            if dep not in issues:
                errors.append(f"{key}: prerequisite {dep} is missing or unmanaged")
    for key, issue in issues.items():
        if issue["type"] == "epic" and not children[key]:
            errors.append(f"{key}: epic has no children")
        if issue["type"] == "leaf" and children[key]:
            errors.append(f"{key}: leaf has children")
        if issue["status"] == "Done" and any(issues[c]["status"] not in TERMINAL for c in children[key]):
            errors.append(f"{key}: Done epic has unfinished children")
        issue["open_blockers"] = [dep for dep in issue["blocked_by"] if dep in issues and issues[dep]["status"] not in TERMINAL]
        issue["blocked"] = bool(issue["open_blockers"]) and issue["status"] not in TERMINAL
        issue["children"] = children[key]
    # Completion waits on prerequisites AND children. This also catches parent cycles
    # and a leaf depending on its own parent epic.
    visited, active = set(), set()

    def walk(key):
        if key in active:
            errors.append(f"{key}: hierarchy/dependency cycle")
            return
        if key in visited:
            return
        active.add(key)
        for dep in issues[key]["blocked_by"] + children[key]:
            if dep in issues:
                walk(dep)
        active.remove(key)
        visited.add(key)

    for key in issues:
        walk(key)
    return {"root": str(root), "issues": list(issues.values()), "legacy": legacy, "errors": errors}


def next_id(root):
    if not root.is_dir():
        raise IssueError(f"issue directory missing: {root}")
    numbers = [int(ID.fullmatch(p.stem)[1]) for p in root.glob("issue*.md") if ID.fullmatch(p.stem)]
    return f"issue{max(numbers, default=0) + 1:03d}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("check", "next-id"):
        sub.add_parser(name).add_argument("--root", type=Path, required=True)
    for name in ("register", "locate"):
        command = sub.add_parser(name)
        command.add_argument("--repo", type=Path, default=Path.cwd())
        if name == "register":
            command.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "register":
            result = {"root": str(register(args.repo, args.root))}
        elif args.command == "locate":
            result = {"root": str(locate(args.repo))}
        elif args.command == "next-id":
            result = {"id": next_id(args.root.resolve()), "reserved": False}
        else:
            result = inspect(args.root.resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if result.get("errors") else 0
    except (IssueError, OSError, TypeError, RecursionError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
