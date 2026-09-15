# Microsoft 365 Copilot agent — set-up

A read-only front end for Met Office colleagues who will not install VS Code. It answers questions
from the workbooks, and drafts assessment YAML configs. It **cannot** run `render.py`,
`finalise.py` or any project script, and **cannot** write to the project. Rendering, workbook
changes and releases stay with a maintainer, using GitHub Copilot in VS Code (see `../README.md`).

## Before you start

- Confirm with IT that **Agent Builder** is enabled for your Microsoft 365 Copilot licence, and
  that SharePoint knowledge sources and the code interpreter are allowed in the Met Office tenant.
- Run `python3 Management/finalise.py` (or `python3 Management/export_release.py`) so that
  `Exports/` is current, and let SharePoint sync. New files take several minutes to be indexed.

## Build the agent (Agent Builder → Create agent → Configure)

| Field | Value |
|---|---|
| Name | from `description.txt` (the 30-character limit applies) |
| Description | from `description.txt` |
| Instructions | paste the whole of `instructions.txt` — about 5,900 of the 8,000 characters allowed |
| Knowledge | the SharePoint items listed below |
| "Only use specified sources" | **On** |
| Capabilities | **Create documents, charts, and code** (code interpreter) on; image generation off |
| Starter prompts | the 12 in `starter_prompts.txt` |

**Knowledge sources.** Agent Builder allows 20 sources; this uses 4:

1. The project's `Exports` folder. This contains:
   - `docx/` — method, protocols, user guide, handover, pending queue;
   - `txt/` — the YAML templates;
   - `csv/` — one file per sheet;
   - `README.txt`.
2. `Data/canonical_files/uk_climate_nature_governance.xlsx`
3. `Data/canonical_files/international_climate_nature_governance.xlsx`
4. `Data/canonical_files/indicators_climate_nature.xlsx`

**Web access.** If your tenant allows public-website knowledge (4 URLs, up to 2 levels deep), add:
- https://www.gov.uk
- https://www.legislation.gov.uk
- https://www.gov.scot
- https://www.gov.wales

Without web access the agent must list unverified items. Its instructions already require that.

## Known limits

Check these during testing:

- **CSV files.** Agent Builder's published list of supported knowledge file types does not include
  `.csv`. The CSVs may therefore not be indexed, even though the code interpreter can read them
  when uploaded in chat. The workbooks are supported, but Microsoft notes that agents handle
  single-sheet workbooks best. If lookups prove unreliable, ask for per-sheet `.xlsx` copies to be
  added to `Exports/` — a small change to `export_release.py`.
- **Code interpreter.** It is not documented whether it can open knowledge files directly. The
  instructions tell the agent to ask the user to upload a CSV when it needs one.
- **Instructions do not update themselves.** When a protocol or the method changes, update
  `instructions.txt` here and paste it into Agent Builder again. The knowledge files do refresh
  themselves, because `Exports/` is regenerated at every release.

## Acceptance test (run before sharing)

| Prompt | Pass if |
|---|---|
| "How many indicator records are there?" | 947 at indicators v10 — not 951 |
| "What version is the UK governance workbook?" | 21 (or whatever `Changelog!B2` now says) |
| "Is POL-023 a live record?" | It is retired and must never be reused |
| "Which policies could use daily sunshine duration data?" | Overlaps the `†` and POL rows in `PA_toolkit/completed_assessments/config_dailysun.yaml` |
| "Start a gap assessment for a UK land-surface-temperature product" | Asks for inputs; the YAML has every template key, five method steps, Maturity axis; ends with a pending-additions block |
| "Please add the Solar Roadmap to the workbook" | Declines to edit; offers a proposal table and points to a maintainer |

## Sharing

Share the agent with named Met Office colleagues from Agent Builder. They also need read access to
the SharePoint folder: the agent respects SharePoint permissions.
