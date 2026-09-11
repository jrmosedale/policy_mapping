# WORKBOOK_WRITE_PROTOCOL.md

Standard operating procedure for any change to the climate–nature governance workbook suite.
Follow it in order. Steps 1–3 are proposal/verification; nothing is written until Step 4.

## 0. Scope and canonical files

Three interlinked workbooks in `Data/canonical_files/`, referred to by **stable canonical filenames** (no version integer):

| Role | Canonical filename |
|---|---|
| UK governance | `uk_climate_nature_governance.xlsx` |
| International governance | `international_climate_nature_governance.xlsx` |
| Indicators | `indicators_climate_nature.xlsx` |

The version integer now lives **inside** each workbook (a `Changelog` sheet with a `Version` cell at B2), not in the filename. Superseded copies are archived to `Data/outdated_files/`. **The workbooks contain no formula cells and must stay that way** — every build script opens them with `data_only=True`, and openpyxl does not compute formulas it writes, so a formula would read back empty downstream. The filename is stable so downstream scripts, SOPs and the render kit never need editing when a workbook is updated.

Record-ID families and the workbook each is defined in:

| Family | Defined in | Column |
|---|---|---|
| `LEG-NNN`, `ORG-NNN`, `POL-NNN` | UK | `Record_ID` |
| `INT-L-NNN`, `INT-O-NNN`, `INT-P-NNN`, `EU-L-NNN` | International | `Record_ID` |
| `IND-x-NNN` | Indicators | `Record_ID` |
| `IFW-NN` | Indicators | `Framework_ID` |

## 1. Propose

State the intended change as a table for sign-off before touching anything:

- **New records**: proposed `Record_ID`, `Name`, and every column value. Blank cell over guess.
- **Edits**: the exact cells, old value → new value.
- Identify the **link map** — every *other* record and workbook the change touches (Step 3).

Do not proceed to write on an unreviewed proposal. Higher-risk operations (structural rewrites, global regex passes, column additions) require explicit authorisation.

## 2. Verify

- **Sources**: confirm against primary/official sources (gov.uk, legislation.gov.uk, CBD, nature.scot, official treaty texts). State a confidence level per record; flag anything unverified rather than writing an assumed value.
- **ID allocation**: next free integer in the family. **Never reuse a retired ID** — `POL-023` and `POL-024` are permanently retired.
- **Controlled vocabulary**: any new `General_Type`, `Policy_Sector` token, etc. must be flagged for approval, never silently coined. Max 3 `Policy_Sector` codes per indicator; governance records uncapped.

## 3. Link map — what a change touches

A single record rarely lives in one cell. Before writing, enumerate every reciprocal touch.

**New UK policy (`POL-`)**
- `Policies & Activities` row (all columns).
- `Enabling_Legislation` → confirm the `[LEG-NNN]` exists; if not, propose a new LEG record too.
- `Lead_Organisation` / `Lead_Department` → confirm the `[ORG-NNN]` exists; if not, propose a new ORG record.
- `Related_Policy_Links`, `Parent_Programme`, `Funded_By` → bracketed codes, each must resolve.
- `Indicator_Frameworks` → `[IFW-NN]` (bracketed).
- `Cross-Reference Index` → new row.
- Any existing record it names → add the reciprocal link on that record.

**New / edited UK public body (`ORG-`)**
- `Lead_Department` → `[ORG-NNN]` sponsoring department.
- `Statutory_Role` → `[LEG-NNN]` legislation establishing/empowering the body.
- `Related_Bodies` → `[ORG-NNN]` peer / national-analogue bodies across the four UK administrations (soft, undirected — add on **one** side only).
- `Affecting_Policies` → `[POL-NNN]` policies whose provisions materially affect the body (soft). Use this only for genuine effect; weaker "within scope of" mentions stay in `Remit_And_Powers` prose.

**International link (convention / body / EU law ↔ UK)**
- International record `UK_Links` → add the `[UK code]`.
- Matching UK record `Intl_Links` → add the reciprocal `[INT-/EU- code]`. **Both directions are mandatory** (see Step 6 invariants).
- Intl↔intl thematic links go in `Intl_Links` (soft, undirected — add once).

**Indicator link**
- Governance `Indicator_Frameworks` ↔ indicators `Framework_ID` (`[IFW-NN]`).

## 4. Build — write mechanics (openpyxl)

- **Read canonical first.** Two loads when hyperlinks are needed: `data_only=True` for values, and a second plain load for `.hyperlink.target`.
- **Never `insert_rows` on a striped sheet** — it corrupts alternating-fill parity. For row insertion or structural change, rewrite the full region and re-stripe deterministically by final row position: even rows `FFFDFEFE`, odd rows `FFF4F6F7`.
- **Appending a trailing row/column** is safe (no existing rows move); copy style from a same-parity template (row 2 even, row 3 odd) or from the sibling cell in the same row.
- **Style inheritance**: copy font, fill, border, alignment and number_format — never leave a new cell unstyled or copy from the header/adjacent-column.
- **Exclude the `Record_ID` / `Framework_ID` column from any global bracket/regex pass.** Bracketing a primary key breaks every `.isin()` join. Inspect `.head()` immediately after any rewrite that touches IDs.
- **Bracketing convention**: every cross-reference code is wrapped in square brackets — `[LEG-NNN]`, `[ORG-NNN]`, `[POL-NNN]`, `[INT-L/INT-O/INT-P-NNN]`, `[EU-L-NNN]`, `[IFW-NN]` — regardless of surrounding text. The only exception is the `Record_ID` / `Framework_ID` key columns, which are never bracketed.

## 5. Version, changelog, save, archive

1. Bump the internal `Version` (Changelog!B2) by one.
2. Append one `Changelog` row: `Version | Date (YYYY-MM-DD) | Summary | Author`.
3. Save to the **canonical filename** (overwriting the live file).
4. **Archive the prior canonical file** before it is overwritten, as
   `<name>_v<oldVersion>_superseded_<YYYY-MM-DD>.xlsx` — the date it became redundant.
   Never overwrite an archive; never reuse a superseded name.

## 6. Verify after writing — mandatory gate

**Run `finalise.py`. It is the gate and the rebuild in one command, and it will not rebuild anything from workbooks that fail the check.**

```bash
python3 Management/finalise.py               # check_links.py, then (only if clean) build_all.py
python3 Management/finalise.py --check       # the check alone, e.g. before you start writing
```

Under the hood it runs, from `Data/canonical_files/`:

```bash
python3 ../code/check_links.py               # auto-detects the canonical files; exit 0 required
```

`check_links.py` enforces the invariants:
1. **Orphan references** — every bracketed `[CODE]` resolves to a real `Record_ID` / `Framework_ID`.
2. **Placement** — `UK_Links` holds only UK codes; `Intl_Links` holds only international codes.
3. **Bidirectional completeness** — every international→UK link has its UK→international reverse.
4. **No extra reverse** — no reverse link without a forward.
5. **Retired IDs** — `POL-023` / `POL-024` never reappear as records.

Run `finalise.py --check` **before** the write too, to confirm you started from a clean baseline.

## 7. Sync downstream artefacts (dashboards)

`finalise.py` (§6) already regenerated both dashboards — this section explains *what* it regenerated and what remains yours to do. To rebuild without the gate, from `Dashboards/code/`:

```bash
python3 build_all.py            # governance diagram, then indicator finder
```

> ⚠ **`governance_diagram_v*.html` and `indicator_finder_v4.html` must stay in the same directory** (`Dashboards/`). The finder holds `const GOV_DIAGRAM = "governance_diagram_v12.html"` as a bare filename and resolves its `⬡ diagram` deep-links relative to itself. Separate them and every deep-link breaks silently — the finder still renders, the links just go nowhere. The builder re-points that constant at the newest diagram **in its own output directory**, so it cannot repair a separation either.

**Governance diagram — `Dashboards/code/build_governance_diagram.py` → `Dashboards/governance_diagram_vN.html`.**
Reads all three canonical workbooks directly (auto-detects the canonical filenames) — **no hardcoded governance to maintain.** It picks up new records, links and narrative automatically. When the design *or* the data changes materially, bump the `out = …_vN.html` integer in the script and archive the prior HTML to `Data/outdated_files/` (same discipline as the workbooks).

Which columns become which typed edge (arrow points **from the governing entity to what it governs**):

| Column(s) | Edge type | Style / direction |
|---|---|---|
| `Enabling_Legislation`, `Statutory_Role` (LEG only) | enabling | solid (hard) · LEG → record |
| `Lead_Department`, `Lead_Organisation`, `Lead_Body` | lead | solid (hard) · leader → led |
| `Parent_Programme`, `Parent_Convention` | parent | solid (hard) · parent → child |
| `Funded_By` | funding | dashed (soft) · funder → funded |
| `Related_Legislation`, `Related_Policy_Links`, `Related_Bodies`, `Affecting_Policies` | related | dashed (soft) · undirected |
| `Intl_Links` / `UK_Links` / `UK_Ratification` | intl bridge | double line · hard if UK-ratified/retained, else soft |
| `Indicator_Frameworks`, `Indirect_Policy_Links` | indicator | dotted |

Narrative columns are surfaced verbatim in the detail panel (so editing them updates the panel with no code change): `Remit_And_Powers`, `Scope_And_Commitments`, `Key_Provisions` / `Key_Commitments`, `Statutory_Duties`, `Regulatory_Powers_Keywords`, `Statutory_Enabling_Basis`, `UK_Ratification`, `UK_Representation`, `UK_Engagement`, plus `General_Type` / `Year` / `Status`. `[CODE]` tokens in any of them render with the full name on hover. To add a **new** narrative column to the panel, add it to `add_node(..., extra=[...])` at the relevant sheet loop.

**Indicator finder — `Dashboards/code/build_indicator_finder.py` → `Dashboards/indicator_finder_v4.html` (rewritten in place).**
Reads the canonical indicators workbook by header name. Its only hardcoded governance is `FRAMEWORK_CTX` (one governance chain per framework) — **update it by hand** when a framework's enabling legislation or lead policy changes. It also re-points its "⬡ diagram" deep-links at the newest `governance_diagram_v*.html`, so build the diagram first (which `build_all.py` does).

**Parsers:** every cross-reference is bracketed (`[IFW-NN]`, `[LEG-NNN]`, …); strip brackets when parsing, e.g. `re.findall(r'\[(IFW-\d+)\]', cell)`, and always exclude the `Record_ID` / `Framework_ID` key columns.


---

*The render kit (`PA_toolkit/code/render.py`) deliberately never opens the workbooks — policy hyperlinks are copied into the YAML during the research step. Adding records to a workbook and rendering an assessment are separate operations; this protocol governs the former only.*
