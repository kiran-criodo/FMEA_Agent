# Recommended Actions Worksheet — FCIC FY22 (DOE/EE-2734)

_Generated 2026-06-29 · top 12 high-risk row(s) of 41 triggered · triggers RPN ≥ 200 or Severity ≥ 8_

Scope: the 12 highest-RPN rows. Actions draw on (a) our lessons-learned library where it
matched, and (b) the FCIC report's own documented mitigations (Tables 10 & 18) for the
biomass-specific failures our library does not cover. Rows marked **[new lesson]** had no
library match and should be captured in `resources/lessons-learned.json` once proven.
"Target" = revised S/O/D after the actions.

## 1. [Air Classifier / corn] Inefficient separation — 4-fraction scenario — S10/O10/D10 · RPN 1000 · [new lesson]
- **Containment:** Recirculate off-spec streams; revert to the validated 2-/3-fraction mode
  until 4-fraction separation is characterised.
- **Prevention:** Develop a validated air-speed/feed-rate recipe per moisture and bale type;
  control upstream moisture; evaluate a 3-stream classifier or staged classification.
- **Detection:** In-line stream-composition sensing (optical/NIR) to replace operator-visual;
  closed-loop air-speed control driven by moisture.
- **Target:** S10 / O8 / D6 → **RPN 480**. Detection (D10) is the dominant gap; separation
  remains fundamentally hard, so severity stays 10.

## 2. [LT System-Wide] Material not meeting carbohydrate spec (<59%) — S10/O8/D10 · RPN 800 · [new lesson]
- **Containment:** Queue/segregate incoming lots by expected carbohydrate (supplier/harvest
  data); divert low-carbohydrate material.
- **Prevention:** Blend high-carbohydrate fractions from the air classifier (report estimates
  RPN 800 → 480); set carbohydrate expectations at feedstock intake/contracting.
- **Detection:** Develop an at-line carbohydrate proxy (NIR); today it is offline lab only (D10).
- **Target:** S10 / O6 / D10 → **RPN 480** (report's blending estimate; detection still weak).

## 3. [LT System-Wide] High ash content — DMR disc wear — S10/O10/D8 · RPN 800 · _[CAPA-2021-090, LL-2022-031]_
- **Containment:** Increase DMR disc inspection/replacement frequency; segregate visibly
  dirty bales. _[CAPA-2021-090]_
- **Prevention:** Remove inorganics upstream via air classification + a pre-classification
  disc screen (report estimates RPN 800 → 240); set an ash limit / dockage at intake;
  abrasion-resistant disc material. _[CAPA-2021-090]_
- **Detection:** In-line ash sensing (none today, D8); motor-current / vibration trend on the
  DMR. _[CAPA-2021-090]_
- **Target:** S10 / O3 / D8 → **RPN 240** (report estimate — occurrence falls with ash removal).

## 4. [Deacetylation/DMR] Disc refining — wear in disc plates (soil/inorganics) — S6/O10/D10 · RPN 600 · _[CAPA-2021-090]_
- **Containment:** Increase plate inspection/replacement; track wear against lot ash content.
- **Prevention:** Upstream inorganics removal (disc screen / air classification);
  abrasion-resistant plates. _[CAPA-2021-090]_
- **Detection:** Motor-current and vibration trend monitoring; in-line ash sensing
  (none today, D10). _[CAPA-2021-090]_
- **Target:** S6 / O6 / D6 → **RPN 216** (less inorganic load + trend-based detection).

## 5. [Hammer Mill / corn] Screen plugged — fines from self-heating — S10/O6/D8 · RPN 480 · _[LL-2022-031, CAPA-2021-090]_
- **Containment:** Divert self-heated / high-moisture bales; reduce feed rate to avoid the
  plug. _[LL-2022-031]_
- **Prevention:** Control storage moisture to limit self-heating / biological degradation;
  pre-screen fines before the mill; queue/blend by moisture. _[LL-2022-031]_
- **Detection:** In-line moisture sensors driving feed-rate control; material-height sensors;
  trained-observer self-heating inspection. _[LL-2022-031]_
- **Target:** S10 / O3 / D3 → **RPN 90** (moisture/fines control + sensing).

## 6. [LT System-Wide] Deviation from particle size (fines) — S6/O8/D10 · RPN 480 · _[CAPA-2021-090]_
- **Containment:** Pre-screen to remove fines before downstream steps; divert high-fines lots.
- **Prevention:** Pre-classification disc screen to remove dirt/fines (report estimates
  480 → 180); evaluate a knife mill (generates fewer fines) or larger mill screen.
- **Detection:** Add at-line PSD / vision (offline PSD only today, D10); trained-observer
  soil check.
- **Target:** S6 / O3 / D10 → **RPN 180** (report estimate via disc screen).

## 7. [LT System-Wide] High ash content — wear through system (throughput) — S6/O10/D8 · RPN 480 · _[CAPA-2021-090, LL-2022-031]_
- **Containment:** Increase wear-part inspection/replacement; segregate dirty bales.
- **Prevention:** Upstream ash removal (air classification / disc screen); harder wear
  materials; ash spec at intake. _[CAPA-2021-090]_
- **Detection:** Motor-current / vibration trend; in-line ash sensing. _[CAPA-2021-090]_
- **Target:** S6 / O3 / D8 → **RPN 144** (occurrence falls with ash removal).

## 8. [Hammer Mill / corn] Overs production — early hammer wear — S8/O6/D8 · RPN 384 · _[CAPA-2021-090]_
- **Containment:** Inspect/replace worn hammers; audit PSD on suspect lots.
- **Prevention:** Remove inorganics upstream to slow wear; abrasion-resistant hammers;
  schedule hammer replacement by throughput/ash exposure. _[CAPA-2021-090]_
- **Detection:** Hammer-wear monitoring (motor-current trend, scheduled hammer gauging);
  at-line PSD (visual only today, D8). _[CAPA-2021-090]_
- **Target:** S8 / O6 / D3 → **RPN 144** (detection of wear is the main lever).

## 9. [Air Classifier / pine] White wood lost to light fraction(s) — S10/O6/D6 · RPN 360 · [new lesson]
- **Containment:** Recirculate light/medium discard to recover white wood; hold off-spec.
- **Prevention:** Validated air-speed recipe vs chip size and moisture; avoid over-aggressive
  air speed; upstream moisture control.
- **Detection:** In-line stream-composition sensing to replace operator-visual; closed-loop
  air-speed control.
- **Target:** S10 / O3 / D6 → **RPN 180**.

## 10. [Deacetylation/DMR] Plugging — incoming material too many fines — S6/O6/D10 · RPN 360 · [new lesson]
- **Containment:** Pre-screen incoming material to remove fines; divert high-fines lots.
- **Prevention:** Pre-classification disc screen; add a *minimum* particle-size spec; control
  upstream fines generation (knife mill, storage moisture).
- **Detection:** At-line PSD of incoming material (none today, D10); reactor pressure/flow
  trend monitoring.
- **Target:** S6 / O3 / D6 → **RPN 108** (fines removal + at-line PSD).

## 11. [Air Classifier / corn] Shut off (software / air speed) — S3/O10/D10 · RPN 300 · [new lesson]
- **Containment:** Restart procedure; manual air-speed override to keep running.
- **Prevention:** Update/patch the classifier control software; validate air-speed setpoints
  with alarms; preventive maintenance schedule.
- **Detection:** Energy / air-speed monitoring with an alarm *before* shutdown (today the only
  signal is the machine slowing down, D10).
- **Target:** S3 / O3 / D3 → **RPN 27** (software fix + alarms).
- **🚩 Note:** report prints RPN 240 for this row, but 3×10×10 = **300** — confirm S/O/D.

## 12. [Air Classifier / pine] Needles in medium fraction — S6/O6/D8 · RPN 288 · [new lesson]
- **Containment:** Recirculate the medium fraction; hold off-spec.
- **Prevention:** Air-speed/feed-rate recipe tuned to needle shape/size and moisture; upstream
  moisture control.
- **Detection:** In-line composition sensing; operator-visual today (D8).
- **Target:** S6 / O3 / D8 → **RPN 144**.
- **🚩 Note:** report prints RPN 180 for this row, but 6×6×8 = **288** — confirm S/O/D.

---

## The big picture — actions converge on four shared investments
Across these 12 rows the recommended actions repeat, which means a few capital items knock
down many failures at once:

1. **Pre-classification disc screen** (remove dirt/fines/inorganics before milling) — helps
   rows 3, 4, 6, 7, 8, 10 (ash wear, fines, hammer wear, reactor plugging).
2. **In-line moisture & ash sensors** — helps rows 3, 4, 5, 7, 8 and is the single most-cited
   detection gap in the report.
3. **In-line air-classifier stream-composition sensing** (replace operator-visual) — helps
   rows 1, 9, 12 (separation efficiency), the rows where detection sits at D8–D10.
4. **Storage moisture control / queueing** — helps rows 2, 5, 6 (self-heating, fines, spec).

**Detection is the systemic weakness:** 9 of these 12 rows have detection 8–10 because the
processes rely on trained-operator visual inspection with no in-line sensing. Most of the RPN
reduction above comes from closing that gap, not from changing the equipment.

> Caveat: this report uses the FCIC 1/3/6/8/10 scale; revised targets follow the report's
> own mitigation estimates where given (Tables 10 & 18) and our lessons elsewhere. Two rows
> (#11, #12) also carry RPN-arithmetic discrepancies flagged during triage — resolve those
> S/O/D before committing actions.
