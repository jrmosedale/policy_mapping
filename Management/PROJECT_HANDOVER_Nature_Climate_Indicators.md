# Nature Climate Indicators — project reference

**Current as of 6 October 2026** (workbooks UK governance v33, international v18, indicators v28). This document describes what exists, where it is and how to
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
| `Data/CANONICAL_FILES_GUIDE.md` | Short guide to the three workbooks: contents, linking, versions and archives, reading and changing them. |
| `Dashboards/` | The two generated HTML dashboards, `DASHBOARD_USER_GUIDE.md` (how to use them), and `code/` holding their build scripts. |
| `PA_toolkit/` | The policy-assessment toolkit — everything needed to run a new assessment. |
| `Management/` | This document, the release gate, the export writer, and `protocols/`. |
| `Exports/` | **Generated, never edited.** Written by `export_release.py` at each release. |
| `outputs_other/` | Analysis by-products and method records: `CLIMATE_SCORE_METHOD.md` and the v27 harmonisation review, the export scoping note, MCCIP draft, orphan-code analysis, policy-scan notes and triage workbooks. |
| `presentations/` | Slide decks. |
| `Copilot_setup/` | The GitHub Copilot configuration (`AGENTS.md`, `.github/`), staged for installation at the repository root (§6.1). |

---

## 3. The canonical workbooks

Three interlinked Excel workbooks with **stable filenames**. The version integer lives inside each
workbook at `Changelog!B2` — never in the filename. Superseded copies go to `Data/outdated_files/`
as `<name>_vN_superseded_<date>.xlsx`.

| Role | Filename | Version |
|---|---|---|
| UK governance | `uk_climate_nature_governance.xlsx` | **v33** (2026-10-06) |
| International governance | `international_climate_nature_governance.xlsx` | **v18** (2026-10-06) |
| Indicators | `indicators_climate_nature.xlsx` | **v28** (2026-10-06) |

UK governance holds 49 `ORG`, 69 `LEG` and 114 `POL` records (highest IDs ORG-049, LEG-071, POL-116;
POL-023, POL-024, LEG-008 and LEG-009 retired).

**Indicator content: 1,001 records** across ten framework sheets and **twelve register frameworks** —
EIF 66, CCC 149, JNCC UKBI 77, SoN 2023 32, EEA 62, BIP 81, IPBES 143, CBD GBF 202, UN SDG 173,
MCCIP 16. The
CCC sheet carries three frameworks: [IFW-02] Mitigation Monitoring Framework (79), [IFW-10]
Adaptation Monitoring Framework 2026 (38 proposed targets, IND-C-147 to IND-C-184, added v23) and
[IFW-11] Adaptation Monitoring Framework 2023–2025, superseded but retained (32). The figure was 947
until v23 and 985 until v28; documents citing either predate those versions. [IFW-12] MCCIP (added v28)
holds 16 Impacts Hub topic reviews (IND-M family) — assessment-derived like [IFW-07]; MCCIP's
separate observed and projection confidence ratings are kept in `Framework_Classification`.

> ⚠ **Counting trap.** A naive count of non-empty `Record_ID` returns **1,005**. The CBD GBF sheet
> carries four section-banner rows (`▌ HEADLINE INDICATORS…` and three more) whose divider text sits
> in the `Record_ID` column with no `Indicator_Name`. **Any script counting indicators must require a
> non-empty `Indicator_Name`.**

**Integrity.** `check_links.py` validates every bracketed `[CODE]` against a registry of **1,208**
Record_IDs / Framework_IDs and enforces six invariants (the sixth, added September 2026, validates
every `Controlled` column against the values declared in the Data Dictionary). It must pass clean before any version is
finalised. It is sufficient for referential integrity because the workbooks contain **no
formula cells** — every value is static. It cannot tell whether a URL opens the instrument a record
names: that is `check_legislation_links.py`, the second automated check (§6). Keep it that way: all build scripts read with
`data_only=True`, and openpyxl does not compute formulas.

**The `Cross-Reference Index` sheet in each governance workbook is derived.** `rebuild_xref.py`
regenerates it from the record sheets as step 1 of `finalise.py`; hand edits are overwritten and
nothing reads it.

**The `Data Dictionary` sheet documents the current schema only.** It carries no history. When a
column is added, renamed, re-scoped or removed, edit or delete its row in place; version history
belongs in `Changelog`. The rule is stated in row 2 of the sheet itself.

### Sheet structure worth knowing

- **`Indicator Framework`** — one row per framework (`IFW-01`…`IFW-12`; twelve rows over ten
  sheets). The finder joins indicator rows to this register on `Source_Framework`, so a row's
  `Source_Framework` must match its register row exactly (§4). `Policy_Purpose` carries a
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
- **`Legend`** — the 0–3 `Climate_Score` scale, its core principle and Rules A–H.

### Climate_Score

A **data-dependency** score, not a climate-relevance score: does weather or climate data enter the
indicator's calculation, or does inter-annual weather move its published value? Topical climate
relevance is carried by `Policy_Sector = Climate` instead. Harmonised across all nine sheets in v27
(162 of 985 records changed); distribution 0/1/2/3 = 435/269/201/80 at v27, plus the 16 MCCIP records
scored under the same rules in v28 (0/3/3/10). Blank means *not assessed* and
renders as a hatched badge that never satisfies a score filter. Full method, provenance, borderline
cases and maintenance rules: `outputs_other/CLIMATE_SCORE_METHOD.md`; the review record is in
`outputs_other/climate_score_harmonisation/`. Score new records against the Legend rules, not by
analogy with neighbouring rows.

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

Relationship explorer across all three workbooks. 345 nodes, 1,164 edges (build of 6 October 2026). Six horizontal tiered bands
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
`Key_Instruments` codes are drawn as solid deep-pink edges (28). Precedence: a code already carrying
a `lead` edge keeps it; remaining `Key_Instruments` codes take precedence over the dotted
`indicator` edge; anything left in `Indirect_Policy_Links` stays dotted.

### `indicator_finder_v4.html` — built by `build_indicator_finder.py`

**Policy context is derived, not hardcoded.** Each indicator's right-hand "Policy context" panel is
built from its framework's register row — `Key_Instruments` for designated-monitoring links,
`Indirect_Policy_Links` for policy-relevant ones — resolved against both governance workbooks. The
old `FRAMEWORK_CTX` table was removed on 28 September 2026 after it was found to be keyed on the
sheet (so all 149 CCC rows shared the mitigation chain, including the 38 adaptation targets), to
still cite the superseded CBDP 2023, and to be invisible to `check_links.py`. Chains now change when
the register changes.

> ⚠ **The join is on `Source_Framework`**, row against register row. A mismatch yields an empty
> panel, silently. Fixing the join exposed that **486 of 985 rows** did not match — the CCC rows
> after the v17 rename, and the GBF and SDG rows which carried the frameworks' own fuller titles.
> All are aligned as of indicators v26, and the builder now warns and names any value that does not
> match.

**Hovering a relationship tag** ("Designated monitoring" / "Policy-relevant") names the indicator set
the relationship belongs to, because that claim is about a *framework*, not about the single
indicator on screen, and the panel previously never said which framework was meant.

**Adding a framework sheet** needs two code-side edits besides the workbook: an entry in `FRAMEWORKS`
at the top of `build_indicator_finder.py` (sheet name, short code, label — sheets not listed are not
read) and a filter button in the finder HTML (`setFW('<code>',this)`). Done for MCCIP in v28.

User-facing guide to both dashboards: `Dashboards/DASHBOARD_USER_GUIDE.md`.

Searchable, filterable catalogue of all 1,001 indicators. Filter by sector (the 14 `Policy_Sector`
classes, shared with the governance diagram), NCF category, framework, climate score, geographic
scope and policy-context type; free-text search; centre-panel cards with a right-hand detail panel
carrying units, data source, policy goal, climate score (0–3) and rationale. Every policy-context
item has a `⬡ diagram` deep-link. The Help modal explains the climate score (scale table,
not-assessed badge) and exporting; the footer's workbook versions are filled from each workbook's
`Changelog` at build, so they cannot go stale.

**Export (⤓ Export, header).** Opens a dialog stating how many indicators the current filters have
selected, offering Excel (default) or CSV with an editable pre-filled filename; disabled when
nothing matches. **11 columns**, one row per indicator. The GBF and SDG codes are folded into an
enriched **Policy goal**: a target's `Short_Title` is appended in brackets only where the prose does
not already convey it (676 of 947 records at the 17 September build; not recounted since v23). Sorting or pivoting by GBF/SDG code is not possible —
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

`ASSESSMENT_TOOLKIT_USER_GUIDE.md` is the task-oriented companion for a first-time user.

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
| `Data/code/check_links.py` | **The integrity gate.** Validates every bracketed `[CODE]` across all three workbooks against the ID registry and enforces six invariants — orphan references, column placement, UK↔intl forward and reverse reciprocity, controlled vocabulary against the Data Dictionary, retired-ID reuse. Read-only. Auto-detects canonical filenames, ignoring `_superseded_` archives. |
| `Data/code/check_legislation_links.py` | **The link-title check.** For every `Legislation` record whose Link is on legislation.gov.uk, reads the instrument's title from `<base>/data.xml` and compares it with the record's `Name` (lenient on "The", dashes and trailing annotations such as "(SI 2015/610)"; `EXPECTED` lists records deliberately named otherwise). Fails on a mismatch; warns on a revoked/repealed title or an unreachable site. Spaces requests 2 s apart and caches titles for 30 days in `Data/code/.legislation_title_cache.json` (seeded from the 6 Oct 2026 manual audit, so the first offline runs still report). `--refresh`, `--offline`, `--titles-json`. No new dependency. |
| `Data/code/rebuild_xref.py` | Regenerates the derived `Cross-Reference Index` sheet in both governance workbooks from their record sheets. Run by `finalise.py` as step 1; the only automated write to a canonical workbook, and only to that derived sheet. |
| `Data/code/orphan_codes.py` | Diagnostic companion: finds `[CODE]` mentions in narrative prose that no curated link column captures, so genuine relationships can be promoted. Writes `orphan_narrative_codes.md` and `.csv` to the **current working directory** — run it from `outputs_other/`, or the report lands beside the workbooks. |
| `Dashboards/code/build_governance_diagram.py` | Builds the governance diagram from all three workbooks, parsing each cross-reference column separately so every edge carries a link type. **The entire HTML page lives in a `TEMPLATE` string inside this script** — it writes a fresh file each time, so hand edits to the HTML are lost (§4). Output filename is a hardcoded literal. |
| `Dashboards/code/build_indicator_finder.py` | Builds the indicator finder. Reads the indicators workbook **by header name** (robust to column reordering) and re-injects `INDICATORS` and `EXPORT_LOOKUPS` into the existing v4 HTML, used as both template and output — so hand-made design edits and hand-written code survive a rebuild, but the HTML must exist (§4). Holds no hardcoded governance: each framework's policy context is derived from the `Indicator Framework` register. Prints a warning naming any `Source_Framework` value with no register match and any record with a blank `Climate_Score`; fills the footer versions from each workbook's `Changelog`. |
| `Dashboards/code/build_all.py` | Orchestrator. Runs the two builders in the required order — diagram first, so the finder links to the newest diagram — from the correct working directories. `python3 build_all.py [diagram\|finder]` runs one. |
| `Management/finalise.py` | **The release gate.** Five steps, each only if the previous passed: `rebuild_xref.py` → `check_links.py` → `check_legislation_links.py` → `build_all.py` → `export_release.py`. Exit codes 1 index/check/link check, 2 build, 3 export. Deliberately does *not* bump versions or archive — materiality is a human judgement. `--check` runs the gate alone. |
| `Management/export_release.py` | Writes `Exports/` from the workbooks and Markdown: per-sheet CSVs with a manifest, `.docx` copies of the protocols, method spec, user guide, this document, `pending_additions.md` and `CLIMATE_SCORE_METHOD.md`. The CSVs let GitHub Copilot, pandas and git diffs read workbook content without opening an `.xlsx`; the DOCX copies are for Word readers. Rewrites a file only when its content changes, so unchanged sheets produce no git diff or OneDrive re-sync. An existing output it cannot read (an online-only OneDrive placeholder) is treated as changed and replaced atomically. The `DOC_SOURCES` list sits at the top of the script; bump `CONVERTER_VERSION` whenever the Markdown→DOCX converter changes. |
| `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` | The governing SOP for **any** workbook change: propose → verify → link map → write mechanics → version/changelog/archive → post-write gate → downstream dashboard sync. §7 carries the column→edge-type table. Read before every edit. |
| `Management/protocols/POLICY_SCAN_PROTOCOL.md` | The quarterly scan for new records. Enumerative, not keyword-driven; an overlap match must be the same kind of thing. |
| `PA_toolkit/code/render.py` | YAML → styled PDF (reportlab) + editable DOCX (python-docx). Handles `**bold**` / `*italic*` / `[[label\|url]]` markup, theming, section ordering. |
| `requirements.txt` (×4) | One per code folder, each listing only what that folder needs. Keeps the toolkit independently shippable. |

**Stack.** Python 3; `openpyxl` for workbooks, `reportlab` / `python-docx` / `PyYAML` for
assessments, `pandas` for inspection. Node/npm deliberately avoided — the dashboards are hand-built
HTML/CSS/JS with no dependencies.

### 6.1 AI configuration — GitHub Copilot

GitHub Copilot agent mode in VS Code is the AI environment for managing this project on Met Office
systems (decided October 2026). The Microsoft 365 Agent Builder and Copilot Studio packs drafted in
September, and the `Data/pending_inbox/` mechanism and `.txt` template exports that existed only to
serve them, were retired on 6 October 2026 (copies in `_to_delete/retired_2026-10-06/`, and in git
history at commit e7d744d).

The configuration — `AGENTS.md` (always-on rules), five path-scoped instruction files, seven skills
and five role agents separated by write scope — is staged in `Copilot_setup/` and **has not yet
been installed or tested**. Installation and acceptance tests are in the root `README.md`. No model
is pinned; it is chosen in the chat model picker.

**Design rule: procedure lives in the protocols, routing lives in the skills.** Every agent, skill
and instruction file is a thin pointer to `WORKBOOK_WRITE_PROTOCOL.md`, `POLICY_SCAN_PROTOCOL.md`,
`METHOD_AND_SCORING.md` or `AGENTS.md`. When one of those changes, re-check the pointers:

| Changed | Also check |
|---|---|
| `WORKBOOK_WRITE_PROTOCOL.md` | `AGENTS.md`; the data, dashboards and management instructions; skills `add-record`, `release`; agent `curator` |
| `POLICY_SCAN_PROTOCOL.md` | skills `policy-scan`, `triage-pending`; agent `scanner` |
| `METHOD_AND_SCORING.md`, YAML templates | skill `run-assessment`; the assessments instructions; agent `assessor` |
| `finalise.py`, `export_release.py` | `AGENTS.md` commands; skill `release`; the exports and management instructions |
| Controlled vocabulary, ID families, record counts | `AGENTS.md`; skill `lookup`; the root `README.md` |
| Finder or diagram builders | the dashboards instructions; agent `dashboard-builder` |

Claude desktop project memory, used while the project was built in Claude Cowork, is held outside
the repository and does not travel. Its durable rules are already in `AGENTS.md` and this document.

---

## 7. Making a change

1. **Propose** the change and verify every factual value against primary sources (gov.uk,
   legislation.gov.uk, gov.scot, agency portals, treaty texts) before writing. Blank over guess.
2. **Enumerate the link map** — a single record rarely lives in one cell. Reciprocal touches first.
3. **Write**, respecting the openpyxl hazards in §3.
4. **Bump the version integer** in `Changelog!B2`, write the changelog entry, archive the superseded
   file to `Data/outdated_files/`.
5. **Run `python3 Management/finalise.py`** — Cross-Reference Index regeneration, integrity check,
   legislation link check, then both dashboards, then `Exports/`. Read the builder's warnings: an unmatched `Source_Framework` or an
   unscored record is a warning, not a failure, and does not stop the gate.
6. **Verify structurally afterwards.** Re-read what you wrote and compare against the live headers.
   Two silent openpyxl failures have been caught this way; neither raised an error.

If a dashboard's *design* changed, bump its `_vN` and archive the prior HTML. The finder re-points
`GOV_DIAGRAM` automatically, so a diagram rename is safe provided the old file leaves `Dashboards/`.

---

## 8. Conventions

**Communication** — concise British English; metric units; direct recommendations without hedging;
pushback welcomed; cited sources with explicit confidence levels; state gaps rather than guess.

**Data integrity**

- Never reuse retired Record IDs (`POL-023`, `POL-024`, `LEG-008`, `LEG-009` are permanently retired;
  `check_links.py` holds the list). LEG-008 (BNG, a duplicate of [POL-065]) and LEG-009 (the EPPS, now
  [POL-111]) were retired in v29 because neither is a statutory instrument.
- **The Legislation sheet holds Acts, SIs, Orders and retained/EU instruments only.** A statutory policy
  statement or statutory scheme made under an Act goes in Policies & Activities with the Act as
  `Enabling_Legislation` — precedents [POL-059] Marine Policy Statement, [POL-111] EPPS, [POL-065] BNG.
- Cross-reference codes wrapped in `[CODE]` brackets everywhere **except** `Record_ID` /
  `Framework_ID` primary-key columns — exclude those from any global regex pass.
- No silent controlled-vocabulary additions. Flag new terms for explicit approval.
- Hard/soft international link classification is by **ratification status**, not endpoint type.
- Narrative prose fields are excluded from auto-conversion to edges — hence `orphan_codes.py`.

**ID families** — `LEG-NNN`, `ORG-NNN`, `POL-NNN` (UK); `INT-L/O/P-NNN`, `EU-L-NNN`
(international); `IFW-NN` (frameworks). Indicator Record_IDs are **not** all `IND-x-NNN`:
`IND-E-` EIF, `IND-C-` CCC, `IND-J-` JNCC, `IND-S-` SoN, `IND-B-` EEA, `IND-M-` MCCIP, then the frameworks' own codes —
`BIP-`, `GBF-`, `SDG-`, and `IPBES-N-` / `IPBES-NCP-` / `IPBES-D-`. Gaps in the `IND-C` and `IND-B`
numbering predate July 2026 and are treated as intentional; new records continue from the maximum.

**Devolved tier** *(Jonathan, 18 September 2026)* — the four administrations are held at
administration level ([ORG-034] Scottish Government, [ORG-035] Welsh Government, [ORG-036] Northern
Ireland Executive). No devolved department is held as a record; departments are named in prose in
brackets after the administration. A candidate that is a devolved department is rejected on this rule.

**Controlled vocabulary — `Policy_Sector`.** One vocabulary of **14 classes shared by all three
workbooks**, pipe-separated, max 3 per indicator, uncapped for governance records. Do not fork it
per workbook — both dashboards filter on it.

> Nature & Biodiversity · Marine & Fisheries · Water · Land Use & Agriculture · Urban & Buildings ·
> Trade & Industry · Finance · Health · Climate · Energy · Transport · Biosecurity ·
> Governance, Society & Data · Pollution & Waste

Note the comma in "Governance, Society & Data". `Health` and `Trade & Industry` are in *use* only on
indicator records, but are in *scope* for governance records.

### Scope rules — what is deliberately **not** catalogued

Both rules below were applied repeatedly before they were written down, which meant the same
candidates kept coming back through successive scans. They are decisions, not drift.

**1. Operational agency monitoring statistics are out of scope** *(Jonathan, 11 and 18 September
2026).* Environment Agency dry weather and drought summaries, water situation reports, rainfall and
river flow weekly reports, and equivalent operational series from other agencies are **not**
catalogued as indicator records. They are operational hydrological monitoring, published on a
weekly or monthly operational cycle, and they are not indicators of a policy target.

> ⚠ **Know what this costs.** Drought and water availability is the single largest thematic gap in
> the catalogue, confirmed from three independent source types during the September 2026 scan. The
> workbook holds [IND-C-105] freshwater quality and quantity and [IND-E-044] drought disruption, and
> from indicators v23 the CCC adaptation targets for the water and wastewater system — but no
> drought monitoring series. This is an accepted gap, not an oversight. An earlier note in
> `pending_additions.md` suggesting agency monitoring statistics would "eventually" get their own
> indicators worksheet is **superseded by this rule**; if that changes, change it here first.

**2. Level of generality — indicators are catalogued at framework level, not at site or event
level** *(Jonathan, 18 September 2026).* A candidate is rejected when it is:

- **site- or catchment-specific** where a national series exists — the River Tyne, Tees and Wear
  fish counts were rejected because a generalised national measure is the right level;
- **event reporting rather than monitoring** — the South West octopus bloom, seaweed species new to
  science, and single-catchment salmon stock notices;
- **operational rather than policy-target monitoring** — the provisional Cormorant population
  indices are released early expressly "to enable their use for operational purposes" (Natural
  England licensing of fish-eating bird control), and the underlying Wetland Bird Survey is already
  held at the right generality as [IND-J-010] and [IND-J-013];
- **an activity rather than a measure** — the UK bluefin tuna fishery is a genuine range-shift
  signal but is a fishery, not a monitoring indicator. It would qualify only with a clear monitoring
  series attached.

The test is whether the candidate measures something a framework tracks, at the level the framework
tracks it. A climate-interesting phenomenon is not automatically an indicator.

---

## 9. Open work

Uncompleted work only — completed items are removed, and their record is the workbook `Changelog`, the
queue's `Resolution` column and git history. Checked against the workbooks, the queue and the file store
on 6 October 2026.

### Queue and record backlog

1. **D8 legislative backlog audit — approved, not yet run** (`Data/pending_additions.md`, Status
   `add`): Taxation (Energy and Vehicles) Act 2026, Finance Act 2026 (check for CBAM provisions),
   English Devolution and Community Empowerment Act 2026, and a sweep of 2024–2026 UK primary
   legislation (only part of it is held), with devolved legislation 2021–2025.

2. **Legislation records to check:** [LEG-044] Plant Health (England) Order 2015 is marked revoked —
   identify the current GB plant-health legislation, then decide whether to repurpose or retire the
   record and whether the `Status` vocabulary needs a "Revoked" stem (queued as an `investigate` row;
   inbound from [ORG-020], [POL-033], [POL-034], [POL-052], [INT-L-023]). [LEG-003] and [LEG-049] have not yet been title-checked — the link
   gate will check them on its first run with network access. [LEG-021] links to bills.parliament.uk,
   which the gate does not read.

3. **Eight `investigate` rows remain open** — Land Use Framework 2026 vs [POL-009], SFI26 vs
   [POL-054], revised NPPF, Fisheries Act post-legislative assessment, biodiversity
   gain statements for NSIPs, the Interactive Story Map, JNCC Signpost Series, UKBI 2026 (below).
   Eight rows are `defer`.

### Indicator decisions

4. **Two new `Indicator_Type` terms to confirm** — "Socio-economic statistic" (52 SDG rows) and
   "Hazard impact" (5). Free text, so not gated, but coined without approval.
5. **`GBF_Targets_Clean` is absent** from the SDG, SoN 2023 and MCCIP sheets — one mapping exercise for all three.
6. **~200 records name SDG goals or targets in `Policy_Goal` prose only**, not in the clean columns.
   The dashboard export parses them at runtime; curating them into `SDG_Goals_Clean` /
   `SDG_Target_Code` would remove that dependency.
7. **[IFW-10] carries targets, not indicators**, and `Data_Source` reads "to be confirmed" on all 38
   rows. When the next CCC adaptation progress report publishes the indicators selected against those
   targets, revisit. Also check the objective count (20 captured, CCC states 21) before citing it.

### Coverage

8. **Next quarterly scan — due around early December 2026.** Its window starts on 2 September, the
   date of the last scan note, **except for the sources the 2 September scan never covered**, which
   start from that scan's own window opening, 6 July, so nothing is missed: gov.wales, DAERA,
   NatureScot, SEPA, NRW; the international bodies (CBD, IPBES, Ramsar, CMS, OSPAR, HELCOM, UNFCCC,
   EUR-Lex, EEA); UK statutory instruments; the Block 3 title sweep of operational items;
   forestresearch.gov.uk; 30by30 at sea. Already covered for 6 July – 2 September: ministerial
   statements, Defra, NE/EA/FC/MMO, JNCC, the record-bearing types for UKHSA/DESNZ/MHCLG/DfT/HMT, UK
   Public General Acts 2026, CCC, OEP; gov.scot via pointer pages only
   (`outputs_other/policy_scan_2026-09-02.md`, final tables).
   **Test the search filters before relying on them** (scan protocol §2.0). In September the gov.uk
   date/organisation filters were lost when called through the fetch tool, which dropped the query
   string and returned the whole corpus — a plausible-looking false result — but worked through a
   browser. gov.scot's publication search ignored its URL parameters by either route, so gov.scot is
   enumerated through its policy pointer pages. GitHub Copilot on Met Office systems may behave
   differently again: check that a filtered query returns a filtered result before counting a source
   as enumerated; `.atom` feeds and pointer pages are the fallback.
9. **Watch items.** JNCC UKBI 2026 ([IFW-03] still records UKBI 2025; usually an autumn release, so
    likely imminent); the Nature Recovery Strategy for Northern Ireland to 2032 (approved for adding,
    still a draft — write when adopted; queue Status `add`); the Scottish and Welsh statutory target sets, which both 2026 Acts mandate and
    which will be `IFW` + `IND` candidates when published.

### Content and documentation

10. **Install and test the GitHub Copilot configuration** (§6.1, root `README.md`). Nothing has yet
    run in VS Code; the tool-set names and handoff syntax are from documentation only.
11. **Scale the MO research→policy relevance rubric** from 5 piloted entries to the remaining ~41
    policy records. Three design questions block it: the scope of `Cur_MO`; whether Supplier entries
    share the main matrix or get a separate tab; the confidence floor below which a score is not
    reportable.
12. **Add the two missing completed configs** (biosecurity, LST) to `PA_toolkit/completed_assessments/`
    so all four rendered assessments are reproducible from source. Only `config_dailysun.yaml` and
    `config_ocean_heatwaves.yaml` exist.
13. **CHECK-row judgement calls** left from the orphan-code promotion
    (`outputs_other/ORPHAN_CODES_promotion_analysis.md`).

### Housekeeping

14. **`governance_diagram_v12.html` is arguably due a `_vN` bump** — a link type and the detail-panel
    semantics changed on 17 September, and the data again on 28 September.
15. **The governance diagram's detail panel is `clamp(118px, 20vh, 200px)` tall.** The longest
    framework `Policy_Purpose` now runs to 1,343 characters and scrolls. One CSS line in the
    `TEMPLATE` string of `build_governance_diagram.py` (not the HTML).
16. **`SDG Target Lookup` holds 129 of 169 official targets.** SDG-3, SDG-4, SDG-16 and SDG-5.1–5.6
    are out of scope by decision, but **SDG-11.c is an unexplained singleton gap** — confirm whether
    its deletion from the global framework is the reason.

---

## 10. Standing risks

Three failure modes, none of which fails loudly.

1. **Silent join failures in the finder.** Policy context is now derived from the register, which
   removed the hardcoded `FRAMEWORK_CTX` risk, but it moved the fragility to the `Source_Framework`
   join: a renamed framework or a new sheet whose rows do not match their register row renders with an
   empty policy-context panel. The builder warns and names the offending values, but a warning does not
   stop `finalise.py`. Read the build output after any change to the `Indicator Framework` sheet or to
   `Source_Framework` values; promoting the warning to a build failure would close this.
2. **Completeness decay.** The knowledge base does not decay visibly — a workbook six months stale
   passes every check and builds every dashboard. The only symptom is an absence. Mitigated by the
   quarterly policy scan and `Data/pending_additions.md`, but the scan is manual and depends on
   someone remembering; §8 of the scan protocol says what scheduling it would take. **An approved
   queue is not a written one:** rows at `add` in the queue are invisible to every gate.
3. **Documentation drift.** A protocol or guide referencing tooling, counts or conventions that no
   longer hold causes bad edits, because a diligent reader assumes it is current. It recurs whenever
   code or workbooks change without the documents being re-checked; §6.1 lists which configuration files to re-check.

---

## Self-review (6 October 2026)

**Verified on 6 October against the live files:** workbook versions (`Changelog!B2`); record counts
per sheet (Record_ID and Indicator_Name both non-empty: 985; naive count 989); eleven register rows;
Climate_Score distribution; ORG/LEG/POL counts and highest IDs; `check_links.py` run clean (registry
1,186 after v29, six invariants pass); `finalise.py` step order; diagram node, edge and key-instrument edge
counts from the built HTML; finder footer; lookup-sheet code counts and the SDG-11.c gap; indicator
ID prefixes; `orphan_codes.py` output location; queue statuses, and absence from the workbooks of
every `add` row approved on 10–11 September; the "Operational service / System" term missing from the Data
Dictionary; which completed configs exist; stale counts in the
root README and the GitHub Copilot configuration (corrected 6 October; §6.1).

**Inherited, not re-checked:** "676 of 947" enriched export records (§4; predates v23); the ~200
prose-only SDG records; the MCCIP topic structure and the scan-coverage tables, taken from the scan
note and queue rather than re-enumerated; the next-scan date, which assumes the quarterly cadence.
Confidence: high on the verified items, medium on the inherited ones.
