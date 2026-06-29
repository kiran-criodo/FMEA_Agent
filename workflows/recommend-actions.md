# Generate Recommended Actions for High-Risk Items (UC5)

## Purpose
For the high-risk failure modes in a PFMEA, propose **containment, prevention and
detection** actions — drawing on the organisation's past CAPAs / 8D reports / lessons
learned — so every line benefits from the whole organisation's corrective-action history,
not just what the engineer in the room recalls.

## When to use
The user says: "recommend actions", "what should we do about the high-risk rows", "propose
corrective actions", "containment/prevention/detection for these failures".

## Inputs
- An existing PFMEA (`.xlsx` template workbook, or a `rows.json` from UC1). Richer text
  (causes/controls) gives better lessons matching, so prefer the `rows.json` when available.
- The lessons-learned library `resources/lessons-learned.json` (the corrective-action
  memory). Keep it current — add a new entry whenever a real action is proven.

## Steps
1. **Identify the targets.** By default, act on the **triggered** rows (RPN ≥ 200 or
   Severity ≥ 8). Use `--top N` to cap the list, or `--all` to cover every row.
2. **Run the tool** to build the worksheet and retrieve matching lessons:
   `python tools/recommend_actions.py --input <file>` (add `--top`/`--all`/`--rpn`/`--sev`).
   It writes `output/PFMEA-actions-<slug>-<date>.md` (worksheet) and `.json` (scaffold).
3. **Author the actions.** For each row, write tailored **Containment** (immediate, stop
   the bleeding), **Prevention** (reduce occurrence/severity at the cause), and
   **Detection** (catch it earlier / improve the control) actions. Start from the matched
   lessons but adapt them to this process; cite the lesson source (e.g. `8D-2023-014`). If
   a row had no match, author from FMEA first principles **and** add a new lessons entry.
4. **Estimate the revised risk.** Propose target S/O/D after the actions and the resulting
   RPN, so the benefit is visible (mirrors the template's Action Results columns).
5. **Review gate.** Present the proposed actions and wait for engineer approval before
   writing anything back into the workbook.
6. **(Optional) Close the loop.** On approval, write the chosen actions into the
   `recommended_action` field of the `rows.json` and regenerate the workbook with
   `tools/fill_pfmea_template.py` so the Recommended Action(s) column is populated.

## Tools
- `tools/recommend_actions.py` — selects high-risk rows, matches lessons by keyword, and
  writes the worksheet + scaffold. Retrieval only; it does not invent actions.
- `tools/fill_pfmea_template.py` — used in step 6 to write actions back into the template.

## Output
- `output/PFMEA-actions-<slug>-<date>.md` — the worksheet with matched lessons and the
  agent's authored actions.
- `output/PFMEA-actions-<slug>-<date>.json` — scaffold for feeding actions back into the
  workbook.

## Validation (check before showing results)
- Every targeted high-risk row has all three action types (containment / prevention /
  detection) — none left blank.
- Actions are specific to the failure's cause and control, not generic boilerplate.
- Any lesson cited actually matches the failure (don't cite an unrelated source).
- Proposed revised S/O/D is justified and not lower than is credible for the action taken.
- Nothing fabricated: if there is no relevant lesson, say so rather than inventing history.
