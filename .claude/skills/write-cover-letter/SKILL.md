---
name: write-cover-letter
description: Draft a tailored cover letter for one job description in the user's own voice, built only from their confirmed inventory and their own approved writing (never inventing experience), get an independent copy-edit and fact-check, and render a one-page letter-format PDF with an optional signature. Use whenever the user wants a cover letter for a job, usually after `tailor-resume-usa`, `tailor-resume-uk-contract` or `tailor-cv-uk-permanent` has drafted the résumé or CV for that job.
---

# Write cover letter

Turns one target JD, the tailored résumé or CV for it, and the confirmed
inventory into a cover letter draft. A cover letter is new prose, so unlike a
résumé nothing in it passes through verbatim: the whole letter is shown to the
user and approved before it's final, and every claim in it must trace to a
source the user wrote or confirmed.

Letter craft (length, structure, salutation and sign-off by market, layout,
the review checklist) lives in `reference/cover-letter-principles.md`. Read it
before drafting.

## Inputs

- The target JD, saved under `job_descriptions/` (run `extract-jd-signal`
  first if it isn't).
- The tailored résumé or CV for this JD, `resumes/<slug>/resume.md`, if one
  exists. The letter complements it and must not contradict it.
- The full inventory: `inventory/profile.yaml`, `inventory/education.yaml`,
  `inventory/skills.yaml`, `inventory/interview_stories.yaml` and every file in
  `inventory/roles/`.
- The user's voice: the optional `cover_letter_style` block in
  `inventory/profile.yaml` (see `inventory/schema.md`), and any cover letters
  they've already approved in `resumes/*/cover_letter.md`.
- Application details the inventory doesn't hold, asked for each time and
  never stored in the inventory: the market (US or UK), a named recipient if
  the advert gives one, where they saw the advert, when they can start and
  any dates they're unavailable for interviews, and anything the advert asks
  the letter to cover (salary expectations, notice period, work
  authorization).

## Steps

1. **Check the inputs.** Confirm the JD is saved and whether a tailored
   résumé exists for it. If the résumé still has rewords or a summary awaiting
   the user's approval, say so: the letter will follow whatever the résumé
   finally says.

2. **Learn the user's voice.** If `cover_letter_style` is empty and there are
   no approved letters in `resumes/`, ask the user for one letter they've
   written and liked (pasted, a file, or a link). Record what's reusable in
   `cover_letter_style`: the structure they use, phrases they like, and any
   personal story lines they wrote (each with where it came from). Show the
   user what you're adding and write it only once they agree. Their own
   words become an approved source for later letters, the same way their CV
   is for the inventory.

3. **Research the employer from the JD**, and from the company's own site if
   the user wants more: its mission, what the team does, and the two or three
   requirements the role leads with. Don't invent company facts; anything not
   in the JD or a page you actually read stays out.

4. **Plan the letter** per `reference/cover-letter-principles.md`: which two
   or three pieces of evidence answer the role's lead requirements, which
   roles they come from, and which personal story line opens the "why this
   company" paragraph. Prefer evidence the résumé already shows, told with
   more context, over new claims.

5. **Draft** `resumes/<slug>/cover_letter.md` in the layout from the
   principles file. Write in the user's voice (step 2), in the market's
   spelling. Every factual claim must trace to one of:
   - a confirmed inventory entry (a `source: original` bullet or a
     `confidence: confirmed` skill), with no stronger verb or wider scope than
     the entry supports;
   - the user's own words in `cover_letter_style` or an approved letter;
   - the JD itself (for what the company does).

   Keep a claim-to-source list as you go; it goes in `rationale.md`.

6. **Get an independent review before showing the user.** Run a subagent
   (Agent tool) as a copy editor and fact-checker. Give it the letter's path,
   the JD's path, the inventory folder, `inventory/profile.yaml`'s
   `cover_letter_style`, and the review checklist in
   `reference/cover-letter-principles.md`. Ask it for a numbered list of
   findings, each marked MUST (a grammar error, or a claim the sources don't
   support) or SHOULD (style, clarity, repetition), with the current text and
   a replacement. It reports only and doesn't edit. Apply every MUST. Apply
   the SHOULDs that keep the user's voice. Don't drop the user's own
   approved phrasing just because the reviewer finds it informal; note it
   instead.

7. **Present the draft for approval**: the full letter, the claim-to-source
   list, what the review changed, and anything you kept against the
   reviewer's advice and why. The user approves the letter as a whole, and
   any line they change is their wording from then on.

8. **Render** once the user approves:

   ```
   python3 scripts/render_cover_letter.py resumes/<slug>/cover_letter.md [--paper a4] [--signature <path-to-signature.png>]
   ```

   It writes `resumes/<slug>/cover_letter.pdf` and prints the page count. Use
   `--paper a4` for UK letters. A signature image is the user's personal data:
   take the path from them each time, never commit the image, and leave it
   out if they don't give one. The letter must fit on one page; if it doesn't,
   cut words, never the font size. Rasterize the page and look at it
   (`pdftoppm -r 80 -png cover_letter.pdf pg`) before handing it over.

9. **Record and commit.** Add a *Cover letter* section to
   `resumes/<slug>/rationale.md`: the claim-to-source list, the review
   findings and what was applied, and the approval date. Commit
   `cover_letter.md` and `cover_letter.pdf` on the application's branch (see
   `CLAUDE.md`'s *Working conventions*).

## Hard rules

- Never invent or embellish experience, numbers, employers, titles or
  outcomes. A claim with no source from step 5 stays out.
- Never present the letter as final without the user's approval of the
  whole text.
- Never add salary, notice period or work-authorization details unless the
  advert asks for them and the user has given them for this application.
  A start date and unavailable dates go in only if the user gave them for
  this application.
- Never store application details (salary, notice period, start date, work
  authorization) or the signature image in the inventory.
- Never copy wording from the JD into the letter as if it were the user's
  own experience. Echoing the JD's keywords next to real evidence is fine.
