---
name: tailor-resume-usa
description: Draft a tailored, ATS-sane US-market resume for a specific job description, built entirely from the confirmed inventory in inventory/ (never inventing content), plus a stub interview_prep.md pulling relevant STAR-format interview_stories. Rewords bullets to mirror the JD's language where it genuinely helps, but every reword is shown as an explicit before/after and requires the user's approval before it's written to disk. Use whenever the user wants a resume tailored to a US-market job, or asks to apply US resume best practices to their inventory content. For UK contract-market CVs, use `tailor-resume-uk-contract` instead.
---

# Tailor resume (US market)

Turns the confirmed inventory + one target JD into a tailored US-market
resume draft. Selection and reframing only — nothing here invents
experience, and nothing gets reworded without the user seeing the
before/after first.

For a UK contract-market CV instead, use `tailor-resume-uk-contract` — it
follows different format/structure conventions (see its own
`reference/resume-principles.md`), though the same never-invent and
reword-approval rules apply.

Resume craft (format, ATS rules, bullet formula, keyword rules, self-check
list) lives in `reference/resume-principles.md` — read it before drafting,
and draft against it, don't reinvent it inline.

## Inputs

- The target JD: a path to an already-saved `job_descriptions/*.md` file, or
  fresh JD text/file/link to work from directly.
- The full inventory: `inventory/profile.yaml`, `inventory/education.yaml`,
  `inventory/skills.yaml`, `inventory/interview_stories.yaml`, and every
  file in `inventory/roles/`.

## Steps

1. **Check whether this JD has already been run through `extract-jd-signal`.**
   If not, ask the user whether to run that first (so any real gaps get
   reconciled into the inventory before drafting) or proceed directly with
   what's currently there. Either is fine — just don't assume.

2. **Read the full inventory** and scan for unresolved ambiguity — a
   `notes:`/`TODO` field on a role, an unusual date overlap, anything
   load-bearing for this JD. Flag it to the user before drafting rather than
   silently picking a resolution. A same-company overlap already declared
   with `concurrent_with`/`title_history` isn't ambiguous: present it per
   `reference/resume-principles.md`'s "Concurrent roles and title changes"
   rule instead of asking again.

3. **Select relevant content**, per `reference/resume-principles.md`:
   - Which roles make the cut, and how many bullets each gets (recent/
     relevant roles get more; older/tangential ones get fewer or none).
   - Only `confidence: confirmed` skills and `source: original` bullets —
     never `candidate`/unconfirmed content, regardless of how well it would
     fit the JD.
   - How the Skills section should be grouped/ordered for this JD.

4. **Draft bullets.** Default to the inventory's text verbatim. Where
   mirroring the JD's exact phrasing would genuinely help (a real keyword
   match, not padding), propose a reworded version — never increasing the
   implied strength beyond the bullet's `evidence_strength`.

5. **Present the full plan before writing anything**:
   - Which roles/bullets are included, and what's being omitted (and why).
   - **Every proposed reword as an explicit before/after pair** — this is
     the one thing that always needs per-line sign-off, not just an overall
     thumbs-up on the draft. A Professional Summary counts: unless it's the
     inventory's own summary text verbatim, show it for approval the same
     way.
   - How the Skills section is organized.

6. **Apply only what's approved.** Verbatim bullets pass through as-is;
   reworded ones only go in if approved (use the original text otherwise, or
   drop the bullet if the user says so).

7. **Write three files** under `resumes/YYYY-MM-DD-company-title-slug/`
   (matching the JD's slug from `job_descriptions/`):
   - `resume.md` — the clean, ATS-formatted draft, laid out as `render-resume-pdf`'s *resume.md layout* section describes, so it renders without edits. No
     meta-commentary in this file — it should be ready to convert straight
     to PDF/DOCX.
   - `rationale.md` — what was emphasized and why, what was omitted and why,
     the approved reword log (before/after, per bullet), and the self-check
     results below.
   - `interview_prep.md` — **v1/stub, to be expanded later.** Pull every
     `inventory/interview_stories.yaml` entry whose `skills` or
     `competencies` plausibly relate to this JD (recruiting/hiring,
     incident response, regulated-industry judgment calls, etc. — match on
     substance, not just exact keyword overlap), and list each in full STAR
     format with a one-line note on why it's relevant to this JD. This is
     presentation only — don't edit the underlying story content here, and
     don't invent Action/Result detail to fill a story that's still a TODO
     placeholder in the inventory. If a listed story has incomplete
     Action/Result, say so plainly at the top of its entry rather than
     silently including a half-true STAR breakdown. If no stories are
     relevant to this JD, write the file anyway with a short note saying so
     — don't skip it.

8. **Run the self-check list** from `reference/resume-principles.md` and
   report the results in `rationale.md`, including an honest list of
   required JD keywords that are genuinely *not* covered — don't force a
   match that isn't real. Then commit the three files (on the application's
   branch if you use branches; see `CLAUDE.md`'s *Working conventions*).

9. **Get an independent critique.** This skill doesn't manage branches or
   PRs itself (see `CLAUDE.md`'s Working conventions) — once this output
   has an open PR (already open, or the user opens one now), invoke the
   `resume-critic` subagent (Agent tool, `subagent_type: resume-critic`),
   passing it: this skill's own `reference/resume-principles.md` path, the
   JD file path, the written `resume.md` path, `rationale.md`'s path, and
   the PR number/repo to comment on. It re-checks the self-check list and
   every Skills entry's consistency/JD-relevance independently, and posts
   findings as PR comments — report its summary back to the user rather
   than silently swallowing the result. If there's no PR yet and the user
   doesn't want one opened now, skip this step and say so plainly instead
   of guessing where else to post the critique.

## Hard rules

- Never invent or embellish content — every bullet traces to the inventory,
  verbatim or as an explicitly-approved reword.
- Never use `candidate`/`jd_inferred`/unconfirmed inventory content as if it
  were confirmed.
- Never write a reworded bullet to disk without the user having seen and
  approved that specific before/after.
- Never let a reword imply a stronger claim than the bullet's
  `evidence_strength` supports.
- Converting the final `resume.md` to PDF/DOCX (for actual submission) is a
  separate, later step — this skill's job ends at a clean Markdown draft.
