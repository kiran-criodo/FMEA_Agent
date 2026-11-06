# PFMEA Risk Priorities — FCIC FY22 (DOE/EE-2734)

_Generated 2026-06-29 · Triggers: RPN ≥ 200 or Severity ≥ 8_

- Rows analysed: **72**
- Rows requiring mitigation action (triggered): **41**
- Rows with incomplete S/O/D (not ranked): **2**

## Risk narrative

**Scale caveat (read first).** This report uses the **FCIC 1/3/6/8/10 guidance scale**, not
the company template's calibrated scale, and its RPNs run from 9 up to **1000**. The
company triggers (RPN ≥ 200, Severity ≥ 8) were applied as-is, so on this scale the
RPN ≥ 200 line is comparatively lenient — treat the **relative ranking** below as the
signal, not the raw pass/fail of the 200 cut-off.

**Headline.** 72 failure modes were triaged; **41 trigger mitigation**. The risk is
heavily concentrated in the **low-temperature corn-stover line**, and the single biggest
systemic weakness is **detection** — most top items carry detection 8–10 because the
processes have no in-line sensors and rely on trained-operator visual inspection.

**Top cluster — corn-stover preprocessing (tackle first):**
- **#1 Air classifier 4-fraction separation (RPN 1000)** and **#11 air-classifier shut-off**
  — separation quality with effectively no detection (D=10).
- **#2 Carbohydrate spec (<59%), RPN 800** and **#3 / #7 ash content (800 / 480)** — the
  system can't control these in-feed properties; occurrence is rated *inevitable* (10) and
  detection is poor. The report's own fix (air classification + screening / in-line ash &
  moisture sensors) is estimated to cut these from 800 → 240.
- **#4 DMR disc-plate wear (RPN 600)** and **#5 / #6 hammer-mill fines from self-heating
  (480)** — ash/inorganics and fines drive disc wear, screen plugging and DMR shutdowns.

**Second cluster — pine-residue (high-temperature) line:**
- **#9 white wood lost to the light fraction (360)**, **#12 needles in medium fraction**,
  **#24 bark in heavy fraction (180)** — air-classifier separation efficiency.
- **#18 screw-feeder agglomeration (216)** and **#20 char buildup on auger (192)** — the
  pyrolysis feed screw, plus **#19 fixed-carbon deviation (192)**.

**Cross-cutting themes:** (1) **moisture** is the most common root cause and cascades
downstream (dryer → classifier → mill → DMR); (2) **ash / soil / inorganics** drive both
product-quality and equipment-wear failures; (3) **fines** plug screens and the DMR; and
(4) **detection is the weakest lever** across the board. The report's recurring mitigation
— in-line moisture/ash sensors and a pre-classification disc screen — attacks all four at
once and is the highest-leverage investment.

**⚠️ Data-quality flags (confirm before acting):**
- **2 rows have computed RPN ≠ the RPN printed in the report:** *Air classifier (pine) —
  "too many needles in medium fraction"* computes 6×6×8 = **288** but the report prints
  **180**; *Air classifier (corn) — "Shut off"* computes 3×10×10 = **300** but the report
  prints **240**. One of the S/O/D values or the printed RPN is wrong in each — verify.
- **2 rows could not be ranked** because the report left **Severity = TBD**: LT particle-size
  *overs*, and LT *decreased throughput*. Both need a severity before they can be prioritised.

> Note: ratings are taken verbatim from the FCIC report; this triage re-applies consistent
> trigger logic and recomputes RPN, it does not re-judge the SMEs' S/O/D.

## Ranked action list

| Rank | Process | Failure Mode | S | O | D | RPN | Trigger |
|------|---------|--------------|---|---|---|-----|---------|
| 1 | Air Classifier / corn (Tbl 20) | Inefficient separation — 4-fraction scenario | 10 | 10 | 10 | 1000 | ⚠️ Sev>=8 & RPN>=200 |
| 2 | LT System-Wide (Tbl 17/18) | Material not meeting carbohydrate spec (<59%) | 10 | 8 | 10 | 800 | ⚠️ Sev>=8 & RPN>=200 |
| 3 | LT System-Wide (Tbl 17) | High ash content — DMR disc wear (product/throughput) | 10 | 10 | 8 | 800 | ⚠️ Sev>=8 & RPN>=200 |
| 4 | Deacetylation/DMR / corn (Tbl 22) | Disc refining — wear in disc plates (soil/inorganics) | 6 | 10 | 10 | 600 | ⚠️ RPN>=200 |
| 5 | Hammer Mill / corn (Tbl 21) | Screen plugged — fines from self-heating | 10 | 6 | 8 | 480 | ⚠️ Sev>=8 & RPN>=200 |
| 6 | LT System-Wide (Tbl 17) | Deviation from particle size (fines) — hammer mill / bale grinder | 6 | 8 | 10 | 480 | ⚠️ RPN>=200 |
| 7 | LT System-Wide (Tbl 17) | High ash content — wear through system (throughput) | 6 | 10 | 8 | 480 | ⚠️ RPN>=200 |
| 8 | Hammer Mill / corn (Tbl 21) | Overs production — early hammer wear | 8 | 6 | 8 | 384 | ⚠️ Sev>=8 & RPN>=200 |
| 9 | Air Classifier / pine (Tbl 12) | Inefficient separation — too much white wood lost to light fraction(s) | 10 | 6 | 6 | 360 | ⚠️ Sev>=8 & RPN>=200 |
| 10 | Deacetylation/DMR / corn (Tbl 22) | Deacetylation plugging — incoming material too many fines | 6 | 6 | 10 | 360 | ⚠️ RPN>=200 |
| 11 | Air Classifier / corn (Tbl 20) | Shut off (software / air speed) | 3 | 10 | 10 | 300 | ⚠️ RPN>=200 |
| 12 | Air Classifier / pine (Tbl 12) | Inefficient separation — too many needles in medium fraction | 6 | 6 | 8 | 288 | ⚠️ RPN>=200 |
| 13 | Hammer Mill / corn (Tbl 21) | Fines production — self-heated / high soil | 6 | 6 | 8 | 288 | ⚠️ RPN>=200 |
| 14 | Hammer Mill / corn (Tbl 21) | Process slowdown >50% (partial screen plug) | 10 | 8 | 3 | 240 | ⚠️ Sev>=8 & RPN>=200 |
| 15 | Air Classifier / corn (Tbl 20) | Inconsistent feeding — lower throughput | 8 | 3 | 10 | 240 | ⚠️ Sev>=8 & RPN>=200 |
| 16 | Rotary Dryer / pine (Tbl 11) | Outgoing moisture >10% after single pass (Scenario 1) | 3 | 10 | 8 | 240 | ⚠️ RPN>=200 |
| 17 | Air Classifier / corn (Tbl 20) | Rock trap fills up with husks | 3 | 8 | 10 | 240 | ⚠️ RPN>=200 |
| 18 | HT Screw Feeder / pine (Tbl 16) | Deviation from target particle size (agglomeration/attrition) | 6 | 6 | 6 | 216 | ⚠️ RPN>=200 |
| 19 | HT System-Wide (Tbl 9) | Fixed carbon deviation — conversion efficiency (air classifier) | 8 | 3 | 8 | 192 | ⚠️ Sev>=8 |
| 20 | HT Screw Feeder / pine (Tbl 16) | Char buildup on auger | 8 | 8 | 3 | 192 | ⚠️ Sev>=8 |
| 21 | Hammer Mill / corn (Tbl 21) | ~50% throughput decrease (25-35% moisture) | 8 | 8 | 3 | 192 | ⚠️ Sev>=8 |
| 22 | HT System-Wide (Tbl 9) | Moisture deviation (>10%) — HT conversion + cascading (rotary dryer) | 10 | 3 | 6 | 180 | ⚠️ Sev>=8 |
| 23 | HT System-Wide (Tbl 9) | Throughput lower than target — low feed rate generates fines | 10 | 3 | 6 | 180 | ⚠️ Sev>=8 |
| 24 | Air Classifier / pine (Tbl 12) | Inefficient separation — too much bark in heavy fraction | 10 | 6 | 3 | 180 | ⚠️ Sev>=8 |
| 25 | Oscillating Screen / pine (Tbl 14) | Bottom screen plugs @30% moisture — product quality | 10 | 3 | 6 | 180 | ⚠️ Sev>=8 |
| 26 | HT System-Wide (Tbl 9) | Moisture deviation — hammer-mill energy/throughput | 8 | 3 | 6 | 144 | ⚠️ Sev>=8 |
| 27 | Rotary Dryer / pine (Tbl 11) | Fire within drum and/or stack | 8 | 3 | 6 | 144 | ⚠️ Sev>=8 |
| 28 | Hammer Mill / corn (Tbl 21) | Overs production — moisture >15% | 8 | 6 | 3 | 144 | ⚠️ Sev>=8 |
| 29 | HT Screw Feeder / pine (Tbl 16) | Feed system plug | 10 | 1 | 10 | 100 | ⚠️ Sev>=8 |
| 30 | HT System-Wide (Tbl 9) | Ash deviation — conversion efficiency | 8 | 1 | 10 | 80 | ⚠️ Sev>=8 |
| 31 | Bale Grinder / corn (Tbl 19) | Screen plugs and system plugs | 8 | 3 | 3 | 72 | ⚠️ Sev>=8 |
| 32 | Oscillating Screen / pine (Tbl 14) | Bottom screen plugs @10% moisture — product quality | 10 | 1 | 6 | 60 | ⚠️ Sev>=8 |
| 33 | LT System-Wide (Tbl 17) | Material over moisture specification | 10 | 6 | 1 | 60 | ⚠️ Sev>=8 |
| 34 | Hammer Mill / corn (Tbl 21) | Screen plugged — material buildup/volume | 10 | 6 | 1 | 60 | ⚠️ Sev>=8 |
| 35 | Air Classifier / pine (Tbl 12) | Conveyor jam | 10 | 1 | 3 | 30 | ⚠️ Sev>=8 |
| 36 | Oscillating Screen / pine (Tbl 14) | Sheet metal cracking on system | 8 | 1 | 3 | 24 | ⚠️ Sev>=8 |
| 37 | LT System-Wide (Tbl 17) | High energy consumption (all equipment) | 8 | 3 | 1 | 24 | ⚠️ Sev>=8 |
| 38 | Bale Grinder / corn (Tbl 19) | Bale strings/twine — product contamination | 10 | 1 | 1 | 10 | ⚠️ Sev>=8 |
| 39 | Deacetylation/DMR / corn (Tbl 22) | Deacetylation plugging — overfeeding biomass | 10 | 1 | 1 | 10 | ⚠️ Sev>=8 |
| 40 | Deacetylation/DMR / corn (Tbl 22) | Deacetylation plugging — overcooking / excess fines | 10 | 1 | 1 | 10 | ⚠️ Sev>=8 |
| 41 | Deacetylation/DMR / corn (Tbl 22) | Disc refining — overheating (low moisture) | 10 | 1 | 1 | 10 | ⚠️ Sev>=8 |
| 42 | Drag Chain Conveyors (Tbl 15) | Clogging (closed-system conveyor) | 6 | 3 | 8 | 144 |  |
| 43 | Hammer Mill / corn (Tbl 21) | ~25% throughput decrease (15-25% moisture) | 6 | 8 | 3 | 144 |  |
| 44 | HT System-Wide (Tbl 9) | Excessive overs production (>6mm) — mill/oscillating screen | 6 | 3 | 6 | 108 |  |
| 45 | Oscillating Screen / pine (Tbl 14) | Bottom screen plugs @30% moisture — downtime/throughput | 6 | 3 | 6 | 108 |  |
| 46 | Oscillating Screen / pine (Tbl 14) | Motor failures | 6 | 3 | 6 | 108 |  |
| 47 | Bale Grinder / corn (Tbl 19) | Inconsistent material volumes | 6 | 6 | 3 | 108 |  |
| 48 | Air Classifier / corn (Tbl 20) | Unintended material loss | 1 | 10 | 10 | 100 |  |
| 49 | HT System-Wide (Tbl 9) | Ash deviation (>1.75%) — equipment wear / throughput | 3 | 3 | 10 | 90 |  |
| 50 | Air Classifier / corn (Tbl 20) | Inefficient separation — 3-fraction scenario | 3 | 3 | 10 | 90 |  |
| 51 | HT System-Wide (Tbl 9) | Excessive fines production (<1.18mm) | 3 | 3 | 8 | 72 |  |
| 52 | HT System-Wide (Tbl 9) | Fixed carbon deviation — inorganic carryover / equipment wear | 3 | 3 | 8 | 72 |  |
| 53 | Hammer Mill / corn (Tbl 21) | Throughput decrease — overs from 1st-stage grinder | 1 | 6 | 10 | 60 |  |
| 54 | Hammer Mill / pine (Tbl 13) | Screen plugs (partial) | 6 | 3 | 3 | 54 |  |
| 55 | Oscillating Screen / pine (Tbl 14) | Bearings breaking/cracking | 6 | 3 | 3 | 54 |  |
| 56 | HT System-Wide (Tbl 9) | Throughput lower than target — material volume not achieved | 3 | 3 | 6 | 54 |  |
| 57 | Oscillating Screen / pine (Tbl 14) | Belt breaking | 3 | 6 | 3 | 54 |  |
| 58 | Rotary Dryer / pine (Tbl 11) | Plugging of cyclones before airlock | 6 | 1 | 6 | 36 |  |
| 59 | Oscillating Screen / pine (Tbl 14) | Bottom screen plugs @10% moisture — downtime/throughput | 6 | 1 | 6 | 36 |  |
| 60 | Deacetylation/DMR / corn (Tbl 22) | Deacetylation plugging — degraded incoming material | 6 | 6 | 1 | 36 |  |
| 61 | Rotary Dryer / pine (Tbl 11) | Outgoing moisture >spec after multiple passes (Scenario 2) | 3 | 1 | 8 | 24 |  |
| 62 | Oscillating Screen / pine (Tbl 14) | Screen tears — bottom screen | 3 | 1 | 8 | 24 |  |
| 63 | Oscillating Screen / pine (Tbl 14) | Top (primary) screen plugs | 3 | 1 | 6 | 18 |  |
| 64 | Oscillating Screen / pine (Tbl 14) | Screen cracks — top screen | 1 | 1 | 10 | 10 |  |
| 65 | Rotary Dryer / pine (Tbl 11) | Material loss through stack | 3 | 1 | 3 | 9 |  |
| 66 | Hammer Mill / pine (Tbl 13) | Too many particles under spec (fines) | 3 | 1 | 3 | 9 |  |
| 67 | Drag Chain Conveyors (Tbl 15) | Slipping off track | 3 | 3 | 1 | 9 |  |
| 68 | Hammer Mill / pine (Tbl 13) | Too many particles over spec (>10%) | 3 | 1 | 1 | 3 |  |
| 69 | Bale Grinder / corn (Tbl 19) | Bale strings/twine wrap grinder shaft (throughput) | 3 | 1 | 1 | 3 |  |
| 70 | Drag Chain Conveyors (Tbl 15) | Overloading | 1 | 1 | 3 | 3 |  |
| 71 | LT System-Wide (Tbl 17) | Deviation from particle size (overs) — severity not estimated (TBD) |  | 1 | 10 | — |  |
| 72 | LT System-Wide (Tbl 17) | Decreased throughput — severity not estimated (TBD) |  | 3 | 3 | — |  |

