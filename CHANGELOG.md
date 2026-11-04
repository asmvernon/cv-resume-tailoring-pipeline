# Changelog

What changed in the pipeline, in plain language, newest first. When you ask
your assistant to check for pipeline updates, it shows you the entries added
since your copy was last updated.

Each entry says what you'll notice and, when there is something, **what you
need to do**. Changes to `inventory/schema.md` always say whether your
inventory needs updating to match.

## Unreleased

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
