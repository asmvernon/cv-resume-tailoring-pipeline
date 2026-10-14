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
   asks you for real specifics (numbers, outcomes) rather than making them
   up.
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
they'll be committed to your copy of this repo. **Don't fork this repo
publicly, and don't push your data to a public repository.**

On GitHub, click **Use this template → Create a new repository** and choose
**Private**. Or clone it and push it to a new private repository of your
own. A local folder with no remote at all also works.

## What you need

- **An AI coding assistant that can read and write files in a folder.**
  [Claude Code](https://claude.com/claude-code) works out of the box: it
  picks up `CLAUDE.md` and the skills in `.claude/skills/` automatically.
  Other assistants (Cursor, GitHub Copilot, Codex, Windsurf and others) work
  by following `AGENTS.md`, which points them at the same instructions.
- **Python 3 with PyYAML**, for the inventory checker:
  `python3 -m pip install pyyaml`.
- **For PDFs:** [pandoc](https://pandoc.org/installing.html) and Google
  Chrome or Chromium.
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
   `inventory/roles/`, `inventory/skills.yaml` and
   `inventory/interview_stories.yaml`, and asks you about anything vague. Go
   through what it wrote: this is the record every résumé will be built
   from, so it's worth getting right once.

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
   - saves the job description and checks it against your inventory, walking
     through each gap with you;
   - drafts the résumé and shows you every inclusion, omission and reword
     before writing anything;
   - writes `resumes/<date>-<company>-<title>/resume.md`, `rationale.md` and
     `interview_prep.md`.

5. **Get the PDF:**

   > Make the PDF of that résumé

   The PDF lands next to `resume.md`. If it runs over the page budget, the
   assistant cuts the least relevant bullets rather than shrinking the type.

6. **Commit.** Your inventory, the job description and the résumé are now in
   your private repo, ready for the next application.

## Day to day

| You say | What happens |
|---|---|
| "Add this job to my inventory" | `extract-jd-signal`: match the job against your inventory and resolve gaps, without drafting a résumé |
| "Add my new role" or "I also did X at Y" | `seed-inventory-from-source`: update the inventory from what you tell it |
| "Tailor my résumé for this job" | `apply-to-job`: the whole path, job description to draft |
| "Make the PDF" | `render-resume-pdf` |
| "Create a tailoring skill for German CVs" | `create-tailor-skill`: add a new country or kind of role |

Open questions the assistant can't settle for you, such as two sources that
disagree about a skill, go in `docs/tasks.md`.

## What's in the repo

```
.claude/skills/        the workflows (one SKILL.md each)
.claude/agents/        resume-critic, an independent review of each draft
inventory/schema.md    the inventory data model
inventory/             your experience and skills (yours, private)
job_descriptions/      the jobs you've applied to (yours, private)
resumes/               one folder per application (yours, private)
scripts/               the inventory checker and the PDF renderer
docs/tasks.md          open items the assistant logs for your decision
CLAUDE.md, AGENTS.md   the rules every assistant follows here
```

## What it costs

Nothing beyond your AI assistant's own plan or API usage. There's no hosting.

## What it doesn't do

- It doesn't find jobs or apply to them. You bring the job descriptions.
- It doesn't write cover letters.
- It won't fill a gap by making something up. A real gap becomes a
  development goal in `inventory/dev_opportunities_tracker.yaml`.

## Contributing

Fixes and new market skills are welcome. Read
[CONTRIBUTING.md](CONTRIBUTING.md) first: in particular, open pull requests
from a fresh fork of this repo, never from your private copy.

## Licence

MIT. See [LICENSE](LICENSE).
