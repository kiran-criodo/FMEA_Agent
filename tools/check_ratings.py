#!/usr/bin/env python3
"""Sanity-check S/O/D ratings in a PFMEA (UC3, deterministic half).

Runs the mechanical consistency checks on an existing PFMEA and writes a findings report.
The agent then does the scale-anchored judgment on top (does each rating fit the calibrated
1-10 anchor for that effect?) — see workflows/check-ratings.md.

Checks performed here:
  ERROR   RANGE       — S/O/D missing or not an integer in 1..10
  ERROR   ARITHMETIC  — a stated/cached RPN that does not equal Sev x Occur x Detec
  WARN    INCONSISTENT— identical failure-mode text rated with different S, O or D
  WARN    NO-ACTION   — a triggered row (RPN>=trigger or Sev>=trigger) with no recommended action

Input: a rows .json (optional per-row "rpn_stated") or a template .xlsx (reads the cached
RPN in column J when present).

Usage:
  python tools/check_ratings.py --input output/battery-pack-pfmea-rows.json
  python tools/check_ratings.py --input output/PFMEA-Foo.xlsx
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required. Run:  pip install -r requirements.txt")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTPUT_DIR = os.path.join(ROOT, "output")
MAIN_SHEET = "PFMEA and Parameters"
FIRST_DATA_ROW = 14
DEFAULT_RPN_TRIGGER = 200
DEFAULT_SEV_TRIGGER = 8
XLSX_COLS = {
    "A": "process", "B": "failure_mode", "C": "effects", "D": "severity",
    "E": "class", "F": "causes", "G": "occurrence", "H": "controls",
    "I": "detection", "K": "recommended_action",
}


def _num(v):
    return v if isinstance(v, (int, float)) else None


def slugify(text):
    return ("-".join("".join(c if c.isalnum() else " " for c in text).split())[:40]
            or "pfmea")


def norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def load_from_xlsx(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[MAIN_SHEET]
    rpn_t = _num(ws["Q5"].value) or DEFAULT_RPN_TRIGGER
    sev_t = _num(ws["Q6"].value) or DEFAULT_SEV_TRIGGER
    title = ws["B8"].value or os.path.basename(path)
    rows = []
    for rn in range(FIRST_DATA_ROW, ws.max_row + 1):
        rec = {f: ws[f"{c}{rn}"].value for c, f in XLSX_COLS.items()}
        if not str(rec.get("process") or "").strip() and \
           not str(rec.get("failure_mode") or "").strip():
            continue
        rec["rpn_stated"] = _num(ws[f"J{rn}"].value)   # cached formula value, if any
        rec["_row"] = rn
        rows.append(rec)
    return title, rpn_t, sev_t, rows


def load_from_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    title = (data.get("header") or {}).get("item") or os.path.basename(path)
    rows = data.get("rows") or []
    for i, r in enumerate(rows):
        r["_row"] = i + 1
    return title, DEFAULT_RPN_TRIGGER, DEFAULT_SEV_TRIGGER, rows


def check(rows, rpn_t, sev_t):
    findings = {"range": [], "arithmetic": [], "inconsistent": [], "no_action": []}

    for r in rows:
        sev, occ, det = (_num(r.get("severity")), _num(r.get("occurrence")),
                         _num(r.get("detection")))
        label = f"row {r['_row']} [{r.get('process','')}] {r.get('failure_mode','')}"

        # RANGE
        bad = []
        for name, v in (("Sev", sev), ("Occ", occ), ("Det", det)):
            if v is None:
                bad.append(f"{name}=missing")
            elif not (isinstance(v, int) and 1 <= v <= 10):
                bad.append(f"{name}={v}")
        if bad:
            findings["range"].append(f"{label}: {', '.join(bad)}")

        # ARITHMETIC
        stated = _num(r.get("rpn_stated"))
        if None not in (sev, occ, det) and stated is not None:
            calc = sev * occ * det
            if stated != calc:
                findings["arithmetic"].append(
                    f"{label}: stated RPN {stated} != Sev*Occ*Det "
                    f"({sev}x{occ}x{det} = {calc})")

        # NO-ACTION on a triggered row
        rpn = sev * occ * det if None not in (sev, occ, det) else None
        triggered = (sev is not None and sev >= sev_t) or (rpn is not None and rpn >= rpn_t)
        if triggered and not str(r.get("recommended_action") or "").strip():
            findings["no_action"].append(f"{label}: triggered (Sev={sev}, RPN={rpn}) "
                                         f"but no recommended action")

    # INCONSISTENT: identical failure-mode text rated differently
    groups = defaultdict(list)
    for r in rows:
        key = norm(r.get("failure_mode"))
        if key:
            groups[key].append(r)
    for key, grp in groups.items():
        if len(grp) < 2:
            continue
        for field, lbl in (("severity", "Sev"), ("occurrence", "Occ"), ("detection", "Det")):
            vals = {_num(r.get(field)) for r in grp}
            vals.discard(None)
            if len(vals) > 1:
                rowlist = ", ".join(f"row {r['_row']}={_num(r.get(field))}" for r in grp)
                findings["inconsistent"].append(
                    f"\"{grp[0].get('failure_mode')}\" — {lbl} differs across rows: {rowlist}")
    return findings


def write_report(title, findings, rpn_t, sev_t, n_rows, out_md):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_path = out_md if os.path.isabs(out_md) else os.path.join(OUTPUT_DIR, out_md)
    total = sum(len(v) for v in findings.values())
    sections = [
        ("Arithmetic errors (RPN ≠ Sev×Occur×Detec)", "arithmetic"),
        ("Out-of-range / missing ratings", "range"),
        ("Inconsistent ratings (same failure mode, different S/O/D)", "inconsistent"),
        ("Triggered rows with no recommended action", "no_action"),
    ]
    lines = [f"# Rating Sanity-Check — {title}", "",
             f"_Generated {date.today().isoformat()} · {n_rows} rows · "
             f"triggers RPN ≥ {int(rpn_t)} or Severity ≥ {int(sev_t)}_", "",
             f"**{total} mechanical finding(s).** Scale-anchored judgment (does each rating "
             f"fit the calibrated 1–10 anchor for its effect?) is added by the agent — see "
             f"workflows/check-ratings.md.", ""]
    for header, key in sections:
        items = findings[key]
        lines.append(f"## {header} — {len(items)}")
        if items:
            lines += [f"- {x}" for x in items]
        else:
            lines.append("- none")
        lines.append("")
    lines.append("## Scale-anchored review (agent to complete)")
    lines.append("- _For each flagged row (and any rating that looks mismatched to its "
                 "effect), note the calibrated-scale anchor, whether the rating fits, and a "
                 "suggested correction with rationale._")
    lines.append("")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return md_path, total


def main():
    ap = argparse.ArgumentParser(description="Sanity-check S/O/D ratings in a PFMEA.")
    ap.add_argument("--input", required=True, help="PFMEA .xlsx or rows .json")
    ap.add_argument("--out", help="Output Markdown filename.")
    ap.add_argument("--rpn", type=float, help="Override RPN trigger.")
    ap.add_argument("--sev", type=float, help="Override Severity trigger.")
    args = ap.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        title, rpn_t, sev_t, rows = load_from_xlsx(args.input)
    elif ext == ".json":
        title, rpn_t, sev_t, rows = load_from_json(args.input)
    else:
        sys.exit(f"Unsupported input type '{ext}'. Use .xlsx or .json.")
    if args.rpn is not None:
        rpn_t = args.rpn
    if args.sev is not None:
        sev_t = args.sev

    findings = check(rows, rpn_t, sev_t)
    out_md = args.out or f"PFMEA-rating-check-{slugify(str(title))}-{date.today().isoformat()}.md"
    md_path, total = write_report(title, findings, rpn_t, sev_t, len(rows), out_md)

    print(f"Checked {len(rows)} row(s). {total} mechanical finding(s).")
    for key, label in (("arithmetic", "Arithmetic errors"), ("range", "Range/missing"),
                       ("inconsistent", "Inconsistent ratings"),
                       ("no_action", "Triggered, no action")):
        print(f"  {label}: {len(findings[key])}")
    print(f"Wrote report: {md_path}")


if __name__ == "__main__":
    main()
