#!/usr/bin/env python3
"""Fill the company PFMEA Excel template from a JSON file of header + rows.

Used by the `draft-pfmea` workflow (UC1). The agent drafts the PFMEA content (failure
modes, effects, causes, S/O/D, etc.) and hands this tool a JSON file; the tool writes it
into `resources/PFMEA-Template.xlsx` and saves a copy to `output/`. RPN is computed by
the sheet's own formula (Sev x Occur x Detec); this tool also checks it in Python.

Usage:
  python tools/fill_pfmea_template.py --print-schema
  python tools/fill_pfmea_template.py --show-scales
  python tools/fill_pfmea_template.py --input rows.json --out PFMEA-<slug>-<date>.xlsx

The cell map matches resources/PFMEA-Template.xlsx (sheet "PFMEA and Parameters"):
  Header  Item=B8  Description=B9  Responsibility=H8  Prepared by=H9  Core Team=B10
          FMEA number=M8  Page=M9  Date(Orig)=M10 Rev=P10  Date(Cur)=M11 Rev=P11
  Table   row 14+ : A Process | B Failure Mode | C Effects | D Sev | E Class |
          F Causes | G Occur | H Controls | I Detec | J RPN(formula) | K Rec. Action |
          L Responsibility/Date | M..Q Action Results (left for later)
  Params  RPN trigger=Q5  Severity trigger=Q6
"""
import argparse
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
DEFAULT_TEMPLATE = os.path.join(ROOT, "resources", "PFMEA-Template.xlsx")
OUTPUT_DIR = os.path.join(ROOT, "output")
MAIN_SHEET = "PFMEA and Parameters"

FIRST_DATA_ROW = 14
# Column letter for each row field, in template order.
ROW_COLS = {
    "process": "A",
    "failure_mode": "B",
    "effects": "C",
    "severity": "D",
    "class": "E",
    "causes": "F",
    "occurrence": "G",
    "controls": "H",
    "detection": "I",
    # J = RPN formula (set automatically)
    "recommended_action": "K",
    "responsibility_date": "L",
}
HEADER_CELLS = {
    "item": "B8",
    "description": "B9",
    "responsibility": "H8",
    "prepared_by": "H9",
    "core_team": "B10",
    "fmea_number": "M8",
    "page": "M9",
    "date_orig": "M10",
    "rev_orig": "P10",
    "date_cur": "M11",
    "rev_cur": "P11",
}

SCHEMA_EXAMPLE = {
    "header": {
        "item": "<Product Part Number(s)>",
        "description": "<Product Description>",
        "responsibility": "<Responsible Engineer>",
        "prepared_by": "",
        "core_team": "",
        "fmea_number": "",
        "page": "",
        "date_orig": "",
        "rev_orig": "",
        "date_cur": "",
        "rev_cur": "",
    },
    "rows": [
        {
            "process": "Op 20 – Press-fit bearing into housing",
            "failure_mode": "Bearing under-pressed (not fully seated)",
            "effects": "Axial play in assembly; premature bearing wear; field noise",
            "severity": 7,
            "class": "",
            "causes": "Press force set too low; worn press tooling",
            "occurrence": 3,
            "controls": "Press monitors force-vs-distance; 100% in-line check",
            "detection": 4,
            "recommended_action": "",
            "responsibility_date": "",
        }
    ],
}


def slugify(text):
    keep = "-".join("".join(c if c.isalnum() else " " for c in text).split())
    return keep[:40] or "pfmea"


def read_thresholds(ws):
    rpn = ws["Q5"].value
    sev = ws["Q6"].value
    return (rpn if isinstance(rpn, (int, float)) else 200,
            sev if isinstance(sev, (int, float)) else 8)


def show_scales(template):
    wb = openpyxl.load_workbook(template, data_only=True)
    ws = wb["Assumptions"]
    print("Calibrated 1-10 rating scales (source: Assumptions sheet)\n")
    section = None
    for row in ws.iter_rows(values_only=True):
        label, num, desc = (list(row) + [None, None, None])[:3]
        text = " ".join(str(x) for x in (label, num, desc) if x not in (None, ""))
        if not text.strip():
            continue
        head = str(label or "")
        if head.startswith(("Severity", "Occurrence", "Detection")):
            section = head.split(":")[0]
            print(f"\n## {section}")
            continue
        if isinstance(num, (int, float)):
            anchor = f"  {int(num):>2}: {desc or ''}".rstrip()
            note = f"   ({label})" if label else ""
            print(anchor + note)


def validate(rows):
    problems = []
    for i, r in enumerate(rows, 1):
        for f in ("process", "failure_mode", "effects", "causes"):
            if not str(r.get(f, "")).strip():
                problems.append(f"Row {i}: missing '{f}'")
        for f in ("severity", "occurrence", "detection"):
            v = r.get(f)
            if not isinstance(v, (int, float)) or not (1 <= v <= 10):
                problems.append(f"Row {i}: '{f}'={v!r} must be an integer 1-10")
    return problems


def fill(template, data, out_name):
    wb = openpyxl.load_workbook(template)
    ws = wb[MAIN_SHEET]
    rpn_trig, sev_trig = read_thresholds(ws)

    # Header
    for key, value in (data.get("header") or {}).items():
        if key in HEADER_CELLS and str(value).strip():
            ws[HEADER_CELLS[key]] = value

    rows = data.get("rows") or []
    problems = validate(rows)
    if problems:
        sys.exit("Input validation failed:\n  - " + "\n  - ".join(problems))

    triggered = []
    for idx, r in enumerate(rows):
        rownum = FIRST_DATA_ROW + idx
        for field, col in ROW_COLS.items():
            val = r.get(field, "")
            if val != "":
                ws[f"{col}{rownum}"] = val
        # RPN formula, mirroring the template
        ws[f"J{rownum}"] = f"=D{rownum}*G{rownum}*I{rownum}"
        ws[f"Q{rownum}"] = f"=IF(N{rownum}*O{rownum}*P{rownum}>0,N{rownum}*O{rownum}*P{rownum},J{rownum})"
        sev = r.get("severity", 0)
        rpn = sev * r.get("occurrence", 0) * r.get("detection", 0)
        if rpn >= rpn_trig or sev >= sev_trig:
            triggered.append((rownum, r.get("process", ""), r.get("failure_mode", ""),
                              sev, rpn))

    # Clear any leftover template rows below the data we wrote, up to row 39.
    for rownum in range(FIRST_DATA_ROW + len(rows), 40):
        for col in list(ROW_COLS.values()) + ["J", "Q"]:
            ws[f"{col}{rownum}"] = None

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = out_name if os.path.isabs(out_name) else os.path.join(OUTPUT_DIR, out_name)
    wb.save(out_path)

    print(f"Wrote {len(rows)} row(s) to: {out_path}")
    print(f"Risk triggers: RPN >= {int(rpn_trig)} or Severity >= {int(sev_trig)}")
    if triggered:
        print(f"\n{len(triggered)} row(s) require mitigation action:")
        for rownum, proc, fm, sev, rpn in triggered:
            print(f"  row {rownum}: [{proc}] {fm}  (Sev={sev}, RPN={rpn})")
    else:
        print("No rows crossed a risk threshold.")
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Fill the PFMEA Excel template from JSON.")
    ap.add_argument("--input", help="Path to JSON file with 'header' and 'rows'.")
    ap.add_argument("--out", help="Output filename (saved under output/ if not absolute).")
    ap.add_argument("--template", default=DEFAULT_TEMPLATE, help="Template .xlsx path.")
    ap.add_argument("--print-schema", action="store_true", help="Print example JSON and exit.")
    ap.add_argument("--show-scales", action="store_true", help="Print S/O/D scales and exit.")
    args = ap.parse_args()

    if args.print_schema:
        print(json.dumps(SCHEMA_EXAMPLE, indent=2))
        return
    if args.show_scales:
        show_scales(args.template)
        return
    if not args.input:
        ap.error("--input is required (or use --print-schema / --show-scales)")

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)
    out_name = args.out
    if not out_name:
        slug = slugify(str((data.get("header") or {}).get("item", "")) or "pfmea")
        out_name = f"PFMEA-{slug}-{date.today().isoformat()}.xlsx"
    fill(args.template, data, out_name)


if __name__ == "__main__":
    main()
