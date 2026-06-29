# Suggest & Sanity-Check S/O/D Ratings (UC3)

## Purpose
Apply the same yardstick to every rating: propose Severity / Occurrence / Detection with
written rationale anchored to the calibrated 1–10 scales, and flag ratings that are
inconsistent within the document — removing the biggest source of engineer-to-engineer
variation.

## When to use
The user says: "check my ratings", "sanity-check S/O/D", "are these ratings consistent",
"suggest severity/occurrence/detection", "review the scoring".

## Inputs
- An existing PFMEA (`.xlsx` template workbook, or a `rows.json`). For arithmetic checks,
  a `.xlsx` with cached RPNs or a `rows.json` carrying a per-row `rpn_stated` field lets
  the tool catch RPN ≠ S×O×D.
- The calibrated scales on the template's **Assumptions** sheet (read with
  `python tools/fill_pfmea_template.py --show-scales`).

## Steps
1. **Run the mechanical checks:** `python tools/check_ratings.py --input <file>`. It writes
   `output/PFMEA-rating-check-<slug>-<date>.md` flagging arithmetic errors, out-of-range or
   missing ratings, inconsistent ratings across identical failure modes, and triggered rows
   with no action.
2. **Load the calibrated scales** (`--show-scales`) so the review is anchored, not opinion.
3. **Scale-anchored judgment (the agent's core job).** For each row — especially flagged
   ones — check whether each rating fits the scale anchor for that effect:
   - **Severity** must match the *effect*, not the failure mode. A fire / bodily-harm /
     shipped-defect effect rated below the scale's high-severity anchor (e.g. < 8) is a flag.
   - **Occurrence** should reflect cause frequency given the current controls.
   - **Detection** should reflect how well current controls *catch or prevent* the cause —
     "no control / operator-visual only" belongs near the low-detection end (high number).
   For each mismatch, state the anchor, why it doesn't fit, and a **suggested rating +
   rationale**.
4. **Suggest missing ratings.** For rows left blank or "TBD", propose S/O/D with rationale
   from the scales; never leave a high-risk row unrated.
5. **Present** the findings: mechanical flags + the agent's scale-anchored suggestions, each
   with rationale. Wait for engineer approval before changing anything.
6. **(Optional) Apply corrections.** On approval, update the `rows.json` and regenerate the
   workbook with `tools/fill_pfmea_template.py`.

## Tools
- `tools/check_ratings.py` — deterministic consistency checks (arithmetic, range, missing,
  cross-row divergence, trigger-without-action).
- `tools/fill_pfmea_template.py --show-scales` — prints the calibrated S/O/D anchors.

## Output
- `output/PFMEA-rating-check-<slug>-<date>.md` — mechanical findings + the agent's
  scale-anchored review and suggested corrections.

## Validation (check before showing results)
- Every mechanical flag from the tool is addressed (confirmed real, or explained).
- Every suggested rating cites a specific scale anchor and a one-line rationale.
- Severity suggestions track the effect; detection suggestions track the control strength.
- No rating invented without basis; where information is missing, the engineer is asked.
