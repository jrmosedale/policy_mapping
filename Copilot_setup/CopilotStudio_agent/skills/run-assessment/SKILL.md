---
name: run-assessment
description: Runs a Met Office research-to-policy relevance assessment for a research field or a prospective product — screens the governance workbook, scores every candidate policy, scans indicators, and returns the finished PDF and Word report. Use when someone asks how their research could inform UK policy, or what policy would do with a product the Met Office could build.
---
# Run a research → policy relevance assessment

## Files bundled with this skill

- `render.py` — the renderer. Run it; never read it whole, rewrite it or reconstruct it.
- `TEMPLATE_applied.yaml`, `TEMPLATE_gap.yaml` — format examples, one per mode.
- `METHOD_AND_SCORING.md` — the method. Read it in full and follow it exactly.

## 1. Inputs

Collect these, asking once for anything missing: research field; mode (`applied` = existing Met
Office research, `gap` = a product the Met Office could build); the bibliography (uploaded by the
user, or its filename in `PA_toolkit/bibliographies/`, fetched with the SharePoint tool); the
flagship Met Office tool or URL, if any; the output basename, default
`MO_<field>_policy_relevance`. Confirm the plan in two lines, then work without further check-ins.

## 2. Gather the data

Fetch into the sandbox the `Policies & Activities` sheet of `uk_climate_nature_governance.xlsx`, or
`Exports/csv/uk_climate_nature_governance/Policies_and_Activities.csv`. Do the same for the
indicator framework sheets when an indicator scan is wanted. Take each policy's hyperlink from the
`Link` column. A row is an indicator only if `Record_ID` and `Indicator_Name` are both non-empty.
Read `Data/pending_additions.md` and any files in `Data/pending_inbox/`, so you do not re-propose
something already queued, deferred or rejected.

## 3. Research — method §2

1. Scope the capability from the bibliography; characterise the flagship output by inspecting it.
2. Establish the research → policy channel from primary sources, and date it.
3. Screen **every** record in `Policies & Activities`, not only those matching the sector tags. Add
   real activities the workbook lacks, marked `†`.
4. Score both axes. Relevance 1–3 is materiality. The second axis is Status (applied) or Maturity
   (gap). An inferred link takes the lower value and says so.
5. Indicator scan: keyword-filter the workbook, then keep only indicators whose *measured quantity*
   the capability could directly inform. Then run a focused web scan for authoritative indicators
   genuinely absent from the workbook, marked `†` with their source. About six in total.

**The sandbox has no internet.** Do every web check with your web tool, not from inside Python.
Verify each status, date and URL against gov.uk, legislation.gov.uk or the agency's own portal. If
web access fails, carry on from the files, err towards the lower second-axis value, and list
everything you could not verify.

## 4. Gap mode differences

- The bibliography is external evidence, not Met Office output.
- Define the prospective product concretely: variables, resolution, cadence, coverage.
- Set `status_axis: {label: "Maturity", values: {Demonstrated: "0B5563", Emerging: "C9871B", Conceptual: "5A6B73"}}`.
- Relabel `labels.summary` and `labels.references_primary` as in `TEMPLATE_gap.yaml`.

## 5. Write the config

Write `config_<field>.yaml` in the sandbox with the template's keys: `meta` (title, subtitle,
prepared, footer, output_basename); `theme` and `scoring` copied unchanged; `section_order`,
`labels`, `status_axis`; `key_points`, `summary`, `policy_rows`, `indicators_intro`,
`indicator_rows`; `methods` (keep its five steps); `gaps`, `references_primary`,
`references_other`. Use `ref: "†"` for any row not held in the workbook. Markup: `**bold**`,
`*italic*`, `[[label|https://url]]`. British English, metric units, no hedging.

## 6. Render

```
python3 render.py config_<field>.yaml --format both --outdir .
```

If it fails, fix the YAML — never the renderer. If reportlab, python-docx or PyYAML are missing
from the sandbox, say so, return the YAML config, and give the user the command to render it
themselves.

## 7. Check

Per the user guide's review checklist: every URL resolves; every `Current` is documented; indicators
pass the measured-quantity test; the methods block still has five steps.

## 8. Save and return

Return the PDF and DOCX in the conversation, and use the SharePoint tool to create
`config_<field>.yaml`, the PDF and the DOCX in `PA_toolkit/completed_assessments/`. Never overwrite
an existing file: if the name is taken, append a suffix and say so.

## 9. Queue the daggers

Run the `queue-finds` skill for every `†` item. This is a required step, not an offer.

## 10. Reply

Briefly: the files written and where; the `†` list with climate input and any overlap; extra sources
used; candidates excluded and why; confidence for Opportunity and lower-maturity links; the
unverified items.
