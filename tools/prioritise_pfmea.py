#!/usr/bin/env python3
"""Prioritise a PFMEA by RPN and risk triggers (UC4).

Reads an existing PFMEA -- either the Excel workbook (resources/PFMEA-Template.xlsx
format) or a rows.json file produced by the draft-pfmea workflow (UC1) -- computes
RPN = Sev x Occur x Detec for every row, ranks them high-to-low, and applies the risk
triggers (RPN >= threshold OR Severity >= threshold). It writes a ranked action list to
output/ as Markdown (and CSV) and prints a summary.

The agent then writes the plain-language risk narrative on top of this ranked data
(see workflows/prioritise-pfmea.md).

Usage:
  python tools/prioritise_pfmea.py --input output/PFMEA-Battery-Pack-Assembly-2026-06-26.xlsx
  python tools/prioritise_pfmea.py --input output/battery-pack-pfmea-rows.json --out priorities.md
  python tools/prioritise_pfmea.py --input <file> --rpn 200 --sev 8   # override thresholds
"""
import argparse
import csv
import json
import os
import sys
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

# Excel column -> field name (matches the template).
XLSX_COLS = {
    "A": "process", "B": "failure_mode", "C": "effects", "D": "severity",
    "E": "class", "F": "causes", "G": "occurrence", "H": "controls",
    "I": "detection", "K": "recommended_action", "L": "responsibility_date",
}


def slugify(text):
    return ("-".join("".join(c if c.isalnum() else " " for c in text).split())[:40]
            or "pfmea")


def _num(v):
    return v if isinstance(v, (int, float)) else None


def load_from_xlsx(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[MAIN_SHEET]
    rpn_trig = _num(ws["Q5"].value) or DEFAULT_RPN_TRIGGER
    sev_trig = _num(ws["Q6"].value) or DEFAULT_SEV_TRIGGER
    title = ws["B8"].value or os.path.basename(path)
    rows = []
    for rownum in range(FIRST_DATA_ROW, ws.max_row + 1):
        rec = {field: ws[f"{col}{rownum}"].value for col, field in XLSX_COLS.items()}
        # Skip rows with no real content.
        if not str(rec.get("process") or "").strip() and \
           not str(rec.get("failure_mode") or "").strip():
            continue
        rows.append(rec)
    return title, rpn_trig, sev_trig, rows


def load_from_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    title = (data.get("header") or {}).get("item") or os.path.basename(path)
    return title, DEFAULT_RPN_TRIGGER, DEFAULT_SEV_TRIGGER, data.get("rows") or []


def trigger_reason(sev, rpn, rpn_trig, sev_trig):
    reasons = []
    if isinstance(sev, (int, float)) and sev >= sev_trig:
        reasons.append(f"Sev>={int(sev_trig)}")
    if isinstance(rpn, (int, float)) and rpn >= rpn_trig:
        reasons.append(f"RPN>={int(rpn_trig)}")
    return " & ".join(reasons)


def prioritise(rows, rpn_trig, sev_trig):
    ranked = []
    for r in rows:
        sev, occ, det = (_num(r.get("severity")), _num(r.get("occurrence")),
                         _num(r.get("detection")))
        rpn = sev * occ * det if None not in (sev, occ, det) else None
        reason = trigger_reason(sev, rpn, rpn_trig, sev_trig)
        ranked.append({**r, "rpn": rpn, "triggered": bool(reason), "reason": reason})
    # Sort: triggered first, then RPN desc, then Severity desc. None sinks to the bottom.
    ranked.sort(key=lambda x: (
        not x["triggered"],
        -(x["rpn"] if x["rpn"] is not None else -1),
        -(_num(x.get("severity")) or -1),
    ))
    return ranked


def write_reports(title, ranked, rpn_trig, sev_trig, out_md):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_path = out_md if os.path.isabs(out_md) else os.path.join(OUTPUT_DIR, out_md)
    csv_path = os.path.splitext(md_path)[0] + ".csv"

    triggered = [r for r in ranked if r["triggered"]]
    incomplete = [r for r in ranked if r["rpn"] is None]

    lines = []
    lines.append(f"# PFMEA Risk Priorities — {title}")
    lines.append("")
    lines.append(f"_Generated {date.today().isoformat()} · "
                 f"Triggers: RPN ≥ {int(rpn_trig)} or Severity ≥ {int(sev_trig)}_")
    lines.append("")
    lines.append(f"- Rows analysed: **{len(ranked)}**")
    lines.append(f"- Rows requiring mitigation action (triggered): **{len(triggered)}**")
    if incomplete:
        lines.append(f"- Rows with incomplete S/O/D (not ranked): **{len(incomplete)}**")
    lines.append("")
    lines.append("> Plain-language risk narrative — to be written by the agent on top of "
                 "this ranked data (see workflows/prioritise-pfmea.md).")
    lines.append("")
    lines.append("## Ranked action list")
    lines.append("")
    lines.append("| Rank | Process | Failure Mode | S | O | D | RPN | Trigger |")
    lines.append("|------|---------|--------------|---|---|---|-----|---------|")
    for i, r in enumerate(ranked, 1):
        rpn = r["rpn"] if r["rpn"] is not None else "—"
        flag = f"⚠️ {r['reason']}" if r["triggered"] else ""
        lines.append(
            f"| {i} | {r.get('process','') or ''} | {r.get('failure_mode','') or ''} "
            f"| {r.get('severity','') or ''} | {r.get('occurrence','') or ''} "
            f"| {r.get('detection','') or ''} | {rpn} | {flag} |")
    lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["rank", "process", "failure_mode", "severity", "occurrence",
                    "detection", "rpn", "triggered", "trigger_reason"])
        for i, r in enumerate(ranked, 1):
            w.writerow([i, r.get("process", ""), r.get("failure_mode", ""),
                        r.get("severity", ""), r.get("occurrence", ""),
                        r.get("detection", ""), r["rpn"] if r["rpn"] is not None else "",
                        r["triggered"], r["reason"]])
    return md_path, csv_path, triggered, incomplete


def main():
    ap = argparse.ArgumentParser(description="Prioritise a PFMEA by RPN and risk triggers.")
    ap.add_argument("--input", required=True, help="PFMEA .xlsx or rows .json")
    ap.add_argument("--out", help="Output Markdown filename (CSV written alongside).")
    ap.add_argument("--rpn", type=float, help="Override RPN trigger threshold.")
    ap.add_argument("--sev", type=float, help="Override Severity trigger threshold.")
    args = ap.parse_args()

    ext = os.path.splitext(args.input)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        title, rpn_trig, sev_trig, rows = load_from_xlsx(args.input)
    elif ext == ".json":
        title, rpn_trig, sev_trig, rows = load_from_json(args.input)
    else:
        sys.exit(f"Unsupported input type '{ext}'. Use .xlsx or .json.")

    if args.rpn is not None:
        rpn_trig = args.rpn
    if args.sev is not None:
        sev_trig = args.sev
    if not rows:
        sys.exit("No PFMEA rows found in the input.")

    ranked = prioritise(rows, rpn_trig, sev_trig)
    out_md = args.out or f"PFMEA-priorities-{slugify(str(title))}-{date.today().isoformat()}.md"
    md_path, csv_path, triggered, incomplete = write_reports(
        title, ranked, rpn_trig, sev_trig, out_md)

    print(f"Analysed {len(ranked)} row(s). Triggers: RPN >= {int(rpn_trig)} or "
          f"Severity >= {int(sev_trig)}")
    print(f"Wrote ranked report: {md_path}")
    print(f"Wrote CSV:           {csv_path}")
    if incomplete:
        print(f"WARNING: {len(incomplete)} row(s) have incomplete S/O/D and were not ranked.")
    print(f"\nTop priorities ({len(triggered)} triggered):")
    for i, r in enumerate(ranked, 1):
        if not r["triggered"]:
            continue
        print(f"  #{i}: [{r.get('process','')}] {r.get('failure_mode','')} "
              f"(S={r.get('severity')}, RPN={r['rpn']}, {r['reason']})")


if __name__ == "__main__":
    main()
