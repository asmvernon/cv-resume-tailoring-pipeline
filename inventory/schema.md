# Inventory schema

Two kinds of files, kept separate so skills can read them independently:

## `inventory/roles/<role-slug>.yaml` — one per job/role

```yaml
id: role-slug                    # stable slug, e.g. acme-senior-engineer-2022
company: Acme Corp
title: Senior Software Engineer
start_date: "2022-01"            # YYYY-MM, or YYYY if the source gives only the year (see Dates)
end_date: "present"              # YYYY-MM, YYYY or "present"
location: Bristol, UK
concurrent_with: [acme-tech-lead-2023]   # optional — same-company roles this one overlaps in time
title_history:                   # optional — title changes inside this role's date range
  - title: "Squad Lead"
    start_date: "2022-06"
    end_date: "2022-12"
  - title: "Lead Engineer"
    start_date: "2023-01"
    end_date: "2023-12"
summary: >
  One or two sentence narrative of the role/scope.
bullets:
  - text: >
      Led the migration of X to Y, reducing Z by 30% across N services.
    skills: [distributed-systems, kubernetes, technical-leadership]
    source: original                # original | inferred
    evidence_strength: strong        # strong | moderate | weak
    # strong  = has a real metric/outcome the user can back up
    # moderate = true but qualitative, no hard number. A scope figure alone
    #            (team size, site size, volume) doesn't make a bullet strong;
    #            see "Scope figures and outcome metrics"
    # weak    = plausible phrasing drafted from a JD, NOT YET CONFIRMED
    evidence_strength_rationale: >   # required — why THIS bullet earned that rating
      Has a real quantified outcome (30% reduction across N services) the
      user stated directly.
    usage_note: >                    # optional — true and valuable, but flagged
      Best suited for interview conversation, not a public resume bullet.
tags: [backend, leadership, fintech]
notes: >                             # optional — role-level caveats/TODOs
  Free-text flags that don't fit elsewhere: confidentiality caveats before
  external use, unresolved date/title ambiguity, provenance of a bulk edit.
```

### Personal projects (optional)

A project that isn't employment, such as a side project, an open-source
tool or a portfolio piece, is optional. It goes in its own file under
`roles/`, with the same shape as a role plus these optional keys:

```yaml
id: budget-tracker-project
kind: personal_project           # marks it as a project, not a job
company: "Personal project"
title: "Budget Tracker"
url: "example.com/budget"        # the public link
repo_url: "github.com/you/budget-tracker"   # optional — a more specific key when there are several links
stack: [Python, Flask, PostgreSQL]          # the technologies used
tagline: >                       # optional — the line shown under the heading
  A household budgeting web app, designed, built and run solo.
```

A link that isn't live yet is `"TODO"`, and tailoring leaves it out rather
than inventing one. Tailoring puts projects in a "Projects" section after
Experience, never inside it. When a project file holds several alternative
bullets, each one's `usage_note` says which job descriptions it suits and
which bullets it replaces, so tailoring picks one consistent set instead of
stacking overlapping variants.

## `inventory/skills.yaml` — flat taxonomy, single file

```yaml
skills:
  - id: distributed-systems
    name: Distributed Systems
    category: technical            # technical | domain | leadership | tool | methodology | language
    aliases: ["distributed computing"]
    confidence: confirmed          # confirmed | candidate
    source_type: cv                # cv | jd_inferred
    evidence:
      - role: acme-senior-engineer-2022
        note: "migration bullet"
      - source: "cv-skills-section:programming"
        note: "Also self-declared in the CV's Skills list"
    first_seen_jd: job_descriptions/2026-09-08-acme-staff-eng.md   # only when source_type: jd_inferred
```

## `inventory/interview_stories.yaml` — flat list, same shape as `skills.yaml`

```yaml
interview_stories:
  - id: acme-outage-recovery
    title: "Recovering a failed nightly data load"
    star:
      situation: >
        One or two sentences of context — when/where, what was at stake.
      task: >
        YOUR specific responsibility in that situation, not the team's
        general goal.
      action: >
        The specific steps YOU took. This is the part interviewers probe
        hardest — be concrete. Use "I", even for team efforts; name your
        individual contribution honestly without erasing the team's.
      result: >
        The outcome, quantified wherever the underlying evidence supports
        it, plus what was learned or changed afterward.
    skills: [problem-solving, critical-thinking, technical-leadership]   # inventory/skills.yaml ids this story demonstrates
    competencies: ["ownership under pressure", "incident response"]      # freeform behavioral-question tags — how interviewers actually phrase "tell me about a time..."
    confidence: confirmed            # confirmed | candidate — same meaning as skills.yaml
    source_type: cv                  # cv | jd_inferred
    evidence:
      - role: acme-senior-engineer-2022
        note: "Bullet tagged usage_note: interview-story only."
    notes: >                         # optional — incomplete-STAR TODOs, confidentiality caveats
      TODO (confirm with user): Action and Result need real specifics —
      currently placeholders, not yet filled from confirmed detail.
```

- Same evidence shape and rules as `skills.yaml` (below) — every story needs
  at least one `evidence` item, tracing to the role bullet(s) it's grounded
  in.
- `skills` cross-references real `inventory/skills.yaml` ids (what
  technical/professional skill this demonstrates) — `competencies` is a
  separate, freeform list for the *behavioral* framing interviewers actually
  use ("tell me about a time you...", "describe a conflict...", "tell me
  about a failure..."). A story usually needs both: `skills` for JD-keyword
  matching, `competencies` for picking the right story for the question
  being asked.
- **All four STAR fields are required, non-empty** — `scripts/validate_inventory.py`
  checks this structurally (they exist and aren't blank), but only a human
  can judge whether they're honest and specific. If real Action/Result
  detail isn't available yet, write an explicit placeholder (e.g. "TODO:
  needs the actual recovery steps and timeline from the user") rather than
  inventing specifics to fill the field — same rule as everywhere else in
  this inventory: never fabricate to complete a shape.
- **Never invent Action or Result detail.** A story usually starts from a
  role bullet tagged `usage_note: <something suited for interview, not
  resume>` — that note is real, but usually one sentence, nowhere near
  enough for an honest STAR breakdown. Situation/Task can often be
  reasonably paraphrased from what's already confirmed; Action and Result
  almost always need to be asked for directly.

## `inventory/dev_opportunities_tracker.yaml` — flat list, genuine gaps only

```yaml
dev_opportunities:
  - id: kubernetes-production-ops        # stable slug, same style as skills.yaml ids
    area: "Kubernetes (production operations)"   # human-readable label
    category: technical                  # technical | domain | leadership | tool | methodology | credential
    status: open                         # open | closed | declined
    related_skill_id: kubernetes         # optional — set once/if this becomes a skills.yaml id
    seen_in:
      - jd: job_descriptions/2026-09-08-acme-staff-eng.md
        note: "Required: 3+ years production Kubernetes operations"
        date: "2026-09-15"
    times_seen: 1
    date_added: "2026-09-15"
    date_updated: "2026-09-15"
    resolution_note: >                   # required once status != open
      Why the status changed — e.g. "User completed hands-on Kubernetes work
      at Acme, now tracked as confirmed skill `kubernetes`" or "Declined —
      not a direction the user wants to pursue."
```

- Written and maintained exclusively by `extract-jd-signal`, step 7. Never a
  place for `seed-inventory-from-source` or `tailor-resume-usa` to write.
- **Only genuine gaps go here** — something the JD required/preferred that,
  after the mandatory gap walkthrough, the user confirmed they don't
  actually have. If the user says they *do* have the experience, it's added
  to the inventory as normal (`confirmed`/`strong` per the usual rules) and
  never written here — this file is not a duplicate of `skills.yaml`.
- **Reconciling against an existing tracker entry:** match on `id` (exact)
  or case-insensitive against `area`. If it matches and the JD is a new
  source not already in `seen_in`, append a `seen_in` item, bump
  `times_seen`, and update `date_updated` — do not create a second entry
  for the same gap. Every entry's `seen_in` list must contain at least one
  item, same rule as `skills.yaml`'s `evidence`.
- **`status` transitions require the user's explicit say-so in that
  conversation**, same spirit as the `confidence`/`evidence_strength`
  rules above:
  - `open` → `closed`: the user has since gained real experience/confirmed
    a matching skill. Set `related_skill_id` to the now-confirmed
    `skills.yaml` id and write a `resolution_note` explaining it.
  - `open` → `declined`: the user explicitly says they don't want to
    pursue this — stops it from being re-raised as "actionable" on future
    runs (it can still be noted as "previously declined" if it recurs, but
    shouldn't prompt another walkthrough). Requires a `resolution_note`.
  - Never flip a status without the user saying so in-conversation, same
    as `candidate` → `confirmed` elsewhere in this schema.
- Not validated as strictly as `skills.yaml`/roles — but
  `scripts/validate_inventory.py` does check: no duplicate ids, `status` is
  one of the allowed values, `resolution_note` is non-empty whenever
  `status != open`, `related_skill_id` (if set) exists in `skills.yaml`,
  and no entry has an empty `seen_in` list.

## Additional top-level files

- `inventory/profile.yaml` — name, contact details, professional summary, languages.
  Needed verbatim by the tailoring skills' resume output; not skill/role data.
- `inventory/education.yaml` — degrees/institutions/dates/honors, plus an optional
  `certifications:` list. Kept separate from `roles/` since it's credentials, not
  experience bullets. Each certification:

  ```yaml
  certifications:
    - id: osha-10-general-industry
      name: OSHA 10-Hour General Industry
      issuer: OSHA Outreach Training Program   # optional
      date: "2019"                              # optional; YYYY-MM or YYYY
      expires: "2027-06"                        # optional; omit if it doesn't expire
      source_type: cv
  ```

  Only what the user's own CV or words attest. A job description asking for a
  certification is a gap for `dev_opportunities_tracker.yaml`, never an entry
  here.

  It also has an optional `publications:` list, for papers and pre-prints:

  ```yaml
  publications:
    - id: soil-sensor-network-2021
      citation: 'Doe, J., Smith, A. (2021). A low-cost soil moisture sensor network. Journal of Example Studies, 12(3).'
      url: "https://doi.org/10.0000/example.2021.001"
      related_role: acme-research-assistant-2020   # optional; omit for a standalone publication
      notes: >                             # optional
        Context, e.g. why it isn't tied to a role.
  ```

  Citations keep the author names exactly as published, even if the user's
  name has changed since. A role bullet may also cite a publication when the
  work belongs to that role.

Both carry a `seeded_from` field recording provenance (e.g. which CV/date), the
same way role/skill entries trace back to a JD.

## `source` field

Every role, bullet, and skill also carries `source_type: cv | jd_inferred`:
- `cv` — taken directly from the user's own CV or their direct statements. Always
  `confidence: confirmed` / `evidence_strength: strong|moderate` (never `weak`).
- `jd_inferred` — proposed by `extract-jd-signal` from a job description's language.
  Starts as `confidence: candidate` / `evidence_strength: weak` per the rules below.

`skills.yaml` entries also allow `category: language` (spoken languages), alongside
`technical | domain | leadership | tool | methodology`.

## Evidence rules (important)

- **Every skill entry's `evidence` list must contain at least one item. Never write
  `evidence: []`.** An unevidenced skill is a claim with nothing backing it — either
  find the backing or don't add the skill.
- Each evidence item is exactly one of:
  - `{role: <role-slug>, note?: <string>}` — the skill is demonstrated in that role's
    bullets.
  - `{source: <string>, note?: <string>}` — no specific role bullet cites it, but it's
    attested elsewhere. `source` must name the actual place it came from (e.g.
    `"cv-skills-section:programming"`, `"job_descriptions/2026-09-08-acme.md"`,
    `"user-conversation-2026-09-08"`) — never a vague placeholder.
- **Reconciling against an existing skill (from a CV, a JD, or conversation):** match
  on `id` (exact) or case-insensitive against `name`/`aliases` first. If it matches,
  **append** a new evidence item to that entry's existing `evidence` list — do not
  create a second `skills.yaml` entry for the same skill. Before appending, check the
  new item isn't already present (same `role`, or same `source` + `note`) to avoid
  evidence duplicates.
- This same rule applies to `inventory/roles/*.yaml` bullets: don't add a bullet that
  duplicates an existing one for the same role — extend/edit the existing bullet's
  `skills` list instead.
- **The link between a bullet's `skills:` tags and a skill's `evidence` must never
  drift apart.** If a bullet tags `skills: [foo]`, then `foo`'s entry in
  `skills.yaml` must have a `{role: <that role>}` evidence item — always, both
  directions. This is easy to break silently (editing a bullet's `skills:` list
  without also touching `skills.yaml`, or vice versa). Run
  `python3 scripts/validate_inventory.py` after touching either file; both
  `extract-jd-signal` and `seed-inventory-from-source` run it as a required last
  step before any commit.

## Evidence strength rationale (required on every bullet)

- **Every bullet must carry a non-empty `evidence_strength_rationale`** — one
  short sentence stating *why* this specific bullet earned its
  `evidence_strength` rating, not a restatement of the bullet itself.
  Examples: `"Quantified outcome (58% drop) the user stated directly."` /
  `"True but qualitative — no hard number given."` / `"Plausible phrasing
  drafted from the JD, not yet confirmed by the user."`
- Fill it whenever a bullet is created, and update it whenever
  `evidence_strength` changes — the rationale should always justify the
  *current* rating, never a stale one from an earlier edit.
- This exists so a strength rating is a checkable claim, not just an
  assertion — it's what makes a review of every entry's strength actually
  auditable instead of requiring re-deriving the reasoning from scratch. `scripts/validate_inventory.py`
  checks this field is present on every bullet; both `extract-jd-signal` and
  `seed-inventory-from-source` are required to fill it on every bullet they
  create or edit.

## Confidence rules (important)

- Anything the `extract-jd-signal` skill proposes goes in as `confidence: candidate`
  (skills) / `evidence_strength: weak` + a clear TODO marker (role bullets).
- Nothing moves to `confirmed` / `strong` except by the user's explicit confirmation.
- This keeps the inventory honest: it should always be possible to tell "things I've
  verified are true" apart from "things a JD's language suggested I might be able to
  claim."

## Provenance sanitization (important)

- **Never write an internal ticket ID, PR number, or other work-environment-only
  identifier into a bullet or an evidence `note`** (e.g. a Jira key like
  `DATA-1234`, a PR reference like `PR #4567`). These are meaningless — and
  potentially identifying of a current employer's internal systems — outside
  the environment they came from, unlike a public artifact (a DOI, a GitHub
  repo, a named publication) which stays independently verifiable.
- Describe what happened in plain language instead, and add a short note that
  the internal reference was omitted and can be pulled again if it would be
  useful context later. For example: `note: "Led the queue migration
  (internal ticket reference omitted; ask the user if it's needed)."`

## Conflicting evidence (important)

- **When two sources disagree about the same skill or claim, flag both —
  never silently prefer one.** E.g. the user's own quick recollection said
  one thing about a skill; a deeper source (a colleague-reviewed session, a
  more careful CV re-read) said another. Record the disagreement directly in
  the affected evidence `note` (what each source says, and that it's
  unresolved) and add an open item to `docs/tasks.md` so it doesn't get lost
  — don't guess which is more accurate.
- Resolve it only once the user explicitly says which is accurate — same
  standard as any other `confidence`/`evidence_strength` change.

## Dates

- Role, `title_history` and certification dates are `YYYY-MM`. When the
  source gives only the year ("promoted in 2019"), write the year alone
  (`"2019"`) rather than guessing a month, and ask the user for the month if
  it matters. Résumés then show that date as the year alone.
- `scripts/validate_inventory.py` treats a year-only date as anywhere in
  that year: it flags a same-company overlap only when the dates must
  overlap, so a promotion "in 2019" splits into two role files without a
  false alarm.

## Scope figures and outcome metrics

Numbers in a bullet are one of two kinds:

- **Scope figures** describe the job: team size, site size, order volume,
  budget, number of clients. The user stated them as facts about the role,
  so they can appear on a résumé from any confirmed bullet (`strong` or
  `moderate`), but on their own they don't make a bullet `strong`.
- **Outcome metrics** claim a result: an improvement, a percentage, a
  before/after, money saved. They're what `strong` means, and they appear on
  a résumé only from a `strong` bullet.

Say which kind a bullet's numbers are in its `evidence_strength_rationale`
when it isn't obvious (e.g. "Scope figures only (30 associates, 400,000 sq
ft); no outcome stated").

## Concurrent roles and title changes

Two role files at the same company may legitimately overlap in time: extra
scope taken on while still holding the earlier title (Squad Lead from Apr 2021
while titled Senior Data Scientist until Dec 2021), an acting role layered on
an ongoing individual-contributor role (Acting Engineering Manager), or
teaching alongside a PhD. Declare it rather than leaving it to be rediscovered:

- `concurrent_with` lists the other role ids at the same company whose dates
  overlap this one. One side is enough. `scripts/validate_inventory.py`
  rejects any same-company overlap that isn't declared, so a real date error
  can't hide behind a legitimate one.
- `title_history` (optional) records title changes inside a single role
  file's range, so tailoring can show dates that don't overlap (for example
  "Lead Data Scientist, Jan 2022 – Jun 2023 (Squad Lead from Apr 2021)")
  without guessing.
- On resumes/CVs, never show concurrent roles as raw overlapping date ranges,
  because screeners read that as an error. Use one company block with a title
  progression, or the `title_history` dates.
