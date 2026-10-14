#!/usr/bin/env python3
"""
Validate inventory/ for internal consistency. Run this after ANY change to
inventory/skills.yaml or inventory/roles/*.yaml, before considering the
change complete — required by extract-jd-signal and seed-inventory-from-source.

Checks:
  1. Every inventory/**/*.yaml file parses as valid YAML.
  2. No duplicate skill ids in skills.yaml.
  3. No skill entry has an empty `evidence` list.
  4. No skill's evidence references a role file that doesn't exist.
  5. No role bullet tags a skill id that doesn't exist in skills.yaml.
  6. Every (role, skill) pair implied by a bullet's `skills:` list has a
     matching {role: ...} evidence entry on that skill in skills.yaml.
     (A bullet tagging a skill is a claim; the skill's evidence list is
     what backs that claim. They must never drift apart.)
  7. No duplicate {role: ...} evidence entries within a single skill.
  8. Every role bullet has a non-empty `evidence_strength_rationale` — a
     strength rating with no stated reason it earned that rating.
  9. interview_stories.yaml: no duplicate ids, every entry has all four
     non-empty STAR fields (situation/task/action/result — presence only,
     not judging honesty/quality), a non-empty `evidence` list, every
     `skills` tag exists in skills.yaml, and every evidence `role` exists
     as a role file.
 10. dev_opportunities_tracker.yaml: no duplicate ids, `status` is one of
     open/closed/declined, `resolution_note` is non-empty whenever
     `status != open`, `related_skill_id` (if set) exists in skills.yaml,
     and no entry has an empty `seen_in` list.
 11. Same-company role date overlaps are declared: two role files at the
     same company whose date ranges overlap must be linked by
     `concurrent_with` (on either side). Every `concurrent_with` id must be
     an existing role at the same company, and every `title_history` entry
     must have a title and YYYY-MM dates that sit inside the role's own
     range, in chronological order without overlapping.

Exits 0 and prints "All checks passed" if clean; otherwise prints every
issue found and exits 1. Never modifies anything.

Usage: python3 scripts/validate_inventory.py [inventory_dir]
"""
import glob
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "inventory"
    problems = []

    files = sorted(glob.glob(os.path.join(root, "**", "*.yaml"), recursive=True))
    if not files:
        print(f"No .yaml files found under {root!r} — wrong directory?", file=sys.stderr)
        sys.exit(2)

    parsed = {}
    for f in files:
        try:
            with open(f) as fh:
                parsed[f] = yaml.safe_load(fh)
        except yaml.YAMLError as e:
            problems.append(f"PARSE ERROR in {f}: {e}")

    skills_path = os.path.join(root, "skills.yaml")
    if skills_path not in parsed:
        problems.append(f"Missing or unparsed {skills_path}")
        _report(problems)

    skills = (parsed[skills_path] or {}).get("skills", [])

    # 2. duplicate skill ids
    ids = [s.get("id") for s in skills]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        problems.append(f"Duplicate skill ids in skills.yaml: {sorted(dupes)}")

    # 3. empty evidence
    empty = [s.get("id") for s in skills if not s.get("evidence")]
    if empty:
        problems.append(f"Skills with empty/missing evidence: {sorted(empty)}")

    # role files that exist
    role_files = {
        os.path.splitext(os.path.basename(f))[0]
        for f in glob.glob(os.path.join(root, "roles", "*.yaml"))
    }

    skill_ids = set(ids)

    # 4. dangling role refs in evidence
    dangling = set()
    evidence_role_skill_pairs = set()
    dupe_evidence = []
    for s in skills:
        seen_roles = []
        for e in s.get("evidence", []) or []:
            role = e.get("role")
            if role is None:
                continue
            if role not in role_files:
                dangling.add((s.get("id"), role))
            evidence_role_skill_pairs.add((role, s.get("id")))
            if role in seen_roles:
                dupe_evidence.append((s.get("id"), role))
            seen_roles.append(role)
    if dangling:
        problems.append(f"Skill evidence pointing at a nonexistent role file: {sorted(dangling)}")
    if dupe_evidence:
        problems.append(f"Duplicate role-evidence entries within a skill: {sorted(dupe_evidence)}")

    # 5, 6 & 8. bullet skill tags vs skills.yaml, and rationale presence
    unknown_tags = set()
    bullet_role_skill_pairs = set()
    missing_rationale = []
    for rf in glob.glob(os.path.join(root, "roles", "*.yaml")):
        rdata = parsed.get(rf)
        if not rdata:
            continue
        role_id = rdata.get("id")
        for i, b in enumerate(rdata.get("bullets", []) or []):
            for tag in b.get("skills", []) or []:
                if tag not in skill_ids:
                    unknown_tags.add((rf, tag))
                else:
                    bullet_role_skill_pairs.add((role_id, tag))
            if not (b.get("evidence_strength_rationale") or "").strip():
                snippet = (b.get("text") or "").strip().replace("\n", " ")[:60]
                missing_rationale.append(f"{role_id} bullet #{i + 1}: \"{snippet}...\"")
    if unknown_tags:
        problems.append(f"Role bullets tagging a skill id that doesn't exist: {sorted(unknown_tags)}")
    if missing_rationale:
        lines = "\n".join(f"    {m}" for m in missing_rationale)
        problems.append(
            f"Bullets missing evidence_strength_rationale ({len(missing_rationale)}):\n{lines}"
        )

    missing_links = bullet_role_skill_pairs - evidence_role_skill_pairs
    if missing_links:
        lines = "\n".join(f"    {skill:40s} <- {role}" for role, skill in sorted(missing_links))
        problems.append(
            "Bullets tag a skill with no matching evidence entry for that role "
            f"({len(missing_links)} pairs) — every skill a bullet claims must be "
            f"backed by {{role: ...}} evidence on that skill:\n{lines}"
        )

    # 9. interview_stories.yaml
    stories_path = os.path.join(root, "interview_stories.yaml")
    if stories_path in parsed:
        stories = (parsed[stories_path] or {}).get("interview_stories", [])

        story_ids = [s.get("id") for s in stories]
        story_dupes = {i for i in story_ids if story_ids.count(i) > 1}
        if story_dupes:
            problems.append(f"Duplicate interview_story ids: {sorted(story_dupes)}")

        star_fields = ("situation", "task", "action", "result")
        incomplete_star = []
        empty_story_evidence = []
        unknown_story_skill_tags = set()
        dangling_story_roles = set()
        for s in stories:
            star = s.get("star") or {}
            missing_fields = [f for f in star_fields if not (star.get(f) or "").strip()]
            if missing_fields:
                incomplete_star.append(f"{s.get('id')}: missing {missing_fields}")
            if not s.get("evidence"):
                empty_story_evidence.append(s.get("id"))
            for tag in s.get("skills", []) or []:
                if tag not in skill_ids:
                    unknown_story_skill_tags.add((s.get("id"), tag))
            for e in s.get("evidence", []) or []:
                role = e.get("role")
                if role is not None and role not in role_files:
                    dangling_story_roles.add((s.get("id"), role))

        if incomplete_star:
            lines = "\n".join(f"    {m}" for m in incomplete_star)
            problems.append(f"interview_stories with incomplete STAR fields:\n{lines}")
        if empty_story_evidence:
            problems.append(f"interview_stories with empty evidence: {sorted(empty_story_evidence)}")
        if unknown_story_skill_tags:
            problems.append(f"interview_stories tagging a nonexistent skill id: {sorted(unknown_story_skill_tags)}")
        if dangling_story_roles:
            problems.append(f"interview_stories evidence pointing at a nonexistent role file: {sorted(dangling_story_roles)}")

    # 10. dev_opportunities_tracker.yaml
    tracker_path = os.path.join(root, "dev_opportunities_tracker.yaml")
    if tracker_path in parsed:
        opportunities = (parsed[tracker_path] or {}).get("dev_opportunities", [])

        opp_ids = [o.get("id") for o in opportunities]
        opp_dupes = {i for i in opp_ids if opp_ids.count(i) > 1}
        if opp_dupes:
            problems.append(f"Duplicate dev_opportunities ids: {sorted(opp_dupes)}")

        valid_statuses = {"open", "closed", "declined"}
        bad_status = []
        missing_resolution = []
        unknown_related_skill = []
        empty_seen_in = []
        for o in opportunities:
            status = o.get("status")
            if status not in valid_statuses:
                bad_status.append((o.get("id"), status))
            if status != "open" and not (o.get("resolution_note") or "").strip():
                missing_resolution.append(o.get("id"))
            related = o.get("related_skill_id")
            if related is not None and related not in skill_ids:
                unknown_related_skill.append((o.get("id"), related))
            if not o.get("seen_in"):
                empty_seen_in.append(o.get("id"))

        if bad_status:
            problems.append(f"dev_opportunities with invalid status: {sorted(bad_status)}")
        if missing_resolution:
            problems.append(
                f"dev_opportunities with status != open but no resolution_note: {sorted(missing_resolution)}"
            )
        if unknown_related_skill:
            problems.append(
                f"dev_opportunities with related_skill_id not in skills.yaml: {sorted(unknown_related_skill)}"
            )
        if empty_seen_in:
            problems.append(f"dev_opportunities with empty/missing seen_in: {sorted(empty_seen_in)}")

    # 11. same-company overlaps declared via concurrent_with; title_history sane
    def _end(d):
        return "9999-12" if d == "present" else d

    roles = {}
    for rf in glob.glob(os.path.join(root, "roles", "*.yaml")):
        rdata = parsed.get(rf)
        if rdata and rdata.get("id"):
            roles[rdata["id"]] = rdata
    bad_concurrent = []
    undeclared_overlaps = []
    bad_title_history = []
    for rid, r in sorted(roles.items()):
        cw = r.get("concurrent_with") or []
        if isinstance(cw, str):
            cw = [cw]
        for other in cw:
            o = roles.get(other)
            if o is None:
                bad_concurrent.append(f"{rid} -> {other} (no such role)")
            elif o.get("company") != r.get("company"):
                bad_concurrent.append(f"{rid} -> {other} (different company)")
        start, end = str(r.get("start_date")), _end(str(r.get("end_date")))
        prev_end = None
        for i, h in enumerate(r.get("title_history") or []):
            hs, he = str(h.get("start_date")), _end(str(h.get("end_date")))
            if not (h.get("title") or "").strip():
                bad_title_history.append(f"{rid} entry #{i + 1}: missing title")
            if hs > he or hs < start or he > end:
                bad_title_history.append(f"{rid} entry #{i + 1}: {hs}..{he} outside {start}..{end}")
            if prev_end is not None and hs <= prev_end:
                bad_title_history.append(f"{rid} entry #{i + 1}: starts before the previous entry ends")
            prev_end = he

    def _declared(a, b):
        for x, y in ((a, b), (b, a)):
            cw = roles[x].get("concurrent_with") or []
            if y in ([cw] if isinstance(cw, str) else cw):
                return True
        return False

    ids = sorted(roles)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ra, rb = roles[a], roles[b]
            if ra.get("company") != rb.get("company"):
                continue
            if str(ra.get("start_date")) <= _end(str(rb.get("end_date"))) and \
                    str(rb.get("start_date")) <= _end(str(ra.get("end_date"))):
                if not _declared(a, b):
                    undeclared_overlaps.append(f"{a} and {b}")
    if bad_concurrent:
        problems.append(f"concurrent_with pointing at a missing or different-company role: {bad_concurrent}")
    if undeclared_overlaps:
        problems.append(
            "Same-company roles with overlapping dates but no concurrent_with link "
            f"(either fix the dates or declare the concurrency): {undeclared_overlaps}"
        )
    if bad_title_history:
        lines = "\n".join(f"    {m}" for m in bad_title_history)
        problems.append(f"Invalid title_history entries:\n{lines}")


    _report(problems)


def _report(problems):
    if problems:
        print(f"{len(problems)} issue(s) found:\n")
        for p in problems:
            print(f"- {p}\n")
        sys.exit(1)
    print("All checks passed.")
    sys.exit(0)


if __name__ == "__main__":
    main()
