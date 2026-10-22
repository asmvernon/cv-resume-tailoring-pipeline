"""Tests for scripts/lint_skills.py. Run: python3 -m unittest discover -s tests"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import lint_skills  # noqa: E402

GOOD_DESC = (
    "Turn a job description into a list of keywords for the inventory. "
    "Use when the user shares a job description they want to mine."
)


def skill_md(name="my-skill", description=GOOD_DESC, extra="", body="Do the thing.\n"):
    return f"---\nname: {name}\ndescription: {description}\n{extra}---\n\n{body}"


class LintTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        os.makedirs(os.path.join(self.root, ".claude", "skills"))

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)

    def run_lint(self, *flags):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = lint_skills.main([*flags, self.root])
        return code, out.getvalue()

    def assertFails(self, needle):
        code, out = self.run_lint()
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)

    def test_clean_skill_passes(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md())
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_no_skills_is_a_usage_error(self):
        self.assertEqual(self.run_lint()[0], 2)

    def test_missing_skill_md(self):
        os.makedirs(os.path.join(self.root, ".claude/skills/empty"))
        self.assertFails("missing SKILL.md")

    def test_missing_frontmatter(self):
        self.write(".claude/skills/my-skill/SKILL.md", "# Just a heading\n")
        self.assertFails("must start with YAML frontmatter")

    def test_unclosed_frontmatter(self):
        self.write(".claude/skills/my-skill/SKILL.md", "---\nname: my-skill\n")
        self.assertFails("not closed")

    def test_unknown_field(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(extra="model: sonnet\n"))
        self.assertFails("aren't in the Agent Skills spec")

    def test_name_must_match_folder(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(name="other-skill"))
        self.assertFails("must match its folder")

    def test_bad_name_format(self):
        for bad in ("My-Skill", "-skill", "skill-", "my--skill", "my_skill"):
            with self.subTest(name=bad):
                self.write(f".claude/skills/{bad}/SKILL.md", skill_md(name=bad))
                self.assertFails("must be lowercase letters")
                os.remove(os.path.join(self.root, f".claude/skills/{bad}/SKILL.md"))
                os.rmdir(os.path.join(self.root, f".claude/skills/{bad}"))

    def test_description_needs_a_trigger(self):
        desc = "Turns a job description into a list of keywords and writes them to the inventory files."
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(description=desc))
        self.assertFails("doesn't say when to use it")

    def test_description_too_long(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(description=GOOD_DESC + " x" * 600))
        self.assertFails("max 1024")

    def test_description_names_unknown_skill(self):
        desc = GOOD_DESC + " For PDFs, use `render-resume-pdf` instead."
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(description=desc))
        self.assertFails("`render-resume-pdf`, which isn't a skill or agent here")
        self.write(".claude/skills/render-resume-pdf/SKILL.md", skill_md(name="render-resume-pdf"))
        self.assertEqual(self.run_lint()[0], 0)

    def test_short_description_warns(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(description="Use when asked."))
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)
        self.assertIn("WARNING", out)
        self.assertEqual(self.run_lint("--strict")[0], 1)

    def test_metadata_must_be_strings(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(extra="metadata:\n  version: 1.0\n"))
        self.assertFails("`metadata` must map strings to strings")

    def test_empty_body(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body=""))
        self.assertFails("no instructions")

    def test_too_many_lines(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body="line\n" * 500))
        self.assertFails("max 500")

    def test_missing_referenced_file(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body="Read `reference/spec.md` first.\n"))
        self.assertFails("points to `reference/spec.md`")

    def test_referenced_file_found_in_skill_or_repo(self):
        body = "Read `reference/spec.md`, then run `scripts/tool.py`. See [docs](docs/x.md).\n"
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body=body))
        self.write(".claude/skills/my-skill/reference/spec.md", "spec\n")
        self.write("scripts/tool.py", "print('hi')\n")
        self.write("docs/x.md", "x\n")
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_placeholders_and_user_data_are_skipped(self):
        body = (
            "Write `resumes/<slug>/resume.md` and `inventory/skills.yaml`; read "
            "`job_descriptions/2026-01-01-acme.md`, `inventory/roles/*.yaml`, "
            "`/opt/tool/bin` and [the form](https://example.com/a/b.html). Use it and/or not.\n"
        )
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body=body))
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_unmentioned_bundled_file(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md())
        self.write(".claude/skills/my-skill/notes.md", "orphan\n")
        self.assertFails("never mentions its file notes.md")

    def test_deeply_nested_file_warns(self):
        body = "Read `reference/deep/more.md`.\n"
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body=body))
        self.write(".claude/skills/my-skill/reference/deep/more.md", "x\n")
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)
        self.assertIn("nested more than one folder deep", out)

    def test_interactive_script(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body="Run `scripts/ask.py`.\n"))
        self.write(".claude/skills/my-skill/scripts/ask.py", "name = input('Name? ')\n")
        self.assertFails("waits for keyboard input")

    def test_interactive_shell_script_referenced_from_repo(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body="Run `scripts/ask.sh`.\n"))
        self.write("scripts/ask.sh", "#!/bin/sh\nread -r -p 'Sure? ' yn\n")
        self.assertFails("waits for keyboard input")

    def test_piped_read_is_not_interactive(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md(body="Run `scripts/loop.sh`.\n"))
        self.write("scripts/loop.sh", "#!/bin/sh\nls | while read -r f; do echo $f; done\n")
        code, out = self.run_lint()
        self.assertEqual(code, 0, out)

    def test_agent_checks(self):
        self.write(".claude/skills/my-skill/SKILL.md", skill_md())
        self.write(
            ".claude/agents/critic.md",
            "---\nname: reviewer\ndescription: Reviews drafts.\ntools: Read\n---\n\nReview.\n",
        )
        code, out = self.run_lint()
        self.assertEqual(code, 1, out)
        self.assertIn("must match its folder/file name 'critic'", out)
        self.assertIn("doesn't say when to use it", out)


if __name__ == "__main__":
    unittest.main()
