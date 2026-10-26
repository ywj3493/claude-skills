"""Behavioral checks in disposable repositories; no GitHub or Orca runtime needed."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "local-issues.py"
spec = importlib.util.spec_from_file_location("local_issues", SCRIPT)
issues = importlib.util.module_from_spec(spec)
spec.loader.exec_module(issues)


def document(key, kind="leaf", parent=None, deps=None, status="Open", count=1):
    meta = dict(id=key, type=kind, status=status, parent=parent,
                blocked_by=deps or [], size=issues.size_for(count) if kind == "leaf" else None)
    text = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in meta.items()) + "\n---\n"
    text += f"# {key} example\n\n## Background\n\nA real work item.\n\n## Acceptance Criteria\n\n"
    text += "\n".join(f"- [ ] Observable criterion {n + 1}" for n in range(count))
    text += "\n\n## Tasks\n\n1. [ ] Perform work\n\n## Notes\n\nCreated for testing.\n"
    if kind == "epic":
        text += f"\n{issues.START}\n| Issue | Status |\n|---|---|\n{issues.END}\n"
    return text


class LocalIssuesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve() / "docs" / "en" / "issue"
        self.root.mkdir(parents=True)

    def write(self, key, **kwargs):
        (self.root / f"{key}.md").write_text(document(key, **kwargs), encoding="utf-8")

    def inspect(self):
        return issues.inspect(self.root)

    def test_remote_free_epic_leaf_lifecycle(self):
        repo = self.root.parents[2]
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        self.assertEqual(issues.register(repo, self.root), self.root)
        self.write("issue001", kind="epic")
        self.write("issue002", parent="issue001")
        self.write("issue003", parent="issue001", deps=["issue002"], count=2)
        initial = self.inspect()
        self.assertFalse(initial["errors"])
        self.assertTrue(initial["issues"][2]["blocked"])
        self.write("issue002", parent="issue001", status="Done")
        self.write("issue003", parent="issue001", deps=["issue002"], count=2, status="In Progress")
        after = self.inspect()
        self.assertFalse(after["errors"])
        self.assertFalse(after["issues"][2]["blocked"])
        self.write("issue001", kind="epic", status="Done")
        self.assertTrue(self.inspect()["errors"])
        self.write("issue003", parent="issue001", deps=["issue002"], count=2, status="Done")
        self.assertFalse(self.inspect()["errors"])

    def test_legacy_reserves_number_but_is_not_migrated(self):
        path = self.root / "issue010.md"
        path.write_text("# Old issue\n**Status**: Done\n", encoding="utf-8")
        before = path.read_bytes()
        self.assertEqual(issues.next_id(self.root), "issue011")
        self.assertEqual(self.inspect()["legacy"], ["issue010"])
        self.assertEqual(path.read_bytes(), before)
        self.write("issue011", deps=["issue010"])
        self.assertIn("unmanaged", " ".join(self.inspect()["errors"]))

    def test_parent_and_completion_wait_cycles(self):
        self.write("issue001", kind="epic")
        self.write("issue002", parent="issue001", deps=["issue001"])
        self.assertIn("cycle", " ".join(self.inspect()["errors"]))

    def test_dependency_cycle(self):
        self.write("issue001", deps=["issue002"])
        self.write("issue002", deps=["issue001"])
        self.assertIn("cycle", " ".join(self.inspect()["errors"]))

    def test_cross_parent_dependency_allowed(self):
        self.write("issue001", kind="epic")
        self.write("issue002", parent="issue001")
        self.write("issue003", kind="epic")
        self.write("issue004", parent="issue003", deps=["issue002"])
        result = self.inspect()
        self.assertFalse(result["errors"])
        self.assertEqual(result["issues"][3]["open_blockers"], ["issue002"])

    def test_missing_parent_and_missing_prerequisite(self):
        self.write("issue001", parent="issue002", deps=["issue003"])
        self.assertEqual(len(self.inspect()["errors"]), 2)

    def test_leaf_cannot_have_children(self):
        self.write("issue001")
        self.write("issue002", parent="issue001")
        self.assertIn("leaf has children", " ".join(self.inspect()["errors"]))

    def test_epic_cannot_be_empty(self):
        self.write("issue001", kind="epic")
        self.assertIn("epic has no children", " ".join(self.inspect()["errors"]))

    def test_size_boundaries(self):
        for count, size in [(1, "XS"), (2, "S"), (3, "M"), (4, "M"), (5, "L"), (6, "L")]:
            self.assertEqual(issues.size_for(count), size)
        for count in [0, 7]:
            with self.assertRaises(issues.IssueError):
                issues.size_for(count)
        self.write("issue001", count=2)
        path = self.root / "issue001.md"
        path.write_text(path.read_text().replace('size: "S"', 'size: "XS"'))
        self.assertIn("size must be S", " ".join(self.inspect()["errors"]))

    def test_counts_only_criteria_outside_fences(self):
        body = "## 수용 기준\n- [x] Real\n```md\n- [ ] Example\n```\n## 작업\n- [ ] Task\n"
        self.assertEqual(issues.criteria(body), 1)

    def test_cancelled_predecessor_unblocks_but_does_not_close_child(self):
        self.write("issue001", status="Cancelled")
        self.write("issue002", deps=["issue001"])
        child = self.inspect()["issues"][1]
        self.assertFalse(child["blocked"])
        self.assertEqual(child["status"], "Open")

    def test_malformed_metadata_does_not_become_legacy(self):
        path = self.root / "issue001.md"
        path.write_text(document("issue001").replace('status: "Open"', 'status: Blocked'))
        result = self.inspect()
        self.assertTrue(result["errors"])
        self.assertFalse(result["legacy"])

    def test_epic_requires_ordered_markers(self):
        self.write("issue001", kind="epic")
        path = self.root / "issue001.md"
        path.write_text(path.read_text().replace(issues.END, issues.START))
        self.assertIn("marker", " ".join(self.inspect()["errors"]))

    def test_shared_store_across_git_worktrees_and_no_silent_rebind(self):
        repo = self.root.parents[2]
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        subprocess.run(["git", "-C", str(repo), "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "--allow-empty", "-qm", "initial"], check=True)
        child = repo / "child"
        subprocess.run(["git", "-C", str(repo), "worktree", "add", "-qb", "child", str(child)],
                       check=True, capture_output=True)
        issues.register(repo, self.root)
        self.assertEqual(issues.locate(child), self.root)
        with self.assertRaises(issues.IssueError):
            issues.register(child, child / "docs" / "en" / "issue")
        self.root.rename(self.root.with_name("moved"))
        with self.assertRaises(issues.IssueError):
            issues.locate(child)

    def test_cli_needs_no_git_github_or_orca_for_file_operations(self):
        self.write("issue001")
        trap = self.root / "bin"
        trap.mkdir()
        marker = self.root / "forbidden-called"
        for name in ["git", "gh", "orca"]:
            path = trap / name
            path.write_text(f'#!/bin/sh\nprintf called > "{marker}"\nexit 99\n')
            path.chmod(0o755)
        env = {**os.environ, "PATH": str(trap)}
        for command in ["check", "next-id"]:
            result = subprocess.run([sys.executable, str(SCRIPT), command, "--root", str(self.root)],
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)
        self.assertFalse(marker.exists())

    def test_cli_error_codes_and_number_overflow(self):
        self.write("issue999")
        self.assertEqual(issues.next_id(self.root), "issue1000")
        self.write("issue1000", deps=["issue777"])
        result = subprocess.run([sys.executable, str(SCRIPT), "check", "--root", str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 1)
        result = subprocess.run([sys.executable, str(SCRIPT), "check", "--root", str(self.root / "missing")], capture_output=True)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
