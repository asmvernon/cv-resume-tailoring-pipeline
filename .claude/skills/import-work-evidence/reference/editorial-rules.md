# Editorial rules: format and how each kind is applied

`inventory/editorial_rules.yaml` holds the user's standing rules and
corrections: the things they've told the assistant once and shouldn't have
to say again. It lives under `inventory/` because the rules are personal
(they name employers, teams and projects), so it stays in the user's
private copy and never ships with the public pipeline.

Every skill that writes the user's words (the inventory skills, the
tailoring skills and `write-cover-letter`) reads this file when it exists
and applies it. `scripts/check_editorial_rules.py` checks the rules that
can be matched by text.

An invented example of a full file: `example-editorial-rules.yaml`.

## Fields

```yaml
rules:
  - id: no-internal-team-codes     # required: lowercase-hyphenated, unique
    kind: term                     # required: term | style | exclude | conditional | fact | precedence | process
    rule: >                        # required: the rule in plain language
      Never use the internal squad codes. Describe the team by what it does.
    find: ["Squad 7"]              # optional: literal text, case-insensitive, whole words
    find_regex: []                 # optional: Python regexes (case-sensitive unless (?i))
    replace: "payments platform team"   # optional: the approved replacement for every `find`
    where: [inventory, resume, cover_letter]   # optional: default all three; also `stories`
    fields: [any]                  # optional: any | title | summary | bullets
    roles: [some-role-id]          # optional: only these role files
    why: >                         # optional: why the user wants it
      ...
    added: "2026-01-15"            # optional: when the user gave the rule
    from: "conversation, 2026-01-15"   # optional: where the user said it
```

`conditional` rules also carry `when`: the condition, in plain language,
under which the content they cover may be used.

`precedence` rules also carry `source` (which kind of source the rule is
about) and `outcome`: `inventory_wins` or `flag`.

`where` names the outputs a rule covers. `inventory` is the role files
(`title`, `summary`, `bullets`), `stories` is `inventory/interview_stories.yaml`,
`resume` is any `resumes/<slug>/resume.md` and `cover_letter` any
`resumes/<slug>/cover_letter.md`. Interview stories are left out by default
because they're the user's own prep notes, where internal names can help.

## The kinds

| Kind | What it says | How it's applied |
|---|---|---|
| `term` | A word or name that must never appear, usually with a replacement | Checked by script. A `replace` is the user's standing approval for that exact substitution; anything more is a normal before/after reword. With no `replace`, propose wording each time |
| `style` | A rule about form (no first person in bullets, "present" for active roles) | Checked by script when it has a `find`/`find_regex`; otherwise read and applied |
| `exclude` | A true claim the user wants kept out (a stalled proposal, an unmeasured projection) | Don't import or draft anything that makes the claim, and say what was left out. A `find` lets the script catch it |
| `conditional` | Content that is in the inventory but goes on a résumé or cover letter only when `when` holds (e.g. a volunteer role only when the job description mentions community work) | Tailoring skills check `when` against the job description, include or leave out accordingly, and say which in the rationale. Imports are unaffected: the content still goes in the inventory |
| `fact` | The one accepted version of a title, date or figure | Use it wherever the fact appears. A source that says otherwise is a conflict, handled by the `precedence` rules |
| `precedence` | Which source wins when two disagree | `inventory_wins`: keep the inventory, note the source's version in the role's `notes` and tell the user. `flag` (the default for any source with no rule): record both versions and add a `docs/tasks.md` item, per `inventory/schema.md`'s *Conflicting evidence* |
| `process` | How a step works (what counts as a reword, what needs approval) | Followed as written. A process rule can make a step stricter than the skill's default, never looser: it can't waive *Never fabricate* or *Never reword without approval* |

## What a rule can't do

- Make up content. A rule shapes the user's own evidence; it never adds a
  claim the evidence doesn't make.
- Waive approval for a reword, other than the exact substitution a `term`
  rule's `replace` gives.
- Resolve a conflict the user hasn't ruled on. A `precedence` rule is a
  ruling, recorded once, for a whole kind of source.

## Adding or changing a rule

Only the user makes rules. When they correct something during any skill's
run in a way that sounds general ("never call it X", "always say Y", "leave
Z out"), offer once to save it as a rule: show the YAML entry you'd add and
write it only when they agree. A one-off correction stays a one-off. When a
new rule changes how existing inventory text should read, run
`scripts/check_editorial_rules.py` and offer the fixes as before/afters;
don't apply them in bulk without approval.
