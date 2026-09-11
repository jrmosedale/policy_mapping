# Indicator export — scoping note (v2)

**Target:** `Dashboards/indicator_finder_v4.html`
**Revised:** 13 August 2026
**Status:** scoped, prototyped and tested; not yet integrated into the dashboard

> **v2 revisions to your brief:** Word output dropped; policy-context columns removed;
> the two separate tables (Indicators / Policy context) combined into one. Decisions from §9
> of v1 applied: Excel is the default, CSV keeps its four `#` provenance lines, and the same
> export is wanted on `governance_diagram_v12.html` (scoped in §8, not built).

---

## 1. Recommendation

A single **⤓ Export** button in the header, next to Help. It opens a modal stating how many
indicators the current filters have selected, offers **Excel (default) or CSV**, and takes a
filename pre-filled from the active filters. Both formats are generated client-side with
**no external library** — no CDN, no bundled SheetJS — so the dashboard stays a single
self-contained file that works offline and from `file://`.

Integration effort: **~3 hours** for `indicator_finder_v4.html` (down from half a day now
that Word is out).

---

## 2. What gets exported

**Row scope:** exactly the contents of the centre panel — `applySort(applyFilters())`, in the
displayed sort order. Not the whole catalogue unless no filters are set.

**Column scope:** every field shown in the centre card *or* the right-hand detail block, and
nothing else. One row per indicator, one table, both formats. Twelve columns:

| # | Column | Field | Where it appears in the dashboard |
|---|---|---|---|
| 1 | Record ID | `id` | detail panel |
| 2 | Indicator name | `name` | card + detail |
| 3 | Framework | `fw` | card pill |
| 4 | Framework (full) | `fw_full` | detail panel |
| 5 | NCF category | `ncf` | card pill + detail |
| 6 | Geographic scope | `scope` | card pill + detail |
| 7 | Units / measure | `units` | detail |
| 8 | Policy goal | `goal` | card snippet + detail |
| 9 | Data source | `datasrc` | detail |
| 10 | Climate score | `cs` | card badge + detail (0–3, colour-filled in Excel) |
| 11 | Climate relevance | derived | detail (none / low / medium / high) |
| 12 | Climate rationale | `rat` | detail |

### Deliberately excluded

- **All policy-context fields** — link count, designated-monitoring flag, instrument names,
  tiers, notes, URLs — per your instruction (ii). This also removes the framework-level
  granularity problem flagged in v1 §2, since none of that information now leaves the page.
- **Four fields present in the underlying record but shown nowhere in the dashboard:**
  `code` (indicator code), `itype` (indicator type), `sectors`, `gbf` (GBF targets).
  Strictly outside "central panel + detail panel", so they are out.

  *One flag on this, for a later decision:* `gbf` and `sectors` are the two that carry real
  analytical value — `sectors` is what drives the sector filter, and `gbf` is the only link
  from an indicator to a GBF target. If an exported list is ever used for cross-framework
  analysis rather than as a reading list, those two are the ones you will miss. Adding either
  back is a one-line change to `COLS`. Not adding them for now, as instructed.

### One inconsistency worth knowing about

The **Policy-context filter** (Designated monitoring / Policy-relevant only) still exists in
the left panel and still changes which rows are selected — but the export no longer contains
the columns that would explain why. I have therefore kept that filter's setting in the export
metadata (Export info sheet, and the CSV `#` header), so a reader can at least see that the
selection was conditioned on it. Alternatives if that bothers you: hide the filter, or
reinstate a single Yes/No "Designated monitoring" column. My recommendation is to leave it as
now and revisit if it causes confusion.

---

## 3. Excel — `SAMPLE_indicator_export.xlsx`

Two sheets:

1. **Export info** — title, timestamp, *n* exported / 947 in catalogue, column count, source
   workbook version, and all eight filter settings verbatim. Makes an export reproducible
   and citable if it ends up in a report annex.
2. **Indicators** — the single 12-column table. Header row in the dashboard's green
   (`#2F5D50`), frozen at C2 so ID and name stay visible, AutoFilter across `A1:L{n+1}`,
   column widths set per field, wrapped text on the long fields, and the climate-score column
   colour-filled with the dashboard's own 0–3 palette.

Sizes: 103 indicators → **27 KB**; the full 947 → **159 KB** (`SAMPLE_indicator_export_FULL_947.xlsx`,
also included so you can see it at full scale). Both open instantly.

## 4. CSV — `SAMPLE_indicator_export.csv`

Same 12 columns, flat, UTF-8 with BOM (so CO₂, ≥, – and ° open correctly in Excel on Windows),
CRLF line endings, RFC 4180 quoting. Four `#` provenance lines then a blank line then the
header, as agreed:

```
# UK Climate–Nature Indicator Finder — indicator export
# Exported 2026-08-13 13:59,103 of 947 indicators
# Filters: Sector=Climate; NCF category=All; Framework=All; Climate score=≥ 2 (medium+); ...
# Source: indicators_climate_nature.xlsx (v10) via indicator_finder_v4.html

Record ID,Indicator name,Framework,...
```

Read it with:

```r
read.csv("indicators_Climate_cs2plus_2026-08-13.csv", skip = 5, fileEncoding = "UTF-8-BOM")
```
```python
pd.read_csv("indicators_Climate_cs2plus_2026-08-13.csv", skiprows=5, encoding="utf-8-sig")
```

---

## 5. UI design

One header button, `⤓ Export`, styled like the existing `ⓘ Help`. It opens a modal reusing
the existing `.modal` / `.modalbox` CSS:

```
┌─ Export indicators ──────────────────────────────────────────┐
│                                                              │
│   103 indicators will be exported                            │
│   Sector = Climate · Climate score ≥ 2 · sorted by score ↓    │
│   (of 947 in the catalogue — change the filters to alter     │
│    this selection)                                           │
│                                                              │
│   Format    (•) Excel workbook (.xlsx)        ← default      │
│             ( ) CSV (.csv)                                   │
│                                                              │
│   12 columns · one row per indicator                         │
│                                                              │
│   File name  [ indicators_Climate_cs2plus_2026-08-13    ]    │
│                                                              │
│                              [ Cancel ]   [ Export 103 ]     │
└──────────────────────────────────────────────────────────────┘
```

- Count and filter summary read the live `F` state when the modal opens.
- Default filename auto-generated from the active filters plus the date, fully editable.
  The prototype's `suggestName()` produced `indicators_Climate_cs2plus_2026-08-13` for the
  sample filter.
- Confirm button carries the count, so it can't be missed.
- On success a brief toast confirms "103 indicators exported to *filename*.xlsx".
- Zero results → button disabled, modal explains nothing matches.

**Save location.** Chrome and Edge get `showSaveFilePicker()`, a native Save-As dialog where
the user picks folder *and* confirms the name. Firefox and Safari don't implement it and fall
back to a normal download using the modal's filename — which is why the name is asked for in
the dialog rather than left to the browser.

---

## 6. Technical approach

`.xlsx` is a ZIP of XML parts. The dashboard currently has **zero external references**
(verified) and is used as a standalone 1 MB file, so a CDN would break offline use and
bundling SheetJS inline would add ~900 KB. Instead the prototype includes a ~120-line ZIP
writer: CRC-32 from a precomputed table, compression via the browser's native
`CompressionStream('deflate-raw')` (Chrome 80+, Edge 80+, Firefox 113+, Safari 16.4+) with
automatic fallback to STORED entries where unavailable, and minimal but spec-valid OOXML
(`[Content_Types].xml`, `_rels/.rels`, workbook + worksheet parts, hand-written `styles.xml`).

**Total addition to the dashboard: ~19 KB of JavaScript, 0 external requests.**

### Verification performed

`indicator_export.js` run under Node 22 against the real 947-record `INDICATORS` array:

| Check | Result |
|---|---|
| ZIP entries use DEFLATE | ✓ all method 8 |
| `.xlsx` opens in openpyxl — filtered | ✓ 2 sheets, Indicators 104 × 12 |
| `.xlsx` opens in openpyxl — full catalogue | ✓ Indicators 948 × 12, 159 KB |
| Styling round-trip | ✓ header fill `FF2F5D50`, freeze `C2`, AutoFilter `A1:L104`, climate-score fills, column widths, wrap |
| Renders in LibreOffice Calc | ✓ correct layout, colours and widths |
| Unicode | ✓ CO₂, ≥, ↓, en-dashes intact in both formats |
| Filenames | ✓ `suggestName()` builds from live filter state |

The sample `.xlsx` and `.csv` in this folder are the **actual output of the JavaScript**, not
a Python mock-up — what you see is what the dashboard will produce.

---

## 7. Integration into `indicator_finder_v4.html`

1. **Header** (~line 208, `div.hd-right`): insert the Export button before the `hd-tag` span.
2. **Modal markup**: append a `div.modal#exportModal` alongside `#helpModal` at the end of
   `<body>`. Reuses existing modal CSS; ~12 lines of new CSS for the radio rows.
3. **Script**: paste `indicator_export.js` immediately before the closing `</script>` at
   line 570, plus a ~60-line dialog controller.
4. **Build script — no change needed.** `build_indicator_finder.py` uses
   `indicator_finder_v4.html` as both template and output, and `inject_js_var()` replaces only
   the `const INDICATORS = [...]` block (plus the `GOV_DIAGRAM` constant). Everything else is
   preserved verbatim, so the export code survives every rebuild. The one constraint: the
   export code must sit outside that declaration and must not itself contain the literal
   string `const INDICATORS =`. The prototype doesn't.

Optional tidy-up: have `build()` write the workbook version string into the export metadata
via one extra `re.sub`, so the provenance line can't drift from the actual data version.

---

## 8. Same export on `governance_diagram_v12.html` — scoped, not built

You said yes to this. It is a genuinely separate piece of work, because the data model is
different: `const D` holds **293 nodes** and **967 edges**, with node fields
`id, fam, label, acr, type, sec, secs, year, status, url, blurb, rat, x, deg`.

What carries over unchanged: the ZIP writer, the styles, the sheet builder, the save logic,
the modal shell. Roughly 80% of `indicator_export.js` is already generic.

What has to be written fresh:

- A new `COLS` array for governance records — my starting proposal: Record ID, Family, Label,
  Acronym, Type, Sector, Sectors, Year, Status, Description (`blurb`), Rationale (`rat`), URL,
  Connections (`deg`).
- A hook into that dashboard's own filter state (its filter model is not `F`; needs reading).
- **A decision that cuts against the principle you just set here.** The governance diagram's
  substance *is* the network — 967 edges connecting the nodes. A nodes-only export throws that
  away, but including edges means a second table, which is exactly the split you asked me to
  remove from this export. My recommendation: export nodes as the primary sheet and offer
  edges as a second sheet only in Excel, with a clear label. Worth deciding before I build it.
- The `x` field (an array of `[label, text]` pairs, variable length per node) doesn't flatten
  cleanly into a column. Needs a rule — probably concatenate, or drop.

Estimated effort once those two decisions are made: **half a day**. I'd suggest finishing and
signing off the indicator export first, so the shared module settles before it's forked.

---

## 9. Outstanding decisions

1. **`gbf` and `sectors`** — leave out (as now), or add back for analytical use? (§2)
2. **Policy-context filter** — leave visible with no corresponding export column, hide it, or
   reinstate a single Yes/No "Designated monitoring" column? (§2)
3. **Governance diagram: edges** — nodes only, or nodes + an edges sheet in Excel? (§8)
4. **Go-ahead to integrate** into `indicator_finder_v4.html`?

---

## 10. Files in this folder

| File | What it is |
|---|---|
| `indicator_export.js` | Working prototype module, 19 KB, no dependencies, Node-testable |
| `SAMPLE_indicator_export.xlsx` | Real JS output — 2 sheets, 103 indicators × 12 columns, 27 KB |
| `SAMPLE_indicator_export.csv` | Real JS output — 103 rows, 4 provenance lines, 66 KB |
| `SAMPLE_indicator_export_FULL_947.xlsx` | Full catalogue, no filters — 947 rows, 159 KB |

The two filtered samples use **Sector = Climate, Climate score ≥ 2**, sorted by climate score
descending — 103 of 947 indicators.
