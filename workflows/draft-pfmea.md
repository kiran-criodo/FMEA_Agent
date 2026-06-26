# Draft a New PFMEA from Inputs (UC1)

## Purpose
Turn a plain-English process description (or BOM / drawing notes / a similar part) into a
first-pass PFMEA that matches `resources/PFMEA-Template.xlsx`, so an engineer edits a
strong draft instead of starting from a blank page.

## When to use
The user says things like: "draft a PFMEA", "start a new PFMEA", "create a process FMEA
for …", "first-pass FMEA from this process description".

## Inputs
- **Process description** — what the process/product is and the main steps or operations.
  (Free text is fine; a BOM or drawing notes also work.)
- **Header metadata** (ask for what's missing; leave blank if unknown):
  - Item / Product Part Number(s)
  - Product Description
  - Responsible Engineer (Responsibility)
  - Prepared by
  - Core Team
  - FMEA number
- Optional: a similar existing part's PFMEA to adapt from.

## Steps
1. **Gather & confirm inputs.** If the process description is thin or header fields are
   missing, ask focused questions rather than guessing. Confirm the list of process
   steps you'll analyse before drafting rows.
2. **Decompose the process.** Break the description into discrete process steps /
   functions (these fill the **Process** column).
3. **Draft failure modes.** For each process step, list the potential ways it can fail.
   **Cross-check every step against `resources/standard-failure-modes.md`** so common
   ("standard") failure modes are never forgotten. Note which were added from the
   checklist.
4. **Effects, causes, controls.** For each failure mode, write the Potential Effect(s) of
   Failure, the Potential Cause(s)/Mechanism(s) of Failure, and the Current Process
   Controls (prevention and/or detection controls that exist today; write "None
   identified" if there are none).
5. **Rate S / O / D.** Propose Severity, Occurrence and Detection (each 1–10) using the
   calibrated scales on the **Assumptions** sheet of the template (read them with the
   tool, see below). Give a one-line **rationale** for each rating. Fill **Class** only
   for special/critical characteristics (e.g. safety, regulatory); otherwise leave blank.
6. **Compute RPN & flag triggers.** RPN = Sev × Occur × Detec. Flag any row where
   **RPN ≥ 200** or **Severity ≥ 8** — these require a mitigation action. (Thresholds
   come from the template's Parameters block.) Leave the Recommended Action(s) column for
   the engineer / UC5, but you may note "Mitigation required (trigger)" on flagged rows.
7. **Review gate.** Present the draft as a Markdown table (one row per failure mode) plus
   a short list of the triggered/high-risk rows and any assumptions you made. **Wait for
   the engineer to approve or edit before writing the Excel file.**
8. **Write the workbook.** On approval, run the tool to fill the template and save to
   `output/` (see Output).
9. **Confirm.** Show the saved file path and a one-line summary (rows written, how many
   triggered a risk threshold).

## Tool
- `tools/fill_pfmea_template.py` — fills `resources/PFMEA-Template.xlsx` from a JSON file
  of header metadata + rows and saves a copy to `output/`. It computes RPN itself.
  - Inspect the calibrated scales first: `python tools/fill_pfmea_template.py --show-scales`
  - Write a workbook: `python tools/fill_pfmea_template.py --input <rows.json> --out <name>`
  - See the JSON shape: `python tools/fill_pfmea_template.py --print-schema`

## Output
- An Excel workbook saved to `output/`, named `PFMEA-<part-or-slug>-<YYYY-MM-DD>.xlsx`,
  using the company template (other sheets preserved).
- Keep the intermediate `rows.json` alongside it in `output/` for traceability.

## Validation (check before showing results)
- Every process step from the description appears in the table; no step silently dropped.
- Each row has a failure mode, at least one effect, at least one cause, a control entry,
  and S/O/D each in 1–10.
- RPN in the sheet equals Sev × Occur × Detec for every row.
- Every row with Severity ≥ 8 or RPN ≥ 200 is flagged in the review summary.
- Standard failure modes from the checklist were considered for each step (and noted).
- The file opens and the header metadata is populated; no template formula/sheet broken.
- Nothing fabricated: where input was missing, the engineer was asked rather than guessed.
