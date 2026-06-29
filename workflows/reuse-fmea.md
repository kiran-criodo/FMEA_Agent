# Reuse & Propagate the Foundation/Family FMEA (UC2)

## Purpose
Enforce the biggest AIAG-VDA savings lever — **reuse**. Pull the right foundation/family
FMEA for a new part, adapt it (carrying ratings, controls and actions), flag what is
*genuinely new*, and cascade an approved foundation change to every child FMEA it affects —
all of which teams rarely do well because tracking it by hand is tedious.

## When to use
- Adapt: "start a PFMEA for <new part> from the family", "reuse the foundation FMEA",
  "adapt <existing> for <new part>".
- Cascade: "propagate this change to the child FMEAs", "we changed the foundation — what's
  affected", "cascade the update".

## Inputs
- The **family index** `resources/fmea-family-index.json` (foundations + children, with
  paths to each `rows.json`). Keep it current as FMEAs are created.
- Foundation FMEAs live in `resources/fmea-library/`.
- For adapt: a description of the new part, and optionally a UC1 draft of the new part
  (`rows.json`) to diff against for automatic reuse/new classification.

## Steps — Adapt (reuse for a new part)
1. **Find the foundation.** `python tools/reuse_fmea.py list`, or let the tool match by
   description: `adapt --new-part "<desc>"`. Confirm the match is the right family.
2. **Carry it over.** The tool writes a child draft (`output/<name>.json`) with every
   foundation row tagged by origin, plus an adaptation worksheet.
3. **Flag what is genuinely new.** Best practice: run **UC1** on the new part first, then
   `adapt --foundation <id> --against <that-draft.json>`. The tool classifies every failure
   mode as **reused / genuinely-new / possibly-not-applicable**. Without a draft, walk the
   carried rows manually.
4. **Reconcile (agent judgment).** Confirm reused rows still apply (re-rate with UC3 where
   the new part differs); add the genuinely-new rows; remove rows that don't apply — never
   blindly accept the carry-over.
5. **Finalise.** Present the reconciled child FMEA; on approval, regenerate the workbook
   (UC1's tool) and **register the child** in the family index under `children` with
   `derived_from: <foundation id>` so future changes can cascade to it.

## Steps — Cascade (propagate a foundation change)
1. **Identify the change.** `cascade --foundation <id> --row <n> --change "<what changed>"`.
2. **See who's affected.** The tool lists every child derived from that foundation and marks
   which ones actually carry the affected row.
3. **Apply with approval.** For each affected child, apply the approved change, re-rate if
   needed (UC3), regenerate the workbook, and record the propagation so it is auditable.
   Do not change child FMEAs without sign-off.

## Tools
- `tools/reuse_fmea.py` — `list` / `adapt` / `cascade` (match, copy, diff, find children,
  scaffold worksheets).
- `tools/fill_pfmea_template.py` — regenerate a child workbook after reconciliation.
- `workflows/draft-pfmea.md` (UC1) and `workflows/check-ratings.md` (UC3) — used inside the
  adapt step.

## Output
- `output/<child>.json` — the adapted child FMEA draft (rows tagged by origin).
- `output/<child>-adaptation.md` — reuse/new/dropped reconciliation worksheet.
- `output/cascade-<id>-<date>.md` — change-propagation worksheet.

## Validation (check before showing results)
- The matched foundation really is the right family for the new part.
- Every carried row is confirmed (kept / re-rated / removed) — none accepted unread.
- Genuinely-new failure modes specific to the new part are added.
- For a cascade, every affected child is accounted for and the change is applied only with
  approval; the family index is updated when a new child is created.
