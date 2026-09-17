# Indicator export — scoping note (v3)

**Target:** `Dashboards/indicator_finder_v4.html`
**Revised:** 17 September 2026 (workbook v12; v4 enriched-goal variant added — see §9a)
**Status:** ✅ **INTEGRATED 17 September 2026** — the v4 (11-column, enriched Policy goal) design is live in `Dashboards/indicator_finder_v4.html`. SDG target titles now come from a curated `Short_Title` column added to the SDG Target Lookup in workbook v16, replacing the derived truncation. Sorting/pivoting by GBF or SDG code is accepted as lost. This note is retained as the design record.

> **v3 revisions to your brief:** Framework (full) and Climate relevance dropped from the row
> and replaced by lookup blocks; GBF target `Short_Title`, SDG goal `Full_Text_Official` and
> SDG target text resolved inline; Sector column added. 17 columns, one row per indicator.
>
> **Read §2.1 and §2.4 before signing this off** — the GBF/SDG source-field decision and the
> Sector taxonomy both need a call from you, and §2.4 is a data-quality finding rather than a
> design preference.

---

## 1. What changed, and what it costs

| | v2 | v3 |
|---|---|---|
| Columns | 12 | 17 |
| Excel sheets | Export info, Indicators | Export info, Indicators, **Lookups** |
| Filtered sample | 27 KB | 26 KB (83 rows) |
| Full catalogue (947) | 159 KB | 212 KB |
| Added to dashboard HTML | ~19 KB JS | ~23 KB JS **+ ~36 KB lookup data** |

New column order:

| # | Column | Source |
|---|---|---|
| 1 | Record ID | `id` |
| 2 | Indicator name | `name` |
| 3 | Framework | `fw` — resolved on the **Lookups** sheet |
| 4 | **Sector** | `sectors` (see §2.4) |
| 5 | NCF category | `ncf` |
| 6 | Geographic scope | `scope` |
| 7 | Units / measure | `units` |
| 8 | Policy goal | `goal` |
| 9 | **GBF targets** | codes (see §2.1) |
| 10 | **GBF target title** | `Short_Title`, GBF Target Lookup |
| 11 | **SDG goals** | codes |
| 12 | **SDG goal text** | `Full_Text_Official`, SDG Goal Lookup |
| 13 | **SDG targets** | codes |
| 14 | **SDG target text** | `Target_Text_Official`, SDG Target Lookup — see §2.3 |
| 15 | Data source | `datasrc` |
| 16 | Climate score | `cs` — resolved on the **Lookups** sheet |
| 17 | Climate rationale | `rat` |

---

## 2. Four things you need to decide or know about

### 2.1 I did not parse GBF targets out of the Policy goal text — and you shouldn't want me to

Your instruction was "where a GBF target is mentioned in Policy goal". I built and tested that
parser against the alternative — the curated `GBF_Targets_Clean` column that already exists on
eight of the nine indicator sheets. Across all 947 records:

- GBF targets recoverable **only** from the prose: **0**
- GBF targets in the clean column but **not** recoverable from the prose: **321 records**

The prose is a strict subset. 321 records say only "…Kunming-Montreal Global Biodiversity
Framework (GBF)" with no target number, while `GBF_Targets_Clean` correctly carries `GBF-T7`
for them. Parsing the prose would silently drop a third of the GBF coverage.

**So: GBF targets come from `GBF_Targets_Clean`.** Result — 727 of 947 records carry at least
one GBF target, and 727 of 727 resolve to a `Short_Title`.

### 2.2 SDG is the opposite case, so I used both sources

Here the clean columns are *not* a superset. `SDG_Goals_Clean` is populated on the **SDG
Indicators** sheet (173 records) and **BIP Indicators** (81) — plus 4 records on EIF/JNCC/EEA
added in workbook v12 — while `SDG_Target_Code` covers the SDG sheet (173) and those same 2
JNCC records. Around **200 further records name SDG goals or targets in the Policy goal prose
alone**, mostly GBF, IPBES and EEA indicators cross-referencing the SDGs.

So SDG goals and targets are the **union** of the clean columns and the parsed prose,
deduplicated and sorted. Result: 470 records carry an SDG goal (all 470 resolve), 352 carry an
SDG target (348 resolve).

*Curating those ~200 prose-only cross-references into the clean columns is an open job* — logged
in the v12 changelog. Until it is done, the export's SDG columns depend on prose parsing for
roughly a fifth of the catalogue.

### 2.3 Two small things in your brief that don't match the workbook

- **"Full_Text_Official from the SDG Target Lookup sheet"** — that sheet has no such column.
  Its columns are `Code, Target_Text_Official, Parent_Goal, Used_In_Workbook, Official_Link`.
  I've used **`Target_Text_Official`**, which is plainly the field you meant. (The SDG *Goal*
  Lookup does have `Full_Text_Official`, and that is what column 12 uses.)
- **4 of the 352 records with an SDG target resolve to blank text** (was 5 before workbook
  v12). The SDG Target Lookup holds 129 of the 169 official targets; SDG-3, SDG-4, SDG-16 and
  SDG-5.1–5.6 are absent by scope. The stragglers are SDG-16.7 (4 records), SDG-5.5 (1) and
  SDG-3.9 (1). SDG-4.7 was added in v12 and now resolves. The code still appears in column 13;
  only the text is empty.

### 2.4 Sector — resolved 16 September 2026 (was the weakest data in this export)

`sectors` used to be generated at build time by `classify_sectors()`, a keyword matcher that
matched bare substrings with no word boundaries: `"mpa"` matched `"impacts"` on 180 records and
`"river"` matched `"drivers"` on 67, so 170 non-marine indicators were tagged Marine.

That is now fixed at source. `classify_sectors()` and `SECTOR_KEYWORDS` have been deleted from
`build_indicator_finder.py`; `sectors` is read straight from the workbook's curated
`Policy_Sector` column, which uses the **14-class controlled vocabulary shared with the
governance workbooks**. The indicator finder and the governance diagram therefore now filter on
the same classes.

Also in workbook v11: the 49 indicator records that had no `Policy_Sector` value were classified
(27 SDG, 13 CBD GBF, 9 across JNCC/SoN/EEA/BIP/IPBES), so all 947 records carry at least one
class and the Sector column is never blank.

| | before | after |
|---|---|---|
| Vocabulary | 7 keyword terms | 14 curated classes |
| Marine | 308 (170 spurious) | 118 |
| Climate | 189 | 160 |
| Blank | 0 (fallback "Cross-cutting") | 0 (all classified) |
| Max per record | unbounded | 3 |

The export's Sector column needed no code change — it reads `r.sectors`, which is now correct.

---

## 3. Excel — `SAMPLE_indicator_export.xlsx`

Three sheets:

1. **Export info** — timestamp, *n* exported / 947, column count, source workbook, and all
   eight filter settings verbatim.
2. **Indicators** — the 17-column table. Header row in the dashboard's green (`#2F5D50`),
   frozen at C2, AutoFilter across `A1:Q{n+1}`, per-field column widths, wrapped text on the
   long fields, climate-score column colour-filled with the dashboard's 0–3 palette.
3. **Lookups** — two stacked tables: **Framework codes** (all nine, with a count of how many
   appear in this export) and **Climate score 0–3** with the canonical definitions lifted
   verbatim from the workbook's `Legend` sheet.

Sizes: 83 indicators → 26 KB; full 947 → 212 KB (`SAMPLE_indicator_export_FULL_947.xlsx`).

## 4. CSV — `SAMPLE_indicator_export.csv`

Same 17 columns, UTF-8 with BOM, CRLF, RFC 4180 quoting. The two lookup tables ride in the
comment block as `#` lines, so the file stays a single artefact:

```
# UK Climate–Nature Indicator Finder — indicator export
# Exported 2026-09-16 17:36,83 of 947 indicators
# Filters: Sector=Climate; NCF category=All; ...
# Source: indicators_climate_nature.xlsx via indicator_finder_v4.html
#
# FRAMEWORK CODES
#,EIF,Environmental Indicator Framework (EIF),4 indicators
#,CCC,CCC Mitigation & Adaptation Monitoring Framework,52 indicators
   ... all nine frameworks ...
#
# CLIMATE SCORE (0–3)
#,0,None,"No relevance to climate or weather. ..."
   ... 0–3 ...
#
# Column headers are on line 25; data begins line 26. Use skip = 24.

Record ID,Indicator name,Framework,Sector,...
```

**`skip` is 24 for every export, not just this one.** That is why all nine frameworks are always
listed rather than only those present — a variable-length header would have meant a different
`skip` each time, which would have been a nasty regression from v2's constant 5. The file also
states its own `skip` on the last comment line, so it is self-documenting either way.

```r
read.csv("indicators_2026-09-16.csv", skip = 24, fileEncoding = "UTF-8-BOM")
```
```python
pd.read_csv("indicators_2026-09-16.csv", skiprows=24, encoding="utf-8-sig")
```

Both verified against the 103-row and 947-row samples: 17 columns, correct header, first
record `GBF-184` / `IND-E-001`.

---

## 5. UI design

Unchanged from v2. One header button `⤓ Export`, styled like `ⓘ Help`, opening a modal that
states the count, offers Excel (default) or CSV, and takes a filename pre-filled from the
active filters:

```
┌─ Export indicators ──────────────────────────────────────────┐
│   103 indicators will be exported                            │
│   Sector = Climate · Climate score ≥ 2 · sorted by score ↓    │
│   (of 947 in the catalogue)                                  │
│                                                              │
│   Format    (•) Excel workbook (.xlsx)        ← default      │
│             ( ) CSV (.csv)                                   │
│                                                              │
│   17 columns · one row per indicator                         │
│                                                              │
│   File name  [ indicators_Climate_cs2plus_2026-09-16    ]    │
│                                                              │
│                              [ Cancel ]   [ Export 103 ]     │
└──────────────────────────────────────────────────────────────┘
```

Chrome and Edge get a native Save-As dialog via `showSaveFilePicker()`; Firefox and Safari fall
back to a download using the modal's filename.

---

## 6. Technical approach

`.xlsx` is a ZIP of XML parts. The dashboard has **zero external references**, so the prototype
writes the container itself: CRC-32 from a precomputed table, compression via the browser's
native `CompressionStream('deflate-raw')` (Chrome 80+, Edge 80+, Firefox 113+, Safari 16.4+)
with automatic fallback to STORED entries, and minimal spec-valid OOXML.

### Verification performed

`indicator_export.js` run under Node 22 against the real 947-record `INDICATORS` array:

| Check | Result |
|---|---|
| ZIP entries use DEFLATE | ✓ all method 8 |
| `.xlsx` opens in openpyxl — filtered | ✓ 3 sheets, Indicators 104 × 17 |
| `.xlsx` opens in openpyxl — full catalogue | ✓ Indicators 948 × 17, 211 KB |
| Styling round-trip | ✓ header fill `FF2F5D50`, freeze `C2`, AutoFilter `A1:Q104`, climate-score fills, widths, wrap |
| Lookups sheet | ✓ 9 frameworks with counts, 4 climate-score rows with Legend definitions |
| GBF resolution | ✓ 727/947 have codes, 727/727 resolve to a title |
| SDG goal resolution | ✓ 470/947 have codes, 470/470 resolve |
| SDG target resolution | ✓ 352/947 have codes, 347/352 resolve (§2.3) |
| CSV `skip` constant | ✓ 24 for both the 103-row and 947-row samples |
| CSV round-trip | ✓ pandas `skiprows=24` → 103 × 17 and 947 × 17, headers correct |
| Unicode | ✓ CO₂, ≥, ’, en-dashes intact in both formats |

The samples in this folder are the **actual output of the JavaScript**, not a Python mock-up.

---

## 7. Integration — now a build-script change, not just an HTML paste

This is the one material change to the plan. v2 needed no change to
`build_indicator_finder.py`. **v3 does**, because none of the new data is currently in the
dashboard:

1. **Two new record fields.** `load_indicators()` must add `sdgg` (`SDG_Goals_Clean`) and
   `sdgt` (`SDG_Target_Code`). `gbf` (`GBF_Targets_Clean`) is already there. Adds ~8 KB to
   `INDICATORS`.
2. **A new injected constant `EXPORT_LOOKUPS`** holding four tables, read from the workbook at
   build time: GBF Target Lookup `Short_Title` (27 rows), SDG Goal Lookup `Full_Text_Official`
   (45), SDG Target Lookup `Target_Text_Official` (127), plus framework code→name and the 0–3
   climate-score scale from `Legend`. **~36 KB.** `inject_js_var()` already does exactly this
   job — it just needs calling a second time, and a matching `const EXPORT_LOOKUPS = {};`
   placeholder in the HTML.
3. **Header, modal and script** into `indicator_finder_v4.html` as before.

`inject_js_var()` replaces only the named declaration, so the export code still survives every
rebuild. The one constraint stands: the export code must not itself contain the literal strings
`const INDICATORS =` or `const EXPORT_LOOKUPS =`. It doesn't.

Storing codes plus lookups rather than resolving the text at build time keeps the HTML ~40 KB
smaller than inlining the official target text on every record, and means a workbook correction
to a target's wording propagates on the next rebuild.

Revised effort: **~4 hours** (was ~3), the extra hour being the build-script work.

---

## 8. Same export on `governance_diagram_v12.html` — still scoped, not built

Unchanged from v2 §8, and re-stated here because you asked what the conflict was.

**The conflict.** You asked me (decision iii, last round) to combine the two separate tables —
Indicators and Policy context — into one, and I agree that was right for this dashboard. But the
governance diagram is a *network*: `const D` holds **293 nodes** and **967 edges**. The nodes are
the legislation, bodies and policies; the edges are the relationships between them, and the
relationships are the entire point of that dashboard. A single combined table can hold one or the
other, not both — 293 rows of nodes, or 967 rows of edges, and neither on its own is the diagram.

So applying "one combined table" there would mean exporting nodes and throwing the network away.
My recommendation is nodes as the primary sheet, edges as a clearly-labelled second sheet in
Excel only — i.e. deliberately *not* following the rule you set here, because the data is shaped
differently. That's the decision I need from you.

Also outstanding for that dashboard:

- A `COLS` array for governance records. Proposed: Record ID, Family, Label, Acronym, Type,
  Sector, Year, Status, Description (`blurb`), Rationale (`rat`), URL, Connections (`deg`).
- The `x` field is an array of `[label, text]` pairs, variable length per node, and doesn't
  flatten into a column. Needs a rule — concatenate, or drop.
- A hook into that dashboard's filter state, which is not the `F` object used here.

Roughly 80% of `indicator_export.js` (ZIP writer, styles, sheet builder, save logic, modal) is
already generic and carries over untouched. **Half a day** once the edges question is settled.

---

## 9. Outstanding decisions

1. **Sector** — fix `classify_sectors()` to use `Policy_Sector` (recommended), export both
   columns, or leave as is? (§2.4)
2. **The 5 unresolved SDG targets** — add SDG-4.7, SDG-16.7, SDG-5.5, SDG-3.9 to the SDG Target
   Lookup, or accept blank text? (§2.3)
3. **Governance diagram: edges** — nodes only, or nodes + an edges sheet in Excel? (§8)
4. **Go-ahead** to integrate into `indicator_finder_v4.html` and `build_indicator_finder.py`?

---

## 9a. v4 variant — one enriched Policy goal instead of six GBF/SDG columns

Prototyped 17 September 2026 at your request; **not yet the default**, and offered alongside
v3 so the two can be compared. Files: `SAMPLE_v4_enriched_goal.xlsx` / `.csv`,
`SAMPLE_v4_enriched_goal_FULL_947.xlsx`, and `indicator_export_v4_enriched.js`.

Columns 9–14 (GBF targets, GBF target title, SDG goals, SDG goal text, SDG targets, SDG target
text) are dropped. Their content is folded into `Policy goal`, but **only where the prose does
not already convey it**.

**The test is "is the meaning already given", not "is the code mentioned".** GBF-071 names both
its codes — `GBF Target 8 / Goal A (component)` — but "(component)" is a classification, not a
gloss, so both titles are added. BIP-074 names seven codes and glosses every one, so it is
returned untouched. Two checks decide it:

1. *Windowed* — for each place the code is named, compare the text up to the next sentence
   break with the code's title. Two content words in common, or a short title substantially
   reproduced ("Life on Land"), counts as glossed.
2. *Whole-prose fallback* — where the code is never named but its substance appears anyway.
   EIF records list aims like "Minimise climate change impacts on biodiversity" without ever
   writing "Target 8"; without this check, 176 additions simply restated the prose. Requiring
   ~60% of the short title anywhere in the text removed all 176.

| | v3 | v4 |
|---|---|---|
| Columns | 17 | **11** |
| Records enriched | — | 682 of 947 (72%) |
| Records already complete | — | 265 |
| Added text median / 90th / max | — | 107 / 178 / 407 chars |
| Additions that restate the prose | — | **0** |
| Filtered sample (83 rows) | 26 KB | 23 KB |
| Full catalogue xlsx | 212 KB | **168 KB** (−21%) |
| Full catalogue CSV | 713 KB | **529 KB** (−26%) |

**Two open points.**

- *SDG target short titles are derived, not curated.* The SDG Target Lookup has only
  `Target_Text_Official`, so the prototype strips a leading "By 2030," and cuts at the first
  clause boundary, capped at 80 characters: *"Take urgent and significant action to reduce the
  degradation of natural…"*. Adding a curated `Short_Title` column to that sheet would remove
  the derivation. GBF titles and SDG **goal** titles are curated already.
- *The codes stop being sortable.* Dropping all six columns means no one can pivot or filter by
  GBF target or SDG goal. Retaining a single `GBF targets` code column alongside the enriched
  prose would cost one column rather than six.

The appended block uses `[code: title; code: title]`; a dash, a line break or another marker is
a one-line change.

---

## 10. Files in this folder

| File | What it is |
|---|---|
| `indicator_export.js` | Working prototype, 23 KB, no dependencies, Node-testable |
| `SAMPLE_indicator_export.xlsx` | Real JS output — 3 sheets, 83 indicators × 17 columns, 26 KB |
| `SAMPLE_indicator_export.csv` | Real JS output — 83 rows, 24-line header block, 65 KB |
| `SAMPLE_indicator_export_FULL_947.xlsx` | Full catalogue, no filters — 947 rows, 212 KB |
| `SAMPLE_v4_enriched_goal.xlsx` / `.csv` | **v4 variant** — 11 columns, enriched Policy goal, 83 rows |
| `SAMPLE_v4_enriched_goal_FULL_947.xlsx` | v4 variant, full catalogue — 947 rows, 168 KB |
| `indicator_export_v4_enriched.js` | v4 prototype module (§9a) |

The two filtered samples use **Sector = Climate, Climate score ≥ 2**, sorted by climate score
descending — 83 of 947 indicators (the count changed from 103 when the Sector vocabulary moved from 7 keyword terms to the 14 curated classes).
