# Changelog

What changed in the pipeline, in plain language, newest first. When you ask
your assistant to check for pipeline updates, it shows you the entries added
since your copy was last updated.

Each entry says what you'll notice and, when there is something, **what you
need to do**. Changes to `inventory/schema.md` always say whether your
inventory needs updating to match.

## Unreleased

- **Check a job's fit before applying.** A new `assess-job-fit` skill reads
  one or more postings from the employer's own site, checks the job ID on
  the live page, and gives you a ranked verdict (Strong, Good, Partial,
  Weak) with where you match, the gaps and up to three questions that could
  change it. It scores against your confirmed inventory and your own
  preferences, which you can keep in a new, optional
  `inventory/fit_profile.yaml` (weights, levels, locations, work
  authorisation, domains, deal-breakers). The assessment is saved as
  `resumes/<job>/fit_assessment.md`. It never changes your inventory.
  **Optional:** start a fit profile; the skill offers to when you first
  tell it what you're looking for. `inventory/schema.md` describes the new
  file; your existing inventory needs no changes.
- **No false update reminders in the public repo.** A checkout of the
  public pipeline repo itself no longer says an update check is due, since
  there's nothing for it to update from. Your own copy is reminded as
  before. Nothing to do.
- **Cover letters.** A new `write-cover-letter` skill drafts a one-page
  cover letter for a job in your own voice, using only your confirmed
  inventory and writing you've approved. A separate reviewer copy-edits
  and fact-checks it before you see it, and nothing is final until you
  approve the whole letter. `scripts/render_cover_letter.py` renders it to
  a letter-format PDF (Letter or A4), with an optional signature image
  that is never saved in the repo. Its rules cite Prospects.
  `inventory/schema.md` documents an optional `cover_letter_style` block
  in `profile.yaml` for your own reusable phrasing. Ask for "a cover
  letter for this job". Nothing to do.
- **A more natural opening for UK CV profiles.** `tailor-cv-uk-permanent`
  now lets the personal profile open with who you are ("Data scientist and
  engineering leader with …") instead of a verb. The rest of the profile
  and every bullet still start with an active verb. Nothing to do.
- **CVs for permanent UK jobs.** A new `tailor-cv-uk-permanent` skill
  drafts a CV for salaried UK roles: 2 A4 pages, a short personal profile,
  British spelling, and no photo, date of birth or references. Its rules
  cite the National Careers Service, Prospects and Michael Page. Ask for "a
  CV for this UK job" and it's picked for you. Nothing to do.
- **Font size and title options for PDFs.** `scripts/render_resume_pdf.py`
  takes `--font-size` (body text in pt) and `--title` (the PDF's title,
  "Resume" by default). The UK permanent CV uses `--font-size 10 --title
  CV`. Other markets render exactly as before. Nothing to do.
- **Updates for your copy.** Ask your assistant to "check for pipeline
  updates" and it brings in improvements from the public repo, explained in
  plain language, without touching your inventory, job descriptions or
  résumés. About once a month it offers to check for you.
- **A check for the skills themselves.** `scripts/lint_skills.py` checks
  every skill against the Agent Skills spec, and `create-tailor-skill` runs
  it on the new skills it writes.
