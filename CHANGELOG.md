# Changelog

What changed in the pipeline, in plain language, newest first. When you ask
your assistant to check for pipeline updates, it shows you the entries added
since your copy was last updated.

Each entry says what you'll notice and, when there is something, **what you
need to do**. Changes to `inventory/schema.md` always say whether your
inventory needs updating to match.

## Unreleased

- **Updates for your copy.** Ask your assistant to "check for pipeline
  updates" and it brings in improvements from the public repo, explained in
  plain language, without touching your inventory, job descriptions or
  résumés. About once a month it offers to check for you.
- **A check for the skills themselves.** `scripts/lint_skills.py` checks
  every skill against the Agent Skills spec, and `create-tailor-skill` runs
  it on the new skills it writes.
