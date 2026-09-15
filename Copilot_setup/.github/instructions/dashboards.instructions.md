---
name: Dashboards
description: Rules for the generated HTML dashboards and their build scripts in Dashboards/.
applyTo: "Dashboards/**"
---
# Working in Dashboards/

- Both HTML files are generated. Data changes come from the workbooks through
  `python3 Management/finalise.py`. Use `python3 Dashboards/code/build_all.py` only to rebuild when
  the integrity check has already passed.
- **`governance_diagram_v*.html` and `indicator_finder_v4.html` must stay in the same directory.**
  The finder links to the diagram by bare filename, and the builder re-points that link only within
  its own output directory. Separating them breaks every deep-link silently.
- Build order is diagram first, then finder; `build_all.py` enforces it.
- Governance diagram (`build_governance_diagram.py`): reads all three workbooks, no hardcoded
  governance. The column → edge-type mapping and the arrow convention (governor → governed) are in
  `WORKBOOK_WRITE_PROTOCOL.md` §7 — keep the eight typed edges and the ≥3:1 contrast palette.
  Hard versus soft international links is decided by UK ratification status, not endpoint type.
  When design or data change materially, bump the `out = …_vN.html` line and archive the prior
  HTML to `Data/outdated_files/`.
- Indicator finder (`build_indicator_finder.py`): re-injects the `INDICATORS` array into
  `indicator_finder_v4.html`, which is both template and output, so hand-made design edits to that
  HTML survive a rebuild. It loads an indicator only if `Record_ID` and `Indicator_Name` are both
  non-empty.
- **`FRAMEWORK_CTX` in `build_indicator_finder.py` hardcodes nine framework governance chains.**
  Whenever a framework's enabling legislation, lead body or lead policy changes in the workbooks,
  check it and update it by hand — and say that you did. Stale chains rebuild cleanly and display
  wrong.
- The dashboards are single self-contained HTML files: no CDN, no external assets, no Node/npm.
  They must open offline from `file://`.
