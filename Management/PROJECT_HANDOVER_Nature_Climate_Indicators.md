# Nature Climate Indicators — project reference

**Current as of 17 September 2026.** This document describes what exists, where it is and how to
use it. It is not a history: settled decisions are not recorded here, only current state and
genuinely unresolved work (§9).

Every path is relative to the project root `MetOffice_cowork_indicators/`.

---

## 1. What this is for

A Met Office science–policy knowledge base with three purposes:

1. **Catalogue nature-related indicators** used in UK government and international reporting —
   biodiversity, ecosystem services, climate change, state of the environment.
2. **Identify which indicators are, or could be, informed by climate data**, and where more
   spatially explicit metrics would make better use of it.
3. **Produce standardised policy-assessment outputs** — a fixed method, scoring scheme and
   document structure so that assessments of different research fields, written months apart,
   remain comparable.

The audience is Met Office scientists asking how climate data and science can better inform
nature–climate policy.

---

## 2. Repository layout

| Folder | Contents |
|---|---|
| `Data/canonical_files/` | The three authoritative workbooks. Everything downstream derives from these. |
| `Data/outdated_files/` | Archived superseded workbook and dashboard versions. |
| `Data/code/` | Workbook integrity tools. |
| `Data/pending_additions.md` | Standing queue of candidate records found but not yet written. |
| `Dashboards/` | The two generated HTML dashboards; `code/` holds their build scripts. |
| `PA_toolkit/` | The policy-assessment toolkit — everything needed to run a new assessment. |
| `Management/` | This document, the release gate, the export writer, and `protocols/`. |
| `Exports/` | **Generated, never edited.** Written by `export_release.py` at each release. |
| `outputs_other/` | Analysis by-products: MCCIP draft, orphan-code analysis, policy-scan notes. |
| `export_scoping/` | Design record for the indicator export, now shipped. Deletable — §9 item 15. |
| `presentations/` | Slide decks. |
| `Copilot_setup/` | Instructions and skills for porting the knowledge base to Microsoft 365 / Copilot Studio. |

---

## 3. The canonical workbooks

Three interlinked Excel workbooks with **stable filenames**. The version integer lives inside each
workbook at `Changelog!B2` — never in the filename. Superseded copies go to `Data/outdated_files/`
as `<name>_vN_superseded_<date>.xlsx`.

| Role | Filename | Version |
|---|---|---|
| UK governance | `uk_climate_nature_governance.xlsx` | **v21** |
| International governance | `international_climate_nature_governance.xlsx` | **v14** |
| Indicators | `indicators_climate_nature.xlsx` | **v16** |

**Indicator content: 947 records** across nine framework sheets — EIF 66, CCC 111, JNCC UKBI 77,
SoN 2023 32, EEA 62, BIP 81, IPBES 143, CBD GBF 202, UN SDG 173.

> ⚠ **Counting trap.** A naive count of non-empty `Record_ID` returns **951**. The CBD GBF sheet
> carries four section-banner rows (`▌ HEADLINE INDICATORS…` and three more) whose divider text sits
> in the `Record_ID` column with no `Indicator_Name`. **Any script counting indicators must require a
> non-empty `Indicator_Name`.**

**Integrity.** `check_links.py` validates every bracketed `[CODE]` against a registry of **1,097**
Record_IDs / Framework_IDs and enforces five invariants. It must pass clean before any version is
finalised. It is the only automated gate, which is sufficient because the workbooks contain **no
formula cells** — every value is static. Keep it that way: all build scripts read with
`data_only=True`, and openpyxl does not compute formulas.

**The `Data Dictionary` sheet documents the current schema only.** It carries no history. When a
column is added, renamed, re-scoped or removed, edit or delete its row in place; version history
belongs in `Changelog`. The rule is stated in row 2 of the sheet itself.

### Sheet structure worth knowing

- **`Indicator Framework`** — one row per framework (`IFW-01`…`IFW-09`). `Policy_Purpose` carries a
  prose statement of each framework's purpose and policy range, written from primary documentation.
  `Key_Instruments` holds bracketed governance codes **only** for the instruments named in that
  purpose text: the body creating/hosting/using the framework, its statutory basis, and the key
  policies or international instruments it informs.
- **Nine framework sheets** — 15 columns common to all, plus framework-specific ones. See the
  Data Dictionary for the exhaustive list.
- **Three lookup sheets** — `GBF Target Lookup` (27 codes: 4 goals, 23 targets), `SDG Goal Lookup`
  (the 17 goals, goals only), `SDG Target Lookup` (129 of the 169 official targets — the
  environment-relevant subset; SDG-3, SDG-4, SDG-16 and SDG-5.1–5.6 are out of scope). All three
  carry `Short_Title` (curated, concise) and the official wording, plus a `Used_In_Workbook` flag
  recomputed from actual use.

### openpyxl hazards, learned the hard way

Both of these fail **silently** — the file saves without error and the loss is invisible until
something downstream misbehaves. Verify after any structural edit.

- **`insert_cols` / `insert_rows` do not move hyperlinks.** Worksheet-level hyperlinks stay anchored
  to the old coordinate and reappear in the new column. **Append columns rather than inserting**
  unless the sheet is known hyperlink-free. The only hyperlinks in the indicators workbook are
  `CCC Indicators` (111) and `JNCC UK Biodiversity Indicators` cells `S15`, `S46`, `S64`.
- **Writes to a merged cell are discarded on save.** Unmerge before rewriting a sheet, then verify
  the result against the live headers.

---

## 4. The dashboards

Two **single self-contained HTML files** in `Dashboards/` — no CDN, no external assets. They open
offline, from `file://`, and can be emailed as they are.

> ⚠ **The two files must stay in the same directory.** `indicator_finder_v4.html` holds
> `const GOV_DIAGRAM = "governance_diagram_v12.html"` — a bare filename — and its `⬡ diagram`
> deep-links resolve relative to its own location. Separate them and every deep-link breaks
> silently. `build_indicator_finder.py` re-points that constant at the newest
> `governance_diagram_v*.html` **in its own output directory**, so it cannot repair a separation.

### How the two builders treat their HTML — they are opposites

This catches people out, so it is worth being explicit. Both builders write a dashboard HTML file,
but only one of them *reads* it first.

| | `build_indicator_finder.py` | `build_governance_diagram.py` |
|---|---|---|
| Needs an existing HTML? | **Yes** — `indicator_finder_v4.html` is both template and output | **No** — the whole page lives in a `TEMPLATE = r"""…"""` string inside the `.py` |
| What a rebuild does | Reads the file, replaces `const INDICATORS = […]` and `const EXPORT_LOOKUPS = {…}`, writes it back | Substitutes `/*DATA*/` with fresh JSON and writes a brand-new file |
| Hand edits to the HTML | **Survive** every rebuild | **Destroyed** on the next rebuild, silently |
| Where the design and code live | In the HTML | In the `.py` |

**Consequences.**

- **Never hand-edit `governance_diagram_v12.html`.** Change the `TEMPLATE` string in
  `build_governance_diagram.py` instead. Editing the HTML looks like it works — the file is valid
  and opens correctly — and the work vanishes at the next `finalise.py` with no warning.
- **`indicator_finder_v4.html` is authoritative for its own design and for any hand-written code it
  contains**, including the ~23 KB export module. The builder only swaps those two `const`
  declarations; it cannot regenerate the page from parts. Deleting or reverting that file loses the
  export code, which exists nowhere else. It is recoverable from git, not from the build.
- If the finder's HTML is ever lost, the builder **cannot** rebuild it — there is no template to
  fall back on. If that risk matters, the fix is to move the hand-written blocks into
  `Dashboards/code/` and have the builder assemble the page, which would make it behave like the
  diagram builder.
- The diagram's output filename is a **hardcoded literal** in the script
  (`"governance_diagram_v12.html"`), so a version bump means editing that string, not a variable.

### `governance_diagram_v12.html` — built by `build_governance_diagram.py`

Relationship explorer across all three workbooks. 293 nodes, 983 edges. Six horizontal tiered bands
(international treaties → international bodies / EU law → UK legislation → UK public bodies → UK
policy → indicator frameworks) joined by cubic-bezier curves. Autocomplete search, back/forward and
URL-hash deep-linking, SVG/PNG export, depth-2 neighbourhood expansion, zoom/pan, acronym tooltips,
EU and soft-link toggles, Help modal, and per-record narrative sections in the bottom detail panel.
Arrow direction is semantic and focus-independent: governor → governed.

**Nine link types** (≥3:1 contrast palette): enabling legislation (red solid), lead org/dept (green
solid), parent/child (purple solid), related/cross-ref (amber dashed), funded-by (orange dashed),
international hard — ratified/retained (teal solid double), international soft — thematic (teal
dotted double), key instrument (deep-pink solid), indicator/monitoring (magenta dotted). Hard vs
soft is decided by **ratification status**, not endpoint type.

**Indicator frameworks.** Selecting an `IFW` node shows its `Policy_Purpose` in the bottom panel
under "Policy purpose", with record count and scope in a secondary "Coverage" section. Its
`Key_Instruments` codes are drawn as solid deep-pink edges (23). Precedence: a code already carrying
a `lead` edge keeps it; remaining `Key_Instruments` codes take precedence over the dotted
`indicator` edge; anything left in `Indirect_Policy_Links` stays dotted.

### `indicator_finder_v4.html` — built by `build_indicator_finder.py`

Searchable, filterable catalogue of all 947 indicators. Filter by sector (the 14 `Policy_Sector`
classes, shared with the governance diagram), NCF category, framework, climate score, geographic
scope and policy-context type; free-text search; centre-panel cards with a right-hand detail panel
carrying units, data source, policy goal, climate score (0–3) and rationale. Every policy-context
item has a `⬡ diagram` deep-link.

**Export (⤓ Export, header).** Opens a dialog stating how many indicators the current filters have
selected, offering Excel (default) or CSV with an editable pre-filled filename; disabled when
nothing matches. **11 columns**, one row per indicator. The GBF and SDG codes are folded into an
enriched **Policy goal**: a target's `Short_Title` is appended in brackets only where the prose does
not already convey it (676 of 947 records). Sorting or pivoting by GBF/SDG code is not possible —
accepted trade-off.

Generated entirely client-side with no external library: the `.xlsx` ZIP container is written
in-page using a small CRC-32 implementation and the browser's native `CompressionStream`, falling
back to stored (uncompressed) entries where unavailable. Excel output is three sheets (Export info,
Indicators, Lookups); CSV is one flat table with the lookups in a comment header, **data from line
26, `skip = 24`, constant for every export**.

> ⚠ **Never let the literal string `</script>` appear in code pasted into the dashboard HTML** —
> including inside comments. It terminates the script block and everything after it silently
> becomes stray text.

---

## 5. Assessment toolkit — research → policy relevance

A self-contained kit producing comparable assessments of how a Met Office research field could
inform UK climate–nature policy, rendered from one YAML config to **both** a styled PDF and an
**editable Word** document.

Two modes, switched entirely in the YAML and never in code:

- **applied** — where does or could existing MO research inform UK policy. Second axis = Status
  (Current / Opportunity).
- **gap / prospective** — if MO built product X, evidenced by others' work elsewhere, what could UK
  policy do with it. Second axis = Maturity (Demonstrated / Emerging / Conceptual).

Relevance (materiality, 1–3) is the primary axis in both and is deliberately separate from the
second axis, so a high-value-but-unrealised link does not read as weak.

**Internet search is part of the method, not an optional extra.** Rendering is offline and
deterministic; the *research* step is not. Where the AI has web access, `PROMPT_TEMPLATE.md` directs
it to verify every status, date and URL against primary sources and to scan for indicators published
since the workbook version. Anything found that is not in the workbooks is marked with a dagger (†)
and **appended to `Data/pending_additions.md`** — never silently added. Without web access it
renders normally but must list every unverified claim and err toward the lower second-axis value.

**To run one**, six files under `PA_toolkit/` plus your own inputs:

| File | Role |
|---|---|
| `code/render.py` | The renderer. Never edited. |
| `code/requirements.txt` | Three packages. |
| `PROMPT_TEMPLATE.md` | The prompt to paste into Claude; its INPUTS block is the only per-run edit. |
| `METHOD_AND_SCORING.md` | The rules the AI follows. Attached to the prompt, not read by code. |
| `template_files/TEMPLATE_applied.yaml` **or** `TEMPLATE_gap.yaml` | Format example only. |
| `README.md` | Run instructions and YAML field reference. |

Plus a bibliography for the field, the UK governance workbook, and optionally the indicators
workbook. **Nothing else in the project is required** — the kit can be zipped and sent to anyone
with Python 3.

**Templates vs records.** `template_files/` holds *templates* — structural exemplars, attached to
the prompt, never rendered as deliverables. `completed_assessments/` holds *records* — the
reproducible source of a specific rendered assessment, beside its PDF and DOCX. Copy a template to
start; save the result as a record.

**Completed assessments** (`completed_assessments/`, bibliographies in `bibliographies/`): plant
pest, pathogen & biosecurity (applied); daily sunshine duration (gap); land surface temperature
(gap); ocean heatwaves.

Run: `python PA_toolkit/code/render.py CONFIG.yaml --format both --outdir PA_toolkit/completed_assessments`

---

## 6. Code inventory

| File | Role |
|---|---|
| `Data/code/check_links.py` | **The integrity gate.** Validates every bracketed `[CODE]` across all three workbooks against the ID registry and enforces five invariants — orphan references, column placement, UK↔intl forward and reverse reciprocity, retired-ID reuse. Auto-detects canonical filenames, ignoring `_superseded_` archives. |
| `Data/code/orphan_codes.py` | Diagnostic companion: finds `[CODE]` mentions in narrative prose that no curated link column captures, so genuine relationships can be promoted. Writes Markdown + CSV to `outputs_other/`. |
| `Dashboards/code/build_governance_diagram.py` | Builds the governance diagram from all three workbooks, parsing each cross-reference column separately so every edge carries a link type. **The entire HTML page lives in a `TEMPLATE` string inside this script** — it writes a fresh file each time, so hand edits to the HTML are lost (§4). Output filename is a hardcoded literal. |
| `Dashboards/code/build_indicator_finder.py` | Builds the indicator finder. Reads the indicators workbook **by header name** (robust to column reordering) and re-injects `INDICATORS` and `EXPORT_LOOKUPS` into the existing v4 HTML, used as both template and output — so hand-made design edits and hand-written code survive a rebuild, but the HTML must exist (§4). `FRAMEWORK_CTX` is the one piece of hardcoded governance knowledge (§10). |
| `Dashboards/code/build_all.py` | Orchestrator. Runs the two builders in the required order — diagram first, so the finder links to the newest diagram — from the correct working directories. `python3 build_all.py [diagram\|finder]` runs one. |
| `Management/finalise.py` | **The release gate.** Runs `check_links.py` and, only if it passes, `build_all.py`, then `export_release.py`. Deliberately does *not* bump versions or archive — materiality is a human judgement. `--check` runs the gate alone. |
| `Management/export_release.py` | Writes `Exports/` from the workbooks and Markdown: per-sheet CSVs with a manifest, `.docx` copies of the protocols, method spec, user guide, this document and `pending_additions.md`, `.txt` copies of the YAML templates. Rewrites a file only when its content changes, so unchanged sheets produce no git diff or OneDrive re-sync. |
| `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` | The governing SOP for **any** workbook change: propose → verify → link map → write mechanics → version/changelog/archive → post-write gate → downstream dashboard sync. §7 carries the column→edge-type table. Read before every edit. |
| `Management/protocols/POLICY_SCAN_PROTOCOL.md` | The quarterly scan for new records. Enumerative, not keyword-driven; an overlap match must be the same kind of thing. |
| `PA_toolkit/code/render.py` | YAML → styled PDF (reportlab) + editable DOCX (python-docx). Handles `**bold**` / `*italic*` / `[[label\|url]]` markup, theming, section ordering. |
| `requirements.txt` (×4) | One per code folder, each listing only what that folder needs. Keeps the toolkit independently shippable. |

**Stack.** Python 3; `openpyxl` for workbooks, `reportlab` / `python-docx` / `PyYAML` for
assessments, `pandas` for inspection. Node/npm deliberately avoided — the dashboards are hand-built
HTML/CSS/JS with no dependencies.

---

## 7. Making a change

1. **Propose** the change and verify every factual value against primary sources (gov.uk,
   legislation.gov.uk, gov.scot, agency portals, treaty texts) before writing. Blank over guess.
2. **Enumerate the link map** — a single record rarely lives in one cell. Reciprocal touches first.
3. **Write**, respecting the openpyxl hazards in §3.
4. **Bump the version integer** in `Changelog!B2`, write the changelog entry, archive the superseded
   file to `Data/outdated_files/`.
5. **Run `python3 Management/finalise.py`** — integrity check, then both dashboards, then `Exports/`.
6. **Verify structurally afterwards.** Re-read what you wrote and compare against the live headers.
   Two silent openpyxl failures have been caught this way; neither raised an error.

If a dashboard's *design* changed, bump its `_vN` and archive the prior HTML. The finder re-points
`GOV_DIAGRAM` automatically, so a diagram rename is safe provided the old file leaves `Dashboards/`.

---

## 8. Conventions

**Communication** — concise British English; metric units; direct recommendations without hedging;
pushback welcomed; cited sources with explicit confidence levels; state gaps rather than guess.

**Data integrity**

- Never reuse retired Record IDs (`POL-023`, `POL-024` are permanently retired).
- Cross-reference codes wrapped in `[CODE]` brackets everywhere **except** `Record_ID` /
  `Framework_ID` primary-key columns — exclude those from any global regex pass.
- No silent controlled-vocabulary additions. Flag new terms for explicit approval.
- Hard/soft international link classification is by **ratification status**, not endpoint type.
- Narrative prose fields are excluded from auto-conversion to edges — hence `orphan_codes.py`.

**ID families** — `LEG-NNN`, `ORG-NNN`, `POL-NNN` (UK); `INT-L/O/P-NNN`, `EU-L-NNN`
(international); `IND-x-NNN`, `IFW-NN` (indicators).

**Controlled vocabulary — `Policy_Sector`.** One vocabulary of **14 classes shared by all three
workbooks**, pipe-separated, max 3 per indicator, uncapped for governance records. Do not fork it
per workbook — both dashboards filter on it.

> Nature & Biodiversity · Marine & Fisheries · Water · Land Use & Agriculture · Urban & Buildings ·
> Trade & Industry · Finance · Health · Climate · Energy · Transport · Biosecurity ·
> Governance, Society & Data · Pollution & Waste

Note the comma in "Governance, Society & Data". `Health` and `Trade & Industry` are in *use* only on
indicator records, but are in *scope* for governance records.

---

## 9. Open work

### Queued records awaiting approval

1. **Four records from the first policy scan** (`Data/pending_additions.md`): the Natural
   Environment (Scotland) Act 2026 and the Environment (Principles, Governance and Biodiversity
   Targets) (Wales) Act 2026 as `LEG`; Environmental Standards Scotland and the Office of
   Environmental Governance Wales as `ORG`. All are coverage gaps, not new publications. Writing
   them takes UK governance to v22. A fifth, the draft NI Nature Recovery Strategy, is held pending
   adoption.
2. **Twelve items from the retrospective assessment sweep** (`Data/pending_additions.md`) — Solar
   Roadmap 2025, Future Homes Standard, Heat-Health Alerting System, Adverse Weather and Health
   Plan, Building Regs Part O, NSWWS Extreme Heat warnings, GB Plant Health Risk Register, Defra
   plant-health contingency plans, Observatree, a UKHSA `ORG` record, and two indicator candidates
   (MCCIP sea temperature; UKHSA heat mortality, which overlaps IND-C-130).

### Schema decisions blocking those rows

3. **Three decisions now on the critical path**: the UKHSA `ORG` record (blocks five rows), a new
   `General_Type` value "Operational service / System" (blocks NSWWS and arguably two more), and the
   Building Act enabling-legislation `LEG` ID for Part O (blocks one).
4. **Environment Act target delivery plan granularity.** Thirteen statutory delivery plans plus an
   overview were published 16 July 2026 and none is in the workbook, which holds the statute
   (`LEG-004`) and the plan (`POL-001`) but nothing between. One `POL` or thirteen? Recommendation:
   thirteen, so indicators attach to the right plan and the diagram shows the chain at the level it
   operates.

### Coverage

5. **The first policy scan is incomplete.** All 388 Defra items for 6 July – 2 September are
   enumerated and screened. **Natural England, the Environment Agency, JNCC, the Forestry
   Commission, the MMO, UKHSA, DESNZ, legislation.gov.uk, the devolved administrations, the CCC, the
   OEP and the international bodies remain un-enumerated.** Use the `.atom` feeds — the gov.uk
   search API is unusable from this environment, because the fetch tool drops query strings and
   returns the unfiltered corpus, which looks like a successful search.
6. **EIF currency — highest priority queued item.** The Environmental Indicator Framework was
   refreshed six times in 2026 (13 Feb, 17 Mar "new indicators updated", 15 Apr, 13 May, 3 Jul,
   19 Aug). `IFW-01` and its 66 indicator rows may be stale, and whether any indicator was added or
   retired is unknown. The only queued item touching indicator *content* rather than governance.
7. **Devolved backlog sweep.** The first scan looked only at spring 2026 and found two missed Acts.
   Auditing devolved legislation 2021–2025 is probably worth an hour.
8. **Watch for the Scottish and Welsh statutory target sets.** Both Acts mandate targets *and*
   monitoring indicators that do not yet exist. When published they are `IFW` + `IND` candidates and
   go straight to the project's core climate-input question.
9. **~200 records name SDG goals or targets in `Policy_Goal` prose only**, not in the clean columns.
   The dashboard export parses them at runtime; curating them into `SDG_Goals_Clean` /
   `SDG_Target_Code` would remove that dependency for roughly a fifth of the catalogue.

### Content and documentation

10. **MCCIP topic-level scaffold** (26 rows) — draft at `outputs_other/MCCIP_indicators_proposed.xlsx`.
    MCCIP is 26 *topics* with headline messages and confidence ratings, not a quantitative
    catalogue; decomposing it yields ~40–60 indicator rows, ~10–15 climate-driven, ~8–12 overlapping
    existing records. Recommended: topic scaffold first, then priority detail.
11. **Scale the MO research→policy relevance rubric** from 5 piloted entries to the remaining ~41
    policy records. Three design questions block it: the scope of `Cur_MO`; whether Supplier entries
    share the main matrix or get a separate tab; the confidence floor below which a score is not
    reportable.
12. **Two user guides unwritten** — a dashboard guide (what each shows, data vintage, how to search,
    deep-link and export) and a canonical-files guide (stable-filename convention, internal-version
    rule, archive-on-supersede discipline). The in-page Help modals partly cover the first.
13. **Add the two missing completed configs** (biosecurity, LST) to `PA_toolkit/completed_assessments/`
    so all four rendered assessments are reproducible from source.
14. **CHECK-row judgement calls** left from the orphan-code promotion
    (`outputs_other/ORPHAN_CODES_promotion_analysis.md`) — the residual ambiguous cases.

### Housekeeping

15. **`export_scoping/` can be deleted.** The indicator export shipped on 17 September; the
    directory is a design record with no runtime role and nothing in the project reads it. The
    `.js` files duplicate code now living in the dashboard HTML, and the samples are reproducible
    in two clicks from the dashboard. **Move `EXPORT_SCOPING_NOTE.md` to `outputs_other/` first**
    if the reasoning is worth keeping — why GBF codes come from `GBF_Targets_Clean` rather than the
    prose, why SDG needs both sources, and how the gloss test decides what to append.
16. **`OUTSTANDING_ISSUES_AND_NEXT_STEPS.md` should be retired** down to its unique content (the
    per-item analysis this section only summarises), or folded in and deleted. Two partly-stale
    backlogs are worse than one.
17. **`governance_diagram_v12.html` is arguably due a `_vN` bump** — a link type and the detail-panel
    semantics changed on 17 September.
18. **The governance diagram's detail panel is `clamp(118px, 20vh, 200px)` tall.** Framework
    `Policy_Purpose` text now runs to 808 characters and scrolls. One CSS line if you want it taller.
19. **`SDG Target Lookup` holds 129 of 169 official targets.** SDG-3, SDG-4, SDG-16 and SDG-5.1–5.6
    are out of scope by decision, but **SDG-11.c is an unexplained singleton gap** — worth
    confirming whether its deletion from the global framework is the reason.
20. One orphaned Word lock file, `~$imate_nature_summary_of_slides.rtf`, sits in the project root.
    Harmless; delete when convenient. `.DS_Store` files regenerate and can be ignored.

---

## 10. Standing risks

Three failure modes, none of which fails loudly.

1. **Hardcoded governance knowledge.** `FRAMEWORK_CTX` in `build_indicator_finder.py` encodes each
   framework's governance chain by hand — nine chains, eleven distinct codes. If the governance
   workbooks change and it is not updated, the dashboard rebuilds cleanly and displays a chain that
   is quietly wrong.
   *Fix A (real):* derive it from the workbooks. `Indicator_Frameworks` columns on LEG/ORG/POL
   records reverse into framework → instruments, and `build_governance_diagram.py` already has the
   parsing logic. Half a day.
   *Fix B (cheap interim):* assert in `check_links.py` that every `FRAMEWORK_CTX` code exists in the
   registry, and that no governance record points at a framework without appearing in its chain.
   About an hour, and it converts a silent failure into a loud one.
   **Recommendation: B now, A when the finder is next opened substantially.**
2. **Completeness decay.** The knowledge base does not decay visibly — a workbook six months stale
   passes every check and builds every dashboard. The only symptom is an absence. Mitigated by the
   quarterly policy scan and `Data/pending_additions.md`, but the scan is manual and depends on
   someone remembering; §8 of the scan protocol says what scheduling it would take.
3. **Protocol drift.** A protocol referencing tooling or conventions that do not exist causes bad
   edits, because a diligent reader assumes the check ran. Recurs whenever a protocol is edited
   without checking the file store.
