# Resume/CV principles (US market)

Reference for `tailor-resume-usa`. This is the checklist the skill drafts
against and self-checks the final output against — not general advice, a
working spec.

## Format & structure

- **Reverse-chronological**, always. Skip functional/skills-first formats —
  both ATS parsers and recruiters expect chronological for a corporate/tech
  search.
- **Length**: 1 page under ~7 years total experience; up to 2 pages for 7+
  years or leadership scope. Don't force a 2-page-worthy background onto 1
  page by cramming — cut content, don't shrink it.
- **No photo, date of birth, marital status, or nationality.** Standard on a
  UK CV, considered unusual (and can raise unconscious-bias/EEOC concerns for
  the employer) on a US resume — always omit.
- **Section order**: Contact → (optional) Professional Summary → Experience →
  Skills → Education → (optional) Publications/Awards if directly relevant to
  the role.
- **Standard section headers only** ("Experience", "Education", "Skills") —
  no creative headers; ATS parsers pattern-match on these.
- **Single column. No tables, text boxes, images, icons, or graphics. No
  headers/footers holding contact info.** Any of these can silently break ATS
  parsing or get the content dropped entirely.
- **One font, minimal styling** — bold for titles/companies, plain text
  otherwise.
- **No "References available upon request."** Outdated, adds nothing.
- **No first-person pronouns** ("I", "my", "me").

## Contact block

- Name, phone, email, LinkedIn, location. For an out-of-market candidate
  (e.g. UK-based applying to a US on-site role), use the real location plus
  "open to relocation" — never fabricate a US address.
- Personal site/portfolio/GitHub only if substantive and current.

## Professional summary (optional)

Worth including for career changers, senior/leadership roles, or a domain
pivot. 2–3 lines, tailored per JD using the inventory's actual profile
summary as the base — not a generic objective statement. Should read as "why
this specific role", using language that's honestly true of the candidate.

## Experience section

- Reverse-chronological, one block per role (company, title, dates,
  location).
- 3–6 bullets for recent/relevant roles; 1–3 (or omit entirely) for
  older/less relevant ones. The page-length budget should drive what's cut,
  not what's kept.
- **Bullet formula**: action verb + what you did + method/technology +
  outcome. E.g. "Led the redesign of the central ETL framework, enabling
  non-engineers to add pipeline logic across the org."
- **Quantify wherever `evidence_strength: strong` supports it.** Never invent
  a number to fill out a `moderate`/`weak` bullet — that's fabrication, not
  tailoring.
- **Consistent tense** within each role block: past tense for past roles;
  for a current/ongoing role, past tense for completed work and present
  tense for genuinely ongoing responsibilities is fine, but pick one
  convention per role and hold it.
- **Strong, varied action verbs** (Led, Designed, Built, Shipped, Reduced,
  Scaled, Mentored, Drove...) — avoid weak openers like "Responsible for" or
  "Helped with".

### Concurrent roles and title changes

Roles at the same company can overlap in time (see `inventory/schema.md`,
"Concurrent roles and title changes"). Raw overlapping ranges read as an
error to a screener, so:

- When roles are linked by `concurrent_with`, or a role has a
  `title_history`, **never print overlapping date ranges**.
- **Default (US):** one company line, then each title with non-overlapping
  dates from `title_history`, noting when the concurrent scope started.
  E.g. "**Lead Data Engineer** *(Squad Lead from Apr 2021)* | Jan 2022 –
  Jun 2023" above "**Senior Data Engineer** | Jan 2020 – Dec 2021".
- A single title-progression block (e.g. "Data Engineer → Senior
  Data Engineer → Lead Data Engineer, Mar 2018 – Jun 2023") is also fine
  when per-title bullets aren't needed.
- **An acting or extra role held on top of an ongoing one** (e.g. Acting
  Engineering Manager alongside Senior Software Engineer at the same company) sits under
  the same company block, marked "(concurrent)". It is never shown as a
  separate job.
- Every date shown must come from the role's `start_date`/`end_date` or a
  `title_history` entry. Never invent a transition month to make ranges
  tidy. If the inventory has an overlap with no `concurrent_with` link,
  that's a data problem: flag it to the user rather than picking dates.

## Skills section

- Pull only `confidence: confirmed` skills from the inventory — never
  `candidate`.
- Group and order by relevance to *this* JD. Lead with what the JD asks for
  — don't dump the full inventory taxonomy.
- Match the JD's exact terminology when the inventory's `aliases` already
  cover it (e.g. "K8s" vs "Kubernetes") — use whichever the JD says, since
  both are true.

## ATS & keyword alignment

- Mirror the JD's exact phrasing for required skills/qualifications **in
  context, inside real bullets** — not crammed into a keyword list at the
  bottom. Keyword stuffing reads as spam to ATS and humans alike, and modern
  ATS is increasingly good at flagging it.
- Every keyword used must be backed by real inventory evidence. If the JD
  wants something the inventory doesn't support, that's `extract-jd-signal`'s
  gap-review job, not something to paper over here.
- **Rewording a bullet to mirror JD language changes the actual words the
  user is claiming as their own.** It's allowed and often valuable, but
  every reworded bullet must be shown to the user as an explicit
  before/after and approved before it goes in the draft. Bullet
  *selection* (which ones, what order) doesn't need that same per-line
  sign-off — but the full draft is always presented before being written to
  disk.
- A reword must never increase the implied strength of a claim beyond its
  `evidence_strength` — turning a `moderate` bullet into something that
  reads like a headline `strong` achievement is inflation, not tailoring.

## What to omit

- Tailoring is as much subtraction as rewording. Cut roles/bullets that
  don't serve this specific JD, especially padding from early-career or
  tangential roles, when space is tight.
- Never omit something *because it's unflattering* if it's still the most
  relevant experience for the role — omission is about relevance, not spin.

## Self-check before finalizing

- [ ] Every bullet is either verbatim from the inventory or an
      explicitly-approved reword — nothing from `candidate`/`weak`/
      unconfirmed content.
- [ ] Length fits the 1–2 page budget for the seniority level.
- [ ] Tense is consistent within each role block.
- [ ] No two date ranges on the page overlap unless one is explicitly
      marked concurrent, and every date shown traces to the role file's
      dates or its `title_history`.
- [ ] No first-person pronouns, no "references available" line, no
      photo/personal demographic info.
- [ ] Required JD keywords: report which are covered and which are
      genuinely missing — don't force-fit a missing one.
- [ ] Every number/metric traces to a `strong`-evidence bullet in the
      inventory.
