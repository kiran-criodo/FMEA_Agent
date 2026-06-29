#!/usr/bin/env python3
"""Generate a recommended-action worksheet for high-risk PFMEA rows (UC5).

Selects the high-risk rows from a PFMEA (the triggered ones by default), retrieves the
most relevant past corrective actions from the lessons-learned library
(resources/lessons-learned.json) by keyword match, and writes an action worksheet to
output/. The agent then authors the tailored Containment / Prevention / Detection actions
on top of the matched lessons (see workflows/recommend-actions.md).

This tool does retrieval + scaffolding only; it does NOT invent actions.

Usage:
  python tools/recommend_actions.py --input output/battery-pack-pfmea-rows.json
  python tools/recommend_actions.py --input output/PFMEA-Foo.xlsx --top 10
  python tools/recommend_actions.py --input <file> --all          # every row, not just triggered
"""
import argparse
import json
import os
import re
import sys
from datetime import date

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl is required. Run:  pip install -r requirements.txt")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTPUT_DIR = os.path.join(ROOT, "output")
DEFAULT_LESSONS = os.path.join(ROOT, "resources", "lessons-learned.json")
MAIN_SHEET = "PFMEA and Parameters"
FIRST_DATA_ROW = 14
DEFAULT_RPN_TRIGGER = 200
DEFAULT_SEV_TRIGGER = 8
XLSX_COLS = {
    "A": "process", "B": "failure_mode", "C": "effects", "D": "severity",
    "E": "class", "F": "causes", "G": "occurrence", "H": "controls",
    "I": "detection", "K": "recommended_action", "L": "responsibility_date",
}


def _num(v):
    return v if isinstance(v, (int, float)) else None


def slugify(text):
    return ("-".join("".join(c if c.isalnum() else " " for c in text).split())[:40]
            or "pfmea")


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
        rows.append(rec)
    return title, rpn_t, sev_t, rows


def load_from_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    title = (data.get("header") or {}).get("item") or os.path.basename(path)
    return title, DEFAULT_RPN_TRIGGER, DEFAULT_SEV_TRIGGER, data.get("rows") or []


def load_lessons(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("lessons", [])


def row_text(r):
    parts = [r.get(k, "") for k in ("process", "failure_mode", "effects", "causes",
                                    "controls")]
    return " ".join(str(p) for p in parts if p).lower()


def match_lessons(r, lessons, top=3):
    text = row_text(r)
    scored = []
    for L in lessons:
        hits = [kw for kw in L.get("keywords", []) if kw.lower() in text]
        if hits:
            scored.append((len(hits), L, hits))
    scored.sort(key=lambda x: -x[0])
    return scored[:top]


def select_rows(rows, rpn_t, sev_t, include_all, top):
    enriched = []
    for r in rows:
        sev, occ, det = (_num(r.get("severity")), _num(r.get("occurrence")),
                         _num(r.get("detection")))
        rpn = sev * occ * det if None not in (sev, occ, det) else None
        triggered = bool((sev and sev >= sev_t) or (rpn and rpn >= rpn_t))
        enriched.append({**r, "rpn": rpn, "triggered": triggered})
    enriched.sort(key=lambda x: (-(x["rpn"] if x["rpn"] is not None else -1),
                                 -(_num(x.get("severity")) or -1)))
    if include_all:
        chosen = enriched
    else:
        chosen = [r for r in enriched if r["triggered"]]
    if top:
        chosen = chosen[:top]
    return chosen


def write_worksheet(title, chosen, lessons, rpn_t, sev_t, out_md):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_path = out_md if os.path.isabs(out_md) else os.path.join(OUTPUT_DIR, out_md)
    json_path = os.path.splitext(md_path)[0] + ".json"

    lines = [f"# Recommended Actions Worksheet — {title}", "",
             f"_Generated {date.today().isoformat()} · {len(chosen)} high-risk row(s) · "
             f"triggers RPN ≥ {int(rpn_t)} or Severity ≥ {int(sev_t)}_", "",
             "For each row below: matched lessons are retrieved from "
             "`resources/lessons-learned.json`. The agent writes the tailored "
             "**Containment / Prevention / Detection** actions and a revised S/O/D target.",
             ""]
    scaffold = []
    for i, r in enumerate(chosen, 1):
        sev, occ, det, rpn = (r.get("severity"), r.get("occurrence"),
                              r.get("detection"), r["rpn"])
        matches = match_lessons(r, lessons)
        lines.append(f"## {i}. [{r.get('process','')}] {r.get('failure_mode','')}")
        lines.append(f"- **S/O/D = {sev}/{occ}/{det} · RPN = "
                     f"{rpn if rpn is not None else '—'}**"
                     f"{' · ⚠ triggered' if r['triggered'] else ''}")
        if r.get("causes"):
            lines.append(f"- Causes: {r.get('causes')}")
        if r.get("controls"):
            lines.append(f"- Current controls: {r.get('controls')}")
        lines.append("")
        if matches:
            lines.append("**Matched lessons (candidate actions to tailor):**")
            for score, L, hits in matches:
                lines.append(f"- _{L['source']} — {L['title']}_ "
                             f"(match: {', '.join(hits)})")
                lines.append(f"    - Containment: {L['containment']}")
                lines.append(f"    - Prevention: {L['prevention']}")
                lines.append(f"    - Detection: {L['detection']}")
        else:
            lines.append("**Matched lessons:** none — author actions from FMEA first "
                         "principles and add a new lessons-learned entry.")
        lines.append("")
        lines.append("**Recommended actions (agent to complete):**")
        lines.append("- Containment: _(to be completed)_")
        lines.append("- Prevention: _(to be completed)_")
        lines.append("- Detection: _(to be completed)_")
        lines.append("- Revised target S/O/D → RPN: _(to be completed)_")
        lines.append("")
        scaffold.append({
            "process": r.get("process", ""), "failure_mode": r.get("failure_mode", ""),
            "severity": sev, "occurrence": occ, "detection": det, "rpn": rpn,
            "matched_lessons": [L["source"] for _, L, _ in matches],
            "recommended_action": "", "responsibility_date": "",
        })

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"title": title, "rows": scaffold}, f, indent=2)
    return md_path, json_path


def main():
    ap = argparse.ArgumentParser(description="Recommend actions for high-risk PFMEA rows.")
    ap.add_argument("--input", required=True, help="PFMEA .xlsx or rows .json")
    ap.add_argument("--lessons", default=DEFAULT_LESSONS, help="Lessons-learned JSON.")
    ap.add_argument("--out", help="Output Markdown filename.")
    ap.add_argument("--rpn", type=float, help="Override RPN trigger.")
    ap.add_argument("--sev", type=float, help="Override Severity trigger.")
    ap.add_argument("--top", type=int, help="Limit to the top N high-risk rows.")
    ap.add_argument("--all", action="store_true", help="Include all rows, not just triggered.")
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

    lessons = load_lessons(args.lessons)
    chosen = select_rows(rows, rpn_t, sev_t, args.all, args.top)
    if not chosen:
        sys.exit("No rows selected. Use --all or --top, or lower the thresholds.")
    out_md = args.out or f"PFMEA-actions-{slugify(str(title))}-{date.today().isoformat()}.md"
    md_path, json_path = write_worksheet(title, chosen, lessons, rpn_t, sev_t, out_md)

    print(f"Selected {len(chosen)} high-risk row(s); lessons library: "
          f"{len(lessons)} entries.")
    print(f"Wrote worksheet: {md_path}")
    print(f"Wrote scaffold:  {json_path}")
    for i, r in enumerate(chosen, 1):
        m = [L['source'] for _, L, _ in match_lessons(r, lessons)]
        print(f"  {i}. [{r.get('process','')}] {r.get('failure_mode','')} "
              f"(RPN={r['rpn']}) — lessons: {', '.join(m) if m else 'none'}")


if __name__ == "__main__":
    main()
