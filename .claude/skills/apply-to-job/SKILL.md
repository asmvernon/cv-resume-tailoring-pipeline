---
name: apply-to-job
description: Orchestrates the manual, one-JD-at-a-time path from "I found a job, tailor me a resume/CV for it" through to a finished draft — sequencing extract-jd-signal, gap resolution, and tailor-resume-usa/tailor-resume-uk-contract, and enforcing the checkpoints (the extract-jd-signal gate, source-quality routing for gap resolution, conflict flagging, branch hygiene) that are easy to skip when those skills are run separately. Use whenever the user wants to go from a job description to a tailored resume/CV end to end, not just for one step of that path. Doesn't replace the underlying skills, and doesn't discover postings — this is the human-in-the-loop path for one posting the user already has in hand.
---

# Apply to a job

The repeatable checklist for "I have a JD, walk me through getting a tailored
draft out the other end" — distilled from running this by hand. It sequences
three existing skills and adds the judgment calls that tend to get skipped
when they're invoked independently: whether extract-jd-signal has actually
run yet, how to resolve a gap depending on what kind of evidence shows up for
it, what to do when two sources disagree, and which branch a given piece of
work belongs on.

It doesn't discover or score postings; it's the manual path for a posting
the user already has a link or text for.

## Steps

### 1. Get and save the JD

Accept a URL, a file, or pasted text. If fetching a URL directly fails (bot
protection is common on job boards — expect 403s), fall back to a browser
tool before giving up. Save it to `job_descriptions/` — this is
`extract-jd-signal`'s own step 1, don't duplicate the logic, just make sure
it happens before anything else runs.

### 2. Pick the market/track

Ask which resume variant this JD needs, unless it's obvious from the
content:
- **US resume** → `tailor-resume-usa`
- **UK contract CV** → `tailor-resume-uk-contract` (signals: day-rate
  language, "Inside/Outside IR35", an agency/contract-length framing)

### 3. Gate: has extract-jd-signal run on this JD yet?

If not, **ask** whether to run it first — never assume. This is where real
gaps get surfaced before drafting, not discovered mid-draft or missed
entirely.

### 4. Run extract-jd-signal, then resolve what it finds

For each new-skill-candidate or actionable gap it surfaces, the resolution
path depends on what kind of evidence is available — don't treat every gap
the same way:

- **A quick recollection from the user** ("I've used X, didn't implement
  it") → add directly to `skills.yaml`/the role bullet, with a note
  capturing whatever caveat/scope they gave. Fast, low-ceremony.
- **A rich or structured source becomes available** (a pasted analysis, an
  old CV, a document, a poster, a colleague's write-up) → route it through
  `seed-inventory-from-source` instead of hand-editing. That skill enforces
  the bullet formula and evidence-strength rigor that ad hoc edits tend to
  skip, and it's worth the extra step whenever the source itself has real
  precision to preserve.
- **Before using any source to close a gap, check honestly whether it
  actually supports the specific claim the JD is asking about** — a
  related-sounding skill is not the same claim (general image-data
  experience is not clinical/DICOM imaging experience). Say so plainly if
  it doesn't close the gap, and track the gap as genuine
  (`dev_opportunities_tracker.yaml`) rather than stretching the source to
  fit.
- **If two sources disagree about the same skill, flag both** — see
  `inventory/schema.md`'s Conflicting evidence rule. Record the
  disagreement in the evidence `note` and add an open item to
  `docs/tasks.md`. Never silently prefer one source over the other.
- **Never write an internal ticket ID or PR number into the inventory** —
  see `inventory/schema.md`'s Provenance sanitization rule. Describe the
  substance in plain language and flag that the reference was omitted.

### 5. Branch hygiene while resolving gaps

If gap resolution amounts to a real inventory-content change (more than a
one-line caveat), give it its own branch/worktree per `CLAUDE.md`'s Working
conventions — don't pile it onto a skill-development branch, or mix it with
another JD's application work. If it depends on content from another
still-open branch (e.g. an inventory update from a different JD review),
branch from that branch and note the dependency in the PR description
rather than duplicating the work.

### 6. Draft the resume/CV

Once extract-jd-signal's findings are all resolved (no open questions
blocking a draft — declined gaps and flagged conflicts are fine, a genuinely
unanswered question isn't), run `tailor-resume-usa` or
`tailor-resume-uk-contract` per the track chosen in step 2, on its own
branch/worktree (the "JD application work" category from `CLAUDE.md`).

### 7. Summarize

State what's done and what's still open — a flagged conflict, a declined
gap, a pending user follow-up — so nothing silently drops between sessions.

## Hard rules

- Never skip the extract-jd-signal gate (step 3) silently — always ask.
- Never let convenience decide the source-routing call in step 4 — the
  richness/structure of the source decides it, not how much friction
  `seed-inventory-from-source` adds.
- Never merge gap-resolution work and tailoring-output work onto the same
  branch as each other, or onto a skill-development branch.
