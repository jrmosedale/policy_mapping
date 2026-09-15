---
name: run-assessment
description: Run a Met Office research → UK policy relevance assessment (applied or gap mode) using the fixed method in PA_toolkit/METHOD_AND_SCORING.md — research, write the YAML config, render PDF and Word, and append † finds to Data/pending_additions.md. Use when asked to assess a research field, dataset or prospective product against UK climate–nature policy.
argument-hint: "field=<research field> mode=<applied|gap> biblio=<file in PA_toolkit/bibliographies> [flagship=<url>] [basename=<output name>]"
user-invocable: true
---
# Run a research → policy relevance assessment

This skill replaces `PA_toolkit/PROMPT_TEMPLATE.md` for agents that can read the workspace. Nothing
is attached: read the files yourself.

## 0. Inputs

Take these from the arguments; ask once, in a single message, for anything missing:

- **Field** — the research field or dataset.
- **Mode** — `applied` (existing Met Office research → policy) or `gap` (a product the Met Office
  could build, evidenced by others' work elsewhere).
- **Bibliography** — a file in `PA_toolkit/bibliographies/`.
- **Flagship tool/URL** — optional.
- **Output basename** — default `MO_<field>_policy_relevance`.

Confirm the plan in two lines, then proceed without further check-ins.

## 1. Read

Read these in full, in this order:

1. `PA_toolkit/METHOD_AND_SCORING.md` — the method. Follow it exactly.
2. `PA_toolkit/template_files/TEMPLATE_applied.yaml` or `TEMPLATE_gap.yaml` — the **format
   example only**. Produce a new config with the same keys.
3. The bibliography.
4. The `Policies & Activities` sheet of `Data/canonical_files/uk_climate_nature_governance.xlsx`
   (or `Exports/csv/uk_climate_nature_governance/Policies_and_Activities.csv`). Take each policy's
   hyperlink from the `Link` column.
5. The framework sheets of `Data/canonical_files/indicators_climate_nature.xlsx` (or
   `Exports/csv/indicators_climate_nature/`). A row is an indicator only if `Record_ID` and
   `Indicator_Name` are both non-empty.
6. `Data/pending_additions.md` — so you do not re-propose something already queued, deferred or
   rejected.

Do **not** open `PA_toolkit/code/render.py`. You only run it.

## 2. Research — method §2, steps 1–5

1. Scope the capability from the bibliography. Inspect the flagship tool directly.
2. Establish the research → policy channel from primary sources, and date it.
3. Assemble candidates: filter on sector tags, then screen **all** records for a plausible
   dependency. Add real activities that are absent from the workbook as `†` rows.
4. Score each candidate on both axes. Materiality → Relevance 1–3. Second axis: Status in applied
   mode, Maturity in gap mode. An inferred link takes the lower value and says so.
5. Indicator scan: keyword-filter the workbook, then keep only indicators whose *measured
   quantity* the capability could directly inform. Then run a focused web scan for authoritative
   indicators that are genuinely absent from the workbook, marked `†` with their source. Keep to
   about six indicators in total.

**Web use.** Search the web to complement the files, not just to confirm them. Use `web/fetch` for
plain pages. Use the browser tool for any URL with a query string, because some fetch tools drop
query strings silently. Verify every status, date and URL against gov.uk, legislation.gov.uk or
the agency's own portal. If you have no web access, carry on from the files, err towards the lower
second-axis value, and list every claim, date and URL you could not verify.

**Gap mode.**
- The bibliography is external evidence, not Met Office output.
- Define the prospective product concretely: variables, resolution, cadence and coverage.
- Use `status_axis: {label: "Maturity", values: {Demonstrated: "0B5563", Emerging: "C9871B", Conceptual: "5A6B73"}}`.
- Relabel `labels.summary` and `labels.references_primary` as in `TEMPLATE_gap.yaml`.

## 3. Write the config

Write `PA_toolkit/completed_assessments/config_<field>.yaml` with the template's keys:

- `meta` — set `title`, `subtitle`, `prepared` date, `footer` and `output_basename`;
- `theme` and `scoring` — copy unchanged from the template;
- `section_order`, `labels` and `status_axis`;
- `key_points`, `summary`, `policy_rows`;
- `indicator_rows` plus `indicators_intro`, with `indicators` in `section_order`, if you scanned
  indicators;
- `methods` — keep the five-step structure;
- `gaps`, `references_primary`, `references_other`.

Set `ref: †` for any row not held in the workbook. Markup: `**bold**`, `*italic*`,
`[[label|https://url]]`. British English, metric units, no hedging.

## 4. Render and review

```bash
python3 PA_toolkit/code/render.py PA_toolkit/completed_assessments/config_<field>.yaml --format both --outdir PA_toolkit/completed_assessments
```

If rendering fails, fix the YAML, never the renderer. Then work through the review checklist in
`PA_toolkit/ASSESSMENT_TOOLKIT_USER_GUIDE.md` §6:

- every URL resolves;
- every `Current` is documented;
- indicators pass the measured-quantity test;
- the DOCX has been opened and checked;
- the methods block still has five steps.

## 5. Append the daggers — required

Append one row per `†` activity and per `†` indicator to the Queue table in
`Data/pending_additions.md`:

- columns: `Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution`;
- `Found by` = the field; `Status` = `pending`; `Source` must be a primary source.

**Do not ask whether to append.** Record overlap only with a record of the same kind — check
`Record_Type` / `General_Type` — not one that merely mentions the candidate.

## 6. Reply

Keep it short:

- the output files;
- the `†` list, noting for each whether the measured quantity takes a climate input, and any
  overlap;
- extra sources used;
- candidates excluded, and why;
- confidence for Opportunity and lower-maturity links;
- the unverified items.
