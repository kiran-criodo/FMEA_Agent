#!/usr/bin/env python3
"""Reuse & propagate Foundation/Family FMEAs (UC2).

Two modes:

  adapt   — pull the right foundation FMEA for a new part, carry its rows into a child
            draft, and (if given a new-part draft to compare against) classify every
            failure mode as reused / genuinely-new / possibly-not-applicable.

  cascade — given a change to a foundation FMEA, find every child derived from it and
            build a propagation worksheet showing which children carry the affected row.

The tool does the deterministic work (match, copy, diff, find children, scaffold). The
agent decides what is genuinely new, authors the change, and gets approval — see
workflows/reuse-fmea.md.

Usage:
  python tools/reuse_fmea.py list
  python tools/reuse_fmea.py adapt --new-part "battery pack, ultrasonic welded" --out child.json
  python tools/reuse_fmea.py adapt --foundation FND-BATTPACK --against newdraft.json --out child.json
  python tools/reuse_fmea.py cascade --foundation FND-BATTPACK --row 4 --change "add vision interlock"
"""
import argparse
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTPUT_DIR = os.path.join(ROOT, "output")
INDEX_PATH = os.path.join(ROOT, "resources", "fmea-family-index.json")


def norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip().lower())


def load_index(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def resolve(p):
    return p if os.path.isabs(p) else os.path.join(ROOT, p)


def load_rows(path):
    with open(resolve(path), encoding="utf-8") as f:
        d = json.load(f)
    return d.get("header", {}), d.get("rows", [])


def find_foundation(index, fid):
    for f in index.get("foundations", []):
        if f["id"] == fid:
            return f
    return None


def match_foundation(desc, foundations):
    text = norm(desc)
    scored = []
    for f in foundations:
        hits = [k for k in f.get("keywords", []) if norm(k) in text]
        scored.append((len(hits), f, hits))
    scored.sort(key=lambda x: -x[0])
    return scored


def cmd_list(index, args):
    print("Foundations:")
    for f in index.get("foundations", []):
        kids = [c for c in index.get("children", []) if c.get("derived_from") == f["id"]]
        print(f"  {f['id']}: {f['name']}  (family: {f.get('family','')}, "
              f"{len(kids)} child FMEA(s))")
    children = index.get("children", [])
    if children:
        print("Children:")
        for c in children:
            print(f"  {c['id']}: {c['name']}  <- {c.get('derived_from')}")


def cmd_adapt(index, args):
    foundations = index.get("foundations", [])
    if args.foundation:
        fnd = find_foundation(index, args.foundation)
        if not fnd:
            sys.exit(f"Foundation '{args.foundation}' not found. Try: list")
    else:
        if not args.new_part:
            sys.exit("Provide --foundation or --new-part for matching.")
        ranked = match_foundation(args.new_part, foundations)
        if not ranked or ranked[0][0] == 0:
            sys.exit("No foundation matched the new-part description. Use 'list' and pass "
                     "--foundation explicitly.")
        fnd = ranked[0][1]
        print(f"Matched foundation: {fnd['id']} ({fnd['name']}) "
              f"on {', '.join(ranked[0][2])}")

    fheader, frows = load_rows(fnd["rows"])

    against_rows, classification = None, None
    if args.against:
        _, against_rows = load_rows(args.against)
        fset = {norm(r.get("failure_mode")): r for r in frows}
        nset = {norm(r.get("failure_mode")): r for r in against_rows}
        reused = [nset[k] for k in nset if k in fset]
        new = [nset[k] for k in nset if k not in fset]
        dropped = [fset[k] for k in fset if k not in nset]
        classification = {"reused": reused, "new": new, "dropped": dropped}

    # Build the child draft: carry foundation rows (tagged), append genuinely-new rows.
    child_rows = []
    for r in frows:
        cr = dict(r)
        cr["origin"] = r.get("origin", f"{fnd['id']}")
        child_rows.append(cr)
    if classification:
        for r in classification["new"]:
            cr = dict(r)
            cr["origin"] = "NEW (part-specific)"
            child_rows.append(cr)

    child_header = dict(fheader)
    child_header["item"] = args.new_part or f"{fnd['name']} — adapted"
    child_header["derived_from"] = fnd["id"]
    child_header.pop("foundation_id", None)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_json = args.out or f"child-{date.today().isoformat()}.json"
    out_json = out_json if os.path.isabs(out_json) else os.path.join(OUTPUT_DIR, out_json)
    json.dump({"header": child_header, "rows": child_rows},
              open(out_json, "w"), indent=2)

    md_path = os.path.splitext(out_json)[0] + "-adaptation.md"
    lines = [f"# FMEA Adaptation Worksheet — {child_header['item']}", "",
             f"_Generated {date.today().isoformat()} · derived from "
             f"**{fnd['id']} ({fnd['name']})**_", "",
             f"Foundation carried over: **{len(frows)} rows**. Draft child FMEA written to "
             f"`{os.path.basename(out_json)}` (each row tagged with its origin).", ""]
    if classification:
        lines += ["## Reconciliation vs the new-part draft", "",
                  f"- **Reused ({len(classification['reused'])})** — failure modes present "
                  f"in both; carry the foundation's ratings/actions, confirm they still apply.",
                  f"- **Genuinely new ({len(classification['new'])})** — in the new part but "
                  f"not the foundation; review and add (already appended to the draft, tagged "
                  f"NEW).",
                  f"- **Possibly not applicable ({len(classification['dropped'])})** — in the "
                  f"foundation but not the new-part draft; confirm whether to keep or remove.",
                  ""]
        for label, key in (("Genuinely new — REVIEW & ADD", "new"),
                           ("Possibly not applicable — CONFIRM", "dropped"),
                           ("Reused — confirm still valid", "reused")):
            lines.append(f"### {label} ({len(classification[key])})")
            for r in classification[key]:
                lines.append(f"- [{r.get('process','')}] {r.get('failure_mode','')}")
            lines.append("")
    else:
        lines += ["## Review checklist (no new-part draft supplied)",
                  "- Walk every carried row: does it apply to the new part as-is, need new "
                  "ratings, or not apply?",
                  "- Add failure modes specific to the new part (consider running UC1 on the "
                  "new part, then re-run `adapt --against <that draft>` to auto-classify).", ""]
    open(md_path, "w").write("\n".join(lines) + "\n")

    print(f"Wrote child draft:        {out_json}")
    print(f"Wrote adaptation worksheet: {md_path}")
    if classification:
        print(f"Reused {len(classification['reused'])} · new "
              f"{len(classification['new'])} · possibly-N/A {len(classification['dropped'])}")
    print(f"\nTo register this child for future cascades, add to "
          f"resources/fmea-family-index.json under 'children' with "
          f"derived_from='{fnd['id']}'.")


def cmd_cascade(index, args):
    fnd = find_foundation(index, args.foundation)
    if not fnd:
        sys.exit(f"Foundation '{args.foundation}' not found. Try: list")
    fheader, frows = load_rows(fnd["rows"])
    children = [c for c in index.get("children", [])
                if c.get("derived_from") == args.foundation]

    changed = None
    if args.row:
        if not (1 <= args.row <= len(frows)):
            sys.exit(f"--row {args.row} out of range (1..{len(frows)}).")
        changed = frows[args.row - 1]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_md = args.out or f"cascade-{args.foundation}-{date.today().isoformat()}.md"
    md_path = out_md if os.path.isabs(out_md) else os.path.join(OUTPUT_DIR, out_md)

    lines = [f"# FMEA Change Propagation — {fnd['id']} ({fnd['name']})", "",
             f"_Generated {date.today().isoformat()}_", ""]
    if changed:
        lines += [f"**Changed foundation row {args.row}:** [{changed.get('process','')}] "
                  f"{changed.get('failure_mode','')}",
                  f"- Change requested: {args.change or '(describe the change)'}", ""]
    lines.append(f"## Affected children ({len(children)})")
    if not children:
        lines.append("- none registered yet (add children to the family index).")
    for c in children:
        _, crows = load_rows(c["rows"]) if os.path.exists(resolve(c["rows"])) else ({}, [])
        present = None
        if changed:
            key = norm(changed.get("failure_mode"))
            present = any(norm(r.get("failure_mode")) == key for r in crows)
        status = ("" if present is None
                  else " — **carries the affected row → apply**" if present
                  else " — affected row not found → verify")
        lines.append(f"- **{c['id']}** ({c['name']}) · `{c['rows']}`{status}")
    lines += ["", "## Action (agent + approval)",
              "- For each affected child, apply the approved change, re-rate if needed "
              "(UC3), and regenerate its workbook. Record the propagation so it is auditable.",
              ""]
    open(md_path, "w").write("\n".join(lines) + "\n")
    print(f"Foundation {args.foundation}: {len(children)} child FMEA(s).")
    print(f"Wrote propagation worksheet: {md_path}")
    for c in children:
        print(f"  - {c['id']}: {c['name']}")


def main():
    ap = argparse.ArgumentParser(description="Reuse & propagate Foundation/Family FMEAs.")
    ap.add_argument("mode", choices=["list", "adapt", "cascade"])
    ap.add_argument("--index", default=INDEX_PATH)
    ap.add_argument("--foundation", help="Foundation FMEA id.")
    ap.add_argument("--new-part", help="New-part description (for adapt / matching).")
    ap.add_argument("--against", help="A new-part rows.json to diff against the foundation.")
    ap.add_argument("--row", type=int, help="Foundation row number changed (for cascade).")
    ap.add_argument("--change", help="Description of the change (for cascade).")
    ap.add_argument("--out", help="Output filename.")
    args = ap.parse_args()

    index = load_index(args.index)
    if args.mode == "list":
        cmd_list(index, args)
    elif args.mode == "adapt":
        cmd_adapt(index, args)
    elif args.mode == "cascade":
        cmd_cascade(index, args)


if __name__ == "__main__":
    main()
