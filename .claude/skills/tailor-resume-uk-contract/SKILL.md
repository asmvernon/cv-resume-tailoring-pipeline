---
name: tailor-resume-uk-contract
description: Draft a tailored UK contract-market CV for a specific job description, built entirely from the confirmed inventory in inventory/ (never inventing content), plus a stub interview_prep.md pulling relevant STAR-format interview_stories. Rewords bullets to mirror the JD's language where it genuinely helps, but every reword is shown as an explicit before/after and requires the user's approval before it's written to disk. Use whenever the user wants a CV tailored to a UK contract/day-rate role, or asks to apply UK contracting CV conventions to their inventory content. For US-market resumes, use `tailor-resume-usa` instead.
---

# Tailor resume (UK contract market)

Turns the confirmed inventory + one target JD into a tailored CV draft for
the UK IT/consulting contract market (day-rate engagements via an agency,
inside/outside IR35 — as opposed to a permanent UK role or a US-market
resume). Selection and reframing only — nothing here invents experience,
and nothing gets reworded without the user seeing the before/after first.

UK contracting CVs follow real conventions that differ meaningfully from
both a US resume and a standard UK permanent CV — engagement-based
structure, a prominent skills/tech summary, longer accepted length, and
IR35/availability framing. Those conventions live in
`reference/resume-principles.md` — read it before drafting, and draft
against it, don't reinvent it inline. For a US-market resume instead, use
`tailor-resume-usa` — its `reference/resume-principles.md` covers the
different (and in places contradictory, e.g. length and skills-table norms)
US conventions.

## Inputs

- The target JD: a path to an already-saved `job_descriptions/*.md` file, or
  fresh JD text/file/link to work from directly.
- The full inventory: `inventory/profile.yaml`, `inventory/education.yaml`,
  `inventory/skills.yaml`, `inventory/interview_stories.yaml`, and every
  file in `inventory/roles/`.
- Contract-logistics details the inventory doesn't hold (day-rate
  expectation, notice period/availability date, inside/outside IR35
  preference) — these are application-specific, not experience, so they're
  never inferred or invented. Ask the user directly each time, and only
  include what the user gives you; it's normal and fine to omit any of
  these entirely if the user prefers to handle them with the agency
  separately rather than on the CV.

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

3. **Ask for the contract-logistics details** listed under Inputs above (day
   rate, availability/notice period, IR35 preference) if the user hasn't
   already given them, and confirm whether to include them on the CV at all
   — see `reference/resume-principles.md` for how each is conventionally
   presented, if included.

4. **Select relevant content**, per `reference/resume-principles.md`:
   - Which engagements make the cut, and how much space each gets (recent/
     relevant, longer engagements get more; short/tangential ones get less
     or a one-line mention).
   - Only `confidence: confirmed` skills and `source: original` bullets —
     never `candidate`/unconfirmed content, regardless of how well it would
     fit the JD.
   - How the Key Skills summary should be grouped/ordered for this JD.

5. **Draft bullets.** Default to the inventory's text verbatim. Where
   mirroring the JD's exact phrasing would genuinely help (a real keyword
   match an agency/client search would look for, not padding), propose a
   reworded version — never increasing the implied strength beyond the
   bullet's `evidence_strength`.

6. **Present the full plan before writing anything**:
   - Which engagements/bullets are included, and what's being omitted (and
     why).
   - **Every proposed reword as an explicit before/after pair** — this is
     the one thing that always needs per-line sign-off, not just an overall
     thumbs-up on the draft.
   - How the Key Skills summary is organized.
   - Which contract-logistics details (if any) are going on the CV, per
     step 3.

7. **Apply only what's approved.** Verbatim bullets pass through as-is;
   reworded ones only go in if approved (use the original text otherwise, or
   drop the bullet if the user says so).

8. **Write three files** under `resumes/YYYY-MM-DD-company-title-slug/`
   (matching the JD's slug from `job_descriptions/`), keeping the same file
   names the pipeline and `tailor-resume-usa` use, even though the content
   is a CV rather than a US resume:
   - `resume.md` — the clean CV draft, formatted per
     `reference/resume-principles.md`. No meta-commentary in this file — it
     should be ready to convert straight to PDF/DOCX.
   - `rationale.md` — what was emphasized and why, what was omitted and why,
     the approved reword log (before/after, per bullet), the contract-
     logistics decisions from step 3, and the self-check results below.
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

9. **Run the self-check list** from `reference/resume-principles.md` and
   report the results in `rationale.md`, including an honest list of
   required JD keywords that are genuinely *not* covered — don't force a
   match that isn't real.

10. **Get an independent critique.** This skill doesn't manage branches or
    PRs itself (see `CLAUDE.md`'s Working conventions) — once this output
    has an open PR (already open, or the user opens one now), invoke the
    `resume-critic` subagent (Agent tool, `subagent_type: resume-critic`),
    passing it: this skill's own `reference/resume-principles.md` path, the
    JD file path, the written `resume.md` path, `rationale.md`'s path, and
    the PR number/repo to comment on. It re-checks the self-check list and
    every Key Skills entry's consistency/JD-relevance independently, and
    posts findings as PR comments — report its summary back to the user
    rather than silently swallowing the result. If there's no PR yet and
    the user doesn't want one opened now, skip this step and say so plainly
    instead of guessing where else to post the critique.

## Hard rules

- Never invent or embellish content — every bullet traces to the inventory,
  verbatim or as an explicitly-approved reword.
- Never use `candidate`/`jd_inferred`/unconfirmed inventory content as if it
  were confirmed.
- Never write a reworded bullet to disk without the user having seen and
  approved that specific before/after.
- Never let a reword imply a stronger claim than the bullet's
  `evidence_strength` supports.
- Never invent or assume day rate, availability, notice period, or IR35
  status — these come from the user directly, per JD, or are left off the
  CV entirely.
- Converting the final `resume.md` to PDF/DOCX (for actual submission) is a
  separate, later step — this skill's job ends at a clean Markdown draft.
