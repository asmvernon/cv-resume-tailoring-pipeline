# Changelog

What changed in the pipeline, in plain language, newest first. When you ask
your assistant to check for pipeline updates, it shows you the entries added
since your copy was last updated.

Each entry says what you'll notice and, when there is something, **what you
need to do**. Changes to `inventory/schema.md` always say whether your
inventory needs updating to match.

## Unreleased

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
