# Move manifest — reorganisation of 2 September 2026

The project was reorganised from a flat layout into five top-level directories, grouped by
*who needs the file* rather than by file type. This file records the exact mapping so the
move is reversible and so anyone holding an old path can find where it went.

There is no version control on this folder, which is why this record exists.

## Directory mapping

| Old | New |
|---|---|
| `code_files/` (assessment kit) | `PA_toolkit/`, `PA_toolkit/template_files/`, `PA_toolkit/code/` |
| `code_files/` (dashboard builders) | `Dashboards/code/` |
| `code_files/` (integrity tools) | `Data/code/` |
| `code_files/` (protocols) | `Management/protocols/` |
| `html_dashboards/` | `Dashboards/` |
| `canonical_files/` | `Data/canonical_files/` |
| `outdated_files/` | `Data/outdated_files/` |
| `outputs_assessments/` | `PA_toolkit/completed_assessments/` |
| `biblio/` | `PA_toolkit/bibliographies/` |
| root `.md` documents | `Management/`, `Management/protocols/`, `PA_toolkit/` |
| `presentations/`, `export_scoping/`, `outputs_other/` | unchanged |

## File-by-file

| Old path | New path |
|---|---|
| `ASSESSMENT_TOOLKIT_USER_GUIDE.md` | `PA_toolkit/ASSESSMENT_TOOLKIT_USER_GUIDE.md` |
| `code_files/README.md` | `PA_toolkit/README.md` |
| `code_files/PROMPT_TEMPLATE.md` | `PA_toolkit/PROMPT_TEMPLATE.md` |
| `code_files/METHOD_AND_SCORING.md` | `PA_toolkit/METHOD_AND_SCORING.md` |
| `code_files/TEMPLATE_applied.yaml` | `PA_toolkit/template_files/TEMPLATE_applied.yaml` |
| `code_files/TEMPLATE_gap.yaml` | `PA_toolkit/template_files/TEMPLATE_gap.yaml` |
| `code_files/render.py` | `PA_toolkit/code/render.py` |
| `outputs_assessments/MO_biosecurity_policy_relevance.docx` | `PA_toolkit/completed_assessments/MO_biosecurity_policy_relevance.docx` |
| `outputs_assessments/MO_biosecurity_policy_relevance.pdf` | `PA_toolkit/completed_assessments/MO_biosecurity_policy_relevance.pdf` |
| `outputs_assessments/config_dailysun.yaml` | `PA_toolkit/completed_assessments/config_dailysun.yaml` |
| `outputs_assessments/config_ocean_heatwaves.yaml` | `PA_toolkit/completed_assessments/config_ocean_heatwaves.yaml` |
| `outputs_assessments/dailysun_policy_relevance_3.docx` | `PA_toolkit/completed_assessments/dailysun_policy_relevance_3.docx` |
| `outputs_assessments/dailysun_policy_relevance_3.pdf` | `PA_toolkit/completed_assessments/dailysun_policy_relevance_3.pdf` |
| `outputs_assessments/lst_policy_relevance.docx` | `PA_toolkit/completed_assessments/lst_policy_relevance.docx` |
| `outputs_assessments/lst_policy_relevance.pdf` | `PA_toolkit/completed_assessments/lst_policy_relevance.pdf` |
| `outputs_assessments/ocean_heatwaves.docx` | `PA_toolkit/completed_assessments/ocean_heatwaves.docx` |
| `outputs_assessments/ocean_heatwaves.pdf` | `PA_toolkit/completed_assessments/ocean_heatwaves.pdf` |
| `biblio/Biblio_marine_heatwaves.docx` | `PA_toolkit/bibliographies/Biblio_marine_heatwaves.docx` |
| `biblio/Daily_sunshine_duration_biblio.docx` | `PA_toolkit/bibliographies/Daily_sunshine_duration_biblio.docx` |
| `biblio/Deborah-Hemming-Biblio.html` | `PA_toolkit/bibliographies/Deborah-Hemming-Biblio.html` |
| `biblio/Extreme LST biblio.docx` | `PA_toolkit/bibliographies/Extreme LST biblio.docx` |
| `biblio/OCEAN_HEATWAVE_BIBLIO2.rtf` | `PA_toolkit/bibliographies/OCEAN_HEATWAVE_BIBLIO2.rtf` |
| `html_dashboards/governance_diagram_v12.html` | `Dashboards/governance_diagram_v12.html` |
| `html_dashboards/indicator_finder_v4.html` | `Dashboards/indicator_finder_v4.html` |
| `code_files/build_all.py` | `Dashboards/code/build_all.py` |
| `code_files/build_governance_diagram.py` | `Dashboards/code/build_governance_diagram.py` |
| `code_files/build_indicator_finder.py` | `Dashboards/code/build_indicator_finder.py` |
| `canonical_files/indicators_climate_nature.xlsx` | `Data/canonical_files/indicators_climate_nature.xlsx` |
| `canonical_files/international_climate_nature_governance.xlsx` | `Data/canonical_files/international_climate_nature_governance.xlsx` |
| `canonical_files/uk_climate_nature_governance.xlsx` | `Data/canonical_files/uk_climate_nature_governance.xlsx` |
| `outdated_files/biodiversity_indicators_manual_v7_superseded_2026-07-06.xlsx` | `Data/outdated_files/biodiversity_indicators_manual_v7_superseded_2026-07-06.xlsx` |
| `outdated_files/build_indicator_finder_superseded_2026-07-13.py` | `Data/outdated_files/build_indicator_finder_superseded_2026-07-13.py` |
| `outdated_files/governance_diagram_v10_superseded_2026-07-15.html` | `Data/outdated_files/governance_diagram_v10_superseded_2026-07-15.html` |
| `outdated_files/governance_diagram_v11_superseded_2026-07-15.html` | `Data/outdated_files/governance_diagram_v11_superseded_2026-07-15.html` |
| `outdated_files/governance_diagram_v8_superseded_2026-07-14.html` | `Data/outdated_files/governance_diagram_v8_superseded_2026-07-14.html` |
| `outdated_files/governance_diagram_v9_superseded_2026-07-15.html` | `Data/outdated_files/governance_diagram_v9_superseded_2026-07-15.html` |
| `outdated_files/indicator_finder_v3_superseded_2026-07-15.html` | `Data/outdated_files/indicator_finder_v3_superseded_2026-07-15.html` |
| `outdated_files/indicators_climate_nature_v8_superseded_2026-07-07.xlsx` | `Data/outdated_files/indicators_climate_nature_v8_superseded_2026-07-07.xlsx` |
| `outdated_files/indicators_climate_nature_v9_superseded_2026-07-07.xlsx` | `Data/outdated_files/indicators_climate_nature_v9_superseded_2026-07-07.xlsx` |
| `outdated_files/international_climate_nature_governance_v12_superseded_2026-07-06.xlsx` | `Data/outdated_files/international_climate_nature_governance_v12_superseded_2026-07-06.xlsx` |
| `outdated_files/international_climate_nature_governance_v13_superseded_2026-07-15.xlsx` | `Data/outdated_files/international_climate_nature_governance_v13_superseded_2026-07-15.xlsx` |
| `outdated_files/uk_climate_nature_governance_v17_superseded_2026-07-06.xlsx` | `Data/outdated_files/uk_climate_nature_governance_v17_superseded_2026-07-06.xlsx` |
| `outdated_files/uk_climate_nature_governance_v18_superseded_2026-07-13.xlsx` | `Data/outdated_files/uk_climate_nature_governance_v18_superseded_2026-07-13.xlsx` |
| `outdated_files/uk_climate_nature_governance_v19_superseded_2026-07-13.xlsx` | `Data/outdated_files/uk_climate_nature_governance_v19_superseded_2026-07-13.xlsx` |
| `outdated_files/uk_climate_nature_governance_v20_superseded_2026-07-15.xlsx` | `Data/outdated_files/uk_climate_nature_governance_v20_superseded_2026-07-15.xlsx` |
| `code_files/check_links.py` | `Data/code/check_links.py` |
| `code_files/orphan_codes.py` | `Data/code/orphan_codes.py` |
| `PROJECT_HANDOVER_Nature_Climate_Indicators.md` | `Management/PROJECT_HANDOVER_Nature_Climate_Indicators.md` |
| `code_files/WORKBOOK_WRITE_PROTOCOL.md` | `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` |
| `POLICY_SCAN_PROTOCOL.md` | `Management/protocols/POLICY_SCAN_PROTOCOL.md` |

## Files created in the same operation

| File | Why |
|---|---|
| `Management/finalise.py` | The release gate: `check_links.py`, then `build_all.py` only if it passes. |
| `PA_toolkit/code/requirements.txt` | Renderer dependencies only (reportlab, python-docx, PyYAML). |
| `Dashboards/code/requirements.txt` | openpyxl. |
| `Data/code/requirements.txt` | openpyxl. |

The former single `code_files/requirements.txt` was superseded by these three and moved to `_to_delete/`.

## Code changed in the same operation

| File | Change |
|---|---|
| `Dashboards/code/build_all.py` | Path constants rebased: `DASH_DIR` is now the script's parent, `ROOT` its grandparent, `CANON_DIR = ROOT/Data/canonical_files`. |
| `Dashboards/code/build_indicator_finder.py` | Same rebasing; `CANON` now `ROOT/Data/canonical_files/indicators_climate_nature.xlsx`. |
| `Dashboards/code/build_governance_diagram.py` | Docstring only — it resolves workbooks from the working directory and takes `--outdir`, both supplied by `build_all.py`. |

## To reverse

Run the table above backwards — every move was a plain rename with no content change, and no
destination collided with an existing file. The three code edits would also need undoing;
they are the only content changes made during the move.

## Not deleted

The mounted folder does not permit deletion from this session, so the emptied source directories
(`code_files/`, `html_dashboards/`, `canonical_files/`, `outdated_files/`, `biblio/`,
`outputs_assessments/`) remain as empty husks, along with `_to_delete/` and `_mvtest/`.
Nothing in them is in use. Delete them in Finder.
