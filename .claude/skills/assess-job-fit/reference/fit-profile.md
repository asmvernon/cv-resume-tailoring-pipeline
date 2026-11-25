# Fit profile: format and defaults

`inventory/fit_profile.yaml` says what the user wants from their next job,
so `assess-job-fit` scores postings the way *they* would. It lives under
`inventory/` because it's personal (target pay, work authorisation,
companies they'd avoid), so it stays in the user's private copy and never
ships with the public pipeline. Every field is optional; anything missing
falls back to the defaults below. Check it with
`python3 scripts/check_fit_profile.py`.

An invented example of a full file: `example-fit-profile.yaml`.

## Fields

```yaml
version: 1                      # format version of this file

rubric: docs/my_rubric.md       # optional: a fuller scoring document in the
                                # private copy; its anchors replace the defaults

weights:                        # must add up to 1
  experience: 0.5
  company: 0.25
  culture: 0.25

ratings:                        # highest first; the first whose min the total reaches
  - {min: 4.25, label: Strong}
  - {min: 3.5,  label: Good}
  - {min: 2.75, label: Partial}
  - {min: 0,    label: Weak}

levels:                         # how the level shapes the experience score
  best: [Data Engineering Manager, Lead Data Engineer]
  step_lower: [Senior Data Engineer]  # score one step below the same role at the right level
  stretch: [Head of Data]        # experience score capped at 4

locations:
  preferred: [Manchester hybrid]
  acceptable: [Remote (UK)]
  adjustments:                   # added to the total, each with a reason
    - {match: "London", delta: -0.5, why: "Would only commute to London twice a month"}
  notes: Not open to relocation.

work_authorisation:             # per country: has_right | needs_sponsorship | unknown
  UK: has_right
  EU: unknown

domains:
  preferred: [climate, energy]   # what lifts company focus to 4-5
  avoid: [gambling]              # a deal-breaker unless the user says otherwise

culture:
  look_for: [data treated as a core asset, design reviews and maintainability]
  warning_signs: ['"Move fast" with nothing about quality']
  source: docs/what_matters_to_me.md   # optional: the user's own notes
  notes: Prefers small teams.          # optional

compensation:                   # optional; never shown to employers
  currency: GBP
  floor: 70000                  # 0 or omitted: no floor

deal_breakers:                  # reported at the top whatever the score
  - Five days a week in the office

report:                         # free-form: how the user likes the report, and limits to check
  job_id: Read the requisition number from the live page every time.
  style: Ranked table first, then matches, gaps and questions.

notes: Anything else worth knowing when scoring.   # optional
```

## Default scoring (no profile, or no `rubric`)

Three dimensions, each an integer 1–5, weighted as above.

**Relevant experience.** Against the confirmed inventory only.

| Score | Anchor |
|---|---|
| 5 | Nearly every required qualification backed, the level fits, and the domain overlaps. |
| 4 | Most required qualifications backed; one real gap or a modest level stretch. |
| 3 | The core fits but several required items aren't backed, or the role is adjacent. |
| 2 | A different discipline at its core, or a hard requirement the inventory clearly lacks. |
| 1 | Little overlap. |

**Company focus.** How well the mission and domain fit `domains`.

| Score | Anchor |
|---|---|
| 5 | Squarely in a preferred domain, and the user's kind of work is central to the product. |
| 4 | In or next to a preferred domain, or a clearly positive mission with their work central. |
| 3 | A solid company with a neutral mission. |
| 2 | Their work is incidental to the company, or the employer is unnamed (agency). |
| 1 | In an `avoid` domain or against the user's values. |

**Cultural fit.** Against `culture`, from the posting's wording and the
employer's own pages, never anonymous reviews alone.

| Score | Anchor |
|---|---|
| 5 | Clear evidence for everything in `look_for`. |
| 4 | Clear evidence for some, nothing against the rest. |
| 3 | No real signal either way (the default). |
| 2 | One of the `warning_signs`. |
| 1 | Several warning signs. |

**Not scored, always reported:** location and days in office, salary
range against `compensation.floor`, sponsorship wording against
`work_authorisation`, closing date, and any `deal_breakers` hit.

## Changing the profile

Only the user changes it. When they say something general about what they
want, offer once to save it, show the YAML change, and write it only when
they agree. If the private copy also keeps a rubric document, change both
together so they don't drift.
