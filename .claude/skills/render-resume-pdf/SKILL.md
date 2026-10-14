---
name: render-resume-pdf
description: Render a finished tailored resume/CV (resumes/<slug>/resume.md) to a text-based, ATS-safe PDF for submission. Use whenever the user asks for the PDF of a resume or CV produced by tailor-resume-usa or tailor-resume-uk-contract.
---

# Render resume PDF

The last step after `tailor-resume-usa` / `tailor-resume-uk-contract`: turns
an approved `resume.md` into the PDF the user actually submits. Presentation
only. It never changes wording, so no reword approval is involved, but it
also never "fixes" content to make the page count work.

## Steps

1. **Pick the source.** Use `resumes/<slug>/resume.md` from the branch that
   holds the latest approved draft (the JD application branch, or `main` if
   it has merged). Don't render a draft whose rewords are still awaiting the
   user's approval.

2. **Pick the paper size from the track.** US resume → `--paper letter` (the
   default). UK contract CV → `--paper a4`.

3. **Render:**

   ```
   python3 scripts/render_resume_pdf.py resumes/<slug>/resume.md [--paper a4]
   ```

   This writes `resumes/<slug>/resume.pdf` and prints the page count. It
   needs `pandoc` and a Chromium/Chrome binary (`$CHROMIUM`,
   `/opt/pw-browsers/chromium`, or `chromium`/`google-chrome` on PATH).

4. **Check the output before handing it over.**
   - Page count is within the market spec's budget (US: 1–2 pages per
     `tailor-resume-usa/reference/resume-principles.md`; UK: per
     `tailor-resume-uk-contract`'s own spec). If it overflows, don't shrink
     the font or margins below the stylesheet's values. Cut bullets instead,
     using the order the rationale names, then re-render and re-check. Record
     every cut in `rationale.md` (which bullet, from which role, and that it
     was cut for length at render time).
   - Rasterize and look at every page (`pdftoppm -r 80 -png resume.pdf pg`):
     the name/contact header renders as two lines, bullets render as real
     lists (not "- " text), and no section heading is stranded at a page
     bottom.
   - Confirm the text is extractable (`pdftotext resume.pdf - | head`).
     That's what an ATS reads.

5. **Commit and deliver.** Commit `resume.pdf` next to `resume.md` on the
   same branch (it's part of that JD's application work per `CLAUDE.md`),
   and give the user the file directly.

6. **Report length cuts to the user.** If any bullets were removed to fit
   the page budget, say so in the same message that delivers the PDF. List
   each removed bullet by role and its full text, and note that the cuts
   are also logged in `rationale.md`, so the user can ask for a different
   trade-off. If nothing was cut, say that the PDF matches `resume.md`
   unchanged.

## Hard rules

- Never cut a bullet for length silently. Every cut is both logged in
  `rationale.md` and reported to the user with the PDF.
- Never edit resume wording in this step. Any content change goes back
  through the tailoring skill's before/after approval.
- Never add graphics, columns, tables, icons or headers/footers carrying
  contact info. The stylesheet (`resume.css` in this folder) is deliberately
  plain to keep the PDF ATS-parseable.
- Never publish the PDF outside the repo or the user's own delivery channel.
  This is a private repo.
