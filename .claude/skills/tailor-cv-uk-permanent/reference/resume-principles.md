# CV principles (UK permanent roles)

Reference for `tailor-cv-uk-permanent`. This is the checklist the skill
drafts against and self-checks the final output against: a working spec,
not general advice. It covers permanent, salaried UK roles. Day-rate
contract CVs follow `tailor-resume-uk-contract`'s spec instead.

## Sources

Researched 2026-11-04. Every rule below names the sources it rests on;
**(unverified)** marks a rule no authoritative source settles, where the
safer default was picked.

- **NCS**: National Careers Service, *How to write a CV*,
  https://nationalcareers.service.gov.uk/careers-advice/cv-sections (the
  government's careers service): sections, contact details, introduction,
  work history, references.
- **Prospects CV**: Prospects, *How to write a CV*,
  https://www.prospects.ac.uk/careers-advice/cvs-and-cover-letters/how-to-write-a-cv
  (quoting the University of Chester careers team): length, contact details,
  section order, layout, ATS, references, interests, cover letter.
- **Prospects profile**: Prospects, *Writing a personal statement for your
  CV*,
  https://www.prospects.ac.uk/careers-advice/cvs-and-cover-letters/writing-a-personal-statement-for-your-cv:
  personal profile length and layout.
- **Michael Page**: *10 things to remember when writing your CV*,
  https://www.michaelpage.co.uk/advice/career-advice/cover-letter-and-cv-advice/10-things-remember-when-writing-your-cv
  (a UK recruiter): length, voice, personal details, bullets.
- **University careers guides** (read through search-result quotes, not in
  full): Imperial College (*How to write a CV for roles outside
  academia*), Cambridge, Dundee, Edinburgh Napier, Surrey (2017): length
  for non-academic CVs, publications, right to work, references.

## Format & structure

- **Reverse-chronological.** Work history comes before education for an
  experienced candidate. *(NCS; Prospects CV)*
- **Length: 2 A4 pages by default.** A 3rd page only for a high-level role
  with a lot of relevant experience, never to avoid cutting. Summarise
  detail older than about ten years in a line or two, or omit it.
  *(Prospects CV; Michael Page; Cambridge, Dundee, Napier)*
- **A4 paper**, one plain font (Arial, Calibri or similar) with body text
  at **10pt or above**, rendered with `--paper a4 --font-size 10`.
  *(Prospects CV: 10–12pt. NCS asks for 11pt or bigger; the 10pt floor
  follows Prospects so an experienced candidate fits 2 pages.)*
- **Margins**: the renderer's stylesheet (about 1.3–1.5 cm). Prospects
  suggests 2.5 cm; that isn't adopted, because it costs most of a page,
  and the stylesheet still leaves clear white space. **(deviation from the
  source, noted)**
- **No "Curriculum Vitae" or "CV" heading.** The name is the title.
  *(Prospects CV)*
- **Submission file name**: `Firstname-Lastname-CV-Company-Role-Title.pdf`
  (for example `Jane-Smith-CV-Acme-Lead-Data-Scientist.pdf`), and the same
  name with `.docx` for a Word copy. The repo keeps `resume.pdf`;
  `render-resume-pdf` gives the user the named copy. *(Prospects CV for
  "Firstname-Lastname-CV"; the company and role suffix is a pipeline
  preference, **unverified**.)*
- **Section order**: Contact → Personal profile → Experience → Skills →
  Education → (optional) Certifications, Selected publications.
  Certifications come from `inventory/education.yaml`'s
  `certifications:` list; leave out expired ones. *(NCS; Prospects CV)*
- **Standard section headings** ("Experience", "Skills", "Education") and
  **one column, text only**: no tables, text boxes, images, logos or
  icons, and no contact details in page headers or footers. *(Prospects
  CV: an ATS can't read images or logos, "Use text only".)*
- **Year-only dates**: a role date recorded as a year alone (`"2019"`)
  shows as the year alone ("2016 – 2019"); never add a month. *(pipeline
  rule)*
- **No first-person pronouns** ("I", "my", "me"). Start bullets and
  profile sentences with an **active verb** (Led, Designed, Built,
  Delivered, Mentored), never a passive or weak opener ("Responsible
  for", "Was involved in", "Helped with"). *(Michael Page: "Don't write
  in the first person - start sentences with verbs"; Prospects CV: "Use
  active verbs". Prospects' own profile examples use "I", so the sources
  conflict; the recruiter's rule is used.)*
- **Exception: the profile's opening line** may be a noun phrase that
  names who the candidate is ("Data scientist and engineering leader with
  …"), the conventional UK opener. Every later profile sentence starts
  with an active verb. *(Prospects profile: "Introduce who you are";
  pipeline preference, after a verb opener read awkwardly in use.)*
- **British English spelling** throughout ("organisation", "optimise",
  "analysed"), and the document is always a **CV**, never a résumé.
  *(Prospects CV: "In other countries, such as the USA and Canada, CVs
  are known as résumés.")*

## Contact block

- Name, phone, email, LinkedIn, and **town/city**. Add a portfolio, website
  or GitHub only if it's substantive and current. *(NCS; Prospects CV)*
- **Town/city only, not the full home address.** Prospects says to give
  the full address but also not to include it when posting a CV online;
  applications now go through online portals, so the safer rule is used.
- **Never** a photo, age, date of birth, marital status or nationality.
  *(NCS: "You should not include your age, your date of birth, whether
  you're married or your nationality"; Prospects CV: no photograph;
  Michael Page: avoid age, religion and sex.)*
- **Right to work**: one line ("Full right to work in the UK", or the
  visa type) **only if** the user isn't a UK or Irish citizen, or the
  advert asks. Never state nationality to do it. *(Edinburgh Napier,
  Surrey careers guides; partly verified.)*

## Personal profile

- **Include one** for an experienced candidate: a single paragraph
  straight under the contact details, **with no heading**, at most **150
  words** (aim for 3–5 lines). *(NCS: "a few short lines ... just under
  your name and contact details"; Prospects profile: no longer than 150
  words, "a single paragraph, without a title or subheading".)*
- Say who the candidate is, the strengths that fit this role, and the
  role they want, using the inventory's profile summary as the base.
  Tailored per JD, no clichés ("hardworking", "team player"). *(Prospects
  profile; Prospects CV)*

## Experience section

- Newest first, one block per employer: job title, employer, dates,
  location, then bullets. More bullets for recent, relevant roles (3–6);
  1–3 or none for older or tangential ones. *(NCS: employer, title,
  dates; Michael Page: "include more detail on recent roles".)*
- **Date style**: "Mon YYYY – Mon YYYY" (for example "Mar 2023 – Dec
  2024"). **(unverified: no source specifies one.)**
- **Bullet formula**: active verb + what was done + method/technology +
  outcome. Back claims with evidence, not adjectives. *(NCS: the STAR
  method; Prospects CV: "Lack of evidence" is a common mistake.)*
- **Quantify wherever `evidence_strength: strong` supports it.** Never
  invent a number to fill out a `moderate`/`weak` bullet. Scope figures
  the user stated (team size, volume) are fine from any confirmed bullet;
  outcome metrics need `strong` (see `inventory/schema.md`'s *Scope
  figures and outcome metrics*).
- **Consistent tense** within each role block: past tense for past roles;
  for a current role, pick one convention and hold it. *(pipeline rule)*
- **Gaps**: if the inventory shows a gap the user has explained, give the
  reason briefly with dates, in the right section. Never invent a reason.
  *(Prospects CV; Michael Page: "explaining any gaps")*

### Concurrent roles and title changes

Roles at the same company can overlap in time (see `inventory/schema.md`,
"Concurrent roles and title changes"). Raw overlapping ranges read as an
error to a screener, so:

- When roles are linked by `concurrent_with`, or a role has a
  `title_history`, **never print overlapping date ranges**.
- **Default:** one employer line, then each title with non-overlapping
  dates from `title_history`, noting when the concurrent scope started.
  E.g. "**Lead Data Engineer** *(Squad Lead from Apr 2021)* | Jan 2022 –
  Jun 2023" above "**Senior Data Engineer** | Jan 2020 – Dec 2021".
- A single title-progression block (e.g. "Data Engineer → Senior Data
  Engineer → Lead Data Engineer, Mar 2018 – Jun 2023") is also fine when
  per-title bullets aren't needed.
- **An acting or extra role held on top of an ongoing one** sits under the
  same employer block, marked "(concurrent)". It is never shown as a
  separate job.
- Every date shown must come from the role's `start_date`/`end_date` or a
  `title_history` entry. Never invent a transition month. If the inventory
  has an overlap with no `concurrent_with` link, flag it to the user
  rather than picking dates.

## Skills section

- A short **Skills** section: technical skills, languages and relevant
  training, grouped and ordered by relevance to *this* JD. *(Prospects CV;
  Michael Page)*
- Only `confidence: confirmed` skills, never `candidate`.
- Use the JD's exact term when the inventory's `aliases` already cover it.

## ATS & keyword alignment

- Large UK employers and recruiters screen with an ATS on keywords from
  the **job description and person specification**. Mirror their exact
  wording **inside real bullets**, never as a keyword dump. Name
  qualifications and certifications in full. *(Prospects CV, quoting the
  University of Chester)*
- Every keyword used must be backed by real inventory evidence. A JD
  requirement the inventory doesn't support is `extract-jd-signal`'s gap
  review, not something to paper over here.
- **Rewording a bullet to mirror JD language changes the words the user
  claims as their own.** Every reworded bullet is shown as an explicit
  before/after and approved before it goes in the draft. Bullet
  *selection* doesn't need per-line sign-off, but the full draft is always
  presented before being written to disk.
- A reword must never increase the implied strength of a claim beyond its
  `evidence_strength`.
- **File format**: send what the advert asks for (PDF or .docx); some ATS
  can't read PDFs. *(Prospects CV)*

## Market-specific sections

- **Education**: qualification (with degree class where it helps),
  institution, dates, newest first. *(NCS; Prospects CV)* Leave out school
  grades (GCSE/A-level) for an experienced candidate **(unverified)**.
- **Selected publications**: a short section only for R&D or science
  roles; otherwise omit. *(Imperial careers, via search quote)*
- **Cover letter**: recommend one in the summary to the user unless the
  employer says not to. *(Prospects CV: "Always include a cover letter
  unless the employer states otherwise".)* This skill doesn't write it.

## What to omit

- **References**, including "References available on request": never
  required, and employers assume it. *(Prospects CV: "if you're stuck for
  space, leave this out"; Napier, Dundee. NCS and Michael Page allow the
  line, so it's omitted to save space, not because it's wrong.)*
- **Interests and hobbies** unless directly relevant to the role.
  *(Prospects CV; Michael Page)*
- Photo, age, date of birth, marital status, nationality (see *Contact
  block*).
- Notice period and salary expectation: never on the CV. They go on the
  application form or in the cover letter. **(unverified: none of the
  sources lists them as CV content, but none says so outright.)**
- *(pipeline rule)* Tailoring is as much subtraction as rewording: cut roles and bullets
  that don't serve this JD. Never omit something *because it's
  unflattering* if it's still the most relevant experience.

## Self-check before finalizing

Every rule above has an item here; the `resume-critic` agent works through
them one by one.

**Content and evidence**
- [ ] Every bullet is verbatim from the inventory or an explicitly-approved
      reword: nothing from `candidate`/`weak`/unconfirmed content.
- [ ] Skills section uses only `confidence: confirmed` skills, grouped and
      ordered for this JD.
- [ ] Every outcome metric traces to a `strong`-evidence bullet; scope
      figures trace to any confirmed bullet. See `inventory/schema.md`'s
      *Scope figures and outcome metrics*.
- [ ] Required JD and person-specification keywords appear inside real
      bullets, not as a keyword dump. Report which are covered and which
      are genuinely missing; don't force-fit a missing one.
- [ ] No gap reason is invented; any gap explanation comes from the
      inventory.

**Format**
- [ ] 2 A4 pages or fewer, or 3 with a stated reason (a high-level role,
      a lot of relevant experience).
- [ ] Rendered on A4 with body text at 10pt or above (`--paper a4
      --font-size 10`), with the stylesheet's margins.
- [ ] Reverse-chronological; section order is Contact → Personal profile
      → Experience → Skills → Education → optional Certifications and
      Selected publications.
- [ ] No "CV"/"Curriculum Vitae" heading; the name is the title.
- [ ] Text only, one column, standard headings: no tables, images or
      icons.
- [ ] Dates are "Mon YYYY – Mon YYYY", or year-only where the inventory
      records only a year.
- [ ] No two date ranges on the page overlap unless one is explicitly
      marked concurrent, and every date traces to the role file's dates or
      its `title_history`.
- [ ] 3–6 bullets for recent, relevant roles; 1–3 or none for older or
      tangential ones; detail older than about ten years summarised or
      omitted.

**Language**
- [ ] British English spelling throughout; called a CV, never a résumé.
- [ ] Every bullet, and every profile sentence after an optional
      noun-phrase opener, starts with an active verb; no first-person
      pronouns; no "Responsible for"/"Was involved in".
- [ ] Tense is consistent within each role block.

**Profile and contact**
- [ ] A personal profile of at most 150 words, one paragraph, no heading,
      tailored to this JD and free of clichés.
- [ ] Contact block has town/city only: no full address, photo, age, date
      of birth, marital status or nationality.
- [ ] A right-to-work line appears only if the user isn't a UK or Irish
      citizen, or the advert asks, and then without stating nationality.

**Sections and omissions**
- [ ] No references line, no notice period, no salary.
- [ ] Interests appear only if directly relevant.
- [ ] Education: qualification, institution and dates, newest first; no
      school grades for an experienced candidate.
- [ ] Selected publications only for an R&D or science role; otherwise
      none.
- [ ] Certifications come from `inventory/education.yaml`'s
      `certifications:` list, with expired ones left out.

**Delivery**
- [ ] The delivery message gives the submission file name
      (`Firstname-Lastname-CV-Company-Role-Title`), and a .docx copy is
      provided if the advert asks for one.
