#!/usr/bin/env python3
"""Put the archive data back into index.html.

index.html holds one line that starts "const DATA = ". This script rebuilds
that line from three files, and changes nothing else on the page:

  data/lecturers.json   the 54 lecturer profiles (every field kept as stored)
  data/schedule.json    the 108 dated classes
  data/summary.json     the module subject counts and the home page stats

Run from anywhere:  python3 scripts/build_archive.py
Standard library only. If a data file has an error, the page is not written.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAGE = ROOT / "index.html"
MARK = "const DATA = "


class DataError(ValueError):
    pass


def load(name, kind):
    try:
        obj = json.loads((DATA / name).read_text(encoding="utf-8"))
    except json.JSONDecodeError as err:
        raise DataError(f"{name} is not valid JSON: {err}") from None
    if not isinstance(obj, kind) or not obj:
        raise DataError(f"{name} must be a non-empty {kind.__name__}")
    return obj


def check(items, name, required):
    for n, item in enumerate(items, 1):
        label = item.get("name") or item.get("date") or f"item {n}"
        missing = [k for k in required if str(item.get(k) if item.get(k) is not None else "").strip() == ""]
        if missing:
            raise DataError(f"{name}, {label}: missing {', '.join(missing)}")


def main():
    lecturers = load("lecturers.json", list)
    schedule = load("schedule.json", list)
    summary = load("summary.json", dict)
    check(lecturers, "lecturers.json", ("name", "slug", "category"))
    check(schedule, "schedule.json", ("date", "disp", "module", "subject", "lecturer", "lslug", "type"))
    for k in ("modules", "stats"):
        if k not in summary:
            raise DataError(f"summary.json must have '{k}'")

    slugs = {l["slug"] for l in lecturers}
    for c in schedule:
        if c["lslug"] not in slugs:
            raise DataError(f"schedule.json, {c['date']} {c['subject']}: lecturer slug "
                            f"'{c['lslug']}' is not in lecturers.json")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c["date"])):
            raise DataError(f"schedule.json: date must look like 2025-07-11, got {c['date']!r}")

    data = {"lecturers": lecturers, "schedule": schedule,
            "modules": summary["modules"], "stats": summary["stats"]}
    line = MARK + json.dumps(data, ensure_ascii=False) + ";"

    page = PAGE.read_text(encoding="utf-8")
    pattern = re.compile(r"^const DATA = .*?;$", re.M)
    if len(pattern.findall(page)) != 1:
        raise DataError("index.html: expected exactly one 'const DATA = ...;' line")
    new = pattern.sub(lambda m: line, page, count=1)
    if new != page:
        PAGE.write_text(new, encoding="utf-8")
    print(f"Built: {len(lecturers)} lecturers, {len(schedule)} classes. "
          f"index.html {'updated' if new != page else 'already up to date'}.")


if __name__ == "__main__":
    try:
        main()
    except DataError as err:
        sys.exit(f"Build stopped, index.html was not changed: {err}")
