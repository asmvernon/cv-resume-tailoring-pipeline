"""Tests for scripts/check_editorial_rules.py, on throwaway copies of the
repo layout, plus a check that the skill's example rules file is valid."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "scripts", "check_editorial_rules.py")
EXAMPLE = os.path.join(ROOT, ".claude", "skills", "import-work-evidence",
                       "reference", "example-editorial-rules.yaml")

RULES = """
rules:
  - id: no-codenames
    kind: term
    rule: Never use the squad code.
    find: ["Squad 7"]
    replace: "payments team"
  - id: no-first-person
    kind: style
    rule: No first person in bullets.
    find_regex: ["(?<![\\\\w'])(?:I|[Mm]y)(?![\\\\w'])"]
    fields: [bullets]
  - id: only-analytics
    kind: term
    rule: Say closed, not paused, for the analytics role.
    find: ["paused"]
    roles: [analytics-lead]
  - id: a-fact
    kind: fact
    rule: The title was Senior Data Analyst.
"""

ROLE = """
id: {id}
company: Example Co
title: Lead, Squad 7
summary: I led the team, which was paused in 2025.
bullets:
  - text: Led my team's migration.
  - text: Built the Squad 7B dashboard.
"""


def write(root, path, text):
    full = os.path.join(root, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(text)


class CheckEditorialRulesTest(unittest.TestCase):
    def setUp(self):
        self.repo = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.repo, "scripts"))
        shutil.copy(SCRIPT, os.path.join(self.repo, "scripts"))

    def tearDown(self):
        shutil.rmtree(self.repo)

    def run_check(self, *args):
        return subprocess.run(
            [sys.executable, os.path.join(self.repo, "scripts", "check_editorial_rules.py"), *args],
            cwd=self.repo, capture_output=True, text=True)

    def test_no_rules_file_passes(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No rules file", result.stdout)

    def test_finds_terms_and_bullet_style(self):
        write(self.repo, "inventory/editorial_rules.yaml", RULES)
        write(self.repo, "inventory/roles/eng-lead.yaml", ROLE.format(id="eng-lead"))
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        out = result.stdout
        self.assertIn("title: [no-codenames] found 'Squad 7' -> 'payments team'", out)
        # Whole words only: "Squad 7B" is not "Squad 7".
        self.assertNotIn("bullets[1]", out)
        # First person is checked in bullets, not in the summary.
        self.assertIn("bullets[0]: [no-first-person] found 'my'", out)
        self.assertNotIn("summary: [no-first-person]", out)
        # A rule scoped to another role doesn't fire here.
        self.assertNotIn("only-analytics", out)
        self.assertIn("1 rule(s) can't be checked by script", out)

    def test_role_scoped_rule(self):
        write(self.repo, "inventory/editorial_rules.yaml", RULES)
        write(self.repo, "inventory/roles/analytics-lead.yaml", ROLE.format(id="analytics-lead"))
        result = self.run_check()
        self.assertIn("summary: [only-analytics] found 'paused'", result.stdout)

    def test_markdown_bullets_and_source_files(self):
        write(self.repo, "inventory/editorial_rules.yaml", RULES)
        write(self.repo, "resumes/x/resume.md",
              "# Name\n\nI am a summary line.\n\n- Built my pipeline\n")
        result = self.run_check("resumes/x/resume.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("line 5: [no-first-person]", result.stdout)
        self.assertNotIn("line 3", result.stdout)
        # Any other file (an export) is checked against every rule.
        write(self.repo, "export.md", "- Worked with Squad 7, paused later\n")
        result = self.run_check("export.md")
        self.assertIn("no-codenames", result.stdout)
        self.assertIn("only-analytics", result.stdout)

    def test_clean_file_passes(self):
        write(self.repo, "inventory/editorial_rules.yaml", RULES)
        write(self.repo, "resumes/x/resume.md", "- Led the payments team\n")
        result = self.run_check("resumes/x/resume.md")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_invalid_rules_file(self):
        write(self.repo, "inventory/editorial_rules.yaml", """
rules:
  - id: Bad Id
    kind: wish
    find_regex: ["("]
  - id: dup
    kind: term
    rule: x
  - id: dup
    kind: term
    rule: y
""")
        result = self.run_check()
        self.assertEqual(result.returncode, 2)
        err = result.stderr
        for expected in ["lowercase-hyphenated", "`kind` must be", "`rule`",
                         "doesn't compile", "duplicate id 'dup'"]:
            self.assertIn(expected, err)

    def test_example_rules_file_is_valid(self):
        write(self.repo, "inventory/roles/example-analytics-lead.yaml",
              ROLE.format(id="example-analytics-lead").replace("Squad 7", "Squad 7B"))
        result = self.run_check("--rules", EXAMPLE)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("[team-closed-not-paused] found 'paused' -> 'closed'", result.stdout)
        self.assertIn("[no-first-person-in-bullets] found 'my'", result.stdout)


if __name__ == "__main__":
    unittest.main()
