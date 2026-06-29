# FMEA Agent

A **PFMEA (Process Failure Mode and Effects Analysis) agent** for quality and reliability
engineers, built on Claude Code. It turns process descriptions, BOMs, drawings, or existing
"foundation/family" FMEAs into structured PFMEAs that match the company template
(`resources/PFMEA-Template.xlsx`), applies the same calibrated yardstick every time, and
brings the whole organisation's corrective-action history to every line.

The agent **assists**; the engineer reviews and approves. It never treats a draft as a
final, approved FMEA.

## What it can do

| # | Capability | Say something like | Workflow |
|---|------------|--------------------|----------|
| **UC1** | Draft a new PFMEA from inputs | "draft a PFMEA for this process…" | [draft-pfmea](workflows/draft-pfmea.md) |
| **UC2** | Reuse & propagate foundation/family FMEAs | "adapt the foundation for this new part", "cascade this change" | [reuse-fmea](workflows/reuse-fmea.md) |
| **UC3** | Suggest & sanity-check S/O/D ratings | "check my ratings", "are these consistent?" | [check-ratings](workflows/check-ratings.md) |
| **UC4** | Auto-prioritise by RPN & risk triggers | "triage / rank this PFMEA" | [prioritise-pfmea](workflows/prioritise-pfmea.md) |
| **UC5** | Generate recommended actions | "recommend actions for the high-risk rows" | [recommend-actions](workflows/recommend-actions.md) |

The workflows interlock on a shared rows JSON / workbook:

```
reuse a foundation (UC2) → draft (UC1) → check ratings (UC3)
        → prioritise (UC4) → recommend actions (UC5) → cascade changes back out (UC2)
```

## Quick start

1. One-time setup — see [docs/SETUP.md](docs/SETUP.md). In short:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Open the folder in VS Code with the Claude extension (or run Claude Code in this dir).
3. Just describe what you want, e.g. *"Draft a PFMEA for: manual battery-pack assembly —
   load cells, laser-weld bus bars, test weld resistance, label and pack."* The agent picks
   the right workflow, does the work, shows you a draft for review, and saves results to
   `output/`.

## How it's organised

| Path | What's there |
|------|--------------|
| `CLAUDE.md` | The agent's operating contract (purpose, rules, template facts, request routing). |
| `workflows/` | The five plain-English recipes (the core of the agent). |
| `tools/` | The scripts each workflow uses — see [tools/README.md](tools/README.md). |
| `resources/` | `PFMEA-Template.xlsx` (source of truth), `standard-failure-modes.md`, `lessons-learned.json`, and the `fmea-library/` + `fmea-family-index.json` for reuse. |
| `output/` | Generated PFMEAs, triage reports, action worksheets (git-ignored). |
| `docs/` | [SETUP](docs/SETUP.md), [ARCHITECTURE](docs/ARCHITECTURE.md), [GIT_GUIDE](docs/GIT_GUIDE.md). |

## Key conventions

- **Template is the source of truth** for format, the calibrated 1–10 S/O/D scales
  (Assumptions sheet), and the risk triggers (**RPN ≥ 200** or **Severity ≥ 8**).
- **RPN = Severity × Occurrence × Detection**, computed by the workbook formula.
- **Nothing is fabricated** — where input is missing the agent asks; ratings are anchored
  to the scales with written rationale.
- **Generated results go to `output/`** and are not committed; reference data and the FMEA
  library live in `resources/` and are committed.
