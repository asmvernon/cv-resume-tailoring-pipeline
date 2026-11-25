#!/usr/bin/env python3
"""
Check inventory/fit_profile.yaml, the user's preferences that the
assess-job-fit skill scores postings against. Format:
.claude/skills/assess-job-fit/reference/fit-profile.md

Errors (fail the run):
  - the file doesn't parse, or isn't a mapping
  - an unknown field at the top level or inside a section other than
    `report`, which is free-form (usually a typo, which would silently fall
    back to a default)
  - weights that aren't numbers between 0 and 1, or don't add up to 1
  - ratings that aren't a list of {min (0-5), label}, aren't highest first,
    or don't end at min 0 (so every total gets a label)
  - levels, domains, culture lists or deal_breakers that aren't lists of
    strings
  - a work_authorisation value other than has_right, needs_sponsorship or
    unknown
  - a location adjustment without match, a numeric delta and a why
  - a negative compensation floor

A missing or empty file is fine (the skill uses its defaults): exits 0
with a note. Exits 0 if the profile is valid, 1 if not, 2 if it can't run
(PyYAML missing, or the file can't be read). Never modifies anything.

Usage: python3 scripts/check_fit_profile.py [path]
"""
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

DEFAULT_PATH = "inventory/fit_profile.yaml"
TOP_LEVEL = {
    "version", "rubric", "weights", "ratings", "levels", "locations",
    "work_authorisation", "domains", "culture", "compensation",
    "deal_breakers", "report", "notes",
}
AUTH_VALUES = {"has_right", "needs_sponsorship", "unknown"}
SECTION_KEYS = {
    "levels": {"best", "step_lower", "stretch"},
    "locations": {"preferred", "acceptable", "adjustments", "notes"},
    "domains": {"preferred", "avoid"},
    "culture": {"look_for", "warning_signs", "source", "notes"},
    "compensation": {"currency", "floor"},
}


def _is_str_list(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check(profile):
    """Return a list of problems with a parsed profile."""
    problems = []
    if not isinstance(profile, dict):
        return ["the file must be a mapping of fields (see fit-profile.md)"]

    for key in sorted(set(profile) - TOP_LEVEL, key=str):
        problems.append(f"unknown field '{key}'")
    for section, allowed in SECTION_KEYS.items():
        value = profile.get(section)
        if isinstance(value, dict):
            for key in sorted(set(value) - allowed, key=str):
                problems.append(f"{section}: unknown field '{key}'")
    for key in ("rubric", "notes"):
        if key in profile and not isinstance(profile[key], str):
            problems.append(f"{key}: must be text")

    weights = profile.get("weights")
    if weights is not None:
        if not isinstance(weights, dict) or not weights:
            problems.append("weights: must be a mapping of dimension to weight")
        else:
            bad = [k for k, v in weights.items() if not _is_number(v) or not 0 <= v <= 1]
            for k in bad:
                problems.append(f"weights.{k}: must be a number between 0 and 1")
            if not bad and abs(sum(weights.values()) - 1) > 0.001:
                problems.append(
                    f"weights: add up to {sum(weights.values()):g}, not 1")

    ratings = profile.get("ratings")
    if ratings is not None:
        if not isinstance(ratings, list) or not ratings:
            problems.append("ratings: must be a non-empty list of {min, label}")
        else:
            mins = []
            for i, r in enumerate(ratings):
                if (not isinstance(r, dict) or not _is_number(r.get("min"))
                        or not 0 <= r["min"] <= 5
                        or not isinstance(r.get("label"), str) or not r["label"]):
                    problems.append(f"ratings[{i}]: needs a min between 0 and 5 and a label")
                else:
                    mins.append(r["min"])
            if len(mins) == len(ratings):
                if mins != sorted(mins, reverse=True) or len(set(mins)) != len(mins):
                    problems.append("ratings: list them highest min first, each min different")
                if mins[-1] != 0:
                    problems.append("ratings: the last one needs min 0, so every total gets a label")

    for section, keys in (("levels", ("best", "step_lower", "stretch")),
                          ("domains", ("preferred", "avoid")),
                          ("culture", ("look_for", "warning_signs"))):
        value = profile.get(section)
        if value is None:
            continue
        if not isinstance(value, dict):
            problems.append(f"{section}: must be a mapping")
            continue
        for k in keys:
            if k in value and not _is_str_list(value[k]):
                problems.append(f"{section}.{k}: must be a list of text")

    if "deal_breakers" in profile and not _is_str_list(profile["deal_breakers"]):
        problems.append("deal_breakers: must be a list of text")

    auth = profile.get("work_authorisation")
    if auth is not None:
        if not isinstance(auth, dict):
            problems.append("work_authorisation: must map a country to a status")
        else:
            for country, status in auth.items():
                if status not in AUTH_VALUES:
                    problems.append(
                        f"work_authorisation.{country}: '{status}' should be one of "
                        + ", ".join(sorted(AUTH_VALUES)))

    locations = profile.get("locations")
    if isinstance(locations, dict):
        for k in ("preferred", "acceptable"):
            if k in locations and not _is_str_list(locations[k]):
                problems.append(f"locations.{k}: must be a list of text")
        adjustments = locations.get("adjustments")
        if adjustments is not None and not isinstance(adjustments, list):
            problems.append("locations.adjustments: must be a list")
            adjustments = []
        for i, adj in enumerate(adjustments or []):
            if (not isinstance(adj, dict) or not isinstance(adj.get("match"), str)
                    or not _is_number(adj.get("delta"))
                    or not isinstance(adj.get("why"), str) or not adj["why"]):
                problems.append(f"locations.adjustments[{i}]: needs match, a numeric delta and why")
    elif locations is not None:
        problems.append("locations: must be a mapping")

    comp = profile.get("compensation")
    if comp is not None:
        if not isinstance(comp, dict):
            problems.append("compensation: must be a mapping")
        elif "floor" in comp and (not _is_number(comp["floor"]) or comp["floor"] < 0):
            problems.append("compensation.floor: must be a number, 0 or more (0 means no floor)")

    report = profile.get("report")
    if report is not None and not isinstance(report, dict):
        problems.append("report: must be a mapping")

    return problems


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_PATH
    try:
        with open(path) as fh:
            profile = yaml.safe_load(fh)
    except FileNotFoundError:
        print(f"No fit profile at {path}; assess-job-fit will use its defaults.")
        return 0
    except (OSError, UnicodeDecodeError) as e:
        print(f"Can't read {path}: {e}", file=sys.stderr)
        return 2
    except yaml.YAMLError as e:
        print(f"PARSE ERROR in {path}: {e}")
        return 1
    if profile is None:
        print(f"{path} is empty; assess-job-fit will use its defaults.")
        return 0
    problems = check(profile)
    if problems:
        for p in problems:
            print(f"{path}: {p}")
        return 1
    print(f"{path}: fit profile OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
