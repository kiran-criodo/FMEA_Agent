# Example outputs

Real outputs from the agent, run on public data: the FMEA tables in the U.S. Department of
Energy's Feedstock-Conversion Interface Consortium report **DOE/EE-2734 (FY22)**. You can see
what the agent produces without installing anything.

| File | Workflow | What it shows |
|---|---|---|
| [PFMEA-rating-check-FCIC-FY22-2026-06-29.md](PFMEA-rating-check-FCIC-FY22-2026-06-29.md) | [check-ratings](../workflows/check-ratings.md) | Sanity-checks Severity / Occurrence / Detection ratings for consistency against the report's own scale |
| [PFMEA-priorities-FCIC-FY22-2026-06-29.md](PFMEA-priorities-FCIC-FY22-2026-06-29.md) | [prioritise-pfmea](../workflows/prioritise-pfmea.md) | Triage of 72 failure modes by RPN and risk triggers, with a risk narrative |
| [PFMEA-actions-FCIC-FY22-2026-06-29.md](PFMEA-actions-FCIC-FY22-2026-06-29.md) | [recommend-actions](../workflows/recommend-actions.md) | Recommended actions for the high-risk rows, matched to lessons learned and the report's documented mitigations |

The FCIC report uses a 1/3/6/8/10 rating scale rather than this repo's calibrated template
scale. Each report says so up front and explains how that affects the ranking.
