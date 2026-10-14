# Adding a tailoring skill for another country or market

The repo ships two tailoring skills: `tailor-resume-usa` (a US résumé) and
`tailor-resume-uk-contract` (a CV for UK contract, day-rate roles). Résumé
conventions differ a lot between countries and between kinds of role, so
each market gets its own skill rather than one skill with a switch. This guide
walks through adding one, for example `tailor-cv-germany`,
`tailor-cv-uk-permanent` or `tailor-resume-canada`.

You can do every step below by asking your AI assistant, one step at a time.
Review its research yourself: the spec it writes is only as good as the
sources behind it.

## What stays the same in every market

Don't change these. They are what make every output trustworthy, and the
other skills and the critic rely on them:

- **Inputs.** The same inventory (`inventory/`) and a saved job description
  (`job_descriptions/`). A new market never needs new inventory fields for
  experience; if it needs application-specific details (a notice period, a
  day rate, a work-permit status), ask the user each time, as
  `tailor-resume-uk-contract` does, and never store or infer them.
- **Never invent.** Only `confirmed` inventory content goes in. Nothing
  `candidate` or `jd_inferred`, however well it fits.
- **Reword approval.** Every change to a bullet's wording is shown as a
  before/after and written only once the user approves it. A reword never
  implies more than the bullet's `evidence_strength` supports.
- **Outputs.** `resumes/<slug>/resume.md`, `rationale.md` and
  `interview_prep.md`, in the same shape as the existing skills.
- **The self-check and critique.** The skill ends by running its spec's
  self-check list, then (optionally) the `resume-critic` agent, which reviews
  any market as long as it's given the right spec file.

## What changes: the market spec

Everything market-specific lives in one file,
`reference/resume-principles.md`, which the skill drafts against and
self-checks against. Copy the section headings from
`tailor-resume-usa/reference/resume-principles.md` and fill each one for the
new market:

| Section | Questions to answer for the new market |
|---|---|
| Format & structure | Reverse-chronological or another order? Expected length in pages? Paper size (Letter or A4)? One column? |
| Contact block | What goes in and what's left out? Many markets expect no photo, date of birth or marital status; some (for example Germany, Japan) traditionally include a photo and personal details. Address or just city? |
| Summary or profile | Expected, optional or unusual? How long, and in what voice (first person, implied first person, third person)? |
| Experience section | Grouped by employer or by engagement? How are dates written? How many bullets per role? |
| Concurrent roles and title changes | Keep the existing rule (never print overlapping date ranges) and say how this market shows a title progression. |
| Skills section | A short list, a grouped table, or a prominent summary near the top? |
| Screening and keywords | Who screens first (an applicant tracking system, an agency, a hiring manager)? How literally should the job description's wording be mirrored? |
| Language and spelling | Which language and spelling (US or British English, or another language entirely)? "Résumé" or "CV"? |
| Market-specific sections | Anything the market expects that others don't: a cover page, references, a signature and date, availability, work authorisation. |
| What to omit | Anything that's normal elsewhere but a mistake here. |
| Self-check before finalizing | A numbered checklist of every rule above, written so it can be ticked off one by one. The critic works through this list item by item. |

Write each rule as something checkable ("2 pages maximum", "no photo"), not
as general advice. Where sources disagree, say so in the spec and pick the
safer default.

### Where to research

Prefer, in order: the country's official public employment service or
government careers guidance; established university careers services in that
country; recruiters and agencies who place people in that market; then
general career sites. Note the sources at the top of the spec so they can be
re-checked later. If you can, ask someone who hires in that market to read
the finished spec.

## Steps

1. **Pick a name.** `tailor-<resume|cv>-<market>`, lower case with hyphens,
   using the word the market itself uses. Add a qualifier when the kind of
   role changes the conventions (`-contract`, `-academic`, `-permanent`).

2. **Copy the closest existing skill.**

   ```bash
   cp -R .claude/skills/tailor-resume-usa .claude/skills/tailor-cv-germany
   ```

   Start from `tailor-resume-uk-contract` instead if the new market is also
   contract or agency work.

3. **Rewrite `reference/resume-principles.md`** for the new market, using
   the table above.

4. **Edit the new `SKILL.md`:**
   - The frontmatter `name` must match the folder name.
   - Rewrite the `description`: what it drafts, for which market, and when to
     use it instead of the other tailoring skills. Claude Code uses this text
     to decide which skill to run, so name the market plainly.
   - Change the title and opening paragraph to the new market, and add a line
     pointing at the other markets' skills.
   - Add any application-specific inputs to ask the user for (see *What stays
     the same*).
   - Leave the steps, the hard rules and the output files alone unless the
     market genuinely needs a different output.

5. **Wire it into the other skills.**
   - `.claude/skills/apply-to-job/SKILL.md`, step 2 (*Pick the market/track*):
     add a line naming the new skill and the signals in a job description
     that point to it.
   - `.claude/skills/render-resume-pdf/SKILL.md`, step 2: add the paper size
     for the new market. `scripts/render_resume_pdf.py` supports `letter`
     and `a4`; anything else needs a change there too.
   - `.claude/agents/resume-critic.md`: it names the existing specs as
     examples; add the new one.
   - Add a line to the skills table in `AGENTS.md` and to the README.

6. **Try it on a real job description** from that market, with your own
   inventory. Read the draft and the critic's findings against the spec, and
   tighten any rule the draft got wrong because the spec was vague.

7. **Share it back** (optional). If you think the new market would help
   others, open a pull request against the upstream repo with only the skill
   and the wiring changes. Never include anything from your `inventory/`,
   `job_descriptions/` or `resumes/`.
