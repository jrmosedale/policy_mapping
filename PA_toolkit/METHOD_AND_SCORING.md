# Method & scoring specification

This is the fixed methodology behind every "Met Office research → UK policy relevance"
assessment produced with this kit. Keep it constant across research fields so reports are
comparable. The per-report content lives in a YAML config; this document defines *how* that
content is derived and scored.

## 1. Inputs

- **Bibliography** for the MO research field (e.g. a researcher's publication list, HTML/CSV/Markdown).
- **Governance workbook** `uk_climate_nature_governance.xlsx`, sheet **Policies & Activities**
  (POL records, with a `Link` column used for hyperlinks). Canonical filename; POL IDs stable across versions.
- **Indicators workbook** `indicators_climate_nature.xlsx` (framework sheets) — optional,
  used only for the Policy indicators section.
- **Flagship MO tool/dataset** for the field (e.g. the Climate-Pest Risk web tool), inspected directly.
- **Additional reliable sources**: gov.uk, legislation.gov.uk, Defra/agency portals, Met Office
  pages/blogs, peer-reviewed papers. Verify before writing; record what was used.

## 2. Procedure

1. **Scope the MO research** from the bibliography: filter to the field and adjacent work.
   Characterise the flagship tool/output by direct inspection (what it measures, at what resolution,
   what coverage/limits).
2. **Establish the research→policy channel(s)**: confirm any documented, operational use of MO
   outputs (named partnerships, tools feeding a register/contingency process, etc.) from primary
   sources, dated.
3. **Assemble policy candidates** from the Policies & Activities sheet: filter first on the relevant
   sector tags, then screen *all* records for a plausible dependency on the research. Add operational
   activities that are real but absent from the workbook, marked with a dagger (†).
4. **Score** each candidate on the two axes in §3.
5. **Indicator scan** (whenever an indicators workbook is supplied — applied *and* gap mode):
   keyword-filter the indicators workbook for the field, then keep only indicators whose *measured
   quantity* the capability could directly inform (exclude indicators whose measured quantity takes no
   climate input, e.g. a GIS area). **Then run a focused web scan** for authoritative indicators *absent*
   from the workbook (framework indicators published since the workbook version, or operational/agency
   monitoring statistics not catalogued in any framework). Discipline: authoritative sources only
   (gov.uk, agencies, recognised frameworks); it must genuinely not be in the workbook (check by name
   and framework); it must pass the same measured-quantity test; mark it `†` with its source; note any
   overlap with an existing indicator. Expect a small yield — the workbook already catalogues most
   published framework indicators. Propose, never silently add.
6. **Write** the report from the YAML config; verify every factual claim and URL against source.
7. **Record the † additions — do not merely offer them.** At the end of the run, append one row to
   `Data/pending_additions.md` for every activity and every indicator you marked `†`. Append them;
   do not ask whether to. This changes no workbook and needs no approval — the file is a candidate
   queue, and every row still passes the screen and triage in
   `Management/protocols/POLICY_SCAN_PROTOCOL.md` before any record is written.

   Why this is a step and not an option: daggered items are a targeted, well-researched scan of one
   field, and are better evidence than a quarterly sweep produces. Previously they were offered once
   in a chat reply and captured only if that individual chose to act, which made the completeness of
   a shared knowledge base depend on the disposition of whoever happened to run the assessment. It
   is not an individual user's call.

   If `Data/pending_additions.md` is not reachable — a ported copy of `PA_toolkit/` alone, say —
   emit the rows as a fenced, copy-paste-ready block explicitly labelled for pasting into that file.
   Silence is not an acceptable outcome. Also summarise the daggered items in the chat reply, as
   before, so the user knows what was found.

## 3. Scoring — two independent axes

Keep these two axes **separate**. They answer different questions; collapsing them (as a single
"confidence" or "relevance" score) makes a high-value-but-unrealised link look weak.

**Relevance (materiality of MO science to the policy)** — shown by row colour:
- **3 High** — a direct, often named, evidence input.
- **2 Medium** — informs a defined risk or evidence component.
- **1 Low** — indirect dependency.

**Status (realisation)** — shown by the chip:
- **Current** — MO science already informs the activity, and this is documented.
- **Opportunity** — a credible but not-yet-realised use.

So an activity can be `3 / Opportunity` (high materiality, not yet used — a priority) or
`2 / Current` (already used, moderate materiality). Materiality drives the colour; realisation drives
the chip.

## 3a. Two modes — applied vs gap (prospective)

The same backbone (capability → UK policy, scored, same layout) serves two question types. Only the
framing, labels and the **second axis** change; the renderer is identical and mode is set entirely in
the YAML.

| | **Applied mode** (default) | **Gap / prospective mode** |
|---|---|---|
| Question | Where does / could *existing* MO research inform UK policy? | If MO *built* product X, what could UK policy do with it? |
| Bibliography | MO's own publications | External reading list (proof the approach works elsewhere) |
| Summary section | Summary of MO research | The evidence base for the prospective product |
| `references_primary` label | "Met Office research (from bibliography)" | "Evidence base (external literature)" |
| Second axis (`status_axis`) | **Status**: Current / Opportunity (is MO science *already used* here?) | **Maturity**: Demonstrated / Emerging / Conceptual (how *proven* is the application?) |
| Relevance axis | unchanged — materiality 1–3 | unchanged — materiality 1–3 |

Why the second axis must change: in gap mode nothing is "Current" (the product doesn't exist), so the
realisation axis is empty and useless. Replace it with one that *discriminates between prospective
applications* — Maturity is the natural choice (how proven elsewhere, hence how near-term). The kit
makes this a config block (`status_axis: {label, values}`), so switching mode is editing YAML, not code.
See `TEMPLATE_applied.yaml` (applied) and `TEMPLATE_gap.yaml` (gap) for both.

Other valid second axes you may define instead of Maturity — e.g. **Policy pull** (Explicit / Implicit /
Latent demand) or **Feasibility** (how readily MO could deliver it). Pick one axis and keep it constant
within a report. Whatever you choose, keep **Relevance = materiality** so reports stay comparable on the
primary axis.

## 4. Rules (carried over from the workbook discipline)

- **British English** throughout; metric units.
- **Verify before writing**: dates, statuses, URLs checked against official sources.
- **Blank over guess**: leave a field empty rather than inserting a presumptive value.
- **State confidence / inference**: where a link is inferred rather than documented, say so (and it is
  almost always `Opportunity`, often `Low`).
- **No silent vocabulary additions**: Relevance is 1–3; Status is Current/Opportunity. Don't invent
  new bands without flagging.
- **Dagger (†)** marks activities not held as records in the governance workbook.

## 5. Document structure (fixed for comparability)

Key points → Summary of MO research → Policy activities table (Relevance × Status) →
Policy indicators (optional) → Methods → References (primary = MO research; other = sources + workbooks).
Section order, headings and colours are set in the YAML `section_order`, `labels` and `theme`.
