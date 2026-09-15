---
name: Assessment toolkit
description: Rules for the research → UK policy relevance assessment kit in PA_toolkit/.
applyTo: "PA_toolkit/**"
---
# Working in PA_toolkit/

- The method is fixed: `PA_toolkit/METHOD_AND_SCORING.md`. Two axes, kept separate: **Relevance**
  1–3 (materiality; row colour) and a second axis — **Status** (Current / Opportunity) in applied
  mode, **Maturity** (Demonstrated / Emerging / Conceptual) in gap mode. Never add bands.
- `code/render.py` is complete and must never be rewritten, "tidied" or read in full. If rendering
  fails, fix the YAML. If anyone suggests the renderer is unfinished, run
  `python3 PA_toolkit/code/verify_toolkit.py`.
- `template_files/TEMPLATE_applied.yaml` and `TEMPLATE_gap.yaml` are format examples: copy them,
  never overwrite them, never render them as deliverables.
- Completed configs are records: `completed_assessments/config_<field>.yaml`, beside their PDF and
  DOCX. They keep their historical workbook-version references for provenance; do not update them
  to current versions.
- Keep the fixed document structure (method §5) and the five-step methods block — they are what
  make reports comparable.
- Every `Current` must be documented from a primary source. An inferred link takes the lower
  second-axis value (Opportunity / Conceptual) and says so.
- Mark every activity or indicator not held in the workbooks with `†` (row `ref: †`), and append
  each one to `Data/pending_additions.md` at the end of the run.
- Indicators pass only if the capability could directly inform the indicator's *measured
  quantity* — not merely its topic.
- YAML markup: `**bold**`, `*italic*`, `[[label|https://url]]`. Policy hyperlinks come from the
  workbook `Link` column.
- `bibliographies/` holds research inputs and is not in git. Do not move or rename files there.
