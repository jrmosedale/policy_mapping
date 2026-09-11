# Project handover — Nature Climate Indicators

**Revised 1 September 2026.** State verified against the file store on that date.

This is the single reference document for the *Met Office cowork* project. It is written for two readers:

- **A new project manager** — read §1 (what this is for), §3 (what has been delivered), §7 (the live backlog) and §8 (an honest assessment of where the project is fragile). Skip §5.
- **A new AI chat** — read §§1–3 for orientation, then **§5 before touching anything**, then §7 to avoid redoing work. Every path below is relative to the project root `MetOffice_cowork_indicators/`.

Companion: `OUTSTANDING_ISSUES_AND_NEXT_STEPS.md` — the older detailed backlog. **§7 here now supersedes it**; it is retained only for the per-item analysis it carries (orphan-code CHECK rows, the v10/v14 provenance record).

---

## 1. Purpose

A Met Office science–policy knowledge base with three goals:

1. **Identify and collate nature-related indicators and metrics** used in UK government policy/reports and international reports — covering biodiversity, ecosystem services, climate change and state of the environment. Outputs: a structured indicator/source database, plus short policy-context notes per source.
2. **Identify which indicators are, or could be, informed by climate data**, and how more spatially explicit metrics could make better use of climate data. This drives the research-to-policy relevance assessment work.
3. **Exploit AI to produce standardised policy-assessment outputs.** A fixed method, a fixed two-axis scoring scheme and a fixed document structure are encoded in the assessment toolkit, so that an AI does the research and drafting for a new Met Office research field while the *method* stays constant. The value is comparability: assessments of different fields, produced months apart by different people, can be read side by side because none of the judgement structure was reinvented. This is the delivery mechanism for goal 2.

The project serves Met Office scientists seeking to understand how climate data and science can better inform nature–climate policy.

---

## 2. Repository layout

| Folder | Contents |
|---|---|
| `PA_toolkit/` | The policy-assessment toolkit — everything a user needs to run a new assessment. User guide, README, prompt, method spec; `template_files/` (the two YAML templates), `code/` (the renderer, which users never edit), `completed_assessments/` (the four rendered assessments and their configs), `bibliographies/`. |
| `Dashboards/` | The two generated HTML dashboards, and `code/` holding the build scripts. |
| `Data/` | `canonical_files/` (the three authoritative workbooks — everything downstream derives from these), `outdated_files/` (archived superseded versions), `code/` (the workbook integrity tools), and `pending_additions.md` — the standing queue of candidate records found but not yet written. |
| `Management/` | This document, `finalise.py` (the release gate), the outstanding-issues file, and `protocols/` holding the two AI-facing protocols for updating the workbooks. |
| `presentations/` | Slide decks. |
| `export_scoping/` | Prototype and scoping note for a dashboard export feature (not yet integrated). |
| `outputs_other/` | Analysis by-products: the MCCIP draft, orphan-code analysis and its reports. Also where a policy scan writes its triage note. |

Reorganised 2 September 2026 from a flat layout, on the principle of grouping by *who needs the file* rather than by file type. `Management/move_manifest.md` records the old→new mapping.

Empty husks of the former directories (`code_files/`, `html_dashboards/`, `canonical_files/`, `outdated_files/`, `biblio/`, `outputs_assessments/`) may still be present, along with `_to_delete/` and `_mvtest/`. They hold nothing that is still in use and can be deleted in Finder.

---

## 3. What has been built

### 3.1 Canonical workbooks — the single source of truth

Three interlinked Excel workbooks in `Data/canonical_files/`, with **stable filenames**. The version integer lives *inside* each workbook, in the `Changelog` sheet at cell B2 — never in the filename. Superseded copies are archived to `Data/outdated_files/`.

| Role | Canonical filename | Version | Sheets |
|---|---|---|---|
| UK governance | `uk_climate_nature_governance.xlsx` | **v21** | Public Bodies, Legislation, Policies & Activities, Data Dictionary, Cross-Reference Index, Changelog |
| International governance | `international_climate_nature_governance.xlsx` | **v14** | Conventions & Treaties, EU Legislation, Associated Bodies, Intl Policies & Activities, Data Dictionary, Cross-Reference Index, Changelog |
| Indicators | `indicators_climate_nature.xlsx` | **v10** | Indicator Framework + 9 framework sheets + SDG/GBF lookups, References, Data Dictionary, Legend, NCF Legend, Changelog |

**Indicator content:** **947 indicator records** across 9 framework sheets — EIF 66, CCC 111, JNCC UKBI 77, SoN 2023 32, EEA 62, BIP 81, IPBES 143, CBD GBF 202, UN SDG 173. Confirmed 2 September 2026 against the figure the builder itself loads.

*One trap, recorded so nobody falls into it twice.* A naive count of non-empty `Record_ID` values returns **951**, and a previous revision of this document wrongly asserted that 951 was correct and the long-quoted 947 was wrong. It is the other way round. The CBD GBF sheet carries four **section-banner rows** (`▌ HEADLINE INDICATORS…`, `▌ BINARY…`, `▌ COMPONENT…`, `▌ COMPLEMENTARY…`) whose divider text sits in the `Record_ID` column with no `Indicator_Name`. They are visual dividers, not records. `build_indicator_finder.py` requires both `Record_ID` and `Indicator_Name` and so correctly loads 947. **Any script counting indicators must require a non-empty `Indicator_Name`.**

**Integrity status — verified 1 September 2026.** `check_links.py` run against all three canonical files: registry of **1,097** Record_IDs / Framework_IDs, **all five invariants PASS**. The indicators workbook's file timestamp had drifted ahead of its internal version; the clean check confirms no unrecorded structural edit, and **v10 is accepted as genuine**. Re-verified after the 2 September reorganisation: check clean, both dashboards rebuild green from the new paths.

### 3.2 Governance and indicator dashboards

Two dashboards in `Dashboards/`. Both are **single self-contained HTML files** — no CDN, no external assets — so they open offline and from `file://`, and can be emailed as they are.

> ⚠ **The two dashboard HTML files must stay in the same directory.** `indicator_finder_v4.html` holds `const GOV_DIAGRAM = "governance_diagram_v12.html"` — a bare filename — and its `⬡ diagram` deep-links resolve relative to the finder's own location. Move or separate them and every deep-link breaks silently: the finder still renders, the links simply go nowhere. `build_indicator_finder.py` re-points that constant at the newest `governance_diagram_v*.html` **in its own output directory**, so it cannot repair a separation either. If either file is ever relocated, the other goes with it.

**`governance_diagram_v12.html`** (365 KB, built by `build_governance_diagram.py`)
Relationship explorer across all three workbooks. Six horizontal tiered bands — international treaties → international bodies / EU law → UK legislation → UK public bodies → UK policy → indicator frameworks — connected by cubic-bezier curves. Features: autocomplete search with keyboard navigation; back/forward and URL-hash deep-linking; SVG/PNG export; depth-2 neighbourhood expansion; zoom/pan; adaptive chip and font sizing; acronym hover tooltips; EU and soft-link toggles; a Help/info modal; and per-record narrative sections in the detail panel (statutory duties, regulatory powers, enabling basis, UK ratification/representation/engagement, status). Edge direction is semantic and focus-independent: arrows point governor → governed.

**Link-type taxonomy** (eight typed edges, ≥3:1 contrast palette): enabling legislation (red solid), lead org/dept (green solid), parent/child (purple solid), related/cross-ref (amber dashed), funded-by (orange dashed), international hard — ratified/retained (teal solid double), international soft — thematic (teal dotted double), indicator/monitoring (magenta dotted). Hard vs soft is decided by **ratification status**, not endpoint type.

**`indicator_finder_v4.html`** (1.06 MB, built by `build_indicator_finder.py`)
Searchable, filterable catalogue of the canonical indicator set — filter by framework, NCF category, geographic scope, sector, climate score and policy context; centre-panel cards with a right-hand detail panel carrying units, data source, policy goal, climate score (0–3) and rationale. Every policy-context item carries a `⬡ diagram` deep-link that opens that record as the focus node in the governance diagram; the builder re-points those links at the newest diagram version automatically. Canonical-only: the 37 "Other / Conceptual" indicators from the pre-canonical build were deliberately dropped.

**Export feature — scoped and prototyped, not shipped.** `export_scoping/` holds a v2 scoping note, a working client-side `indicator_export.js` (Excel + CSV, no external library) and sample outputs including a full-catalogue export. Estimated ~3 hours to integrate into the indicator finder. An equivalent export for the governance diagram is scoped but not built. Awaiting a go/no-go.

### 3.3 Assessment toolkit — research → policy relevance

The delivery mechanism for purpose 3. A self-contained kit for producing comparable assessments of how a Met Office research field could inform UK climate–nature policy, rendered from a single YAML config to **both** a styled PDF and an **editable Word** document.

Two modes, switched entirely in the YAML and never in code: **applied** — where does or could existing MO research inform UK policy, second axis = Status (Current / Opportunity); and **gap / prospective** — if MO built product X, evidenced by others' work elsewhere, what could UK policy do with it, second axis = Maturity (Demonstrated / Emerging / Conceptual). Relevance (materiality, 1–3) is the primary axis in both modes and is deliberately kept separate from the second axis, so that a high-value-but-unrealised link does not read as weak.

**Internet search is part of the method, not an optional extra.** The rendering step is fully offline and deterministic. The *research* step is not: where the AI running the assessment has web access, `PROMPT_TEMPLATE.md` directs it to search rather than rely on the attached files or its own knowledge — to find policy activities absent from the governance workbook, to confirm and date the research→policy channel from primary sources, to verify every status, date and URL against gov.uk / legislation.gov.uk / agency portals, to inspect the flagship MO tool directly, and to scan for authoritative indicators published since the workbook version. Anything found by search that is not in the workbooks is marked with a dagger (†) and offered as a proposed addition in the chat reply — never silently added, and never written into the PDF as though it came from the workbook. Where the AI has **no** web access it renders normally but must list every claim, date and URL it could not verify as "unverified — needs checking", and err toward the lower second-axis value.

**What a user actually needs to run a new assessment.** Six files under `PA_toolkit/`, plus their own inputs:

| Needed | Why |
|---|---|
| `PA_toolkit/code/render.py` | The renderer. Never edited. |
| `requirements.txt` | Three packages. `pip install -r requirements.txt`. |
| `PA_toolkit/PROMPT_TEMPLATE.md` | The prompt to paste into Claude. Its INPUTS block is the only thing filled in per run. |
| `PA_toolkit/METHOD_AND_SCORING.md` | The rules the AI must follow. Attached to the prompt, not read by the code. |
| **One** worked-example YAML — `TEMPLATE_applied.yaml` (applied) or `TEMPLATE_gap.yaml` (gap) | Attached to the prompt as a **format example only**. The AI produces a new config with the same keys. |
| `PA_toolkit/README.md` | Run instructions and the YAML field reference for hand-editing afterwards. |

Plus, as research inputs: a bibliography for the field, the UK governance workbook, and optionally the indicators workbook. **Nothing else in the project is required** — the kit can be zipped and sent to a colleague who has Python 3 and will get the same method, scoring and layout.

**The two classes of YAML are different things and should be named as such.** `TEMPLATE_applied.yaml` and `TEMPLATE_gap.yaml` in `PA_toolkit/template_files/` are *templates* — structural exemplars, attached to the prompt, never rendered as deliverables. The files in `PA_toolkit/completed_assessments/` (`config_dailysun.yaml`, `config_ocean_heatwaves.yaml`) are *records* — the reproducible source of a specific rendered assessment, which belong beside their PDF and DOCX. The split is correct, and the templates were renamed on 1 September 2026 to make the distinction unambiguous. Copy a template to start; save the result as a record.

**Completed assessments** (`PA_toolkit/completed_assessments/`, each with a bibliography in `PA_toolkit/bibliographies/`): plant pest, pathogen & biosecurity (applied); daily sunshine duration (gap); land surface temperature (gap); ocean heatwaves.

### 3.4 Code and protocol inventory

Paths are given relative to the project root.

| File | Role |
|---|---|
| `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` | The governing SOP for **any** workbook change: propose → verify → link map → write mechanics → version/changelog/archive → mandatory post-write gate → downstream dashboard sync. §7 carries the column→edge-type table and the governor→governed arrow convention. Read before every edit. |
| `METHOD_AND_SCORING.md` | Fixed methodology and two-axis scoring for the policy-relevance assessments, including both modes and the indicator-scan discipline. Exists so separate assessments stay comparable with each other. |
| `PROMPT_TEMPLATE.md` | Copy-paste prompt that has an AI research a new field and emit a ready-to-render YAML config. Its INPUTS block is the only part edited per run; it also carries the web-search and dagger-marking rules. |
| `README.md` | Overview and run instructions for the assessment kit — what each file does, how to switch mode in YAML, how to share the kit with a colleague. |
| `render.py` | The renderer: YAML → styled PDF (reportlab) + editable DOCX (python-docx). Handles `**bold**` / `*italic*` / `[[label\|url]]` markup, theming and section ordering. Rarely edited — everything configurable lives in the YAML. |
| `PA_toolkit/template_files/TEMPLATE_applied.yaml` | Worked example, **applied mode** (plant pest, pathogen & biosecurity). The starting point for a new applied assessment. |
| `PA_toolkit/template_files/TEMPLATE_gap.yaml` | Worked example, **gap/prospective mode** (a UK land-surface-temperature product). The starting point for a new gap assessment. |
| `Data/code/check_links.py` | The integrity gate. Validates every bracketed `[CODE]` cross-reference across all three workbooks against a registry of known IDs, and enforces five invariants — orphan references, column placement, UK↔intl forward and reverse reciprocity, retired-ID reuse. Auto-detects canonical filenames, ignoring `_superseded_` archives. Must pass clean before any version is finalised. |
| `Data/code/orphan_codes.py` | Diagnostic companion to `check_links.py`: finds `[CODE]` mentions sitting in narrative prose fields that no curated link column captures, so genuine relationships can be promoted to typed columns. Writes Markdown + CSV to `outputs_other/`. |
| `Dashboards/code/build_governance_diagram.py` | Builds the governance diagram. Reads all three workbooks directly and parses each cross-reference column separately, so every edge carries a link type. Fully self-contained. Output version is set by the `out = …_vN.html` line, currently v12. |
| `Dashboards/code/build_indicator_finder.py` | Builds the indicator finder. Reads the canonical indicators workbook by **header name** (robust to column reordering) and re-injects a fresh `INDICATORS` array into the existing v4 HTML, used as both template and output — so hand-made design edits in the HTML survive a rebuild. `FRAMEWORK_CTX` is the one piece of hardcoded governance knowledge; see §7 item 10. Also re-points the finder's `GOV_DIAGRAM` constant — see the co-location warning in §3.2. |
| `Dashboards/code/build_all.py` | Orchestrator. Runs the two builders as subprocesses in the required order — diagram first, so the finder can link to the newest diagram — from the correct working directories. `python3 build_all.py [diagram\|finder]` runs one. |
| `Management/finalise.py` | The release gate. Runs `check_links.py` and, **only if it passes**, `build_all.py`. Exists because the failure it prevents — finalising a workbook without rebuilding what depends on it — is not caught by running the two by hand, since by hand they are two decisions and one gets skipped. Deliberately does *not* bump versions or archive: materiality is a human judgement. `--check` runs the gate alone. |
| `requirements.txt` (×3) | One per code folder, each listing only what that folder needs: `PA_toolkit/code/` reportlab, python-docx, PyYAML; `Dashboards/code/` and `Data/code/` openpyxl. Splitting them makes the toolkit's "zip it and send it to a colleague" claim true. |

**Retired 1 September 2026.** `build_climate_heatmap.py`, `utils.py` and the mislabelled `climate_heatmap_v2.html` were a dead chain — `utils.py` pointed at a retired project folder on a different machine, and the "heatmap" HTML was a copy of the indicator finder. All three deleted, along with `__pycache__/`. The heatmap is no longer a project deliverable; the indicator finder's climate-score filter covers most of what it was for. Revive only if a specific audience asks for the framework × relevance matrix view.

*Housekeeping remainder:* macOS `.DS_Store` files regenerate on their own and can be ignored (or added to `.gitignore` if this ever goes into version control). One orphaned Word lock file, `~$imate_nature_summary_of_slides.rtf`, remains in the project root — harmless, delete when convenient.

---

## 4. Standing risks

Three failure modes are worth a manager's attention because **none of them fails loudly**:

1. **Hardcoded governance knowledge.** `FRAMEWORK_CTX` in `build_indicator_finder.py` encodes each framework's governance chain by hand. If the governance workbooks change and it is not updated, the dashboard rebuilds cleanly and displays a chain that is quietly wrong. §7 item 10.
2. **Completeness decay.** The knowledge base does not decay visibly — a workbook six months stale still passes every check and builds every dashboard. The only symptom is an absence. Now addressed by `Management/protocols/POLICY_SCAN_PROTOCOL.md` (quarterly, manual, assisted) and by `Data/pending_additions.md`, which captures finds from assessment runs automatically instead of relying on whoever ran the assessment to act on an offer. **The first scan, 2 September 2026, found four missing records — two devolved framework Acts and two environmental governance bodies — so the mechanism was demonstrably needed.** It also *missed* the 30by30 delivery plan published inside its own window, which exposed two method defects now fixed in the protocol: the scan was keyword-driven rather than enumerative (§2.0 now requires enumeration first), and the overlap check accepted an adjacent record — the 30×30 Technical Working Group — as evidence that the 30by30 policy was catalogued (§4 now requires an overlap match to be the same kind of thing). **The gov.uk window enumeration has not yet been re-run, so the first scan remains incomplete for gov.uk sources.** The residual risk is now that a *manual* quarterly scan depends on someone remembering; §8 of the protocol says what putting it on a schedule would take.
3. **Protocol drift.** A protocol that references tooling or conventions which do not exist causes bad edits, because a diligent new person assumes the check ran. One instance of this was found and closed (see §7, closed item 2); the class of problem recurs whenever a protocol is edited without checking the store.

---

## 5. Working conventions (carry into any new chat)

**Communication** — concise British English; metric units only; direct recommendations without hedging; pushback welcomed; cited sources with explicit confidence levels; no corporate tone; state gaps and uncertainty rather than guess.

**Data integrity**
- Never reuse retired Record IDs. Blank over zero/placeholder. No silent controlled-vocabulary additions — flag all new terms for explicit approval.
- Cross-reference codes (LEG, ORG, POL, INT-L/O/P, EU-L, IFW) wrapped in `[CODE]` brackets everywhere **except** `Record_ID` / `Framework_ID` primary-key columns.
- Hard/soft international link classification is by **ratification status**, not endpoint type: hard only when confirmed ratified or retained by the UK.
- Narrative prose fields are excluded from auto-conversion to edges (avoids noisy unvalidated links) — hence `orphan_codes.py`.

**Schema mechanics**
- `insert_rows` in openpyxl is unsafe on striped sheets — use full-region rewrite with deterministic parity re-striping by row index (`FFFDFEFE` even, `FFF4F6F7` odd).
- Exclude `Record_ID` from any global `bracket_codes()` regex pass.
- New columns append trailing only; inherit sibling styles.
- python-docx column widths need `fix_grid()` immediately after table creation.
- The workbooks contain **no formula cells** (verified 1 September 2026, all three files, all sheets). Every value is static. Keep it that way: introducing formulas would break every downstream reader, because all build scripts open workbooks with `data_only=True` and openpyxl does not compute formulas it writes.

**Process** — Propose → verify (web-check against gov.uk, legislation.gov.uk, gov.scot before writing) → build. Then **`python3 Management/finalise.py`**, which runs the integrity check and rebuilds both dashboards only if it passes. `check_links.py` must pass clean before any version is finalised; it is the only automated gate, and it is sufficient given the no-formulas rule above. Version bumps and archiving to `Data/outdated_files/` remain manual — materiality is a judgement call. Assessments: edit YAML → `python PA_toolkit/code/render.py CONFIG.yaml --format both --outdir PA_toolkit/completed_assessments` → validate the DOCX → convert to PDF → rasterise to inspect.

**Controlled vocab — Policy_Sector** (14 classes, pipe-separated, max 3 per indicator; uncapped for governance records): Nature & Biodiversity, Marine & Fisheries, Water, Land Use & Agriculture, Urban & Buildings, Trade & Industry, Finance, Health, Climate, Energy, Transport, Biosecurity, Governance Society & Data, Pollution & Waste.

**ID families** — LEG-NNN, ORG-NNN, POL-NNN (UK); INT-L/O/P-NNN, EU-L-NNN (international); IND-x-NNN, IFW-NN (indicators).

---

## 6. Tools & stack

Python 3. `openpyxl` for workbook reads/writes and styling; `pandas` for inspection; `reportlab` ≥4.0, `python-docx` ≥1.1 and `PyYAML` ≥6.0 for assessment rendering. Node/npm deliberately abandoned for portability — the dashboards are hand-built HTML/CSS/JS with no dependencies.

Validation: `Data/code/check_links.py` (the gate), `Data/code/orphan_codes.py` (diagnostic). Dashboards: `build_governance_diagram.py`, `build_indicator_finder.py`, coordinated by `build_all.py`, all in `Dashboards/code/`. `Management/finalise.py` chains the gate to the rebuild. DOCX/PDF pipeline uses the docx skill's `validate.py`, `soffice --headless --convert-to pdf`, and `pdftoppm` / `pdf2image` for rasterisation. Hyperlinks in YAML configs use `[[label|url]]` markup.

Key domain frameworks: HadUK-Grid, JNCC UKBI, CCC Mitigation/Adaptation Monitoring Frameworks, EIF, EIP, CBD/GBF, MCCIP, NCF, IPBES, BIP, UN SDG, SoN.

---

## 7. Open threads

### Closed since the last revision

1. **Indicators workbook confirmed genuine v10** — `check_links.py` passes all five invariants; the record count settled at 947 (see §3.1).
2. **`recalc.py` closed — the script is not needed, and the protocol was the thing that was wrong.** A recalc gate exists to refresh Excel's cached formula values (openpyxl writes formulas but never computes them, so anything reading with `data_only=True` — which every build script does — would read stale or empty cells) and to regenerate derived rollup sheets. A check of all three workbooks found **zero formula cells**: every value is static, entered directly. There is therefore nothing for a recalc step to recalculate, and it would differ from `check_links.py` only in checking something the workbooks do not contain. **Action taken:** the no-formulas rule is now recorded in §5, and `check_links.py` is stated as the sole gate. The recalc reference has been struck from `WORKBOOK_WRITE_PROTOCOL.md` §6.
3. **`fix_eea_chains.py` closed — the problem it existed to fix is already solved.** Its purpose was to attach governance chains to EEA indicators, which sit awkwardly in a UK-centric governance model: an EEA indicator's chain runs to EU instruments, not UK legislation, so the generic chain-building logic left them bare. The rewritten `build_indicator_finder.py` handles this: all nine frameworks including EEA carry an explicit chain in `FRAMEWORK_CTX`, EEA's pointing at the European Green Deal / Biodiversity Strategy 2030 (INT-P-015) and the EU Nature Restoration Law (EU-L-006). No further action; the missing script can stop being tracked.
4. **Retired the heatmap chain** — three files deleted (§3.4).
5. **`requirements.txt` corrected** — `openpyxl` added, with the two dependency groups commented so a new user knows which packages serve which half of the project.
6. **Orphan `[CODE]` promotion** — the bulk work is done (50 links promoted into typed columns).
7. **Policy scan design settled** (2 September 2026) — manual quarterly built to be schedulable, AI-assisted assembly with human approval and human write, tiered triage cataloguing everything in scope, devolved administrations retained in the standing watchlist. Reasoning recorded in the protocol's §7; §8 covers adding a schedule later.
8. **Daggered finds from assessment runs are now captured, not offered.** Runs append to `Data/pending_additions.md` as a required step. Previously they were offered in a chat reply and captured only if that individual chose to act, which made a shared knowledge base's completeness depend on whoever happened to run the assessment. Changed in `METHOD_AND_SCORING.md` §2 step 7, `PROMPT_TEMPLATE.md` and the user guide §7.
9. **Template YAMLs renamed** to `TEMPLATE_applied.yaml` / `TEMPLATE_gap.yaml`; every dependent document updated (`README.md`, `PROMPT_TEMPLATE.md`, `METHOD_AND_SCORING.md`, `ASSESSMENT_TOOLKIT_USER_GUIDE.md`, this file).
10. **Recalc reference struck** from `WORKBOOK_WRITE_PROTOCOL.md`; its stale references to the retired `build_climate_heatmap.py` and `utils.py` removed at the same time.

### Active work

1. **Approve the four queued records** from the first policy scan (`outputs_other/policy_scan_2026-09-02.md`, queued in `Data/pending_additions.md`): the Natural Environment (Scotland) Act 2026 and the Environment (Principles, Governance and Biodiversity Targets) (Wales) Act 2026 as `LEG`; Environmental Standards Scotland and the Office of Environmental Governance Wales as `ORG`. All four are gaps in existing coverage rather than new publications. A fifth, the draft NI Nature Recovery Strategy, is held pending adoption. Writing them takes UK governance to v22.
2. **Approve or reject the twelve queued items from the retrospective assessment sweep** (`Data/pending_additions.md`). The four completed assessments were re-read for `†` items on 2 September: 15 found, 3 already actioned (POL-067/068/069, from the ocean-heatwave run that continued into a workbook edit), **12 never captured** — the Solar Roadmap 2025, Future Homes Standard, Heat-Health Alerting System, Adverse Weather and Health Plan, Building Regs Part O, NSWWS Extreme Heat warnings, GB Plant Health Risk Register, Defra plant-health contingency plans, Observatree, a UKHSA `ORG` record, and two indicator candidates (MCCIP sea temperature; UKHSA heat mortality, which overlaps IND-C-130).
3. **Settle three of the five open schema decisions — they now block seven queued rows.** The UKHSA `ORG` record (blocks five), the `General_Type` value "Operational service / System" (blocks the NSWWS row and arguably two more), and the Building Act enabling-legislation `LEG` ID for Part O (blocks one). These were logged as abstract questions; they are now on the critical path.
4. **Decide the Environment Act target delivery plan granularity** — thirteen statutory target delivery plans plus an overview were published on 16 July 2026 and none is in the workbook, which currently holds the statute ([LEG-004]) and the plan ([POL-001]) but nothing of the delivery layer. One `POL` for the programme, or thirteen? My recommendation is thirteen, so indicators attach to the right plan and the diagram shows the chain at the level it operates.
5. **Complete the first scan — Defra is done, everything else is not.** All 388 Defra items for 6 July – 2 September are now enumerated, title-swept and screened. **Natural England, the Environment Agency, JNCC, the Forestry Commission, the MMO, UKHSA, DESNZ, legislation.gov.uk, the devolved administrations, the CCC, the OEP and the international bodies remain un-enumerated.** Method: browser + gov.uk search API (a plain fetch drops query strings and silently returns the unfiltered corpus). Two passes have run and each found more than the last: pass 1 found 4 records, pass 2 found 5 more plus 3 supersession/currency checks. Only Defra's Atom feed (reaching back to 19 Aug) and one ministerial statement were enumerated. **Natural England, the Environment Agency, JNCC, the Forestry Commission, the MMO, UKHSA, DESNZ, legislation.gov.uk, the devolved administrations, the CCC, the OEP and the international bodies remain un-enumerated for the 6 July – 2 September window.** Note the gov.uk search API is unusable from this environment — the fetch tool drops query strings and returns the unfiltered corpus, which looks like a successful search; use the `.atom` feeds.
6. **Resolve the EIF currency question — highest priority of the queued items.** The Environmental Indicator Framework was refreshed six times in 2026 (13 Feb, 17 Mar "new indicators updated", 15 Apr, 13 May, 3 Jul, 19 Aug). `[IFW-01]` and its 66 EIF indicator rows may be stale, and whether any indicator was added or retired is unknown. This is the only queued item that touches the indicators workbook's content rather than adding governance records.
7. **Consider a one-off devolved backlog sweep.** The first scan looked only at spring 2026 and found two missed Acts; it did not look further back. If two were missed in six months, auditing devolved legislation 2021–2025 is probably worth an hour.
8. **Watch for the Scottish and Welsh statutory target sets.** Both Acts mandate targets *and* monitoring indicators that do not yet exist. When published they are `IFW` + `IND` candidates and go straight to the project's core climate-input question — the highest-value thing currently on the horizon.
9. **User documentation.** `PA_toolkit/ASSESSMENT_TOOLKIT_USER_GUIDE.md` is now drafted — the end-to-end how-to for the assessment kit. Two pieces remain unwritten: a **dashboard user guide** (what each dashboard shows, its data vintage, how to search, deep-link and export) and a **canonical-files and update guide** (the stable-filename convention, the internal-version rule, the archive-on-supersede discipline). The dashboards' in-page Help modals partly cover the first.
10. **Add the two missing completed configs** (biosecurity, LST) to `PA_toolkit/completed_assessments/`, so all four rendered assessments are reproducible from source. *(The template rename to `TEMPLATE_applied.yaml` / `TEMPLATE_gap.yaml` is done, and all dependent documents updated; the `outputs/` path in `README.md` is corrected.)*
11. **Work the CHECK-row judgement calls** left over from the orphan-code promotion (`outputs_other/ORPHAN_CODES_promotion_analysis.md`) — the residual ambiguous cases.
### Decisions deferred

5. **MCCIP topic-level scaffold** (26 rows) — draft at `outputs_other/MCCIP_indicators_proposed.xlsx`. MCCIP is organised as 26 *topics* with headline messages and confidence ratings, not a quantitative indicator catalogue; decomposing it would yield roughly 40–60 indicator-level rows, of which ~10–15 are climate-driven and ~8–12 overlap existing records. Recommended two-stage build: topic scaffold first, then priority indicator-level detail.
6. **Five open schema questions** — a new `General_Type` value "Operational service / System"; "Health" as a `Policy_Sector` token; whether to add a UKHSA ORG record; how to handle a UKHSA heat-mortality statistic; the Building Act enabling-legislation LEG ID for Part O.
7. **Scale the MO research→policy relevance rubric** from the 5 piloted entries to the remaining ~41 policy records. Three design questions block it: the scope of `Cur_MO`; whether Supplier entries share the main matrix or get a separate tab; the confidence floor below which a score is not reportable.
8. **Integrate the indicator export** into `indicator_finder_v4.html` (~3 h, prototype ready in `export_scoping/`), then decide on the governance-diagram equivalent. Related: whether `gbf` and `sectors` belong in the export — the scoping note flags them as the two excluded fields with real analytical value.

### Answered clarifications

9. **What `DASHBOARD_BUILD_PROTOCOL.md` and `RELEASE_CHECKLIST.md` would do — and my recommendation.**
    - *`DASHBOARD_BUILD_PROTOCOL.md`* would specify: which script builds which dashboard, the working directory each must run from, where output lands, when to bump the `_vN` integer, and how to archive the superseded file. **Recommendation: do not write it.** All of that already exists in two places — `build_all.py`'s docstring documents the scripts, order and cwd; `WORKBOOK_WRITE_PROTOCOL.md` §7 documents the downstream sync. A third copy is a third thing to keep in step, and the same silent-drift risk as §4.1. If anything is missing, it is the version-bump-and-archive rule, which belongs *inside* §7 of the write protocol.
    - *`RELEASE_CHECKLIST.md`* is different in kind and worth having: not a procedure to read but a one-page gate to tick before finalising a version — `check_links.py` clean → changelog entry written → version integer bumped → superseded file archived → affected dashboards rebuilt → dashboard `_vN` bumped and old file archived. Six lines. Its value is that it is short enough to actually be used, and it catches the specific failure of finalising a workbook without rebuilding what depends on it. **Recommendation: write this one, skip the other.** Say the word and I will.

10. **`FRAMEWORK_CTX` — yes, still live, and here is how to fix it.** Retiring the heatmap removed `POLICY_CONTEXT`, its twin. `FRAMEWORK_CTX` is unaffected: it sits in `build_indicator_finder.py`, feeds the policy-context panel of the live indicator finder, and hardcodes a governance chain for each of the nine frameworks. It is currently small — nine chains, eleven distinct governance codes — which makes both fixes cheap.
    - **Option A — derive it from the workbooks (the real fix).** The governance workbooks already carry `Indicator_Frameworks` columns on LEG, ORG and POL records; reversing those gives framework → (legislation, bodies, policies) directly, and `build_governance_diagram.py` already contains the parsing logic to do it. Cost: perhaps half a day, best done when the finder is next rebuilt substantially. Removes the class of problem rather than monitoring it.
    - **Option B — a staleness check (the cheap interim).** Assert that every code in `FRAMEWORK_CTX` still exists in the `check_links.py` registry, and that no governance record points at a framework without appearing in that framework's chain. Roughly an hour, and it converts a silent failure into a loud one — which is most of the value.
    - **Recommendation: B now, A when the finder is next opened.** The danger is not that the chains are wrong today; it is that nothing would tell you if they became wrong.

---

## 8. Review of this document

Written by Claude (Cowork), 1 September 2026, so you can judge how much weight to put on the sections above.

**Verified directly.** §2, §3.1, §3.4 and the closed items in §7 come from reading the file store and running the code. The workbook versions were read from the `Changelog` sheets; the 1,097-ID registry and five PASS results are from an actual `check_links.py` run; the 947-record count is the figure the builder loads, cross-checked against the workbook; the zero-formula finding is a full scan of every cell in all three workbooks; the `FRAMEWORK_CTX` contents were parsed out of the build script. §3.3's account of the assessment method and its search behaviour is drawn from `METHOD_AND_SCORING.md` and `PROMPT_TEMPLATE.md` directly.

**Inherited, not verified.** §5's working conventions, schema mechanics, controlled vocabulary and ID families are carried forward from the previous handover. They are plausible and internally consistent, but I have not re-derived them from the workbooks — I have not, for example, confirmed that the 14 `Policy_Sector` classes match the Data Dictionary. §3.2's dashboard feature lists are compiled from build-script source and prior documentation, not from opening the dashboards and exercising every control. **Confidence: high on the file inventory, integrity results and code behaviour; medium on the convention and feature detail.**

**What I would still fix before relying on this:**

1. **Spot-check §5 against the Data Dictionary.** It is the section a new chat will follow most literally, and the section I verified least. Half an hour would move it from inherited to confirmed.
2. **Open both dashboards and confirm the §3.2 feature lists.** Described from source, not from use. If a listed control has since been removed, a reader loses trust in the whole document.
3. ~~Re-run the builders to prove the dashboards match the workbooks.~~ **Done 2 September 2026** — `finalise.py` ran clean and both dashboards were regenerated from the current workbooks, which also proved the reorganised paths.
4. **Retire `OUTSTANDING_ISSUES_AND_NEXT_STEPS.md` down to its unique content.** It now overlaps this document substantially, and two partly-stale backlogs are worse than one. Cut it back to the per-item analysis §7 only summarises, or fold that in and delete it.

**On splitting this into a manager document and an AI document.** My recommendation is to keep one document, for the same reason that §4 lists silent drift as the main standing risk: two documents sharing sixty per cent of their content will diverge, and the divergence will mislead precisely the reader who trusted the wrong copy. The overlap here is genuinely large — §§1–4 serve both readers, and a new chat needs the backlog as much as a manager does, so that it does not redo settled work. The routing note at the top costs a manager two minutes of skimming, which is cheaper than maintaining a second file. If the reader is a non-technical manager who would be put off by §§3.4 and 5, the right answer is a two-page executive summary that *points at* this document rather than restating it — a summary, not a split. Offered if wanted.
