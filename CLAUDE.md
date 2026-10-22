# Project context

A job-search workspace: a structured inventory of the user's real experience,
grown from their CV and from the job descriptions they apply to, and used to
draft a résumé or CV tailored to each job. The skills in `.claude/skills/` do
the work; this repo's files are the source of truth they read and write.

- `inventory/` — the user's experience and skills as YAML. Data model:
  `inventory/schema.md`.
- `job_descriptions/` — the job descriptions the user has saved, one Markdown
  file each, kept for provenance (which JD prompted which inventory entry).
- `resumes/<slug>/` — one folder per application: `resume.md`,
  `rationale.md`, `interview_prep.md`, and optionally `resume.pdf`.
- `docs/tasks.md` — open items the skills log for the user's decision.

## Ground rules

- **Never fabricate or embellish experience.** Everything in a résumé traces
  back to an inventory entry the user confirmed. Inventory entries suggested
  by a job description stay `candidate` until the user confirms they're true
  (see `inventory/schema.md`'s *Confidence rules*).
- **Never reword without approval.** Any change to a bullet's wording is
  shown to the user as a before/after and written only once they approve it.
- Keep `inventory/`, `job_descriptions/` and `resumes/` as the source of
  truth; skills read from them and never hold duplicate state.
- Never write an internal ticket ID or PR number from a current or past
  employer's systems into `inventory/`. Describe the substance in plain
  language and note that the reference was omitted (see `inventory/schema.md`'s
  *Provenance sanitization*).
- When two sources disagree about the same skill or claim, flag the conflict
  in place and add it to `docs/tasks.md` rather than silently picking one
  (see `inventory/schema.md`'s *Conflicting evidence*).
- This repo holds personal data. Keep it private, and never publish its
  contents as part of an unrelated task.
- **Check this copy is private before writing personal data.** The first
  time in a session that you're about to write to `inventory/`,
  `job_descriptions/` or `resumes/`, run `scripts/check_private_copy.sh`
  and act on its exit code:
  - `0` (private, or a local folder with no remote): go ahead.
  - `1` (the public upstream repo, or a public copy): stop, show the user
    its message, and write nothing until they've made the copy private.
  - `2` (it can't tell, for example offline or not on GitHub): show the
    message and ask the user to confirm this copy is private. Go ahead only
    once they confirm.

  If the script can't run at all, ask the user to confirm the same way.

## Working conventions

- Run `python3 scripts/validate_inventory.py` after any change to
  `inventory/`; the inventory skills run it before committing.
- Run `python3 scripts/lint_skills.py` after any change to `.claude/skills/`
  or `.claude/agents/`; CI runs it on every pull request.
- If you use git branches, keep one branch per concern: (a) changes to the
  skills themselves, (b) inventory updates from a CV or a job description,
  (c) one job's application work (`resumes/<slug>/`). If a task needs content
  from an unmerged branch (e.g. tailoring depends on an inventory update in
  progress), branch from that branch and say so in the pull request.
- `.githooks/` has optional hooks that block commits and pushes straight to
  `main`. Turn them on with `git config core.hooksPath .githooks`.
- **Pipeline updates.** Once per session, when you start the user's first
  task, run `python3 scripts/update_pipeline.py due` (it works offline). If
  it says `due`, add one line at the end of your reply offering to check for
  pipeline updates (the `update-pipeline` skill), and don't raise it again
  that session. Never update without the user's yes. If the script isn't
  there or can't run, skip this.
