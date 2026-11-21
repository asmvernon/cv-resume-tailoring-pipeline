#!/usr/bin/env python3
"""
Check text against the user's standing editorial rules
(inventory/editorial_rules.yaml): names that must never appear, preferred
wording, claims to keep out, and style rules such as "no first person in
bullets". The rules file format is documented in inventory/schema.md and
.claude/skills/import-work-evidence/reference/editorial-rules.md.

Only rules with a `find` or `find_regex` can be checked mechanically. Every
other rule (a fact to keep consistent, how to handle conflicts) is applied
by the skill that reads the file; this script only lists how many there are.

What it scans:
  - With no paths: every role file in inventory/roles/ (titles, summary,
    bullets) and inventory/interview_stories.yaml for rules that cover
    `stories`.
  - With paths: just those files. A file under inventory/roles/ is read as a
    role file. A file named resume.md or cover_letter.md is a resume or a
    cover letter. Any other file (for example a work-session export saved
    before importing it) is checked against every rule.

Exit codes: 0 no hits (or no rules file), 1 at least one hit,
2 the rules file is invalid or can't be read. Never modifies anything.

Usage: python3 scripts/check_editorial_rules.py [--rules PATH] [file ...]
"""
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

KINDS = {"term", "style", "exclude", "fact", "precedence", "process"}
WHERE = {"inventory", "stories", "resume", "cover_letter"}
FIELDS = {"any", "title", "summary", "bullets"}
DEFAULT_WHERE = ["inventory", "resume", "cover_letter"]
BULLET_LINE = re.compile(r"^\s*(?:[-*•]|\d+\.)\s+")


def load_rules(path):
    """Returns (rules, errors). Each rule gets compiled `patterns`."""
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    errors = []
    if not isinstance(data, dict) or not isinstance(data.get("rules", []), list):
        return [], [f"{path}: expected a mapping with a `rules:` list"]
    rules, seen = [], set()
    for i, rule in enumerate(data.get("rules") or []):
        where = f"rules[{i}]"
        if not isinstance(rule, dict):
            errors.append(f"{where}: each rule must be a mapping")
            continue
        rid = rule.get("id")
        if not isinstance(rid, str) or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", rid):
            errors.append(f"{where}: `id` must be a lowercase-hyphenated slug")
        elif rid in seen:
            errors.append(f"{where}: duplicate id {rid!r}")
        else:
            seen.add(rid)
            where = rid
        if rule.get("kind") not in KINDS:
            errors.append(f"{where}: `kind` must be one of {sorted(KINDS)}")
        if not isinstance(rule.get("rule"), str) or not rule["rule"].strip():
            errors.append(f"{where}: `rule` (the plain-language rule) is required")
        rule_where = rule.get("where", DEFAULT_WHERE)
        if not isinstance(rule_where, list) or not set(rule_where) <= WHERE:
            errors.append(f"{where}: `where` must be a list from {sorted(WHERE)}")
            rule_where = DEFAULT_WHERE
        fields = rule.get("fields", ["any"])
        if not isinstance(fields, list) or not set(fields) <= FIELDS:
            errors.append(f"{where}: `fields` must be a list from {sorted(FIELDS)}")
            fields = ["any"]
        patterns = []
        find = rule.get("find", [])
        if isinstance(find, str):
            find = [find]
        if not isinstance(find, list) or not all(isinstance(s, str) and s for s in find):
            errors.append(f"{where}: `find` must be a list of non-empty strings")
            find = []
        for term in find:
            # Literal, case-insensitive, not inside a longer word.
            patterns.append(re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE))
        regexes = rule.get("find_regex", [])
        if isinstance(regexes, str):
            regexes = [regexes]
        for rx in regexes if isinstance(regexes, list) else []:
            try:
                patterns.append(re.compile(rx))
            except (re.error, TypeError) as e:
                errors.append(f"{where}: `find_regex` {rx!r} doesn't compile: {e}")
        roles = rule.get("roles")
        if roles is not None and (not isinstance(roles, list)
                                  or not all(isinstance(r, str) for r in roles)):
            errors.append(f"{where}: `roles` must be a list of role ids")
        if "replace" in rule and not isinstance(rule["replace"], str):
            errors.append(f"{where}: `replace` must be a string")
        rules.append({**rule, "where": rule_where, "fields": fields, "patterns": patterns})
    return rules, errors


def role_texts(path):
    """(field, label, text) for the checkable parts of a role file."""
    with open(path) as f:
        role = yaml.safe_load(f) or {}
    out = []
    if role.get("title"):
        out.append(("title", "title", str(role["title"])))
    for j, t in enumerate(role.get("title_history") or []):
        if isinstance(t, dict) and t.get("title"):
            out.append(("title", f"title_history[{j}]", str(t["title"])))
    if role.get("summary"):
        out.append(("summary", "summary", str(role["summary"])))
    for j, b in enumerate(role.get("bullets") or []):
        if isinstance(b, dict) and b.get("text"):
            out.append(("bullets", f"bullets[{j}]", str(b["text"])))
    return out


def story_texts(path):
    with open(path) as f:
        data = yaml.safe_load(f) or []
    stories = data.get("interview_stories", []) if isinstance(data, dict) else data
    out = []
    for s in stories or []:
        if not isinstance(s, dict):
            continue
        parts = {"title": s.get("title")}
        if isinstance(s.get("star"), dict):
            parts.update(s["star"])
        for key, value in parts.items():
            if value:
                out.append(("any", f"{s.get('id', '?')}.{key}", str(value)))
    return out


def markdown_texts(path):
    with open(path) as f:
        lines = f.read().splitlines()
    return [("bullets" if BULLET_LINE.match(line) else "any", f"line {n}", line)
            for n, line in enumerate(lines, 1) if line.strip()]


def category(path, repo):
    rel = os.path.relpath(os.path.abspath(path), repo)
    name = os.path.basename(path)
    if rel.startswith(os.path.join("inventory", "roles") + os.sep) and name.endswith(".yaml"):
        return "inventory"
    if name == "interview_stories.yaml":
        return "stories"
    if name == "resume.md":
        return "resume"
    if name == "cover_letter.md":
        return "cover_letter"
    return None  # a source file: every rule applies


def texts_for(path, cat):
    if cat == "inventory":
        return role_texts(path)
    if cat == "stories":
        return story_texts(path)
    return markdown_texts(path)


def applies(rule, cat, field, path):
    if cat is not None and cat not in rule["where"]:
        return False
    if cat == "inventory" and rule.get("roles"):
        if os.path.splitext(os.path.basename(path))[0] not in rule["roles"]:
            return False
    if "any" in rule["fields"]:
        return True
    # In Markdown, a non-bullet line can't be told apart as title or summary,
    # so a title/summary rule checks every non-bullet line.
    if cat in (None, "resume", "cover_letter") and field == "any":
        return bool(set(rule["fields"]) & {"title", "summary"})
    return field in rule["fields"]


def main(argv):
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    rules_path = os.path.join(repo, "inventory", "editorial_rules.yaml")
    paths = []
    args = iter(argv)
    for a in args:
        if a == "--rules":
            rules_path = next(args, None)
            if rules_path is None:
                print("--rules needs a path", file=sys.stderr)
                return 2
        else:
            paths.append(a)

    if not os.path.exists(rules_path):
        print(f"No rules file at {os.path.relpath(rules_path)}; nothing to check.")
        return 0
    try:
        rules, errors = load_rules(rules_path)
    except (OSError, yaml.YAMLError) as e:
        print(f"Can't read {rules_path}: {e}", file=sys.stderr)
        return 2
    if errors:
        print(f"{os.path.relpath(rules_path)} is invalid:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 2

    if not paths:
        roles_dir = os.path.join(repo, "inventory", "roles")
        if os.path.isdir(roles_dir):
            paths = sorted(os.path.join(roles_dir, f) for f in os.listdir(roles_dir)
                           if f.endswith(".yaml"))
        stories = os.path.join(repo, "inventory", "interview_stories.yaml")
        if os.path.exists(stories) and any("stories" in r["where"] for r in rules):
            paths.append(stories)

    hits = 0
    for path in paths:
        cat = category(path, repo)
        try:
            texts = texts_for(path, cat)
        except (OSError, yaml.YAMLError) as e:
            print(f"Can't read {path}: {e}", file=sys.stderr)
            return 2
        for field, label, text in texts:
            for rule in rules:
                if not rule["patterns"] or not applies(rule, cat, field, path):
                    continue
                found = sorted({m.group(0) for p in rule["patterns"] for m in p.finditer(text)})
                if not found:
                    continue
                hits += 1
                fix = f" -> {rule['replace']!r}" if rule.get("replace") else ""
                print(f"{os.path.relpath(path)}: {label}: [{rule['id']}] "
                      f"found {', '.join(repr(f) for f in found)}{fix}")
                print(f"    rule: {' '.join(rule['rule'].split())}")

    manual = sum(1 for r in rules if not r["patterns"])
    if hits:
        print(f"\n{hits} hit(s). Rewording them is still a before/after for the user "
              "unless the rule's `replace` covers the exact change.")
    else:
        print("No editorial-rule hits.")
    if manual:
        print(f"{manual} rule(s) can't be checked by script; apply them by reading "
              "the rules file.")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
