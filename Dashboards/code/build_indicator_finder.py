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
FRAMEWORK_CTX is the only hardcoded governance knowledge. Update it when the governance
workbook changes a framework's enabling legislation / lead policy (see
WORKBOOK_WRITE_PROTOCOL.md §7). Everything else derives from the workbook.

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
    ("CCC Indicators",                  "CCC",   "CCC Mitigation & Adaptation Monitoring Framework"),
    ("JNCC UK Biodiversity Indicators", "JNCC",  "JNCC UK Biodiversity Indicators 2025"),
    ("SoN 2023 Indicators",             "SoN",   "State of Nature 2023"),
    ("EEA Biodiversity Indicators",     "EEA",   "EEA Biodiversity Indicators"),
    ("BIP Indicators",                  "BIP",   "Biodiversity Indicators Partnership (BIP)"),
    ("IPBES Indicators",                "IPBES", "IPBES Indicators"),
    ("CBD GBF Indicators",              "GBF",   "CBD Kunming-Montreal GBF Indicators"),
    ("SDG Indicators",                  "SDG",   "UN Sustainable Development Goals"),
]

# ── Governance chains, one per framework (replaces GOV_CHAINS) ──────────────────
# Each entry: {id, name, tier, url, mon, note}. `mon` = this framework is a designated
# monitoring indicator for that instrument. Update on governance-workbook changes.
# IDs validated against uk_climate_nature_governance.xlsx v20 / international v13.
FRAMEWORK_CTX = json.loads(r'''
{
 "EIF": [
  {"id":"POL-001","name":"Environmental Improvement Plan (EIP) 2025","tier":"Policy activity","url":"https://www.gov.uk/government/publications/environmental-improvement-plan","mon":true,"note":"Designated indicator for EIP 2025 / OEP monitoring"},
  {"id":"INT-L-007","name":"Kunming-Montreal Global Biodiversity Framework (GBF)","tier":"International","url":"https://www.cbd.int/gbf/","mon":true,"note":"Designated indicator for EIP 2025 / OEP monitoring"}
 ],
 "CCC": [
  {"id":"LEG-001","name":"Climate Change Act 2008","tier":"UK Legislation","url":"https://www.legislation.gov.uk/ukpga/2008/27/contents","mon":true,"note":"CB4 ≤1,950 MtCO₂e (2023–27); CB5 ≤1,725 (2028–32); CB6 ≤965 (2033–37)"},
  {"id":"LEG-003","name":"Carbon Budget Orders (1st–7th)","tier":"UK Legislation","url":"https://www.legislation.gov.uk/uksi/2021/1059/contents","mon":true,"note":"Each Order sets the 5-year cap tracked by the CCC framework"},
  {"id":"POL-004","name":"UK Net Zero Strategy / Carbon Budget Delivery Plan (CBDP) 2023","tier":"Policy activity","url":"https://www.gov.uk/government/publications/net-zero-strategy","mon":true,"note":"Government delivery response tracked by the CCC framework"},
  {"id":"INT-L-007","name":"Kunming-Montreal Global Biodiversity Framework (GBF)","tier":"International","url":"https://www.cbd.int/gbf/","mon":true,"note":""}
 ],
 "JNCC": [
  {"id":"LEG-004","name":"Environment Act 2021","tier":"UK Legislation","url":"https://www.legislation.gov.uk/ukpga/2021/30/contents","mon":true,"note":"Official JNCC UK Biodiversity Indicator (UKBI 2025)"},
  {"id":"POL-003","name":"UK National Biodiversity Strategy and Action Plan (NBSAP) 2025","tier":"Policy activity","url":"https://www.gov.uk/government/publications/uk-national-biodiversity-strategy-and-action-plan","mon":true,"note":"Official JNCC UK Biodiversity Indicator (UKBI 2025)"},
  {"id":"INT-L-007","name":"Kunming-Montreal Global Biodiversity Framework (GBF)","tier":"International","url":"https://www.cbd.int/gbf/","mon":true,"note":"Official JNCC UK Biodiversity Indicator (UKBI 2025)"}
 ],
 "SoN": [
  {"id":"INT-L-007","name":"Kunming-Montreal Global Biodiversity Framework (GBF)","tier":"International","url":"https://www.cbd.int/gbf/","mon":false,"note":""}
 ],
 "EEA": [
  {"id":"INT-P-015","name":"European Green Deal — Biodiversity Strategy 2030 and Farm to Fork Strategy","tier":"International policy","url":"https://ec.europa.eu/info/strategy/priorities-2019-2024/european-green-deal/actions-being-taken-eu/eu-biodiversity-strategy-2030_en","mon":false,"note":""},
  {"id":"EU-L-006","name":"EU Nature Restoration Law (Regulation EU 2024/1991)","tier":"EU Legislation","url":"https://eur-lex.europa.eu/eli/reg/2024/1991/oj/eng","mon":false,"note":""}
 ],
 "BIP": [
  {"id":"INT-L-004","name":"UN Convention on Biological Diversity (CBD)","tier":"International","url":"https://www.cbd.int/","mon":false,"note":""},
  {"id":"INT-L-007","name":"Kunming-Montreal Global Biodiversity Framework (GBF)","tier":"International","url":"https://www.cbd.int/gbf/","mon":false,"note":""}
 ],
 "IPBES": [
  {"id":"INT-L-004","name":"UN Convention on Biological Diversity (CBD)","tier":"International","url":"https://www.cbd.int/","mon":false,"note":""},
  {"id":"INT-L-007","name":"Kunming-Montreal Global Biodiversity Framework (GBF)","tier":"International","url":"https://www.cbd.int/gbf/","mon":false,"note":""}
 ],
 "GBF": [
  {"id":"INT-L-004","name":"UN Convention on Biological Diversity (CBD)","tier":"International","url":"https://www.cbd.int/","mon":true,"note":"GBF official monitoring indicator (CBD/COP16 approved)"},
  {"id":"INT-P-006","name":"GBF Monitoring Framework and Indicator Framework","tier":"International policy","url":"https://www.gbf-indicators.org/","mon":true,"note":"GBF official monitoring indicator (CBD/COP16 approved)"}
 ],
 "SDG": []
}
''')

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


def load_indicators(xlsx_path: Path):
    """Read all framework sheets, mapping columns by header name. Returns list of dicts."""
    wb = load_workbook(xlsx_path, data_only=True, read_only=True)
    records = []
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
                "cs":       cell_int(row[idx["Climate_Score"]]) if "Climate_Score" in idx else 0,
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
            rec["sectors"] = parse_sectors(g(row, "Policy_Sector"))
            rec["ctx"] = FRAMEWORK_CTX.get(fw_short, [])
            records.append(rec)
            n_sheet += 1
        print(f"  {sheet:<34} {fw_short:<6} {n_sheet:>4} indicators")
    wb.close()
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

    indicators = load_indicators(xlsx)
    html = template.read_text(encoding="utf-8")
    data_json = json.dumps(indicators, ensure_ascii=False, separators=(",", ":"))
    html = inject_js_var(html, "INDICATORS", data_json)

    lookups = load_export_lookups(xlsx, indicators)
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
