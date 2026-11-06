# Rating Sanity-Check — FCIC FY22 (DOE/EE-2734)

_Generated 2026-06-29 · 72 rows · triggers RPN ≥ 200 or Severity ≥ 8_

**45 mechanical finding(s).** Scale-anchored judgment (does each rating fit the calibrated 1–10 anchor for its effect?) is added by the agent — see workflows/check-ratings.md.

## Arithmetic errors (RPN ≠ Sev×Occur×Detec) — 2
- row 17 [Air Classifier / pine (Tbl 12)] Inefficient separation — too many needles in medium fraction: stated RPN 180 != Sev*Occ*Det (6x6x8 = 288)
- row 52 [Air Classifier / corn (Tbl 20)] Shut off (software / air speed): stated RPN 240 != Sev*Occ*Det (3x10x10 = 300)

## Out-of-range / missing ratings — 2
- row 41 [LT System-Wide (Tbl 17)] Deviation from particle size (overs) — severity not estimated (TBD): Sev=missing
- row 47 [LT System-Wide (Tbl 17)] Decreased throughput — severity not estimated (TBD): Sev=missing

## Inconsistent ratings (same failure mode, different S/O/D) — 0
- none

## Triggered rows with no recommended action — 41
- row 3 [HT System-Wide (Tbl 9)] Fixed carbon deviation — conversion efficiency (air classifier): triggered (Sev=8, RPN=192) but no recommended action
- row 5 [HT System-Wide (Tbl 9)] Moisture deviation (>10%) — HT conversion + cascading (rotary dryer): triggered (Sev=10, RPN=180) but no recommended action
- row 6 [HT System-Wide (Tbl 9)] Moisture deviation — hammer-mill energy/throughput: triggered (Sev=8, RPN=144) but no recommended action
- row 8 [HT System-Wide (Tbl 9)] Ash deviation — conversion efficiency: triggered (Sev=8, RPN=80) but no recommended action
- row 10 [HT System-Wide (Tbl 9)] Throughput lower than target — low feed rate generates fines: triggered (Sev=10, RPN=180) but no recommended action
- row 11 [Rotary Dryer / pine (Tbl 11)] Outgoing moisture >10% after single pass (Scenario 1): triggered (Sev=3, RPN=240) but no recommended action
- row 14 [Rotary Dryer / pine (Tbl 11)] Fire within drum and/or stack: triggered (Sev=8, RPN=144) but no recommended action
- row 16 [Air Classifier / pine (Tbl 12)] Inefficient separation — too much bark in heavy fraction: triggered (Sev=10, RPN=180) but no recommended action
- row 17 [Air Classifier / pine (Tbl 12)] Inefficient separation — too many needles in medium fraction: triggered (Sev=6, RPN=288) but no recommended action
- row 18 [Air Classifier / pine (Tbl 12)] Inefficient separation — too much white wood lost to light fraction(s): triggered (Sev=10, RPN=360) but no recommended action
- row 19 [Air Classifier / pine (Tbl 12)] Conveyor jam: triggered (Sev=10, RPN=30) but no recommended action
- row 23 [Oscillating Screen / pine (Tbl 14)] Bottom screen plugs @10% moisture — product quality: triggered (Sev=10, RPN=60) but no recommended action
- row 25 [Oscillating Screen / pine (Tbl 14)] Bottom screen plugs @30% moisture — product quality: triggered (Sev=10, RPN=180) but no recommended action
- row 32 [Oscillating Screen / pine (Tbl 14)] Sheet metal cracking on system: triggered (Sev=8, RPN=24) but no recommended action
- row 37 [HT Screw Feeder / pine (Tbl 16)] Feed system plug: triggered (Sev=10, RPN=100) but no recommended action
- row 38 [HT Screw Feeder / pine (Tbl 16)] Char buildup on auger: triggered (Sev=8, RPN=192) but no recommended action
- row 39 [HT Screw Feeder / pine (Tbl 16)] Deviation from target particle size (agglomeration/attrition): triggered (Sev=6, RPN=216) but no recommended action
- row 40 [LT System-Wide (Tbl 17)] Deviation from particle size (fines) — hammer mill / bale grinder: triggered (Sev=6, RPN=480) but no recommended action
- row 42 [LT System-Wide (Tbl 17)] Material over moisture specification: triggered (Sev=10, RPN=60) but no recommended action
- row 43 [LT System-Wide (Tbl 17/18)] Material not meeting carbohydrate spec (<59%): triggered (Sev=10, RPN=800) but no recommended action
- row 44 [LT System-Wide (Tbl 17)] High ash content — DMR disc wear (product/throughput): triggered (Sev=10, RPN=800) but no recommended action
- row 45 [LT System-Wide (Tbl 17)] High ash content — wear through system (throughput): triggered (Sev=6, RPN=480) but no recommended action
- row 46 [LT System-Wide (Tbl 17)] High energy consumption (all equipment): triggered (Sev=8, RPN=24) but no recommended action
- row 49 [Bale Grinder / corn (Tbl 19)] Screen plugs and system plugs: triggered (Sev=8, RPN=72) but no recommended action
- row 51 [Bale Grinder / corn (Tbl 19)] Bale strings/twine — product contamination: triggered (Sev=10, RPN=10) but no recommended action
- row 52 [Air Classifier / corn (Tbl 20)] Shut off (software / air speed): triggered (Sev=3, RPN=300) but no recommended action
- row 54 [Air Classifier / corn (Tbl 20)] Inefficient separation — 4-fraction scenario: triggered (Sev=10, RPN=1000) but no recommended action
- row 56 [Air Classifier / corn (Tbl 20)] Rock trap fills up with husks: triggered (Sev=3, RPN=240) but no recommended action
- row 57 [Air Classifier / corn (Tbl 20)] Inconsistent feeding — lower throughput: triggered (Sev=8, RPN=240) but no recommended action
- row 58 [Hammer Mill / corn (Tbl 21)] Screen plugged — material buildup/volume: triggered (Sev=10, RPN=60) but no recommended action
- row 59 [Hammer Mill / corn (Tbl 21)] Screen plugged — fines from self-heating: triggered (Sev=10, RPN=480) but no recommended action
- row 60 [Hammer Mill / corn (Tbl 21)] Process slowdown >50% (partial screen plug): triggered (Sev=10, RPN=240) but no recommended action
- row 61 [Hammer Mill / corn (Tbl 21)] ~50% throughput decrease (25-35% moisture): triggered (Sev=8, RPN=192) but no recommended action
- row 64 [Hammer Mill / corn (Tbl 21)] Overs production — moisture >15%: triggered (Sev=8, RPN=144) but no recommended action
- row 65 [Hammer Mill / corn (Tbl 21)] Overs production — early hammer wear: triggered (Sev=8, RPN=384) but no recommended action
- row 66 [Hammer Mill / corn (Tbl 21)] Fines production — self-heated / high soil: triggered (Sev=6, RPN=288) but no recommended action
- row 67 [Deacetylation/DMR / corn (Tbl 22)] Deacetylation plugging — overfeeding biomass: triggered (Sev=10, RPN=10) but no recommended action
- row 68 [Deacetylation/DMR / corn (Tbl 22)] Deacetylation plugging — overcooking / excess fines: triggered (Sev=10, RPN=10) but no recommended action
- row 69 [Deacetylation/DMR / corn (Tbl 22)] Deacetylation plugging — incoming material too many fines: triggered (Sev=6, RPN=360) but no recommended action
- row 71 [Deacetylation/DMR / corn (Tbl 22)] Disc refining — wear in disc plates (soil/inorganics): triggered (Sev=6, RPN=600) but no recommended action
- row 72 [Deacetylation/DMR / corn (Tbl 22)] Disc refining — overheating (low moisture): triggered (Sev=10, RPN=10) but no recommended action

## Scale-anchored review (agent)

_Anchored to the **FCIC guidance scale** in this report (Tables 1–3): Severity 8 = "high
disruption, >30% scrapped, process may stop, customer dissatisfied"; 10 = "≈100% scrapped,
process unreliable, failure without warning, **may endanger operator and/or equipment**".
Occurrence 8 = repeated failures; 10 = almost inevitable. Detection 8 = remote chance of
detection; 10 = no process control._

### Resolve the 2 arithmetic errors first
- **Row 17 — needles in medium fraction (stated 180, computes 288).** S/O/D = 6/6/8 gives
  288. The "too much bark" row directly above is 10/6/3 = 180, so 180 was likely carried
  over by mistake. Most probable fix: detection is **5**, not 8 (6×6×5 = 180) — i.e. the
  printed 180 is right and the D=8 is the typo. **Confirm with the SME** whether D is 5 or 8;
  the difference moves RPN between 180 and 288.
- **Row 52 — air-classifier "Shut off" (stated 240, computes 300).** S/O/D = 3/10/10 gives
  300. The "rock trap" row is 3/8/10 = 240, so occurrence may be **8**, not 10 (3×8×10 = 240).
  **Confirm whether occurrence is 8 or 10.**

### Suggest the 2 missing (TBD) severities
- **Row 41 — particle size *overs* (LT).** Effect: oversize particles flow downstream; the
  report found *no* DMR risk from overs and estimates the score "low (10–30 range)". Per the
  scale, minor reprocessing with no downstream harm ≈ **Severity 3** (low). With O=1, D=10 →
  RPN **30**, consistent with the report's own estimate. _Suggest S=3._
- **Row 47 — decreased throughput (LT, all equipment).** Effect is economic (missed yield/
  throughput); the report could not quantify economic severity. Throughput-downtime severities
  elsewhere in the report sit at 6 (conveyor clogging) to 10 (mill shutdown). A general
  throughput shortfall ≈ **Severity 6** (moderate disruption). With O=3, D=3 → RPN **54**.
  _Suggest S=6, and flag that economic severity is better quantified via TEA (the report's own
  caveat)._

### Judgment flags (rating doesn't fit the effect)
- **Row 14 — "Fire within drum and/or stack", rated Severity 8.** A fire is explicitly the
  scale's **Severity 10** territory ("may endanger operator and/or equipment"). Rating it 8
  understates a safety hazard; **suggest Severity 10** (RPN 144 → 180), which also keeps it
  firmly on the action list. This is the most important rating to revisit.
- **Row 19 — "Conveyor jam", rated Severity 10.** Effect is system downtime + equipment
  damage (no safety/scrap consequence), which reads more like the Severity 8 anchor; **10 may
  be overstated** unless the jam risks injury. Confirm.

### On the "41 triggered rows with no action"
Not a genuine gap in the source — the FCIC report *does* provide mitigations (Tables 10 & 18
and the appendix detection columns). The flag fired because those action columns were not
carried into the extracted rows. Treat as resolved for this document; the check remains valid
for an in-house PFMEA where blank actions on triggered rows are real omissions.

> Note: this review anchors to the FCIC scale because it is the FCIC's document. For an
> in-house PFMEA, anchor instead to the company **Assumptions** sheet
> (`tools/fill_pfmea_template.py --show-scales`).

