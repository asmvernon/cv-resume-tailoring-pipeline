# Cover letter principles

The craft rules `write-cover-letter` drafts against. A rule tagged with a
source comes from that source. *(pipeline rule)* marks a rule this pipeline
sets for itself. **(unverified)** marks common practice that the sources here
don't state outright; treat it as a default the user can override.

## Sources

- **Prospects**: Prospects (UK graduate careers service), *Cover letters*,
  https://www.prospects.ac.uk/careers-advice/cvs-and-cover-letters/cover-letters
  (read 2026-11-10): when to send one, length, structure, keywords,
  addressing, sign-off, file format.

## When to write one

- Send a cover letter unless the advert says not to. *(Prospects: "Applications
  should always include a cover letter unless the job advert advises you
  differently.")*
- Write a new one for every application. *(Prospects: "You should rewrite your
  cover letter every time you apply for a position to target the company.")*

## Length and structure

- **One page**, three to five short paragraphs. *(Prospects: "Typically, three
  to five concise paragraphs, cover letters should not exceed one A4 page.")*
  US letters follow the same one-page budget on Letter paper **(unverified)**.
- **Opening**: the role you're applying for, and in one or two sentences who
  you are now and why this role. *(Prospects: "Begin by stating the position
  you're applying for".)*
- **Why this company**: what draws you to its mission or work, tied to
  something true about you, ideally one personal story line the user wrote.
  *(Prospects: "why you're interested in working for the company and what you
  can offer the organisation")*
- **Evidence**: one or two paragraphs that answer the role's lead
  requirements with specific, sourced examples. *(Prospects: "Back up the
  claims in your cover letter with real evidence or examples".)*
- **Close**: restate your interest, and anything practical the role needs
  (relocation, on-site work, travel) if the user has confirmed it. *(Prospects:
  "Reiterate your interest in the role and indicate your desire for an
  interview.")*
- **Complement the résumé; don't repeat it.** Tell the story behind two or
  three of its strongest points instead of listing them again. *(Prospects:
  "cover letters should complement your CV but not duplicate it"; "Don't fill
  up space by repeating what's already covered in your CV.")*
- **Use the advert's keywords** next to real evidence. *(Prospects: "Use
  keywords that appear in the job advert".)*
- **Salary**: only if the advert asks for it. *(Prospects: "only mention your
  current salary or salary expectations if the employer has specifically
  asked you to.")*

## Addressing and signing off

- Address a named person when the advert or the user gives one.
  *(Prospects: "Always try and address your cover letter directly to the
  person who will be reading it.")* Never guess a name.
- **UK**: with a named contact, "Dear Ms Smith" and "Yours sincerely"; with a
  general greeting ("Dear Hiring Manager"), "Yours faithfully". *(Prospects:
  "If you include a named contact, sign it off with 'Yours sincerely'. If you
  use a general greeting, finish with 'Yours faithfully'.")*
- **US**: "Dear <Name>" or "Dear <Company> Hiring Team", signed off
  "Sincerely," **(unverified)**.

## Language

- The market's spelling: British for UK letters, American for US letters,
  including words the user's inventory spells the other way (catalogue and
  catalog, modelled and modeled, analyse and analyze). *(pipeline rule)*
- First person, active voice, plain words. No filler ("I am writing to
  express my interest"), no claims a reader can't check ("passionate
  team player"), no quoting the JD back at the reader. *(pipeline rule)*
- The user's own voice wins over generic polish: keep phrases from their
  `cover_letter_style` and approved letters unless they're ungrammatical.
  *(pipeline rule)*

## Layout of cover_letter.md

`scripts/render_cover_letter.py` depends on this layout. Separate blocks with
one blank line:

```
Jane Doe
City, ST | (555) 010-0000 | jane@example.com | linkedin.com/in/janedoe

November 10, 2026

Hiring Team
Example Bio
South San Francisco, CA

Dear Example Bio Hiring Team,

Opening paragraph.

Body paragraphs.

Closing paragraph.

Sincerely,

Jane Doe
```

- Line 1 is the name and line 2 the contact line, the same as the résumé's
  header. *(pipeline rule)*
- Then the date, then the recipient block (its lines are kept as written),
  then the salutation, the paragraphs, the sign-off and the typed name.
- The renderer puts a signature image, if given, between the sign-off and
  the typed name. *(pipeline rule)*
- Use the same font as the résumé. *(Prospects: "Use the same font and size as
  you use in your CV".)* The renderer does this by default.
- Submit as PDF unless the advert asks for Word. *(Prospects: "save it with a
  .PDF file extension".)*

## Review checklist

The step 6 reviewer and the final self-check both work through this list.

**Truth**
- [ ] Every factual claim traces to a confirmed inventory entry, the user's
      own approved words, or the JD, and is listed in the claim-to-source
      list.
- [ ] No verb, scope or number is stronger than its source (e.g. "led" when
      the bullet says "contributed", "the team's tests" written as "tested").
- [ ] Nothing contradicts the tailored résumé (titles, dates, team names,
      how a project is described).
- [ ] Years of experience and career-span claims match the inventory's
      profile notes.

**Fit**
- [ ] The opening names the exact role title.
- [ ] The evidence paragraphs answer the role's lead requirements.
- [ ] Company facts come only from the JD or a page actually read.
- [ ] Practical details (relocation, on-site, travel, salary, notice) appear
      only if the user confirmed them for this application.

**Language**
- [ ] Grammatical; no run-on sentences; no unclear "which", "that" or "it".
- [ ] No phrase repeated close together, in the letter or in other answers
      going to the same employer.
- [ ] Spelling matches the market.
- [ ] Salutation and sign-off match the market and whether a name is known.

**Format**
- [ ] One page once rendered.
- [ ] Layout matches *Layout of cover_letter.md*.
