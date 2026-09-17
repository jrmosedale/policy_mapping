# Outstanding issues & next steps — Nature Climate Indicators

Prepared 13 July 2026 for the *Met Office cowork* project. This is the working backlog: what is broken or missing, what is stale, what decisions await Jonathan, and a recommended order for addressing them. It sits alongside `PROJECT_HANDOVER_Nature_Climate_Indicators.md` (context) — read that first.

Confidence is stated per item. Anything marked **needs check** was inferred from file inspection, not confirmed against a working run.

---

## 0. State of play (original snapshot, 13 July 2026 — see the 15 July progress update below for current status)

> The versions and blockers in this section were true when the document was first written. They have since moved on — the **Progress update — 15 July 2026** immediately below supersedes this snapshot (workbooks now UK v21 / intl v14; dashboards rebuilt; the three blockers resolved).

- **Canonical workbooks present**, in `canonical_files/`:
  - `uk_climate_nature_governance.xlsx` — v20 (2026-07-13) *(now v21)*.
  - `international_climate_nature_governance.xlsx` — v13 (2026-07-06) *(now v14)*.
  - `indicators_climate_nature.xlsx` — v10 (2026-07-07); 9 frameworks, 947 indicator records.
- **`check_links.py` passes clean** on all three canonical files, all five invariants PASS.
- Assessment toolkit (`render.py`, method/prompt docs, both mode examples) is complete and usable.
- **Three problems then blocked a clean dashboard rebuild** (a missing `utils.py`, two byte-identical dashboard files, stale hardcoded governance chains) — **all since resolved**; see the progress update.

---

## Progress update — 15 July 2026 (supersedes the state-of-play in §0)

Current versions: UK governance **v21**, international **v14**, indicators **v10**. `check_links.py` passes all five invariants. Live dashboards in `html_dashboards/`: **`governance_diagram_v11.html`**, **`indicator_finder_v4.html`** (climate heatmap deferred). Superseded files archived in `outdated_files/`.

Resolved since first draft:

- **Indicators v14 question (§1): closed** — the v14 build was exploratory and never promoted; canonical stays at v10 / 947 indicators. §1 retained for the record only.
- **Missing files restored** (§2.1, §2.4): `utils.py`, `WORKBOOK_WRITE_PROTOCOL.md`, `build_all.py`.
- **`build_indicator_finder.py` rewritten** — reads the canonical workbook by header, canonical-only (947), self-contained (no `utils.py`), governance chains as `FRAMEWORK_CTX`. Output `indicator_finder_v4.html`.
- **`build_all.py` rewritten** — was fully stale (non-existent `build_eif_indicators`, flat output names). Now runs diagram → finder as subprocesses; verified green.
- **`WORKBOOK_WRITE_PROTOCOL.md` updated** — §3 documents the new Public Bodies columns; §7 rewritten with the column→edge-type table (the old "Dashboards" open thread), the governor→governed arrow convention, and the current downstream-sync reality (no more `GOV_CHAINS`).
- **Governance diagram (§2.3): rebuilt and substantially reworked** to `governance_diagram_v11.html` — regenerated from current workbooks; then: edge direction made semantic and focus-independent (arrows point governor→governed: enabling LEG→record, lead leader→led, parent→child, funder→funded); boundary-terminated, larger arrowheads; per-indicator/per-record narrative sections in the detail panel (Statutory duties, Regulatory powers, Statutory enabling basis, UK ratification/representation/engagement, status); acronym hover tooltips; EU + Soft toggles; grouped controls; and a Help/info modal.
- **Indicator finder** gained a Help/info modal and a `⬡ diagram` deep-link on every policy-context item (opens that record as the focus node in the governance diagram; builder auto-points it at the newest diagram version).
- **Orphan `[CODE]` promotion (§4.5 / §6): actioned.** Analysis in `outputs_other/ORPHAN_CODES_promotion_analysis.md`; 50 missing links promoted into typed columns (workbooks → UK v21, intl v14), incl. two new Public Bodies columns `Related_Bodies` and `Affecting_Policies`. 20 were already shown via reciprocal links. `check_links.py` clean.
- **Dashboard user guidance:** brief in-page Help modals now on both the governance diagram and the indicator finder (partially covers §7's dashboard-docs item).

Still outstanding: `recalc.py` and `fix_eea_chains.py` (§2.4); `build_climate_heatmap.py` unmaintained (deferred); the content/decisions in §4 (MCCIP scaffold, five acronyms, five schema decisions, MO rubric scale-up); the new-policy scan protocol (§5); standalone user-doc/protocol files (§7, §8); and the CHECK-row judgement calls flagged in the orphan-promotion analysis.

---

## 1. Discrepancy to resolve first — indicators workbook version

The handover's session history (§4) describes an **indicators workbook v14: 23 sheets, 1,255 records across 15 frameworks**, adding *Burgess 2024 (573 rows)*, *SDG (173)*, *BIP (81)* and an *SDG Goal Lookup*.

The canonical file actually present is **v10: 18 sheets, 947 records across 9 frameworks**, with **no Burgess 2024 sheet**. So either:

- (a) the v14 build was exploratory and never promoted to canonical — in which case the handover text is misleading and should be corrected; or
- (b) a genuinely newer indicators workbook (v11–v14) exists elsewhere and was not migrated into this project store — in which case it is a **missing file** that supersedes the present canonical.

**Action:** confirm which. If (b), locate and migrate the newer file, re-run `check_links.py`, and archive v10. If (a), correct the handover. Everything downstream (dashboards, indicator scans) depends on knowing the true current indicator set. **Confidence: high that the present canonical is v10/947; the v14 provenance is unresolved.**

---

## 2. Broken / missing files (document-only; nothing rebuilt yet)

### 2.1 `utils.py` is missing — two build scripts cannot run
`build_indicator_finder.py` and `build_climate_heatmap.py` both begin `from utils import *`. No `utils.py` exists anywhere in the project. **Both scripts are non-functional as shipped.** `build_governance_diagram.py` is self-contained (imports `openpyxl` directly, auto-detects canonical filenames) and does *not* need `utils.py`.
**Action:** recover `utils.py` from the previous project machine, or reconstruct it from the two scripts' usage (`INDICATOR_SHEETS`, `inject_js_var`, `js`, workbook-reading helpers). **Confidence: high (confirmed by grep).**

### 2.2 Two dashboard files are byte-identical duplicates
`html_dashboards/indicator_finder_v3.html` and `html_dashboards/climate_heatmap_v2.html` have the **same MD5** and both carry the title *"Climate–Nature Indicator Finder"*. The climate-heatmap dashboard output is therefore **missing / mislabelled** — the file named `climate_heatmap_v2.html` is a copy of the indicator finder, not the heatmap.
**Action:** rebuild the real `climate_heatmap` from `build_climate_heatmap.py` (blocked on §2.1) and replace the duplicate. **Confidence: high (confirmed by MD5).**

### 2.3 `governance_diagram_v8.html` is stale
The embedded metadata reads `generated: 2026-07-12`, 288 nodes / 910 edges, built before the workbook edits of 2026-07-13 (POL-067 Fisheries Act objective, POL-068, ORG-043 FSA, ORG-044 FSS). It does not reflect v20/v13.
**Action:** re-run `python build_governance_diagram.py` from `canonical_files/` and replace. This script works today. **Confidence: high.**

### 2.4 Protocol / build files named in the handover but absent from the store
None of these are present anywhere in the project:

| File | Role (per handover) | Impact of absence |
|---|---|---|
| `WORKBOOK_WRITE_PROTOCOL.md` | The central SOP for *any* workbook change (propose→verify→link-map→write→version/changelog/archive→`check_links` gate→downstream sync). | **High** — the governing protocol for all workbook edits is missing. |
| `build_all.py` | Coordinates the three dashboard builds. | Medium — convenience wrapper. |
| `recalc.py` | Part of the mandatory recalc gate before finalising a version. | Medium — validation step. |
| `fix_eea_chains.py` | EEA topic-classification logic to fold into `build_indicator_finder.py`. | Low — one-off fix, but its logic is referenced as an open thread. |
| `utils.py` | Shared helpers for the two dashboard builders (see §2.1). | High. |

**Action:** recover from the previous project machine where possible; where not recoverable, reconstruct (`WORKBOOK_WRITE_PROTOCOL.md` can be rebuilt from handover §5 + this file). **Confidence: high that they are absent here; unknown whether recoverable elsewhere.**

### 2.5 Hardcoded governance knowledge in the build scripts is stale
`GOV_CHAINS` (in `build_indicator_finder.py`) and `POLICY_CONTEXT` (in `build_climate_heatmap.py`) hardcode framework→legislation→body→policy chains and still reference the old source filename `biodiversity_indicators_v12.xlsx` in their docstrings. These must be updated by hand whenever the governance workbooks change; they have not tracked v19–v20.
**Action:** update both dicts against v20/v13 and fix the docstring source names before the next full rebuild. **Confidence: medium — the dicts are visibly outdated; full audit needs a working run.**

---

## 3. Key protocol / method files (the operating manual)

These are the files that govern how work is done. Two of the five core protocols are **present**; the workbook-write SOP is **missing** (§2.4).

**Policy-assessment workflow**
- `code_files/METHOD_AND_SCORING.md` — fixed methodology + two-axis scoring (Relevance 1–3 × Status/Maturity). **Present.**
- `code_files/PROMPT_TEMPLATE.md` — copy-paste prompt to run a new research field and emit a YAML config. **Present.**
- `code_files/README.md` — assessment-kit overview and run instructions. **Present.**
- `code_files/render.py` — YAML → styled PDF + editable Word. **Present.**
- `code_files/assessment_config.yaml` (applied mode) and `assessment_config_GAP_example.yaml` (gap mode) — worked examples. **Present.**

**Workbook update & integrity**
- `WORKBOOK_WRITE_PROTOCOL.md` — the change SOP. **MISSING (§2.4).**
- `code_files/check_links.py` — five referential-integrity invariants; auto-detects canonical filenames. **Present, passing.**
- `code_files/orphan_codes.py` — finds `[CODE]` mentions in prose not promoted to link columns. **Present.**
- `recalc.py` — recalc gate. **MISSING (§2.4).**

**Dashboard build**
- `code_files/build_governance_diagram.py` — self-contained, works today. **Present.**
- `code_files/build_indicator_finder.py`, `build_climate_heatmap.py` — depend on missing `utils.py`. **Present but non-functional (§2.1).**
- `build_all.py`, `fix_eea_chains.py`, `utils.py` — **MISSING (§2.4).**

---

## 4. Content updates & decisions awaiting Jonathan (from previous chats)

Carried forward from the handover's open threads:

1. **MCCIP indicator scaffold** — decision pending on whether to build the topic-level 26-row scaffold (`outputs_other/MCCIP_indicators_proposed.xlsx` is the current draft). Recommended two-stage build (topic scaffold, then priority indicator-level detail).
2. **Five blank Acronym fields** in international conventions: INT-L-011 CMS, INT-L-013 OSPAR, INT-L-015 BBNJ, INT-L-017 HELCOM, INT-L-020 LDN.
3. **Five open schema decisions:** new General_Type "Operational service / System"; ~~"Health" as a Policy_Sector token~~ (settled v11, 2026-09-16 — in the vocabulary, 38 indicator records); a UKHSA ORG record; handling a UKHSA heat-mortality statistic; the Building Act enabling-legislation LEG ID for Part O.
4. **Scale the MO research→policy relevance rubric** (piloted on 5 entries) to the remaining ~41 policy records — pending three design questions: scope of `Cur_MO`; whether Supplier entries share the main matrix or a separate tab; the confidence floor for a reportable score.
5. **70 orphan `[CODE]` mentions across 42 records** (catalogued in `outputs_other/orphan_narrative_codes.md`) — review and promote genuine relationships into curated link columns, leave incidental mentions as prose.
6. **Ocean-heatwaves follow-up:** v20 added ORG-043/044 and updated POL-068; confirm nothing further outstanding from that assessment.

---

## 5. Searching for newly released policies/indicators — proposed protocol

There is no standing process to catch policies, frameworks or indicators published *after* the current workbook versions. Proposed lightweight SOP (to be written up as `POLICY_SCAN_PROTOCOL.md`):

- **Cadence:** quarterly, plus ad hoc when a major publication is trailed (e.g. a new CCC Progress Report, a JNCC UKBI refresh, a Defra strategy).
- **Watchlist sources:** gov.uk/Defra + agency publication feeds (Natural England, EA, JNCC, MMO, Forestry Commission); legislation.gov.uk new-legislation feed; devolved equivalents (gov.scot, gov.wales, DAERA); CCC, OEP; international (CBD/GBF, IPBES, EEA, MCCIP, UN SDG).
- **Screen:** does it introduce or retire a policy/activity (POL), a body (ORG), legislation (LEG), or an indicator/framework (IND/IFW)? Does any indicator take a climate input (the project's core relevance test)?
- **Triage:** propose additions as marked rows (`†`), never silently add; verify dates/status/URLs against primary sources; route through the workbook-write protocol and `check_links.py`.
- **Automation option:** a scheduled task could assemble a fortnightly/quarterly digest of new items from the watchlist for manual triage. Flag if wanted.

**Confidence: this is a design proposal, not yet agreed.**

---

## 6. Linkage options & outstanding link issues

- **Promote the 70 orphan `[CODE]` mentions** (§4.5) — the single biggest linkage backlog. Decide, per record, promote-to-link-column vs leave-as-prose.
- **Draft the "Dashboards" section for the workbook-write protocol** — column-to-edge mapping and the ratification-based hard/soft classification rule, so link edits stay consistent with the diagram taxonomy.
- **Keep hardcoded chains in sync** (§2.5) — `GOV_CHAINS` / `POLICY_CONTEXT` must be updated on every governance-workbook change; this is a recurring linkage-maintenance liability worth reducing (ideally derive from the workbook rather than hardcode).
- **Bidirectional UK↔international links** currently pass `check_links.py`; keep the reciprocity invariant green on every edit.

---

## 7. User documentation to write

None exists yet. Proposed set (all Markdown, in a `docs/` folder):

1. **Dashboard user guide** — how to open, search, deep-link, and export each of the three HTML dashboards (governance diagram, indicator finder, climate heatmap); what each shows and its data vintage.
2. **Policy-assessment how-to** — end-to-end: pick a field/mode → run `PROMPT_TEMPLATE.md` → edit the YAML → `render.py` → deliver PDF+Word → offer `†` additions. A condensed, task-oriented companion to `METHOD_AND_SCORING.md`.
3. **Canonical-files & update guide** — what the three workbooks are, the stable-filename + internal-version convention, the archive-on-supersede rule, and the mandatory `check_links.py`/recalc gate. Depends on recovering `WORKBOOK_WRITE_PROTOCOL.md` (§2.4).

---

## 8. Additional protocols worth having

- `WORKBOOK_WRITE_PROTOCOL.md` — recover or rewrite (§2.4). **Highest priority protocol.**
- `POLICY_SCAN_PROTOCOL.md` — the new-release scan (§5).
- `DASHBOARD_BUILD_PROTOCOL.md` — the exact rebuild sequence (which script, from which folder, where output lands, how to version and archive the old HTML), including the `GOV_CHAINS`/`POLICY_CONTEXT` update checklist.
- `RELEASE_CHECKLIST.md` — a one-page pre-finalisation gate: `check_links.py` clean → recalc → changelog + version bump → archive superseded → downstream dashboard rebuild.

---

## 9. Recommended order

Sequenced so that integrity and the governing protocol come before any new content, and cheap high-impact fixes come before larger builds.

**Phase A — establish ground truth & recover the rules (do first)**
1. Resolve the **v10-vs-v14 indicators discrepancy** (§1) — everything downstream depends on it.
2. Recover or rewrite **`WORKBOOK_WRITE_PROTOCOL.md`** (§2.4) — no workbook edits should proceed without it.
3. Recover **`utils.py`** and the other missing build files (§2.1, §2.4).

**Phase B — cheap fixes that restore the dashboards**
4. Rebuild **`governance_diagram`** from current workbooks (works today; §2.3).
5. Once `utils.py` is back: rebuild **`indicator_finder`** and the **real `climate_heatmap`**, replacing the duplicate (§2.2), after updating `GOV_CHAINS`/`POLICY_CONTEXT` (§2.5).

**Phase C — content backlog & decisions**
6. Work the **schema/acronym/rubric decisions** (§4.2–§4.4) with Jonathan.
7. **Promote the 70 orphan codes** (§4.5, §6).
8. Decide and, if agreed, **build the MCCIP scaffold** (§4.1).

**Phase D — durable process & docs**
9. Write the **new protocols** (§8) and **user documentation** (§7).
10. Stand up the **policy-scan process** (§5), optionally as a scheduled digest.

---

*Prepared by Claude (Cowork) from a full read of the project store and the previous project's `outputs/` directory. Items marked "needs check" or with stated confidence should be verified before acting.*
