# cv-resume-tailoring-pipeline

Tailor your CV or résumé to every job you apply for, from a record of your
real experience that grows with each application, with you approving every
change.

It's a set of instructions (skills) for an AI coding assistant, plus the
folder structure they work in. You run it in
[Claude Code](https://claude.com/claude-code) or another AI-assisted editor,
on your own private copy of this repo. There is no app or server: your files
are the database, and git is the history.

## How it works

1. **Seed your inventory from your CV.** The assistant reads your CV, résumé
   or LinkedIn profile and turns it into structured YAML in `inventory/`:
   your roles, every bullet, your skills and the evidence behind each one. It
   never fills in specifics you didn't give: anything vague or missing (a
   number, an outcome, a date) is flagged for you to fill in.
2. **Add a job description.** It saves the posting to `job_descriptions/`,
   lists what the job asks for, and checks each requirement against your
   inventory. For every gap, it asks you whether it's a real gap or
   experience you have but left off your CV. Real experience goes in as
   confirmed; real gaps are tracked as development goals.
3. **Tailor.** It drafts a résumé for that job in `resumes/<job>/` from your
   confirmed inventory only: what to include, what to leave out, and any
   rewording to match the job's language, each shown to you as a
   before/after for your approval. It also writes a rationale and a short
   interview prep sheet.
4. **Render.** It turns the approved draft into a clean, text-based PDF.

Every application makes the inventory more complete, so the next tailoring
starts from more.

**It never invents experience.** Anything a job description suggests you
*might* have stays a candidate until you confirm it, and a candidate never
appears on a résumé. Every line on a tailored résumé traces back to
something you wrote or confirmed.

## Markets

| Skill | Produces |
|---|---|
| `tailor-resume-usa` | A US-market résumé: 1–2 pages, Letter paper, applicant-tracking-system friendly |
| `tailor-resume-uk-contract` | A CV for UK contract (day-rate) roles: engagement-based, skills summary up front, A4 |

Each market's conventions live in the skill's `reference/resume-principles.md`.
To add another country or kind of role, ask your assistant, for example:

> Create a tailoring skill for German CVs

This runs `create-tailor-skill`. It researches that market's conventions,
shows you each rule with its source for your approval, then writes a new
`tailor-*` skill from the closest existing one and wires it into the other
skills. Everything that makes the output trustworthy (never inventing,
approving every reword) stays the same; only the market's conventions
change. Check its research: the new skill is only as good as its sources.

## Before you start: keep your copy private

Your CV, your inventory and the jobs you apply to are personal data, and
they'll be committed to your copy of this repo. **Don't use GitHub's Fork
button for your copy (a fork of a public repo is always public), and don't
push your data to a public repository.**

On GitHub, click **Use this template → Create a new repository** and choose
**Private**. Or clone it and push it to a new private repository of your
own. A local folder with no remote at all also works.

Your assistant checks this before it writes any of your data: it runs
`scripts/check_private_copy.sh`, stops if the copy is public, and asks you to
confirm when it can't tell (for example, when you're offline).

## What you need

- **An AI coding assistant that can read and write files in a folder.**
  [Claude Code](https://claude.com/claude-code) works out of the box: it
  picks up `CLAUDE.md` and the skills in `.claude/skills/` automatically.
  Other assistants (Cursor, GitHub Copilot, Codex, Windsurf and others) work
  by following `AGENTS.md`, which points them at the same instructions.
- **Python 3 with PyYAML**, for the inventory checker:
  `python3 -m pip install pyyaml`.
- **For PDFs:** [pandoc](https://pandoc.org/installing.html) and Google
  Chrome or Chromium. The PDF step finds Chrome's standard install on macOS
  and `chromium` or `google-chrome` on your PATH; anywhere else, set
  `CHROMIUM` to the browser's path, for example
  `export CHROMIUM="/path/to/chrome"`.
- **Optional:** git and the GitHub CLI (`gh`), if you want each tailored
  résumé reviewed by the `resume-critic` agent as comments on a pull request.

## Your first tailored résumé

1. **Make your private copy** (above), clone it, and open the folder in your
   assistant. In Claude Code: `cd <your-copy>` then `claude`.

2. **Add your CV.** Put it in the folder as a PDF, Markdown or plain text
   file. A LinkedIn profile works too: open your profile, click
   **More → Save to PDF**, and use that file. Then ask:

   > Seed my inventory from my-cv.pdf

   The assistant fills `inventory/profile.yaml`, `inventory/education.yaml`,
   `inventory/roles/` and `inventory/skills.yaml`. It keeps your CV's
   wording, shows you a before/after for any bullet it would tighten, and
   marks anything vague or ambiguous (a missing date, an unclear title) for
   you to confirm. Go through what it wrote: this is the record every résumé
   will be built from, so it's worth getting right once.

   Your CV file can stay in the folder as the record of where your inventory
   came from, or you can delete it: the skills only read `inventory/`.

   `inventory/interview_stories.yaml` starts empty: a CV rarely holds the
   stories you'd tell in an interview. Add them as they come to mind (see
   *Day to day*), and each tailored résumé's interview prep sheet will pull
   in the relevant ones.

3. **Check the inventory:**

   ```bash
   python3 scripts/validate_inventory.py
   ```

   It confirms every file parses and that every skill you claim is backed by
   evidence. The assistant runs it too, before it commits anything.

4. **Tailor for a job.** Paste the job description (or its link, or a file)
   and ask:

   > Tailor my résumé for this job

   This runs `apply-to-job`, which:
   - asks which market the job is in, if it isn't obvious;
   - asks whether to check the job description against your inventory first
     (say yes for a new job), then saves it and walks through each gap with
     you, including requirements your inventory only partly covers;
   - drafts the résumé and shows you every inclusion, omission and reword
     before writing anything;
   - writes `resumes/<date>-<company>-<title>/resume.md`, `rationale.md` and
     `interview_prep.md`.

5. **Get the PDF:**

   > Make the PDF of that résumé

   The PDF lands next to `resume.md`. If it runs over the page budget, the
   assistant cuts the least relevant bullets rather than shrinking the type.

6. **Keep it.** The assistant commits as it goes: the inventory, the saved
   job description, then the résumé and PDF. If you work on git branches,
   `CLAUDE.md` asks for one branch per concern (the inventory update, then
   this application), each starting from the one before; merge them into
   `main` in that order, directly or through pull requests on your private
   repo. If you'd rather not use branches, tell the assistant to commit to
   `main`. Either way, your inventory is now ready for the next
   application.

## Day to day

| You say | What happens |
|---|---|
| "Add this job to my inventory" | `extract-jd-signal`: match the job against your inventory and resolve gaps, without drafting a résumé |
| "Add my new role" or "I also did X at Y" | `seed-inventory-from-source`: update the inventory from what you tell it |
| "Add an interview story about the outage I handled" | `seed-inventory-from-source`: record it as a STAR story (situation, task, action, result), asking you for the details |
| "Tailor my résumé for this job" | `apply-to-job`: the whole path, job description to draft |
| "Make the PDF" | `render-resume-pdf` |
| "Create a tailoring skill for German CVs" | `create-tailor-skill`: add a new country or kind of role |
| "Check for pipeline updates" | `update-pipeline`: bring in improvements from this repo (see *Getting updates*) |

Open questions the assistant can't settle for you, such as two sources that
disagree about a skill, go in `docs/tasks.md`.

## Getting updates

Your copy doesn't change when this repo does. To bring improvements in,
ask your assistant:

> Check for pipeline updates

This runs `update-pipeline`. It explains what's new in plain language
(from `CHANGELOG.md`) and applies it once you say yes. It only touches the
pipeline's own files (the skills, scripts, `inventory/schema.md`, README,
`CLAUDE.md`); your inventory, job descriptions, résumés and
`docs/tasks.md` are never changed. Where your copy changed a skill too
(for example when `create-tailor-skill` wired in a new market), it merges
the two and asks you about anything that overlaps. It notes the version
you're on in `.pipeline-version`.

You don't need to remember: about once a month, your assistant offers to
check at the start of a session. To hear about updates as they come out,
click **Watch → Custom → Releases** at the top of this repo's GitHub page.

The usual `git merge` or `git pull` from this repo doesn't work on a copy
made from the template, because the two share no history; `update-pipeline`
compares the files instead.

## What's in the repo

```
.claude/skills/        the workflows (one SKILL.md each)
.claude/agents/        resume-critic, an independent review of each draft
inventory/schema.md    the inventory data model
inventory/             your experience and skills (yours, private)
job_descriptions/      the jobs you've applied to (yours, private)
resumes/               one folder per application (yours, private)
scripts/               the inventory checker, the PDF renderer, the private-copy
                       check, the skills linter and the updater
docs/tasks.md          open items the assistant logs for your decision
CLAUDE.md, AGENTS.md   the rules every assistant follows here
CHANGELOG.md           what changed in each update, in plain language
```

## What it costs

Nothing beyond your AI assistant's own plan or API usage. There's no hosting.

## What it doesn't do

- It doesn't find jobs or apply to them. You bring the job descriptions.
- It doesn't write cover letters.
- It won't fill a gap by making something up. A real gap becomes a
  development goal in `inventory/dev_opportunities_tracker.yaml`.

## Tell me how it went

Used it for a job application?
[This 3-minute form](https://docs.google.com/forms/d/e/1FAIpQLScSes_ClztVp0wjeUEy45ps2Q6s4_CfdvtdQTQ2DupXiDc--g/viewform)
is the best way to tell me what worked and what didn't, and your answers
stay private unless you choose to be quoted. Fill it in again when you have
news, such as interviews or an offer. For bugs, please open an issue.

## Contributing

Fixes and new market skills are welcome. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first: in particular, open pull requests
from a fresh fork of this repo, never from your private copy.

## Licence

MIT. See [LICENSE](LICENSE).
