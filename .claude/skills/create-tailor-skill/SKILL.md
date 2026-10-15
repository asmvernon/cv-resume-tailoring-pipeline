---
name: create-tailor-skill
description: Create a new tailoring skill for another country or kind of role (e.g. a German CV, a UK permanent-role CV, a Canadian résumé, an academic CV), modelled on tailor-resume-usa and tailor-resume-uk-contract — researching that market's conventions from cited sources, writing its reference/resume-principles.md spec, and wiring it into apply-to-job, render-resume-pdf and resume-critic. Use whenever the user wants to tailor résumés or CVs for a market the existing tailoring skills don't cover.
---

# Create a tailoring skill for a new market

Résumé and CV conventions differ between countries and between kinds of role,
so each market gets its own tailoring skill rather than one skill with a
switch. This skill adds one. Everything that makes the outputs trustworthy
(the inventory, never inventing, reword approval, the output files, the
critique) stays exactly as it is; only the market's conventions change, and
they live in one spec file.

The research is the part most likely to go wrong: conventions that sound
right can be wrong for the market. So every rule in the new spec cites a
source, and the user reviews the spec before anything else is written.

## Inputs

- The market: country, and the kind of role if it changes the conventions
  (permanent or contract, academic, executive, early-career).
- The language the CV is written in, if not English.

## Steps

1. **Check the market isn't already covered.** List the existing
   `tailor-*` skills in `.claude/skills/` and read their descriptions. If
   one already fits, say so and stop.

2. **Agree the name** with the user: `tailor-<resume|cv>-<market>`, lower
   case with hyphens, using the word the market itself uses (e.g.
   `tailor-cv-germany`, `tailor-resume-canada`, `tailor-cv-uk-permanent`).
   Add a qualifier when the kind of role changes the conventions
   (`-contract`, `-academic`).

3. **Research the market's conventions.** Prefer, in order: the country's
   official public employment service or government careers guidance;
   established university careers services in that country; recruiters and
   agencies who place people in that market; then general career sites.
   Answer every question in the table below, noting the source for each
   answer. If you can't reach a source, say so rather than answering from
   memory, and mark that rule as unverified. Where sources disagree, record
   both and pick the safer default.

   | Section | Questions to answer |
   |---|---|
   | Format & structure | Reverse-chronological or another order? Expected length in pages? Paper size (Letter or A4)? One column? |
   | Contact block | What goes in and what's left out? Photo, date of birth, nationality, marital status: expected, optional or a mistake? Full address or city only? |
   | Summary or profile | Expected, optional or unusual? How long, in what voice? |
   | Experience section | Grouped by employer or by engagement? How are dates written? How many bullets per role? |
   | Concurrent roles and title changes | Keep the existing rule (never print overlapping date ranges); how does this market show a title progression? |
   | Skills section | A short list, a grouped table, or a summary near the top? |
   | Screening and keywords | Who screens first (an applicant tracking system, an agency, a hiring manager)? How literally should the job description's wording be mirrored? |
   | Language and spelling | Which language and spelling? "Résumé" or "CV"? |
   | Market-specific sections | Anything the market expects that others don't: a cover page, references, a signature and date, availability, work authorisation. |
   | What to omit | Anything that's normal elsewhere but a mistake here. |

4. **Present the findings to the user before writing anything**: each
   answer with its source, the unverified ones flagged, and the conflicts
   with the default you picked. Ask the user to confirm or correct them;
   if they know someone who hires in that market, suggest asking them to
   read it. Don't continue until the user approves.

5. **Copy the closest existing skill** to
   `.claude/skills/<new-name>/`: `tailor-resume-uk-contract` if the new
   market is contract or agency work, otherwise `tailor-resume-usa`.

6. **Write `reference/resume-principles.md`** for the new market:
   - The same section headings as the copied spec, filled from the
     approved findings, plus any market-specific sections.
   - A *Sources* list at the top, with what each was used for.
   - Every rule written as something checkable ("2 pages maximum",
     "no photo"), not general advice.
   - A *Self-check before finalizing* checklist covering every rule. Keep
     the existing items that apply to every market (nothing from
     `candidate`/unconfirmed content, every outcome metric traces to
     `strong` evidence, no overlapping date ranges unless marked concurrent,
     report missing JD keywords honestly). The `resume-critic` agent works
     through this list item by item.

7. **Edit the new `SKILL.md`:**
   - Frontmatter `name` matches the folder name.
   - Rewrite the `description`: what it drafts, for which market, and when
     to use it instead of the other tailoring skills. The assistant uses
     this text to pick the skill, so name the market plainly.
   - Change the title and opening paragraph to the new market, with a line
     pointing at the other market skills.
   - Add any application-specific inputs to ask the user for each time
     (a notice period, a salary expectation, work-permit status), following
     `tailor-resume-uk-contract`'s Inputs: ask, never store in the
     inventory, never infer.
   - **Leave the steps, the output files and the hard rules alone**, apart
     from adding a hard rule for any new application-specific input.

8. **Wire it into the other skills:**
   - `.claude/skills/apply-to-job/SKILL.md`, step 2 (*Pick the
     market/track*): a line naming the new skill and the signals in a job
     description that point to it.
   - `.claude/skills/render-resume-pdf/SKILL.md`, step 2: the paper size.
     `scripts/render_resume_pdf.py` supports `letter` and `a4`; anything
     else needs a change there too.
   - `.claude/agents/resume-critic.md`: add the new spec to the specs it
     names as examples.
   - `AGENTS.md` (if present): a row in the skills table.
   - `README.md`: a row in the markets table.

9. **Show the user the full diff** of the new skill and the wiring, then
   suggest trying it on a real job description from that market and
   tightening any rule the draft got wrong because the spec was vague.

## Hard rules

- Never change the never-invent rule, the reword-approval rule, the output
  files or the inventory schema for a new market. Only the spec and the
  application-specific inputs differ.
- Never write a convention into the spec without a cited source or an
  explicit "unverified" mark.
- Never write the spec before the user has approved the research findings.
- Never store application-specific details (salary, notice period,
  permit status) in the inventory.
