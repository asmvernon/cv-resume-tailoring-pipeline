# Contributing

Fixes to the skills and scripts, and new market skills, are welcome. Before
you start, read the two rules below: this repo is about personal data, and a
pull request is public the moment it's opened.

## 1. Never include personal data

Nothing from your own inventory, job descriptions, résumés or `docs/tasks.md`
belongs in a pull request, and neither does your name, employer, contact
details or anything copied from your CV, even as an example. Use made-up
examples (Acme Ltd, a fictional role and dates) instead.

A pull request and its commits stay visible on GitHub even if it's closed
unmerged, so check before you open it, not after.

CI runs `scripts/check_no_personal_data.sh`, which fails if anything other
than the empty scaffolding is committed under `inventory/`,
`job_descriptions/` or `resumes/`. It can't spot your name inside a skill
file, so read your own diff too.

## 2. Contribute from a clean fork, never from your private copy

Your private copy holds your data in its history, and it was made from the
template, so it doesn't share this repo's history anyway. To send a change:

1. Fork this repo on GitHub and clone the fork. It contains only this repo's
   files, so it's safe for it to be public.
2. Create a branch.
3. Copy over only the files you changed, for example a new
   `.claude/skills/tailor-cv-germany/` folder and the wiring edits it made.
   Don't copy whole folders from your private copy.
4. Check what you're about to send:

   ```bash
   git status
   git diff --stat main
   scripts/check_no_personal_data.sh
   python3 scripts/lint_skills.py
   ```

   The last line checks every skill against the
   [Agent Skills spec](https://agentskills.io/specification): frontmatter,
   a description that says when to use the skill, file paths that exist,
   and a body short enough to load on every use. CI runs it too.

5. Push the branch to your fork and open a pull request here.

## What's welcome

- **New market skills.** Make them with `create-tailor-skill` ("Create a
  tailoring skill for German CVs"), so they keep the shared rules and their
  `reference/resume-principles.md` cites a source for every convention. Say
  in the pull request how you checked the research, and whether you tried
  the skill on a real job description from that market.
- **Fixes** to a skill, the scripts or the docs: a step that goes wrong, a
  rule a skill doesn't follow, a broken link.

Open an issue first for anything bigger, such as a change to
`inventory/schema.md` or a new skill that isn't a market.

## What won't change

These are what make the output trustworthy, so pull requests that weaken
them won't be merged:

- Never invent or embellish experience. Only confirmed inventory content
  appears on a résumé.
- Every reword is shown as a before/after and written only once the user
  approves it.
- Application-specific details (salary, notice period, work-permit status)
  are asked for each time and never stored.

## Review

Every pull request is reviewed by the maintainer before it's merged. If it's
your first contribution, GitHub waits for the maintainer to approve CI
before it runs.

By contributing, you agree that your contribution is licensed under the
repo's [MIT licence](LICENSE).
