"""Validate data/features.csv as an SCD Type 2 table."""
import csv, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLS = ["id", "lab", "group", "feature", "category", "change_type", "status",
        "description", "valid_from", "valid_to", "is_current", "source_url"]
ENUMS = {
    "group": {"frontier", "media", "fast-follower", "emerging"},
    "category": {"model", "consumer-app", "agent", "developer", "enterprise", "media", "voice", "hardware", "other"},
    "change_type": {"new", "changed", "retired"},
    "status": {"preview", "beta", "ga", "deprecated", "retired"},
    "is_current": {"true", "false"},
}
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
lab_rows = list(csv.DictReader(open(ROOT / "data/labs.csv")))
labs = {r["lab"] for r in lab_rows}
for r in lab_rows:
    if r.get("group") not in ENUMS["group"] or r.get("active") not in {"true", "false"} or not DATE.match(r.get("added_on") or ""):
        sys.exit(f"bad labs.csv row: {r['lab']}")
reader = csv.DictReader(open(ROOT / "data/features.csv"))
errors = []
if reader.fieldnames != COLS:
    sys.exit(f"bad header: {reader.fieldnames}")

by_id = defaultdict(list)
for n, r in enumerate(reader, start=2):
    for k, allowed in ENUMS.items():
        if r[k] not in allowed:
            errors.append(f"line {n}: {k}={r[k]!r}")
    if r["lab"] not in labs:
        errors.append(f"line {n}: unknown lab {r['lab']!r}")
    if not DATE.match(r["valid_from"]) or (r["valid_to"] and not DATE.match(r["valid_to"])):
        errors.append(f"line {n}: bad date")
    if not r["source_url"].startswith("http"):
        errors.append(f"line {n}: missing source_url")
    by_id[r["id"]].append((n, r))

for fid, rs in by_id.items():
    rs.sort(key=lambda x: x[1]["valid_from"])
    current = [n for n, r in rs if r["is_current"] == "true"]
    if len(current) != 1:
        errors.append(f"{fid}: {len(current)} current rows (lines {current})")
    for (n, a), (_, b) in zip(rs, rs[1:]):
        if a["is_current"] == "true" or a["valid_to"] != b["valid_from"]:
            errors.append(f"{fid}: line {n} not closed to {b['valid_from']}")
    if rs[-1][1]["valid_to"]:
        errors.append(f"{fid}: latest row has valid_to")

if errors:
    print("\n".join(errors))
    sys.exit(f"{len(errors)} errors")
print(f"ok: {sum(map(len, by_id.values()))} rows, {len(by_id)} features")
