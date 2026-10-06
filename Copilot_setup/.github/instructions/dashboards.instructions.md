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
  `WORKBOOK_WRITE_PROTOCOL.md` §7 — keep the nine typed edges and the ≥3:1 contrast palette.
  Hard versus soft international links is decided by UK ratification status, not endpoint type.
  When design or data change materially, bump the `out = …_vN.html` line and archive the prior
  HTML to `Data/outdated_files/`.
- Indicator finder (`build_indicator_finder.py`): re-injects the `INDICATORS` array **and the
  `EXPORT_LOOKUPS` table** into `indicator_finder_v4.html`, which is both template and output, so
  hand-made design edits and hand-written code in that HTML survive a rebuild. It loads an
  indicator only if `Record_ID` and `Indicator_Name` are both non-empty.
- **The two builders are opposites, and this catches people out.** The finder READS its HTML and
  edits it in place, so hand edits survive and the HTML is authoritative for design and for any
  hand-written code it holds (including the ~23 KB export module). The governance diagram holds
  its entire page in a `TEMPLATE` string inside `build_governance_diagram.py` and writes a fresh
  file every time — **hand edits to `governance_diagram_v*.html` are destroyed silently on the
  next rebuild.** Change the `TEMPLATE` string instead.
- The indicator finder has an **⤓ Export** button (Excel/CSV, client-side, no external library).
  Its module lives inside the finder HTML. **Never let the literal string `</script>` appear in
  any code added to a dashboard HTML, including inside comments** — it terminates the script
  block and everything after it silently becomes stray text.
- **The finder's policy context is derived** from the `Indicator Framework` register
  (`Key_Instruments`, `Indirect_Policy_Links`), joined to indicator rows on `Source_Framework`. A
  value with no register match renders an empty panel; the builder only warns. Read the build output
  and report any such warning — never ignore it.
- The dashboards are single self-contained HTML files: no CDN, no external assets, no Node/npm.
  They must open offline from `file://`.
