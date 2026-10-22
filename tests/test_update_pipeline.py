"""Tests for scripts/update_pipeline.py, on throwaway git repos.

Each test builds a small "public" repo and a copy of it, changes both, and
runs the script inside the copy, the way the update-pipeline skill does.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "update_pipeline.py")
ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@example.com",
    "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@example.com",
    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
}
LINES = "".join(f"line{i}\n" for i in range(1, 9))


def run(cwd, *args, check=True):
    result = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True)
    if check and result.returncode != 0:
        raise AssertionError(f"{args} failed: {result.stderr}")
    return result


def write(root, path, text):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


def read(root, path):
    with open(os.path.join(root, path)) as f:
        return f.read()


def commit(root, message):
    run(root, "git", "add", "-A")
    run(root, "git", "commit", "-qm", message)


class UpdatePipelineTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.up = os.path.join(self.tmp, "up")
        os.makedirs(self.up)
        run(self.up, "git", "init", "-q", "-b", "main")
        write(self.up, ".claude/skills/apply-to-job/SKILL.md", LINES)
        write(self.up, "README.md", "# Title\n\nIntro\n")
        write(self.up, "inventory/schema.md", "schema v1\n")
        write(self.up, "docs/tasks.md", "- [ ] (nothing yet)\n")
        write(self.up, "old.md", "old\n")
        os.makedirs(os.path.join(self.up, "scripts"))
        shutil.copy(SCRIPT, os.path.join(self.up, "scripts", "update_pipeline.py"))
        commit(self.up, "v1")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def make_copy(self, name="copy", clone=False):
        copy = os.path.join(self.tmp, name)
        if clone:
            run(self.tmp, "git", "clone", "-q", self.up, copy)
        else:
            # Like "Use this template": the same files, a fresh history.
            os.makedirs(copy)
            run(copy, "git", "init", "-q", "-b", "main")
            archive = subprocess.run(["git", "archive", "main"], cwd=self.up, env=ENV,
                                     capture_output=True, check=True).stdout
            subprocess.run(["tar", "-x"], cwd=copy, input=archive, check=True)
            commit(copy, "Initial commit")
        return copy

    def upstream_v2(self):
        write(self.up, ".claude/skills/apply-to-job/SKILL.md", LINES.replace("line7", "line7 public"))
        write(self.up, "README.md", "# New title\n\nIntro\n")
        write(self.up, "inventory/schema.md", "schema v2\n")
        write(self.up, "docs/tasks.md", "- [ ] upstream only\n")
        write(self.up, ".claude/skills/new-skill/SKILL.md", "new\n")
        write(self.up, "CHANGELOG.md", "# Changelog\n\n- Added new-skill.\n")
        os.remove(os.path.join(self.up, "old.md"))
        commit(self.up, "v2")
        return run(self.up, "git", "rev-parse", "main").stdout.strip()

    def script(self, copy, *args, check=True):
        return run(copy, "python3", "scripts/update_pipeline.py", *args, check=check)

    def test_template_copy_update(self):
        copy = self.make_copy()
        write(copy, ".claude/skills/apply-to-job/SKILL.md", LINES.replace("line2", "line2 mine"))
        write(copy, "README.md", "# My title\n\nIntro\n")
        write(copy, "inventory/profile.yaml", "name: Me\n")
        write(copy, ".claude/skills/tailor-cv-germany/SKILL.md", "mine\n")
        write(copy, "docs/tasks.md", "- [ ] my task\n")
        commit(copy, "my work")
        sha = self.upstream_v2()

        report = self.script(copy, "check", "--upstream", self.up).stdout
        self.assertIn("the public version this copy was made from", report)
        self.assertIn("Added new-skill.", report)
        self.assertNotIn("docs/tasks.md", report)
        self.assertNotIn("profile.yaml", report)

        result = self.script(copy, "apply", "--to", sha, check=False)
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertEqual(read(copy, "inventory/schema.md"), "schema v2\n")
        self.assertEqual(read(copy, ".claude/skills/new-skill/SKILL.md"), "new\n")
        self.assertFalse(os.path.exists(os.path.join(copy, "old.md")))
        merged = read(copy, ".claude/skills/apply-to-job/SKILL.md")
        self.assertIn("line2 mine", merged)
        self.assertIn("line7 public", merged)
        self.assertIn("<<<<<<< your copy", read(copy, "README.md"))
        # The user's data and own skill are untouched.
        self.assertEqual(read(copy, "inventory/profile.yaml"), "name: Me\n")
        self.assertEqual(read(copy, "docs/tasks.md"), "- [ ] my task\n")
        self.assertEqual(read(copy, ".claude/skills/tailor-cv-germany/SKILL.md"), "mine\n")
        # Nothing recorded while a file is undecided.
        self.assertFalse(os.path.exists(os.path.join(copy, ".pipeline-version")))

        write(copy, "README.md", "# My title\n\nIntro\n")
        self.script(copy, "record", "--upstream-commit", sha)
        commit(copy, "Update the pipeline")
        self.assertIn(f"upstream_commit: {sha}", read(copy, ".pipeline-version"))
        report = self.script(copy, "check", "--upstream", self.up).stdout
        self.assertIn("recorded by the last update", report)
        self.assertIn("Up to date", report)

    def test_clean_apply_records_version(self):
        copy = self.make_copy()
        sha = self.upstream_v2()
        self.script(copy, "check", "--upstream", self.up)
        self.script(copy, "apply", "--to", sha)
        self.assertEqual(read(copy, "README.md"), "# New title\n\nIntro\n")
        self.assertIn(f"upstream_commit: {sha}", read(copy, ".pipeline-version"))

    def test_shared_history(self):
        copy = self.make_copy(clone=True)
        self.upstream_v2()
        report = self.script(copy, "check", "--upstream", self.up).stdout
        self.assertIn("found from shared git history", report)
        self.assertIn("inventory/schema.md", report)

    def test_unknown_base(self):
        copy = self.make_copy()
        # A first commit that matches no public version.
        write(copy, "README.md", "# Edited before the first commit\n")
        run(copy, "git", "commit", "-q", "--amend", "-a", "--no-edit")
        sha = self.upstream_v2()
        report = self.script(copy, "check", "--upstream", self.up).stdout
        self.assertIn("Your copy's version: unknown", report)
        self.assertIn("README.md: your copy and the pipeline each have their own version", report)
        # Files matching a past public version still update cleanly.
        self.assertEqual(self.script(copy, "apply", "--to", sha, check=False).returncode, 3)
        self.assertEqual(read(copy, "inventory/schema.md"), "schema v2\n")
        self.assertFalse(os.path.exists(os.path.join(copy, "old.md")))
        self.assertEqual(read(copy, "README.md"), "# Edited before the first commit\n")

    def test_refuses_uncommitted_changes(self):
        copy = self.make_copy()
        sha = self.upstream_v2()
        self.script(copy, "check", "--upstream", self.up)
        write(copy, "inventory/schema.md", "local edit\n")
        result = self.script(copy, "apply", "--to", sha, check=False)
        self.assertEqual(result.returncode, 1)
        self.assertIn("inventory/schema.md", result.stderr)
        self.assertEqual(read(copy, "inventory/schema.md"), "local edit\n")

    def test_due(self):
        copy = self.make_copy()
        self.assertTrue(self.script(copy, "due").stdout.startswith("not due"))
        write(copy, ".pipeline-version", "upstream_commit: x\nchecked: 2000-01-01\n")
        self.assertTrue(self.script(copy, "due").stdout.startswith("due"))


if __name__ == "__main__":
    unittest.main()
