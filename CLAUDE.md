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

## Working conventions

- Run `python3 scripts/validate_inventory.py` after any change to
  `inventory/`; the inventory skills run it before committing.
- If you use git branches, keep one branch per concern: (a) changes to the
  skills themselves, (b) inventory updates from a CV or a job description,
  (c) one job's application work (`resumes/<slug>/`). If a task needs content
  from an unmerged branch (e.g. tailoring depends on an inventory update in
  progress), branch from that branch and say so in the pull request.
- `.githooks/` has optional hooks that block commits and pushes straight to
  `main`. Turn them on with `git config core.hooksPath .githooks`.
