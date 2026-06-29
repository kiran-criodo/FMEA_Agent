# tools/

Small Python scripts the FMEA workflows call. Each does the deterministic work (parse the
Excel template, compute RPN, match records, write files) so the agent can focus on
judgment. They read/write the rows-JSON and the Excel template; none need secrets.

Run them from the repo root with the venv active (`source .venv/bin/activate`).

| Script | Used by | What it does |
|--------|---------|--------------|
| `fill_pfmea_template.py` | UC1 | Fills `resources/PFMEA-Template.xlsx` from a rows JSON and saves a workbook to `output/`. Also `--show-scales` (print the calibrated S/O/D scales) and `--print-schema` (print the rows JSON shape). |
| `reuse_fmea.py` | UC2 | `list` / `adapt` / `cascade` over the FMEA family index — match a foundation, carry it into a child draft, classify reused/new/dropped, and find children affected by a change. |
| `check_ratings.py` | UC3 | Sanity-checks ratings: RPN arithmetic, out-of-range/missing, inconsistent ratings across identical failure modes, triggered rows with no action. |
| `prioritise_pfmea.py` | UC4 | Computes RPN, ranks rows, applies the risk triggers, and writes a ranked action list (Markdown + CSV). |
| `recommend_actions.py` | UC5 | Selects high-risk rows, retrieves matching lessons from `resources/lessons-learned.json`, and writes an action worksheet to author from. |

Common conventions:
- Input is either a rows JSON (`{"header": {...}, "rows": [...]}`) or the Excel workbook.
- Risk thresholds (RPN ≥ 200, Severity ≥ 8) are read from the template's Parameters block.
- Each script prints a clear summary and writes its full output under `output/`.
- New Python dependencies go in `requirements.txt`.
