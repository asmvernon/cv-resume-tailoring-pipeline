# Instructions for AI coding assistants

This repo is set up for Claude Code, which loads `CLAUDE.md` and the skills in
`.claude/skills/` automatically. If you are another assistant (Cursor, GitHub
Copilot, Codex, Windsurf or similar), follow the same instructions by hand:

1. Read `CLAUDE.md` first. Its ground rules apply to everything you do here.
2. Each workflow is a `SKILL.md` file. When the user asks for one of the
   tasks below, read that file in full and follow its steps, including every
   point where it says to stop and ask the user.

| When the user wants to… | Follow |
|---|---|
| Add their CV, résumé, LinkedIn PDF or background to the inventory | `.claude/skills/seed-inventory-from-source/SKILL.md` |
| Add a job description and check it against the inventory | `.claude/skills/extract-jd-signal/SKILL.md` |
| Go from a job description to a tailored résumé, end to end | `.claude/skills/apply-to-job/SKILL.md` |
| Tailor a US-market résumé | `.claude/skills/tailor-resume-usa/SKILL.md` |
| Tailor a UK contract-market CV | `.claude/skills/tailor-resume-uk-contract/SKILL.md` |
| Render a finished résumé to PDF | `.claude/skills/render-resume-pdf/SKILL.md` |
| Add a tailoring skill for another country or kind of role | `.claude/skills/create-tailor-skill/SKILL.md` |
| Review a tailored draft | `.claude/agents/resume-critic.md` |

3. Before writing anything to `inventory/`, `job_descriptions/` or
   `resumes/`, run `scripts/check_private_copy.sh` and follow `CLAUDE.md`'s
   rule on its result: this copy must be private before personal data goes
   in.
4. Paths inside a skill are relative to the repo root.
5. Where a skill refers to another skill by name (for example
   `extract-jd-signal`), it means that skill's `SKILL.md` in the table above.
6. Where a skill says to spawn a subagent, do that review yourself, as a
   separate pass after the draft is written.
