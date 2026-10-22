#!/usr/bin/env python3
"""
Bring updates from the public pipeline repo into this copy, without touching
your data. Run by the `update-pipeline` skill.

A copy made with GitHub's "Use this template" shares no git history with the
public repo, so `git merge` can't bring updates across. Instead this script
compares the pipeline's own files (skills, scripts, `inventory/schema.md`,
README, CLAUDE.md...) three ways: the version your copy started from (the
base), your copy now, and the latest public version.

  - Changed upstream, untouched by you  -> replaced with the new version.
  - Changed upstream and by you         -> merged; overlapping edits are
                                           marked for you to decide.
  - New upstream                        -> added.
  - Removed upstream, untouched by you  -> removed.

Your data is never read or written: everything under `inventory/` except
`inventory/schema.md`, `job_descriptions/`, `resumes/` and `docs/tasks.md`.
Files you added yourself (a market skill made with `create-tailor-skill`, for
example) aren't in the public repo, so they're left alone too.

The base is found, in order, from `.pipeline-version` (written by the last
update), shared git history, or the public commit your copy's first commit
matches. If none of these work, a file counts as untouched when it matches
any past public version of it.

Usage:
  python3 scripts/update_pipeline.py due        # is a check due? (offline)
  python3 scripts/update_pipeline.py check      # what would change (read-only)
  python3 scripts/update_pipeline.py apply --to <commit>
  python3 scripts/update_pipeline.py record [--upstream-commit <commit>]

`check` prints the commit to pass to `apply --to`, so `apply` applies exactly
what was shown. `apply` writes `.pipeline-version` only when nothing is left
to decide; otherwise run `record --upstream-commit <commit>` once the user
has decided each remaining file. `record` alone notes that updates were
checked today (so the monthly reminder resets) without moving the base.

Exit codes: 0 done; 1 error (message on stderr); 3 `apply` left files for the
user to decide.
"""

import argparse
import datetime
import os
import subprocess
import sys
import tempfile

UPSTREAM = "asmvernon/cv-resume-tailoring-pipeline"  # as in check_private_copy.sh
UPSTREAM_URL = f"https://github.com/{UPSTREAM}.git"
REMOTE = "pipeline-upstream"
REF = f"refs/remotes/{REMOTE}/main"
RECORD = ".pipeline-version"
REMIND_AFTER_DAYS = 30

DATA_PREFIXES = ("inventory/", "job_descriptions/", "resumes/")
PIPELINE_DATA_FILES = {"inventory/schema.md"}
LOCAL_FILES = {"docs/tasks.md", RECORD}


class Error(Exception):
    pass


def git(*args, check=True, input=None):
    text = input is None or isinstance(input, str)
    result = subprocess.run(
        ["git", *args], capture_output=True, input=input, text=text,
        encoding="utf-8" if text else None, errors="replace" if text else None,
    )
    if check and result.returncode != 0:
        err = result.stderr if isinstance(result.stderr, str) else result.stderr.decode()
        raise Error(f"git {' '.join(args)} failed: {err.strip()}")
    return result


def out(*args):
    return git(*args).stdout.strip()


def is_pipeline_path(path):
    if path in LOCAL_FILES:
        return False
    if path in PIPELINE_DATA_FILES:
        return True
    return not path.startswith(DATA_PREFIXES)


def files_at(commit):
    """{path: (mode, blob)} for the pipeline files in a commit."""
    files = {}
    listing = git("ls-tree", "-r", "-z", commit).stdout
    for entry in listing.split("\0"):
        if not entry:
            continue
        meta, path = entry.split("\t", 1)
        mode, kind, blob = meta.split()
        if kind == "blob" and is_pipeline_path(path):
            files[path] = (mode, blob)
    return files


def local_blob(path):
    if os.path.islink(path) or not os.path.isfile(path):
        return None
    return out("hash-object", "--", path)


def read_record():
    record = {}
    try:
        with open(RECORD, encoding="utf-8") as f:
            for line in f:
                if ":" in line and not line.lstrip().startswith("#"):
                    key, value = line.split(":", 1)
                    record[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return record


def write_record(upstream_commit, checked):
    with open(RECORD, "w", encoding="utf-8") as f:
        f.write(
            "# Written by scripts/update_pipeline.py: the public pipeline version\n"
            "# this copy was last updated to, and when updates were last checked.\n"
            f"upstream_commit: {upstream_commit}\n"
            f"checked: {checked}\n"
        )


def commit_exists(sha):
    return git("cat-file", "-e", f"{sha}^{{commit}}", check=False).returncode == 0


def fetch(url):
    if git("remote", "get-url", REMOTE, check=False).returncode == 0:
        git("remote", "set-url", REMOTE, url)
    else:
        git("remote", "add", REMOTE, url)
    result = git("fetch", "--quiet", "--no-tags", REMOTE, f"+main:{REF}", check=False)
    if result.returncode != 0:
        raise Error(
            f"Couldn't reach the public pipeline repo ({url}). Check you're "
            f"online and try again.\n{result.stderr.strip()}"
        )
    return out("rev-parse", REF)


def find_base(upstream):
    """(commit, how) for the public version this copy last matched, or (None, None)."""
    recorded = read_record().get("upstream_commit")
    if recorded and commit_exists(recorded):
        return recorded, "recorded by the last update"
    shared = git("merge-base", "HEAD", upstream, check=False)
    if shared.returncode == 0 and shared.stdout.strip():
        return shared.stdout.strip(), "found from shared git history"
    roots = out("rev-list", "--max-parents=0", "HEAD").split()
    root_trees = {out("rev-parse", f"{r}^{{tree}}") for r in roots}
    for commit in out("rev-list", upstream).split():
        if out("rev-parse", f"{commit}^{{tree}}") in root_trees:
            return commit, "the public version this copy was made from"
    return None, None


def past_blobs(upstream):
    """{path: every blob that path has had upstream}, for when there's no base."""
    seen = {}
    for commit in out("rev-list", upstream).split():
        for path, (_, blob) in files_at(commit).items():
            seen.setdefault(path, set()).add(blob)
    return seen


def merge(base_blob, local_path, new_blob):
    """(text, conflicts): a three-way merge of one file."""
    with tempfile.TemporaryDirectory() as tmp:
        base = os.path.join(tmp, "base")
        new = os.path.join(tmp, "new")
        yours = os.path.join(tmp, "yours")
        for blob, dest in ((base_blob, base), (new_blob, new)):
            with open(dest, "wb") as f:
                f.write(git("cat-file", "blob", blob, input=b"").stdout)
        with open(local_path, "rb") as f:
            local = f.read()
        # Git for Windows checks files out with CRLF line endings; compare
        # like with like, or every line would conflict.
        with open(yours, "wb") as f:
            f.write(local.replace(b"\r\n", b"\n"))
        result = git(
            "merge-file", "-p", "-L", "your copy", "-L", "before", "-L", "public pipeline",
            yours, base, new, check=False, input=b"",
        )
        if result.returncode > 127:  # git exits negative (255...) on error
            raise Error(f"Couldn't merge {local_path}.")
        return result.stdout, result.returncode


def plan(upstream, base):
    """Sort every pipeline file into an action."""
    new_files = files_at(upstream)
    base_files = files_at(base) if base else {}
    history = None if base else past_blobs(upstream)
    actions = {k: [] for k in ("update", "add", "remove", "merge", "conflict", "decide")}

    for path in sorted(set(base_files) | set(new_files) | set(history or ())):
        new = new_files.get(path, (None, None))[1]
        local = local_blob(path)
        if base:
            old = base_files.get(path, (None, None))[1]
        elif local in history.get(path, ()):
            old = local
        else:
            old = "unknown"
        if local == new or old == new:
            continue  # already up to date, or a change of yours the pipeline didn't touch
        if new is None:
            if local == old:
                actions["remove"].append((path, None))
            elif local is not None:
                actions["decide"].append((path, "removed from the pipeline, but your copy changed it"))
        elif local is None:
            if old in (None, "unknown"):
                actions["add"].append((path, None))
            else:
                actions["decide"].append((path, "you deleted it, and the pipeline changed it"))
        elif local == old:
            actions["update"].append((path, None))
        elif old in (None, "unknown"):
            actions["decide"].append((path, "your copy and the pipeline each have their own version"))
        else:
            _, conflicts = merge(old, path, new)
            actions["conflict" if conflicts else "merge"].append((path, None))
    return actions, new_files


def changelog(base, upstream):
    """The CHANGELOG.md lines added since the base."""
    if not base:
        return []
    diff = git("diff", base, upstream, "--", "CHANGELOG.md", check=False).stdout
    return [
        line[1:] for line in diff.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]


def dirty(paths):
    if not paths:
        return []
    status = git("status", "--porcelain", "-z", "--untracked-files=no", "--", *paths).stdout
    return [entry[3:] for entry in status.split("\0") if entry[3:]]


def short(sha):
    return out("log", "-1", "--format=%h (%cs)", sha)


def cmd_due(args):
    checked = read_record().get("checked")
    if not checked:
        roots = out("rev-list", "--max-parents=0", "HEAD").split()
        checked = out("log", "-1", "--format=%cs", roots[-1]) if roots else None
    if not checked:
        print("not due")
        return 0
    age = (datetime.date.today() - datetime.date.fromisoformat(checked)).days
    print(f"{'due' if age >= REMIND_AFTER_DAYS else 'not due'}: last checked {checked}, {age} days ago")
    return 0


LABELS = {
    "update": "Updated (you hadn't changed these)",
    "add": "New",
    "remove": "Removed from the pipeline (you hadn't changed these)",
    "merge": "Merged with your own changes, no overlap",
    "conflict": "Changed by you and by the pipeline in the same place: needs your decision",
    "decide": "Needs your decision",
}


def cmd_check(args):
    upstream = fetch(args.upstream)
    base, how = find_base(upstream)
    actions, _ = plan(upstream, base)
    print(f"Latest public version: {short(upstream)}")
    print(f"Your copy's version: {short(base) + ' (' + how + ')' if base else 'unknown'}")
    print(f"Apply with: python3 scripts/update_pipeline.py apply --to {upstream}")
    if not any(actions.values()):
        print("\nUp to date: nothing to change.")
        return 0
    notes = changelog(base, upstream)
    if notes:
        print("\nWhat's new (from CHANGELOG.md):")
        print("\n".join(notes))
    for key, label in LABELS.items():
        if actions[key]:
            print(f"\n{label}:")
            for path, why in actions[key]:
                print(f"  {path}" + (f": {why}" if why else ""))
    busy = dirty([p for items in actions.values() for p, _ in items])
    if busy:
        print("\nUncommitted changes in files this would touch; commit or discard them first:")
        print("\n".join(f"  {p}" for p in busy))
    return 0


def cmd_apply(args):
    upstream = args.to
    if not commit_exists(upstream):
        raise Error(f"Unknown commit {upstream}. Run `check` first.")
    base, _ = find_base(upstream)
    actions, new_files = plan(upstream, base)
    busy = dirty([p for items in actions.values() for p, _ in items])
    if busy:
        raise Error("Commit or discard the uncommitted changes in these first:\n"
                    + "\n".join(f"  {p}" for p in busy))

    for path, _ in actions["update"] + actions["add"]:
        mode, blob = new_files[path]
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "wb") as f:
            f.write(git("cat-file", "blob", blob, input=b"").stdout)
        os.chmod(path, 0o755 if mode == "100755" else 0o644)
    for path, _ in actions["remove"]:
        os.remove(path)
    base_files = files_at(base) if base else {}
    for path, _ in actions["merge"] + actions["conflict"]:
        text, _ = merge(base_files[path][1], path, new_files[path][1])
        with open(path, "wb") as f:
            f.write(text)

    for key in ("update", "add", "remove", "merge"):
        for path, _ in actions[key]:
            print(f"{key}: {path}")
    left = actions["conflict"] + actions["decide"]
    if left:
        for path, why in actions["conflict"]:
            print(f"conflict (marked with <<<<<<< your copy / >>>>>>> public pipeline): {path}")
        for path, why in actions["decide"]:
            print(f"decide ({why}; public version: git show {upstream}:{path}): {path}")
        print(f"\nOnce each is decided: python3 scripts/update_pipeline.py record --upstream-commit {upstream}")
        return 3
    write_record(upstream, datetime.date.today().isoformat())
    print(f"\nRecorded in {RECORD}: this copy is now at {short(upstream)}.")
    return 0


def cmd_record(args):
    sha = args.upstream_commit or read_record().get("upstream_commit")
    if not sha:
        if git("rev-parse", "--verify", "--quiet", REF, check=False).returncode == 0:
            sha, _ = find_base(out("rev-parse", REF))
        if not sha:
            sha = "unknown"
    elif not commit_exists(sha):
        raise Error(f"Unknown commit {sha}.")
    write_record(sha, datetime.date.today().isoformat())
    print(f"Recorded in {RECORD}.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("due", help="say whether a monthly check is due (offline)")
    check = sub.add_parser("check", help="fetch the public repo and list what would change")
    check.add_argument("--upstream", default=UPSTREAM_URL, help="the public repo's URL")
    apply = sub.add_parser("apply", help="apply the changes `check` listed")
    apply.add_argument("--to", required=True, help="the commit `check` printed")
    record = sub.add_parser("record", help="note a check, optionally moving the base")
    record.add_argument("--upstream-commit", help="the public commit now merged in")
    args = parser.parse_args()

    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if git("rev-parse", "--is-inside-work-tree", check=False).returncode != 0:
        print("This folder isn't a git repository, so updates can't be compared.", file=sys.stderr)
        return 1
    try:
        return {"due": cmd_due, "check": cmd_check, "apply": cmd_apply, "record": cmd_record}[
            args.command](args)
    except Error as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
