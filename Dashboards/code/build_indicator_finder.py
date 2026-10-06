#!/usr/bin/env python3
"""
Rebuild script: indicator_finder.html  (rewritten 2026-07-13)
=============================================================
Regenerates the Climate–Nature Indicator Finder dashboard from the CURRENT
canonical indicators workbook.

What changed vs the old build
-----------------------------
The previous version read a pre-canonical workbook (`biodiversity_indicators_v12/13.xlsx`)
with obsolete sheet names, hard-wired absolute paths to another machine, and injected a
`GOV_CHAINS` variable that the current dashboard no longer uses. This rewrite:

  * reads the canonical `indicators_climate_nature.xlsx` (v10: 9 framework sheets, 947 rows),
    mapping columns by HEADER NAME (not position) so it is robust to schema drift;
  * emits the 18-field record shape the dashboard expects
    (id, name, fw, fw_full, ncf, scope, cs, goal, units, datasrc, code, rat, gbf,
     sdgg, sdgt, sectors, itype, ctx);
  * injects EXPORT_LOOKUPS — the GBF/SDG/framework/climate-score tables the
    client-side export resolves codes against;
  * attaches each framework's governance chain via the hardcoded FRAMEWORK_CTX table
    below (this replaces GOV_CHAINS — one chain per framework, shared by its indicators);
  * uses paths relative to the repo, with CLI overrides;
  * uses the existing dashboard HTML as a pure template (shell + static lookup vars)
    and re-injects a freshly built INDICATORS array.

It is CANONICAL-ONLY: the 37 "Other / Conceptual" indicators that were present in the
live v3 file are not in the workbook and are intentionally dropped (per decision 2026-07-13).

Maintenance
-----------
There is NO hardcoded governance in this builder. The policy-context chains are read from the
indicators workbook's `Indicator Framework` sheet — `Key_Instruments` for designated-monitoring
links and `Indirect_Policy_Links` for policy-relevant ones — and resolved against both governance
workbooks. To change what a framework's chain shows, edit the register row, not this file.

Usage
-----
    python3 build_indicator_finder.py
    python3 build_indicator_finder.py --xlsx <indicators.xlsx> --template <v3.html> --out <v4.html>

Exit code 0 = written OK.
"""
import argparse
import json
import re
import sys
from pathlib import Path

from openpyxl import load_workbook

# ── Repo-relative default paths ────────────────────────────────────────────────
HERE      = Path(__file__).resolve().parent            # .../Dashboards/code
DASH_DIR  = HERE.parent                                 # .../Dashboards
ROOT      = DASH_DIR.parent                             # .../MetOffice_cowork_indicators
CANON     = ROOT / "Data" / "canonical_files" / "indicators_climate_nature.xlsx"
CANON_UK  = ROOT / "Data" / "canonical_files" / "uk_climate_nature_governance.xlsx"
CANON_INT = ROOT / "Data" / "canonical_files" / "international_climate_nature_governance.xlsx"
# v4 is the current design (top nav removed, sidebar climate-score palette matched to the
# centre badges, columns rebalanced). The builder reads it as the template AND refreshes it
# in place, so re-running only swaps the INDICATORS data and preserves all design edits.
# The read completes before the write, so template == output is safe.
TEMPLATE  = DASH_DIR / "indicator_finder_v4.html"       # design source (shell + static vars)
OUT       = DASH_DIR / "indicator_finder_v4.html"

# ── Framework config: sheet name → (short code, full label) ────────────────────
# Order controls display order. fw_full matches the live dashboard's labels.
FRAMEWORKS = [
    ("EIF Indicators",                  "EIF",   "Environmental Indicator Framework (EIF)"),
    ("CCC Indicators",                  "CCC",   "CCC Monitoring Frameworks"),  # three frameworks share this sheet: IFW-02, IFW-10, IFW-11
    ("JNCC UK Biodiversity Indicators", "JNCC",  "JNCC UK Biodiversity Indicators 2025"),
    ("SoN 2023 Indicators",             "SoN",   "State of Nature 2023"),
    ("EEA Biodiversity Indicators",     "EEA",   "EEA Biodiversity Indicators"),
    ("BIP Indicators",                  "BIP",   "Biodiversity Indicators Partnership (BIP)"),
    ("IPBES Indicators",                "IPBES", "IPBES Indicators"),
    ("CBD GBF Indicators",              "GBF",   "CBD Kunming-Montreal GBF Indicators"),
    ("SDG Indicators",                  "SDG",   "UN Sustainable Development Goals"),
]

# ── Governance chains, DERIVED from the register ──────────────────────────────
# Until September 2026 this was FRAMEWORK_CTX: a hardcoded table, one chain per framework,
# keyed on the short framework code. Three things were wrong with that.
#   1. The key was effectively the SHEET, so every framework sharing a sheet shared a chain.
#      All 149 CCC rows got the mitigation chain, including the 38 adaptation targets, which
#      were shown as governed by the Carbon Budget Orders rather than by CCA 2008 s.58 and NAP3.
#   2. It went stale invisibly. It still cited POL-004 (CBDP 2023) after that was marked
#      superseded, and its own comment claimed validation against UK workbook v20 when the
#      workbook had reached v26.
#   3. check_links.py could not see it, because it was Python source rather than workbook data.
#      The gate passed while the content rotted — the same failure as the Cross-Reference Index.
# The register already holds this per framework: Key_Instruments is the designated-monitoring
# relationship, Indirect_Policy_Links the policy-relevant one. So the chains are read from there
# and resolved against the governance workbooks. There is now NO hardcoded governance in this
# builder, which brings it into line with build_governance_diagram.py.

TIER_BY_FAMILY = {
    "LEG":   "UK Legislation",
    "ORG":   "Statutory body",
    "POL":   "Policy activity",
    "INT-L": "International",
    "INT-O": "International body",
    "INT-P": "International policy",
    "EU-L":  "EU Legislation",
    "IFW":   "Indicator framework",
}
CODE_RE = re.compile(r"\[([A-Z]{2,4}-[A-Z]?-?\d{1,3})\]")


def _family(code):
    return code.rsplit("-", 1)[0]


def load_governance_records(*paths):
    """{record_id: (name, link)} across the governance workbooks."""
    out = {}
    for path in paths:
        if not path.exists():
            print(f"  WARNING: governance workbook not found, chains will be incomplete: {path}")
            continue
        wb = load_workbook(path, data_only=True, read_only=True)
        for sn in wb.sheetnames:
            ws = wb[sn]
            first = next(ws.iter_rows(min_row=1, max_row=1), None)
            if not first:
                continue
            hdr = [c.value for c in first]
            if "Record_ID" not in hdr or "Name" not in hdr:
                continue
            i_id, i_nm = hdr.index("Record_ID"), hdr.index("Name")
            i_lk = hdr.index("Link") if "Link" in hdr else None
            for row in ws.iter_rows(min_row=2, values_only=True):
                rid = row[i_id]
                if not rid or rid in out:
                    continue
                link = row[i_lk] if i_lk is not None and i_lk < len(row) else None
                out[str(rid).strip()] = (row[i_nm], link)
        wb.close()
    return out


def load_framework_ctx(canon_path, gov):
    """{Source_Framework: [ctx item]} from the register's Key_Instruments / Indirect_Policy_Links."""
    wb = load_workbook(canon_path, data_only=True, read_only=True)
    if "Indicator Framework" not in wb.sheetnames:
        wb.close()
        return {}
    ws = wb["Indicator Framework"]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
    idx = {h: i for i, h in enumerate(hdr) if h}
    # a framework may cite another framework (JNCC's England suite feeds the EIF), so IFW codes
    # resolve against this same sheet rather than the governance workbooks
    gov = dict(gov)
    for r in rows:
        fid = r[idx["Framework_ID"]] if "Framework_ID" in idx else None
        nm = r[idx["Source_Framework"]] if "Source_Framework" in idx else None
        if fid and nm:
            gov[str(fid).strip()] = (nm, r[idx["Official_Link"]] if "Official_Link" in idx else None)
    ctx, unresolved = {}, set()
    for row in rows:
        fid = row[idx["Framework_ID"]] if "Framework_ID" in idx else None
        name = row[idx["Source_Framework"]] if "Source_Framework" in idx else None
        if not fid or not name:
            continue                                   # banner and TOTAL rows
        items, seen = [], set()
        for col, mon in (("Key_Instruments", True), ("Indirect_Policy_Links", False)):
            if col not in idx:
                continue
            for code in CODE_RE.findall(str(row[idx[col]] or "")):
                if code in seen:
                    continue                           # Key_Instruments wins on a duplicate
                seen.add(code)
                rec = gov.get(code)
                if not rec:
                    unresolved.add(f"{fid}:{code}")
                    continue
                items.append({"id": code, "name": rec[0],
                              "tier": TIER_BY_FAMILY.get(_family(code), "Policy activity"),
                              "url": rec[1] or "", "mon": mon})
        ctx[str(name).strip()] = items
    wb.close()
    if unresolved:
        print(f"  WARNING: {len(unresolved)} register code(s) did not resolve to a governance "
              f"record and were dropped from the chains: {', '.join(sorted(unresolved))}")
    return ctx

# ── Policy sector (read from the workbook; 14-class controlled vocabulary) ─────
# Replaced the former keyword-based `classify_sectors()` on 2026-09-16. That function
# matched bare substrings with no word boundaries, so "mpa" matched "impacts" (180
# records) and "river" matched "drivers" (67), tagging 170 non-marine indicators as
# Marine. The workbook's curated `Policy_Sector` column is now the single source, and
# it shares its vocabulary with the governance workbooks — so the indicator finder and
# the governance diagram filter on the same 14 classes.
# Order controls the order of the sector tiles in the dashboard sidebar.
POLICY_SECTORS = [
    "Nature & Biodiversity", "Climate", "Land Use & Agriculture", "Marine & Fisheries",
    "Water", "Pollution & Waste", "Energy", "Transport", "Urban & Buildings",
    "Biosecurity", "Health", "Finance", "Trade & Industry", "Governance, Society & Data",
]


def parse_sectors(value: str):
    """Split a pipe-separated Policy_Sector cell into a list, warning on unknown terms."""
    terms = [t.strip() for t in (value or "").split("|") if t.strip()]
    for t in terms:
        if t not in POLICY_SECTORS:
            print(f"  WARNING: Policy_Sector value not in the controlled vocabulary: {t!r}")
    return terms


def cell_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def cell_score(v):
    """Climate_Score as an int, or None when the cell is blank.

    NOT cell_int(). Until September 2026 the climate score was read with cell_int(), which
    returns 0 for a blank cell, so the 173 SDG records that had never been assessed rendered
    as score 0 — indistinguishable from the 283 records assessed and genuinely scored zero.
    An unassessed record must stay visibly unassessed: blank maps to None, the page renders it
    as 'not assessed', and it never satisfies a 'climate score >= N' filter."""
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    try:
        return max(0, min(3, int(v)))
    except (TypeError, ValueError):
        return None


def load_indicators(xlsx_path: Path, framework_ctx: dict):
    """Read all framework sheets, mapping columns by header name. Returns list of dicts."""
    wb = load_workbook(xlsx_path, data_only=True, read_only=True)
    records = []
    unscored = []
    no_chain = set()
    for sheet, fw_short, fw_full in FRAMEWORKS:
        if sheet not in wb.sheetnames:
            print(f"  WARNING: sheet '{sheet}' not in workbook — skipped")
            continue
        ws = wb[sheet]
        rows = ws.iter_rows(values_only=True)
        header = [str(c).strip() if c is not None else "" for c in next(rows)]
        idx = {h: i for i, h in enumerate(header)}

        def g(row, *names):
            for n in names:
                if n in idx and row[idx[n]] not in (None, ""):
                    return str(row[idx[n]]).strip()
            return ""

        n_sheet = 0
        for row in rows:
            rid = g(row, "Record_ID")
            name = g(row, "Indicator_Name")
            if not rid or not name:
                continue
            rec = {
                "id":       rid,
                "name":     name,
                "fw":       fw_short,
                "fw_full":  fw_full,
                "ncf":      g(row, "NCF_Category"),
                "scope":    g(row, "Scope"),
                "cs":       cell_score(row[idx["Climate_Score"]]) if "Climate_Score" in idx else None,
                "goal":     g(row, "Policy_Goal"),
                "units":    g(row, "Units_Measure"),
                "datasrc":  g(row, "Data_Source"),
                "code":     g(row, "Indicator_Code"),          # blank where the sheet has none
                "rat":      g(row, "Climate_Rationale"),
                "gbf":      g(row, "GBF_Targets_Clean"),
                "sdgg":     g(row, "SDG_Goals_Clean"),          # blank where the sheet has none
                "sdgt":     g(row, "SDG_Target_Code"),          # blank where the sheet has none
                "itype":    g(row, "Indicator_Type"),
            }
            if rec["cs"] is None:
                unscored.append(rec["id"])
            rec["sectors"] = parse_sectors(g(row, "Policy_Sector"))
            # keyed on the row's own Source_Framework, so frameworks sharing a sheet
            # (IFW-02 / IFW-10 / IFW-11 all live on "CCC Indicators") get their own chains
            rec["fw_set"] = str(g(row, "Source_Framework")).strip()
            # The chain belongs to the FRAMEWORK, not to the indicator, so it is injected once
            # as CTX_BY_SET and looked up by fw_set. Copying it onto all 985 records added about
            # 900 KB to the page for no information.
            if not framework_ctx.get(rec["fw_set"]):
                no_chain.add(rec["fw_set"])
            records.append(rec)
            n_sheet += 1
        print(f"  {sheet:<34} {fw_short:<6} {n_sheet:>4} indicators")
    wb.close()
    if no_chain:
        print(f"  WARNING: {len(no_chain)} Source_Framework value(s) have no matching register row, "
              f"so those rows render with an EMPTY policy context: {', '.join(sorted(no_chain))}")
    if unscored:
        print(f"  WARNING: {len(unscored)} record(s) have no Climate_Score and will render as "
              f"'not assessed': {', '.join(unscored[:12])}{' …' if len(unscored) > 12 else ''}")
    print(f"  TOTAL {len(records)} indicators across {len(FRAMEWORKS)} frameworks")
    return records


def load_export_lookups(xlsx_path: Path, records):
    """Build the EXPORT_LOOKUPS payload the client-side export needs.

    Shape: {gbf|sdgGoal|sdgTgt: {code: [short] or [short, full]}, fw: {...}, cs: {...}}
    The full text is carried only where it differs from the short title; the export
    uses `short` for display and `full` to decide whether a Policy_Goal already
    glosses the code.
    """
    wb = load_workbook(xlsx_path, data_only=True, read_only=True)

    def pairs(sheet, short_col, full_col, goals_only=False):
        ws = wb[sheet]
        rows = ws.iter_rows(values_only=True)
        hdr = [str(c).strip() if c is not None else "" for c in next(rows)]
        ci = hdr.index("Code")
        si, fi = hdr.index(short_col), hdr.index(full_col)
        out = {}
        for r in rows:
            if len(r) <= max(ci, si, fi) or not r[ci]:
                continue
            code = str(r[ci]).strip()
            if not code.startswith(("GBF-", "SDG-")):
                continue
            if goals_only and "." in code:
                continue
            short = str(r[si]).strip() if r[si] else ""
            full = str(r[fi]).strip() if r[fi] else ""
            if not short:
                continue
            out[code] = [short] if (not full or full == short) else [short, full]
        return out

    lk = {
        "gbf":     pairs("GBF Target Lookup", "Short_Title", "Full_Text_Official"),
        "sdgGoal": pairs("SDG Goal Lookup", "Short_Title", "Full_Text_Official", goals_only=True),
        "sdgTgt":  pairs("SDG Target Lookup", "Short_Title", "Target_Text_Official"),
    }
    # framework code -> full name, in canonical order
    lk["fw"] = {short: full for _, short, full in FRAMEWORKS}
    # climate score scale, lifted from the Legend sheet
    leg = list(wb["Legend"].iter_rows(values_only=True))
    scale = {}
    for r in leg:
        if not r or not r[0]:
            continue
        m = re.match(r"^([0-3])\s*[\u2013-]\s*(\w+)", str(r[0]).strip())
        if m:
            scale[m.group(1)] = {"label": m.group(2),
                                 "desc": str(r[1]).strip() if len(r) > 1 and r[1] else ""}
    lk["cs"] = scale
    wb.close()
    print(f"  Lookups: GBF {len(lk['gbf'])}, SDG goals {len(lk['sdgGoal'])}, "
          f"SDG targets {len(lk['sdgTgt'])}, frameworks {len(lk['fw'])}, "
          f"climate-score levels {len(lk['cs'])}")
    missing = [c for r in records for c in
               [t.strip() for t in (r.get("gbf") or "").split(";") if t.strip()]
               if c not in lk["gbf"]]
    if missing:
        print(f"  WARNING: {len(set(missing))} GBF code(s) used by records but absent "
              f"from the lookup: {sorted(set(missing))[:6]}")
    return lk


def inject_js_var(html: str, var_name: str, value_json: str) -> str:
    """Replace `const VAR = ...;` in the HTML, tracking brace/bracket depth and strings."""
    m = re.search(rf'const {re.escape(var_name)}\s*=\s*', html)
    if not m:
        raise ValueError(f"'const {var_name}' not found in template")
    start, val_start = m.start(), m.end()
    if html[val_start] not in ('[', '{'):
        raise ValueError(f"Expected [ or {{ after 'const {var_name} ='")
    depth = 0
    in_str = escape = False
    i = val_start
    while i < len(html):
        c = html[i]
        if escape:
            escape = False
        elif c == '\\' and in_str:
            escape = True
        elif c == '"':
            in_str = not in_str
        elif not in_str:
            if c in ('[', '{'):
                depth += 1
            elif c in (']', '}'):
                depth -= 1
                if depth == 0:
                    end = i + 1
                    if end < len(html) and html[end] == ';':
                        end += 1
                    break
        i += 1
    new_block = f'const {var_name} = {value_json};'
    print(f"  Injected {var_name} ({len(value_json) // 1024} KB)")
    return html[:start] + new_block + html[end:]


def build(xlsx=CANON, template=TEMPLATE, out=OUT):
    xlsx, template, out = Path(xlsx), Path(template), Path(out)
    print(f"Indicators : {xlsx}")
    print(f"Template   : {template}")
    print(f"Output     : {out}\n")
    for p in (xlsx, template):
        if not p.exists():
            print(f"FATAL: not found — {p}")
            sys.exit(2)

    gov = load_governance_records(CANON_UK, CANON_INT)
    framework_ctx = load_framework_ctx(xlsx, gov)
    print(f"  governance records read: {len(gov)}")
    for fw, items in framework_ctx.items():
        mon = sum(1 for x in items if x["mon"])
        flag = "  <-- NO CHAIN" if not items else ""
        print(f"  chain  {fw[:46]:<48} {len(items):>2} link(s) ({mon} designated){flag}")

    indicators = load_indicators(xlsx, framework_ctx)
    html = template.read_text(encoding="utf-8")
    data_json = json.dumps(indicators, ensure_ascii=False, separators=(",", ":"))
    html = inject_js_var(html, "INDICATORS", data_json)

    lookups = load_export_lookups(xlsx, indicators)
    html = inject_js_var(html, "CTX_BY_SET",
                         json.dumps(framework_ctx, ensure_ascii=False, separators=(",", ":")))

    html = inject_js_var(html, "EXPORT_LOOKUPS",
                         json.dumps(lookups, ensure_ascii=False, separators=(",", ":")))

    # Point the "⬡ diagram" deep-links at the newest governance diagram in the folder.
    def _ver(p):
        m = re.search(r"_v(\d+)\.html$", p.name)
        return int(m.group(1)) if m else -1
    govs = sorted(DASH_DIR.glob("governance_diagram_v*.html"), key=_ver)
    if govs:
        gd = govs[-1].name
        html = re.sub(r'const GOV_DIAGRAM\s*=\s*"[^"]*";', f'const GOV_DIAGRAM = "{gd}";', html)
        print(f"  Linked GOV_DIAGRAM -> {gd}")

    # Counts shown as static text (Help panel, footer, header tag) — filled from the data at each
    # build (added 2026-09-28). They were typed into the template and still read 947 after v23
    # took the catalogue to 985; nothing flagged it because no step compared them to the data.
    n_ind = len(indicators)
    n_fw = len({r["fw"] for r in indicators if r.get("fw")})
    words = "zero one two three four five six seven eight nine ten eleven twelve".split()
    fw_word = words[n_fw] if n_fw < len(words) else str(n_fw)
    for pat, rep in [
        (r'(<span id="help-count">)[^<]*(</span>)', rf"\g<1>{n_ind}\g<2>"),
        (r'(<span id="help-fw-count">)[^<]*(</span>)', rf"\g<1>{fw_word}\g<2>"),
        (r'(<span id="footer-count">)[^<]*(</span>)', rf"\g<1>{n_ind} indicators · {n_fw} frameworks\g<2>"),
        (r'(<span class="hd-tag" id="total-tag">)[^<]*(</span>)', rf"\g<1>{n_ind} indicators\g<2>"),
        (r'(id="res-count"><b>)[^<]*(</b>)', rf"\g<1>{n_ind}\g<2>"),
    ]:
        html, k = re.subn(pat, rep, html)
        if k != 1:
            print(f"FATAL: count placeholder not found exactly once: {pat}")
            sys.exit(3)
    print(f"  Static counts set: {n_ind} indicators, {n_fw} frameworks")

    # Footer workbook versions (added 2026-10-06), read from each workbook's Changelog!B2. The
    # footer had been typed into the template and still read indicators v10 at v27.
    def _wb_ver(path):
        try:
            w = load_workbook(path, data_only=True, read_only=True)
            v = w["Changelog"]["B2"].value
            w.close()
            return f"v{int(v)}"
        except Exception as e:
            print(f"  WARNING: version unreadable for {path.name}: {e}")
            return "v?"
    vers = " · ".join(f"{p.name} ({_wb_ver(p)})" for p in (Path(xlsx), CANON_UK, CANON_INT))
    html, k = re.subn(r'(<span id="footer-versions">)[^<]*(</span>)', rf"\g<1>{vers}\g<2>", html)
    if k != 1:
        print('FATAL: footer-versions placeholder not found exactly once'); sys.exit(3)
    print(f"  Footer versions: {vers}")

    # Startup-order guard (added 2026-09-28). The dashboard script declares INDICATORS, CTX_BY_SET,
    # and EXPORT_LOOKUPS as top-level consts. If the startup `render();` call sits above any of
    # them, the browser throws a temporal-dead-zone ReferenceError on load and the rest of the script
    # never runs: empty indicator list, no framework hover titles, broken export. The build was
    # previously "clean" while shipping exactly that, so refuse to write such a file.
    _start = html.rfind("\nrender();")
    _late = [v for v in ("INDICATORS", "CTX_BY_SET", "EXPORT_LOOKUPS")
             if html.find(f"const {v} ") > _start]
    if _start < 0 or _late:
        print(f"FATAL: startup render() precedes const declaration(s) {_late or '(render() call not found)'} "
              "— move the Startup block to the end of the <script>.")
        sys.exit(3)

    out.write_text(html, encoding="utf-8")
    print(f"\nWritten: {out} ({out.stat().st_size // 1024} KB, {len(indicators)} indicators)")
    return out


def main():
    ap = argparse.ArgumentParser(description="Rebuild the Climate–Nature Indicator Finder dashboard.")
    ap.add_argument("--xlsx", default=CANON, help="canonical indicators workbook")
    ap.add_argument("--template", default=TEMPLATE, help="dashboard HTML used as template")
    ap.add_argument("--out", default=OUT, help="output HTML path")
    a = ap.parse_args()
    build(a.xlsx, a.template, a.out)


if __name__ == "__main__":
    main()
