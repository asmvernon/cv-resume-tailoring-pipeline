# CV principles (UK contract market)

Reference for `tailor-resume-uk-contract`. This is the checklist the skill
drafts against and self-checks the final output against — not general
advice, a working spec.

This covers the UK **contract/day-rate market** specifically (agency-placed
IT/consulting engagements, inside/outside IR35) — not a UK permanent-role
CV and not a US resume (see `tailor-resume-usa`'s
`reference/resume-principles.md` for that). The contract market has its own
conventions that a permanent-role UK CV wouldn't use: engagement-based
structure, a prominent skills/tech summary near the top, longer accepted
length, and explicit availability/IR35 framing — driven by how agencies and
clients actually screen contractor CVs (fast keyword scan, then a quick
human read), which is a different filter than either a corporate ATS or a
permanent-hire recruiter.

## Format & structure

- **Reverse-chronological by engagement/contract**, not by employer — a
  contractor CV is a list of engagements (each with its own client, dates,
  role, and tech stack), not a list of employers.
- **Length**: 2–4 pages is normal and expected, unlike the 1-page norm for a
  US resume or early-career UK permanent CV. Agencies and clients expect
  full project history to assess relevant experience; don't compress a
  real contracting history to look like a permanent CV. Still cut for
  relevance, not padding — length is a byproduct of real engagement count,
  not a target.
- **No photo, date of birth, marital status, or nationality.** Same as any
  UK/US CV — omit.
- **Section order**: Contact → Professional Profile/Summary → Key Skills
  (summary) → Contract/Employment History (reverse-chronological, by
  engagement) → Education → (optional) Certifications if directly relevant
  (from `inventory/education.yaml`'s `certifications:` list; leave out
  expired ones).
- **A compact Key Skills summary (grouped list or simple table) near the
  top is standard and expected** in this market — unlike the stricter
  "no tables" ATS rule for a US corporate resume. Agencies scan CVs for
  keyword matches against a spec before a human reads further, and a
  skills summary is exactly what that scan looks for. Keep it a simple,
  parseable grouped list (e.g. "Cloud: AWS, Terraform, Kubernetes") rather
  than a complex graphic table, since some agency databases still run
  automated parsing on top of the manual review.
- **One font, minimal styling** — bold for client/role/dates, plain text
  otherwise. Simplicity still matters even though tables are acceptable
  here.
- **No "References available upon request."** Outdated, adds nothing.
- **No first-person pronouns** ("I", "my", "me").

## Contact block

- **Name (with credentials, e.g. ", PhD") on its own line, then a blank
  line, then the contact-details line** (phone, email, LinkedIn, location —
  town/region is enough, no need for a full address), **then another blank
  line, then the availability/right-to-work line** if included. Both blank
  lines are a formatting convention, not optional — keep them consistent
  across drafts. A UK contract CV assumes a UK location, so no relocation framing is
  needed here (contrast with `tailor-resume-usa`, where an out-of-market
  location needs an "open to relocation" note).
- Personal site/portfolio/GitHub only if substantive and current.

## Professional profile/summary

**Include, not optional** — unlike the US resume, where a summary is
optional. Agencies and clients expect a 3–5 line profile up top: years of
contracting/relevant experience, domain, key technologies, and (if the user
wants it here rather than left to the agency conversation) contract-type
preference such as remote/onsite and inside/outside IR35. Base it on the
inventory's actual profile summary, tailored per JD — not a generic
objective statement.

## Availability & contract logistics

These fields are **not** part of the inventory (they're application-
specific logistics, not experience) and must never be invented — always
confirm with the user per JD whether to include them at all, and use only
what they give you:

- **Availability / notice period** — e.g. "Available: immediately" or
  "Available: 4 weeks notice". Common and useful near the contact block or
  profile, since agencies filter on this early.
- **IR35 status preference** (inside/outside, or open to either) — worth
  stating explicitly if the user wants to signal it, since it's a real
  screening factor for UK contract roles post-April 2021 reform. Never
  assume a preference or a status; only state what the user confirms.
  - Day rate is normally negotiated with the agency directly rather than
  printed on the CV — default to leaving it off unless the user explicitly
  asks for it to be included.
- **Right to work in the UK** — the user already has it; a brief explicit
  statement is sometimes expected by agencies for fast vetting, but only
  include it if the user wants to state it (don't assume the phrasing).

## Contract/Employment History section

- Reverse-chronological, one block per engagement: **client name** (or an
  anonymized description like "Confidential FinTech client" if the
  inventory notes an NDA — never invent a client name or its absence),
  contract dates, role title/day-to-day.
- **Lead each engagement with a Tech Stack line** — e.g. "Technologies:
  Python, AWS, Terraform, Kubernetes" — this is a strong convention in this
  market and a primary thing agency keyword-matching looks for. Only list
  tech that's actually backed by the inventory's evidence for that
  engagement.
- **Every Tech Stack line uses commas only, across every engagement in the
  same draft** — no mixing in pipes, semicolons, or parenthetical
  sub-labels (e.g. "(standards)", "(ontologies/sources)") to group items
  within one line, even when the items are a natural mix of tools, sources,
  and standards. If the grouping feels worth preserving, that's a signal
  the line is trying to do too much — flatten it to one comma-separated
  list instead of inventing a second separator.
- 3–6 bullets for recent/relevant/longer engagements; 1–3 (or a one-line
  mention) for short/tangential ones. The page-length budget should still
  drive what's cut, even though the overall length ceiling is higher than
  a US resume's.
- **Bullet formula**: action verb + what you did + method/technology +
  outcome — same formula as the US resume (see `tailor-resume-usa`'s
  reference doc), so inventory content already fits both.
- **Quantify wherever `evidence_strength: strong` supports it.** Never
  invent a number to fill out a `moderate`/`weak` bullet. Scope figures the
  user stated (team size, site size, volume) are fine from any confirmed
  bullet; outcome metrics need `strong` (see `inventory/schema.md`'s *Scope
  figures and outcome metrics*). A role date recorded as a year alone shows
  as the year alone; never add a month.
- **Consistent tense**: past tense for completed engagements; for a
  genuinely current/ongoing engagement, past tense for completed work and
  present tense for ongoing responsibilities is fine — pick one convention
  per engagement and hold it.
- **Strong, varied action verbs** (Led, Designed, Built, Shipped, Reduced,
  Scaled, Delivered...) — avoid weak openers like "Responsible for" or
  "Helped with".

### Concurrent roles and title changes

Roles at the same company can overlap in time (see `inventory/schema.md`,
"Concurrent roles and title changes"). Raw overlapping ranges read as an
error to an agency or client screener, so:

- When roles are linked by `concurrent_with`, or a role has a
  `title_history`, **never print overlapping date ranges**.
- **Default (UK contract):** one engagement block for the company, with the
  whole span and a title-progression line. E.g. "**Acme Analytics** — Bristol,
  UK | Mar 2018 – Jun 2023" then "**Data Engineer → Senior Data
  Engineer → Squad Lead / Lead Data Engineer**".
- If per-title dates genuinely help the reader, take them from
  `title_history` so they don't overlap (e.g. "Lead Data Engineer, Jan
  2022 – Jun 2023 (Squad Lead from Apr 2021)").
- **An acting or extra role held on top of an ongoing one** (e.g. Acting
  Engineering Manager alongside Senior Software Engineer at the same company) sits under
  the same company block, marked "(concurrent)". It is never shown as a
  separate job.
- Every date shown must come from the role's `start_date`/`end_date` or a
  `title_history` entry. Never invent a transition month to make ranges
  tidy. If the inventory has an overlap with no `concurrent_with` link,
  that's a data problem: flag it to the user rather than picking dates.

## Key Skills summary

- Pull only `confidence: confirmed` skills from the inventory — never
  `candidate`.
- Group by category (e.g. Languages, Cloud/Infra, Tools) and order by
  relevance to *this* JD — lead with what the JD/spec asks for.
- Match the JD's exact terminology when the inventory's `aliases` already
  cover it (e.g. "K8s" vs "Kubernetes") — use whichever the JD says, since
  both are true.

## Keyword alignment for agency/client screening

- Mirror the spec's exact phrasing for required skills/technologies **both
  in the Key Skills summary and in context inside real bullets** — this
  market's screening is more keyword-driven up front (agency search, then
  client skim) than a US ATS, so the Key Skills summary carries more
  weight here than it would on a US resume, but it still shouldn't be
  stuffed with anything not backed by real inventory evidence.
- Every keyword used must be backed by real inventory evidence. If the JD
  wants something the inventory doesn't support, that's
  `extract-jd-signal`'s gap-review job, not something to paper over here.
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

- Tailoring is as much subtraction as rewording. Cut engagements/bullets
  that don't serve this specific JD, especially padding from short or
  tangential engagements, when space is tight — even with the higher page
  budget, an unfocused CV still reads worse than a tight one.
- Never omit something *because it's unflattering* if it's still the most
  relevant experience for the role — omission is about relevance, not spin.

## Self-check before finalizing

- [ ] Every bullet is either verbatim from the inventory or an
      explicitly-approved reword — nothing from `candidate`/`weak`/
      unconfirmed content.
- [ ] Structured by engagement, reverse-chronological, each with a Tech
      Stack line — every one of them comma-separated only, no pipes/
      semicolons/parenthetical sub-labels mixed in, and no inconsistency
      between engagements in the same draft.
- [ ] Key Skills summary present, grouped, and ordered for this JD.
- [ ] Length is proportionate to real engagement count (2–4 pages typical)
      — not padded, not artificially compressed to 1 page.
- [ ] Tense is consistent within each engagement block.
- [ ] No two date ranges on the page overlap unless one is explicitly
      marked concurrent, and every date shown traces to the role file's
      dates or its `title_history`.
- [ ] No first-person pronouns, no "references available" line, no
      photo/personal demographic info.
- [ ] Any availability/IR35/right-to-work statements included were
      explicitly confirmed by the user, never assumed.
- [ ] Required JD keywords: report which are covered and which are
      genuinely missing — don't force-fit a missing one.
- [ ] Every outcome metric (an improvement, a result, a percentage) traces
      to a `strong`-evidence bullet in the inventory; scope figures (team
      size, site size, volume) trace to any confirmed bullet. See
      `inventory/schema.md`'s *Scope figures and outcome metrics*.
