#!/usr/bin/env python3
"""
Lint the skills in .claude/skills/ (and the agents in .claude/agents/)
against the Agent Skills specification and its best-practice guides
(https://agentskills.io, source: github.com/agentskills/agentskills). Run it
after any change to a skill or agent, the way validate_inventory.py is run
after any change to inventory/. CI runs it on every pull request.

Errors (fail the run):
  1. Every skill folder has a SKILL.md that starts with YAML frontmatter
     between `---` lines, and the frontmatter parses to a mapping.
  2. Frontmatter uses only the fields the spec defines: name, description,
     license, compatibility, metadata, allowed-tools. Other fields are
     client-specific and won't work in every editor.
  3. `name`: present, at most 64 characters, lowercase letters, digits and
     single hyphens only, not starting or ending with a hyphen, and the
     same as the folder name.
  4. `description`: present, non-empty, at most 1024 characters, and says
     when to use the skill ("Use when...", "Use whenever...", "Use
     after..."). The description is all an agent sees when deciding
     whether to load the skill, so a description that only says what the
     skill does won't trigger reliably.
  5. Optional fields: `compatibility` at most 500 characters, `metadata` a
     mapping of strings to strings, `license` and `allowed-tools` strings.
  6. Every skill or agent named in backticks in a description exists, so a
     description never routes the agent to a skill that's been renamed or
     removed.
  7. SKILL.md has a non-empty body of at most 500 lines. Longer material
     belongs in a reference file the body points to.
  8. Every file path in backticks or in a Markdown link in SKILL.md
     exists, relative to the skill folder, .claude/skills/, the repo root
     or another skill's folder. Placeholders (<slug>, YYYY, globs), absolute paths, URLs and
     the user's own data (YAML under inventory/, anything under
     job_descriptions/ or resumes/) are skipped.
  9. Every other file in a skill folder is mentioned in its SKILL.md, by
     path or file name. An agent only loads a bundled file when SKILL.md
     tells it to, so an unmentioned file is never used.
 10. Scripts a skill bundles or points to never wait for keyboard input
     (input(), getpass, `read -p`): agents run them in non-interactive
     shells, where a prompt hangs forever.
 11. Agents (.claude/agents/*.md) have a `name` matching the file name
     (same format as 3) and a `description` that passes 4.

Warnings (printed, don't fail unless --strict):
  - The description is under 80 characters, too short to say both what the
    skill does and when to use it.
  - The SKILL.md body is over about 5,000 tokens, the spec's recommended
    ceiling for what loads on every use.
  - A bundled file is nested more than one folder deep. The spec
    recommends keeping references one level deep from SKILL.md.

Exits 0 and prints "All skill checks passed" if there are no errors, 1 if
any check fails, and 2 if it can't run (no skills found, PyYAML missing).
Never modifies anything.

Usage: python3 scripts/lint_skills.py [--strict] [repo_root]
"""
import os
import re
import sys
import unicodedata

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_COMPATIBILITY = 500
MAX_LINES = 500
MAX_BODY_TOKENS = 5000
MIN_DESCRIPTION = 80

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# "Use when", "Use whenever", "Use after", "Use this skill when", "Use it for"...
TRIGGER_RE = re.compile(
    r"\buse\b(\s+(this|it|this skill|this agent))?\s+(when|whenever|after|before|for|if|to)\b",
    re.IGNORECASE,
)
BACKTICK_NAME_RE = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+)+)`")
BACKTICK_RE = re.compile(r"`([^`\s]+)`")
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
PLACEHOLDER_RE = re.compile(r"[<>*{}]|YYYY")
INTERACTIVE_RE = re.compile(r"\binput\(|\bgetpass\b|\bread\s+(-\w+\s+)*-p\b")
USER_DATA_DIRS = ("job_descriptions/", "resumes/")


def split_frontmatter(text):
    """Return (frontmatter_text, body) or raise ValueError."""
    if not text.startswith("---"):
        raise ValueError("must start with YAML frontmatter (---)")
    lines = text.split("\n")
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    raise ValueError("frontmatter is not closed with ---")


def parse(path):
    """Parse a SKILL.md or agent file: (metadata, body, errors)."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    try:
        fm, body = split_frontmatter(text)
    except ValueError as e:
        return None, None, [f"{path}: {e}"]
    try:
        meta = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        return None, None, [f"{path}: frontmatter is not valid YAML: {e}"]
    if not isinstance(meta, dict):
        return None, None, [f"{path}: frontmatter must be a YAML mapping"]
    return meta, body, []


def check_name(path, meta, expected):
    name = meta.get("name")
    if not isinstance(name, str) or not name.strip():
        return [f"{path}: `name` is missing or empty"]
    name = unicodedata.normalize("NFKC", name.strip())
    errors = []
    if len(name) > MAX_NAME:
        errors.append(f"{path}: `name` is {len(name)} characters (max {MAX_NAME})")
    if not NAME_RE.match(name):
        errors.append(
            f"{path}: `name` {name!r} must be lowercase letters, digits and single "
            "hyphens, not starting or ending with a hyphen"
        )
    if name != expected:
        errors.append(f"{path}: `name` {name!r} must match its folder/file name {expected!r}")
    return errors


def check_description(path, meta, known_names):
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return [f"{path}: `description` is missing or empty"], []
    errors, warnings = [], []
    if len(desc) > MAX_DESCRIPTION:
        errors.append(f"{path}: `description` is {len(desc)} characters (max {MAX_DESCRIPTION})")
    if not TRIGGER_RE.search(desc):
        errors.append(
            f"{path}: `description` doesn't say when to use it; add a sentence like "
            "\"Use when the user...\""
        )
    for ref in BACKTICK_NAME_RE.findall(desc):
        if ref not in known_names:
            errors.append(f"{path}: `description` names `{ref}`, which isn't a skill or agent here")
    if len(desc) < MIN_DESCRIPTION:
        warnings.append(
            f"{path}: `description` is only {len(desc)} characters; say what it does and when to use it"
        )
    return errors, warnings


def check_optional_fields(path, meta):
    errors = []
    unknown = sorted(set(meta) - ALLOWED_FIELDS)
    if unknown:
        errors.append(
            f"{path}: frontmatter fields {unknown} aren't in the Agent Skills spec "
            f"(allowed: {sorted(ALLOWED_FIELDS)})"
        )
    if "compatibility" in meta:
        c = meta["compatibility"]
        if not isinstance(c, str) or not c.strip():
            errors.append(f"{path}: `compatibility` must be a non-empty string")
        elif len(c) > MAX_COMPATIBILITY:
            errors.append(f"{path}: `compatibility` is {len(c)} characters (max {MAX_COMPATIBILITY})")
    if "metadata" in meta:
        m = meta["metadata"]
        if not isinstance(m, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in m.items()
        ):
            errors.append(f"{path}: `metadata` must map strings to strings (quote numbers)")
    for field in ("license", "allowed-tools"):
        if field in meta and not isinstance(meta[field], str):
            errors.append(f"{path}: `{field}` must be a string")
    return errors


def referenced_paths(text):
    """File paths a SKILL.md points to, minus the ones we can't check."""
    out = []
    for ref in BACKTICK_RE.findall(text) + LINK_RE.findall(text):
        ref = ref.split("#")[0]
        if "/" not in ref or "://" in ref or ref.startswith(("/", "~", "mailto:")):
            continue
        last = ref.rstrip("/").rsplit("/", 1)[-1]
        if not (ref.endswith("/") or "." in last):
            continue  # e.g. `and/or`, not a path
        if PLACEHOLDER_RE.search(ref):
            continue
        if ref.startswith(USER_DATA_DIRS) or (ref.startswith("inventory/") and ref.endswith(".yaml")):
            continue  # the user's own data: only exists once they've used the repo
        out.append(ref)
    return sorted(set(out))


def check_scripts(path, script_paths):
    errors = []
    for s in script_paths:
        try:
            with open(s, encoding="utf-8") as fh:
                code = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for n, line in enumerate(code.split("\n"), start=1):
            if line.lstrip().startswith("#"):
                continue
            if INTERACTIVE_RE.search(line):
                errors.append(
                    f"{path}: {s}:{n} waits for keyboard input; agents can't answer prompts, "
                    "so take it as an argument instead"
                )
    return errors


def lint_skill(root, skills_dir, folder, known_names):
    errors, warnings = [], []
    skill_dir = os.path.join(skills_dir, folder)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return [f"{skill_dir}: missing SKILL.md"], []

    meta, body, errs = parse(skill_md)
    if errs:
        return errs, []

    errors += check_optional_fields(skill_md, meta)
    errors += check_name(skill_md, meta, folder)
    e, w = check_description(skill_md, meta, known_names)
    errors += e
    warnings += w

    with open(skill_md, encoding="utf-8") as fh:
        text = fh.read()
    n_lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    if not body.strip():
        errors.append(f"{skill_md}: has no instructions after the frontmatter")
    if n_lines > MAX_LINES:
        errors.append(
            f"{skill_md}: is {n_lines} lines (max {MAX_LINES}); move detail into a "
            "reference file and say in SKILL.md when to read it"
        )
    tokens = len(body) // 4
    if tokens > MAX_BODY_TOKENS:
        warnings.append(f"{skill_md}: body is about {tokens} tokens (recommended under {MAX_BODY_TOKENS})")

    # 8. referenced paths exist
    scripts = []
    for ref in referenced_paths(text):
        # A skill that describes other skills' layout (create-tailor-skill)
        # may name a path that exists in a sibling skill's folder.
        candidates = [os.path.join(skill_dir, ref), os.path.join(skills_dir, ref), os.path.join(root, ref)]
        candidates += [os.path.join(skills_dir, s, ref) for s in sorted(known_names)]
        hit = next((c for c in candidates if os.path.exists(c)), None)
        if hit is None:
            errors.append(f"{skill_md}: points to `{ref}`, which doesn't exist")
        elif hit.endswith((".py", ".sh")):
            scripts.append(hit)

    # 9. bundled files are mentioned; nesting depth
    for dirpath, _, files in os.walk(skill_dir):
        for f in files:
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, skill_dir)
            if rel == "SKILL.md":
                continue
            if f.endswith((".py", ".sh")):
                scripts.append(full)
            if rel not in text and f not in text:
                errors.append(f"{skill_md}: never mentions its file {rel}, so an agent won't load it")
            if rel.count(os.sep) > 1:
                warnings.append(f"{skill_dir}/{rel}: nested more than one folder deep")

    errors += check_scripts(skill_md, sorted(set(scripts)))
    return errors, warnings


def lint_agent(path, known_names):
    meta, _, errs = parse(path)
    if errs:
        return errs, []
    expected = os.path.splitext(os.path.basename(path))[0]
    errors = check_name(path, meta, expected)
    e, w = check_description(path, meta, known_names)
    return errors + e, w


def main(argv):
    strict = "--strict" in argv
    args = [a for a in argv if a != "--strict"]
    root = args[0] if args else "."
    skills_dir = os.path.join(root, ".claude", "skills")
    agents_dir = os.path.join(root, ".claude", "agents")

    folders = sorted(
        d for d in (os.listdir(skills_dir) if os.path.isdir(skills_dir) else [])
        if os.path.isdir(os.path.join(skills_dir, d))
    )
    if not folders:
        print(f"No skills found under {skills_dir!r}: wrong directory?", file=sys.stderr)
        return 2
    agents = sorted(
        os.path.join(agents_dir, f)
        for f in (os.listdir(agents_dir) if os.path.isdir(agents_dir) else [])
        if f.endswith(".md")
    )
    known = set(folders) | {os.path.splitext(os.path.basename(a))[0] for a in agents}

    errors, warnings = [], []
    for folder in folders:
        e, w = lint_skill(root, skills_dir, folder, known)
        errors += e
        warnings += w
    for agent in agents:
        e, w = lint_agent(agent, known)
        errors += e
        warnings += w

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors or (strict and warnings):
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s) "
              f"in {len(folders)} skill(s) and {len(agents)} agent(s).")
        return 1
    print(f"All skill checks passed ({len(folders)} skills, {len(agents)} agents"
          f"{f', {len(warnings)} warning(s)' if warnings else ''}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
