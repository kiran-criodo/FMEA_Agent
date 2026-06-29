# Prioritise a PFMEA by RPN & Risk Triggers (UC4)

## Purpose
Take a completed (or draft) PFMEA, compute RPN for every line, rank by risk, apply the
template's trigger rules (RPN ≥ 200, Severity ≥ 8), and produce a ranked action list with
a short plain-language risk narrative — instant, consistent triage across many rows.

## When to use
The user says: "prioritise this PFMEA", "rank by RPN", "what's high risk", "what needs
action", "triage these failure modes".

## Inputs
- An existing PFMEA, as either:
  - the Excel workbook in the template format (e.g. a file in `output/` or `resources/`), or
  - a `rows.json` produced by `draft-pfmea` (UC1).
- Optional: override thresholds if the user asks (defaults come from the workbook's
  Parameters block: RPN ≥ 200, Severity ≥ 8).

## Steps
1. **Locate the PFMEA.** Confirm which file to analyse if not given.
2. **Run the tool** to compute RPN, rank, and flag triggers:
   `python tools/prioritise_pfmea.py --input <file>` (add `--rpn`/`--sev` to override).
   It writes a ranked Markdown report + CSV to `output/` and prints the top priorities.
3. **Sanity-check the data.** If the tool warns about rows with incomplete S/O/D, tell
   the user those rows could not be ranked and offer to fix them (UC1/UC3) first.
4. **Write the risk narrative.** Read the ranked report and write a short, plain-language
   summary at the top of the report file (replace the placeholder line). Cover:
   - how many rows cross a trigger and *why* (severity-driven vs RPN-driven);
   - the top handful of items in priority order, each in one sentence an engineer/manager
     can act on (what fails, what the consequence is, what to look at);
   - any themes (e.g. several high-severity items concentrated in one operation);
   - what to tackle first.
   Do **not** invent new ratings or failure modes here — narrate what the data shows.
5. **Present** the ranked list (top items) and the narrative, and give the file paths.

## Tool
- `tools/prioritise_pfmea.py` — reads `.xlsx` or `.json`, computes RPN = Sev × Occur ×
  Detec, ranks (triggered first, then RPN desc, then Severity desc), applies thresholds,
  and writes `output/PFMEA-priorities-<slug>-<date>.md` and `.csv`.

## Output
- `output/PFMEA-priorities-<slug>-<date>.md` — ranked action list + the agent's narrative.
- `output/PFMEA-priorities-<slug>-<date>.csv` — same ranking as data.

## Validation (check before showing results)
- Row count in the report matches the number of populated rows in the source PFMEA.
- For a few spot-checked rows, RPN in the report equals Sev × Occur × Detec.
- Every row with Severity ≥ 8 or RPN ≥ 200 is marked as triggered; none missed.
- Ranking is monotonic: no triggered row sits below a non-triggered one; within a group
  RPN does not increase as rank number grows.
- The narrative reflects the actual top rows (no invented items or numbers).
