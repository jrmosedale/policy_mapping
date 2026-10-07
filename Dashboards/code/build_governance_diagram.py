#!/usr/bin/env python3
"""
build_governance_diagram.py
Reads the three canonical governance/indicator workbooks and emits a self-contained
HTML relationship explorer (governance_diagram_vN.html; N set by the `out = ...` line below).
Run from Data/canonical_files/ with --outdir pointing at Dashboards/ (build_all.py does this).

Key idea: every cross-reference column encodes a DIFFERENT relationship type. We parse
each column separately and tag every edge with a link class, so the dashboard can
discriminate hard (statutory/structural) from soft (associative) links, plus the
international-implementation bridge and indicator-monitoring links.

Canonical-file autodetection mirrors check_links.py: prefer the stable canonical name;
fall back to a version glob that EXCLUDES *_superseded_* archives.

Usage:  python3 build_governance_diagram.py [--outdir .]
"""
import openpyxl, re, json, glob, os, argparse, datetime, sys

CODE_RE = re.compile(r'\[((?:LEG|ORG|POL|IFW|INT-L|INT-O|INT-P|EU-L)-\d+)\]')

CANON = {
    "uk":   "uk_climate_nature_governance.xlsx",
    "intl": "international_climate_nature_governance.xlsx",
    "ind":  "indicators_climate_nature.xlsx",
}

def find(canon):
    if os.path.exists(canon):
        return canon
    stem = canon[:-5]
    cands = [f for f in glob.glob(stem + "*.xlsx") if "_superseded_" not in f]
    if not cands:
        sys.exit(f"ERROR: cannot find canonical file {canon} (or a non-superseded fallback).")
    cands.sort()
    print(f"  (canonical {canon} not found; using fallback {cands[-1]})")
    return cands[-1]

def load(path):
    return openpyxl.load_workbook(path, read_only=True, data_only=True)

def rows_of(wb, sheet):
    ws = wb[sheet]
    data = list(ws.iter_rows(values_only=True))
    hdr = data[0]
    idx = {h: i for i, h in enumerate(hdr) if h is not None}
    out = []
    for r in data[1:]:
        if r[0] in (None, "") or str(r[0]).strip() == "":
            continue
        out.append({h: r[i] for h, i in idx.items()})
    return out

def codes(cell):
    if cell in (None, ""):
        return []
    return CODE_RE.findall(str(cell))

def first_sector(cell):
    if not cell:
        return "Cross-cutting"
    return str(cell).split("|")[0].strip()

def sector_list(cell):
    if not cell:
        return []
    return [t.strip() for t in str(cell).split("|") if t.strip()]

# ---- sector palette (12 canonical tokens + fallback) -------------------------
SECTORS = {
    "Climate":                    "#2B6CB8",
    "Nature & Biodiversity":      "#1A7A50",
    "Marine & Fisheries":         "#3A5CC0",
    "Land Use & Agriculture":     "#9A6010",
    "Water":                      "#1A8AA0",
    "Energy":                     "#C0581A",
    "Biosecurity":                "#B07A00",
    "Finance":                    "#6D4AA0",
    "Governance, Society & Data": "#6B6B5A",
    "Pollution & Waste":          "#7A7A2E",
    "Transport":                  "#A03A6A",
    "Urban & Buildings":          "#8A5A3A",
    "Cross-cutting":              "#8A8878",
}

def tint(hex_stroke, amt=0.90):
    h = hex_stroke.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r + (255 - r) * amt); g = int(g + (255 - g) * amt); b = int(b + (255 - b) * amt)
    return f"#{r:02X}{g:02X}{b:02X}"

def darken(hex_stroke, amt=0.45):
    h = hex_stroke.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r * (1 - amt)); g = int(g * (1 - amt)); b = int(b * (1 - amt))
    return f"#{r:02X}{g:02X}{b:02X}"

PAL = {s: {"stroke": c, "fill": tint(c), "text": darken(c)} for s, c in SECTORS.items()}

# ---- family metadata ---------------------------------------------------------
FAMILY = {  # code-prefix -> (group label, workbook)
    "LEG":   ("UK legislation", "uk"),
    "ORG":   ("UK public body", "uk"),
    "POL":   ("UK policy / activity", "uk"),
    "INT-L": ("International convention / treaty", "intl"),
    "INT-O": ("International body", "intl"),
    "INT-P": ("International policy / activity", "intl"),
    "EU-L":  ("EU legislation", "intl"),
    "IFW":   ("Indicator framework", "ind"),
}
def fam(code):
    for p in ("INT-L", "INT-O", "INT-P", "EU-L", "LEG", "ORG", "POL", "IFW"):
        if code.startswith(p):
            return p
    return "?"

# =============================================================================
def build():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    paths = {k: find(v) for k, v in CANON.items()}
    print("Loading:", {k: os.path.basename(v) for k, v in paths.items()})
    uk, intl, ind = load(paths["uk"]), load(paths["intl"]), load(paths["ind"])

    def version(wb):
        try:
            return wb["Changelog"]["B2"].value
        except Exception:
            return "?"
    versions = {k: version(w) for k, w in (("uk", uk), ("intl", intl), ("ind", ind))}

    nodes = {}   # id -> node dict
    edges = []   # {a,b,type,dir}  dir: 'a2b' | 'both'
    edge_seen = set()

    def add_node(nid, label, gtype, sectors, year, url, blurb, acronym="", status="", extra=None):
        if nid in nodes:
            return
        secs = sectors or []
        prim = secs[0] if secs else "Cross-cutting"
        if prim not in PAL:
            prim = "Cross-cutting"
        # extra: list of (label, value) additional narrative sections for the detail panel
        xs = [[l, str(v).strip()] for (l, v) in (extra or []) if v and str(v).strip()]
        nodes[nid] = {
            "id": nid, "fam": fam(nid), "label": label or nid, "acr": acronym or "",
            "type": gtype or "", "sec": prim, "secs": secs, "year": str(year or ""),
            "status": str(status or ""), "url": url or "", "blurb": (blurb or "").strip(),
            "x": xs,
        }

    def add_edge(a, b, etype, directed=True):
        if a == b or not a or not b:
            return
        # directional edges keyed by (a,b,type); undirected keyed by sorted pair+type
        if directed:
            key = (a, b, etype)
        else:
            key = tuple(sorted((a, b))) + (etype,)
        if key in edge_seen:
            return
        edge_seen.add(key)
        edges.append({"a": a, "b": b, "type": etype, "dir": "a2b" if directed else "both"})

    UKF = {"LEG", "ORG", "POL"}

    # ---- ratification status, read from UK_Ratification on Conventions & EU Legislation ----
    NEG = re.compile(r"not a party|not bound|no longer in|no equivalent|not yet ratified|no formal", re.I)
    POS = re.compile(r"ratif|acced|party|retain|implement|transpos|replaced|bound|approved", re.I)
    ratified = {}   # intl Record_ID -> True/False
    rat_pairs = set()  # frozenset({intl_id, uk_code}) explicitly named in UK_Ratification
    for sheet in ("Conventions & Treaties", "EU Legislation"):
        for r in rows_of(intl, sheet):
            i = r["Record_ID"]
            v = r.get("UK_Ratification")
            s = str(v).strip() if v else ""
            if not s:
                ratified[i] = False
                continue
            is_rat = bool(POS.search(s)) and not NEG.search(s)
            ratified[i] = is_rat
            if is_rat:
                for c in codes(s):
                    rat_pairs.add(frozenset((i, c)))

    def intl_class(a, b):
        """UK <-> international bridge, split by ratification (not by endpoint type alone).

        HARD  = the international instrument is one the UK has ratified / retained /
                transposed, AND the UK endpoint is the legislation giving it domestic
                force (or the pair is explicitly named in UK_Ratification).
        SOFT  = everything else: policy- and body-level thematic alignment, and any link
                to an instrument the UK has not ratified or is "not bound" by.
        """
        uk = a if fam(a) in UKF else b
        it = b if uk == a else a
        if frozenset((it, uk)) in rat_pairs:
            return "intl_hard"
        if ratified.get(it, False) and fam(uk) == "LEG":
            return "intl_hard"
        return "intl_soft"

    # ---------- UK Legislation ----------
    for r in rows_of(uk, "Legislation"):
        i = r["Record_ID"]
        add_node(i, r.get("Name"), r.get("General_Type"), sector_list(r.get("Policy_Sector")),
                 r.get("Year"), r.get("Link"), r.get("Key_Provisions"),
                 status=r.get("Status"),
                 extra=[("Statutory enabling basis", r.get("Statutory_Enabling_Basis"))])
    for r in rows_of(uk, "Legislation"):
        i = r["Record_ID"]
        for c in codes(r.get("Enabling_Legislation")):
            add_edge(c, i, "enabling", directed=True)            # legislation enables record: LEG -> record (hard)
        for c in codes(r.get("Related_Legislation")):
            add_edge(i, c, "related", directed=False)            # soft
        for c in codes(r.get("Lead_Department")):
            add_edge(c, i, "lead", directed=True)                # dept leads legislation: dept -> LEG (hard)
        for c in codes(r.get("Intl_Links")):
            add_edge(i, c, intl_class(i, c), directed=False)     # bridge (hard/soft)

    # ---------- UK Public Bodies ----------
    for r in rows_of(uk, "Public Bodies"):
        i = r["Record_ID"]
        add_node(i, r.get("Name"), r.get("General_Type"), sector_list(r.get("Policy_Sector")),
                 "", r.get("Link"), r.get("Remit_And_Powers"), acronym=r.get("Acronym") or "",
                 extra=[("Statutory duties", r.get("Statutory_Duties")),
                        ("Regulatory powers", r.get("Regulatory_Powers_Keywords"))])
    for r in rows_of(uk, "Public Bodies"):
        i = r["Record_ID"]
        for c in codes(r.get("Indicator_Frameworks")):
            add_edge(i, c, "indicator", directed=True)
        for c in codes(r.get("Lead_Department")):
            if c != i:
                add_edge(c, i, "lead", directed=True)            # dept leads body: dept -> ORG (hard)
        for c in codes(r.get("Statutory_Role")):
            if c.startswith("LEG"):
                add_edge(c, i, "enabling", directed=True)        # legislation empowers body: LEG -> ORG (hard)
        for c in codes(r.get("Related_Bodies")):
            add_edge(i, c, "related", directed=False)            # national-analogue / peer body (soft)
        for c in codes(r.get("Affecting_Policies")):
            add_edge(i, c, "related", directed=False)            # policy materially affecting this body (soft)
        for c in codes(r.get("Intl_Links")):
            add_edge(i, c, intl_class(i, c), directed=False)

    # ---------- UK Policies & Activities ----------
    for r in rows_of(uk, "Policies & Activities"):
        i = r["Record_ID"]
        add_node(i, r.get("Name"), r.get("General_Type"), sector_list(r.get("Policy_Sector")),
                 r.get("Year_Status"), r.get("Link"), r.get("Scope_And_Commitments"),
                 acronym=r.get("Acronym") or "", status=r.get("Statutory_Status"))
    for r in rows_of(uk, "Policies & Activities"):
        i = r["Record_ID"]
        for c in codes(r.get("Enabling_Legislation")):
            add_edge(c, i, "enabling", directed=True)            # legislation enables policy: LEG -> POL (hard)
        for c in codes(r.get("Lead_Organisation")):
            add_edge(c, i, "lead", directed=True)                # org leads policy: ORG -> POL (hard)
        for c in codes(r.get("Parent_Programme")):
            add_edge(c, i, "parent", directed=True)              # parent programme -> child: parent -> child (structural)
        for c in codes(r.get("Funded_By")):
            add_edge(c, i, "funding", directed=True)             # funder -> funded (soft-ish)
        for c in codes(r.get("Related_Policy_Links")):
            add_edge(i, c, "related", directed=False)            # soft
        for c in codes(r.get("Indicator_Frameworks")):
            add_edge(i, c, "indicator", directed=True)
        for c in codes(r.get("Intl_Links")):
            add_edge(i, c, intl_class(i, c), directed=False)

    # ---------- International (four sheets) ----------
    intl_sheets = [
        ("Conventions & Treaties", "General_Type", "Key_Provisions", "Year_Adopted", "Official_Link", "Acronym"),
        ("EU Legislation",         "General_Type", "Key_Provisions", "Year_Adopted", "Official_Link", None),
        ("Associated Bodies",      "General_Type", "Remit_And_Powers", None,          "Official_Link", "Acronym"),
        ("Intl Policies & Activities", "General_Type", "Key_Commitments", "Year_Status", "Official_Link", None),
    ]
    for sheet, gt, blurbc, yearc, urlc, acrc in intl_sheets:
        for r in rows_of(intl, sheet):
            i = r["Record_ID"]
            if sheet in ("Conventions & Treaties", "EU Legislation"):
                ex = [("UK ratification", r.get("UK_Ratification"))]
            elif sheet == "Associated Bodies":
                ex = [("UK representation", r.get("UK_Representation"))]
            elif sheet == "Intl Policies & Activities":
                ex = [("UK engagement", r.get("UK_Engagement"))]
            else:
                ex = []
            add_node(i, r.get("Name"), r.get(gt), sector_list(r.get("Policy_Sector")),
                     r.get(yearc) if yearc else "", r.get(urlc), r.get(blurbc),
                     acronym=(r.get(acrc) if acrc else "") or "", extra=ex)
        for r in rows_of(intl, sheet):
            i = r["Record_ID"]
            for c in codes(r.get("Parent_Convention")):
                add_edge(c, i, "parent", directed=True)          # parent convention -> child: parent -> child (structural)
            for c in codes(r.get("UK_Links")):
                add_edge(i, c, intl_class(i, c), directed=False) # bridge (reciprocal, hard/soft)
            for c in codes(r.get("UK_Ratification")):
                add_edge(i, c, intl_class(i, c), directed=False) # UK retaining/ratifying instrument (hard where LEG)
            for c in codes(r.get("Lead_Body")):
                add_edge(c, i, "lead", directed=True)            # body leads activity: body -> activity (hard)
            for c in codes(r.get("Intl_Links")):
                add_edge(i, c, "related", directed=False)        # soft (intl<->intl)
            for c in codes(r.get("Indicator_Frameworks")):
                add_edge(i, c, "indicator", directed=True)

    # ---------- Indicator frameworks ----------
    for r in rows_of(ind, "Indicator Framework"):
        i = r.get("Framework_ID")
        if not i or not str(i).startswith("IFW"):
            continue
        # The detail panel's main narrative for a framework is its Policy_Purpose
        # (workbook v15). Record count and scope move to a secondary section.
        add_node(i, r.get("Source_Framework"), "Indicator framework",
                 ["Governance, Society & Data"], "", r.get("Official_Link"),
                 r.get("Policy_Purpose"),
                 extra=[("Coverage",
                         f"{r.get('Record_Count','?')} indicators. {r.get('Scope','') or ''}".strip())])

        lead_codes = set(codes(r.get("Lead_Organisation")))
        key_codes = set(codes(r.get("Key_Instruments")))

        # Lead organisation keeps its own hard (solid) edge: ORG -> IFW.
        for c in sorted(lead_codes):
            add_edge(c, i, "lead", directed=True)

        # Key_Instruments — the instruments named in Policy_Purpose — are drawn
        # SOLID. A code already carrying a lead edge is skipped so the pair is not
        # drawn twice; the rest take precedence over the dotted indicator edge below.
        for c in sorted(key_codes - lead_codes):
            add_edge(i, c, "key_inst", directed=True)

        # Remaining soft cross-references stay dotted.
        for c in codes(r.get("Indirect_Policy_Links")):
            if c in key_codes or c in lead_codes:
                continue
            add_edge(i, c, "indicator", directed=True)

    # ---------- prune edges whose endpoints are unknown (defensive) ----------
    edges = [e for e in edges if e["a"] in nodes and e["b"] in nodes]

    # ratification status onto international instrument nodes (for the detail panel)
    for i, n in nodes.items():
        if i in ratified:
            n["rat"] = bool(ratified[i])

    # degree
    deg = {n: 0 for n in nodes}
    for e in edges:
        deg[e["a"]] += 1
        deg[e["b"]] += 1
    for n in nodes:
        nodes[n]["deg"] = deg[n]

    payload = {
        "nodes": nodes,
        "edges": edges,
        "pal": PAL,
        "sectors": list(SECTORS.keys()),
        "families": {p: FAMILY[p][0] for p in FAMILY},
        "versions": versions,
        "generated": datetime.date.today().isoformat(),
        "counts": {
            "nodes": len(nodes), "edges": len(edges),
            "by_fam": {p: sum(1 for x in nodes.values() if x["fam"] == p) for p in FAMILY},
            "by_type": {t: sum(1 for e in edges if e["type"] == t)
                        for t in ["enabling", "lead", "parent", "funding", "related", "intl_hard", "intl_soft", "key_inst", "indicator"]},
        },
    }

    html = TEMPLATE.replace("/*DATA*/", json.dumps(payload, ensure_ascii=False))
    out = os.path.join(args.outdir, "governance_diagram_v12.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\nWrote {out}")
    print("  nodes:", payload["counts"]["nodes"], "edges:", payload["counts"]["edges"])
    print("  by family:", payload["counts"]["by_fam"])
    print("  by link type:", payload["counts"]["by_type"])
    print("  versions:", versions)



TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>UK Climate–Nature Governance — Relationship Explorer</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--bg:#F7F6F2;--sf:#fff;--bdr:rgba(30,30,20,.10);--bdrm:rgba(30,30,20,.18);--tx:#1A1A14;--tx2:#6B6B5A;--tx3:#9B9B88;}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--tx);display:flex;flex-direction:column;height:100vh;overflow:hidden}
header{background:var(--sf);border-bottom:1px solid var(--bdr);padding:9px 16px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;flex-shrink:0}
.logo{width:26px;height:26px;background:var(--tx);border-radius:5px;display:flex;align-items:center;justify-content:center}
h1{font-size:13px;font-weight:600}.subtitle{font-size:10px;color:var(--tx2)}
.linklegend{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
.ll{display:flex;align-items:center;gap:5px;font-size:10px;color:var(--tx2);cursor:pointer;user-select:none;padding:2px 4px;border-radius:5px}
.ll:hover{background:#F1EFE8}.ll.off{opacity:.32}
.ll svg{width:26px;height:8px;flex-shrink:0}
.main{display:flex;flex:1;overflow:hidden;min-height:0}
.rail{width:clamp(208px,20vw,290px);flex-shrink:0;border-right:1px solid var(--bdr);background:var(--sf);display:flex;flex-direction:column;min-height:0}
.railtop{padding:9px 11px;border-bottom:1px solid var(--bdr);display:flex;flex-direction:column;gap:6px}
.srch{position:relative}
.si{width:100%;font-size:12px;font-family:inherit;padding:6px 9px 6px 27px;border:1px solid var(--bdrm);border-radius:8px;background:var(--bg);color:var(--tx);outline:none}
.si:focus{border-color:#2B6CB8;background:#fff}
.sico{position:absolute;left:9px;top:13px;width:12px;height:12px;opacity:.4;pointer-events:none}
.ac{position:absolute;left:0;right:0;top:34px;background:var(--sf);border:1px solid var(--bdrm);border-radius:8px;box-shadow:0 8px 24px rgba(0,0,0,.12);z-index:40;max-height:320px;overflow-y:auto;display:none}
.ac.show{display:block}
.acr{display:flex;align-items:baseline;gap:7px;padding:6px 9px;cursor:pointer;line-height:1.25}
.acr:hover,.acr.hi{background:#E8F0FB}
.acr .d{width:7px;height:7px;border-radius:50%;flex-shrink:0;align-self:center}
.acr .i{font-family:'DM Mono',monospace;font-size:9px;color:var(--tx3);width:54px;flex-shrink:0}
.acr .n{font-size:11px}.acr .f{margin-left:auto;font-size:8.5px;color:var(--tx3);white-space:nowrap}
.flbl{font-size:8.5px;font-weight:700;color:var(--tx3);text-transform:uppercase;letter-spacing:.06em;margin:2px 0 -1px}
.filterrow{display:flex;gap:3px;flex-wrap:wrap}
.chip{font-size:9.5px;font-weight:500;padding:2px 7px;border-radius:20px;border:1px solid var(--bdrm);background:transparent;color:var(--tx2);cursor:pointer;font-family:inherit}
.chip:hover{background:#F1EFE8}.chip.on{background:var(--tx);color:#fff;border-color:var(--tx)}
.secblock{margin-top:7px;padding-top:8px;border-top:1px solid var(--bdr)}
.secwrap{display:flex;gap:3px;flex-wrap:wrap}
.secchip{font-size:9px;font-weight:500;padding:2px 7px;border-radius:20px;border:1px solid;cursor:pointer;font-family:inherit;background:transparent}
.railcount{font-size:9.5px;color:var(--tx3);padding:5px 11px 3px}
.idxlist{overflow-y:auto;flex:1;padding:0 6px 10px}
.grphdr{font-size:9px;font-weight:700;color:var(--tx3);text-transform:uppercase;letter-spacing:.07em;padding:9px 6px 3px;position:sticky;top:0;background:var(--sf)}
.irow{display:flex;align-items:baseline;gap:6px;padding:4px 7px;border-radius:6px;cursor:pointer;line-height:1.25}
.irow:hover{background:#F1EFE8}.irow.sel{background:#E8F0FB}
.irid{font-family:'DM Mono',monospace;font-size:9px;color:var(--tx3);flex-shrink:0;width:52px}
.irnm{font-size:11px;color:var(--tx)}
.irdot{width:7px;height:7px;border-radius:50%;flex-shrink:0;margin-top:4px}
.stage{flex:1;display:flex;flex-direction:column;min-width:0;overflow:hidden}
.egowrap{flex:1;position:relative;overflow:hidden;background:radial-gradient(circle at 50% 26%, #FFFFFF 0%, var(--bg) 80%);cursor:grab}
.egowrap.grabbing{cursor:grabbing}
#ego{display:block;width:100%;height:100%;touch-action:none}
.egoctrl{position:absolute;top:10px;right:12px;display:none;gap:4px;z-index:20;background:rgba(255,255,255,.85);backdrop-filter:blur(4px);border:1px solid var(--bdr);border-radius:9px;padding:4px}
.egoctrl.show{display:flex}
.eb{font-size:11px;font-family:inherit;font-weight:600;padding:4px 8px;border:1px solid var(--bdrm);border-radius:6px;background:var(--sf);color:var(--tx2);cursor:pointer;line-height:1}
.eb.off{opacity:.42;text-decoration:line-through}
.ebgrp{display:flex;gap:4px;align-items:center}
.ebgrp+.ebgrp{margin-left:7px;padding-left:9px;border-left:1px solid var(--bdrm)}
.infobtn{font-family:inherit;font-size:11px;font-weight:600;padding:4px 10px;border:1px solid var(--bdrm);border-radius:7px;background:var(--sf);color:var(--tx2);cursor:pointer;white-space:nowrap}
.infobtn:hover{background:#F1EFE8;color:var(--tx)}
.modal{position:fixed;inset:0;background:rgba(20,20,15,.42);display:none;align-items:center;justify-content:center;z-index:80;padding:24px}
.modal.show{display:flex}
.modalbox{position:relative;background:var(--sf);border:1px solid var(--bdrm);border-radius:14px;box-shadow:0 18px 50px rgba(0,0,0,.28);max-width:640px;width:100%;max-height:86vh;overflow-y:auto;padding:22px 26px;font-size:12.5px;line-height:1.5;color:var(--tx2)}
.modalbox h2{font-size:16px;color:var(--tx);margin-bottom:4px}
.modalbox h3{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--tx3);margin:14px 0 5px}
.modalbox p{margin:5px 0}
.modalbox ul{margin:4px 0 4px 18px}.modalbox li{margin:3px 0}
.modalbox b{color:var(--tx)}
.modalx{position:absolute;top:12px;right:14px;border:none;background:none;font-size:18px;color:var(--tx3);cursor:pointer;line-height:1}
.modalx:hover{color:var(--tx)}
.eb:hover:not(:disabled){background:#E8F0FB;color:#2B6CB8}
.eb:disabled{opacity:.35;cursor:default}
.ebsep{width:1px;background:var(--bdrm);margin:2px 2px}
.empty{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:var(--tx3);font-size:12px;text-align:center;padding:24px}
.detail{height:clamp(118px,20vh,200px);flex-shrink:0;border-top:1px solid var(--bdr);background:var(--sf);overflow-y:auto;padding:12px 16px}
/* Collapsible panels — give the diagram more room on laptops */
body.no-rail .rail{display:none}
body.no-detail .detail{display:none}
.infobtn.off{opacity:.5}
.infobtn.off::before{content:"";display:inline-block;width:7px;height:7px;margin-right:3px;border-radius:2px;background:var(--tx3);vertical-align:middle}
@media(max-width:1200px){.rail{width:clamp(190px,22vw,240px)}}
@media(max-height:760px){.detail{height:clamp(104px,17vh,160px)}}
@media(max-height:640px){.detail{height:96px}}
.dhead{display:flex;align-items:flex-start;gap:9px;flex-wrap:wrap}
.did{font-family:'DM Mono',monospace;font-size:10px;color:var(--tx3);letter-spacing:.03em}
.dtitle{font-size:15px;font-weight:600;line-height:1.25}
.dmeta{display:flex;gap:6px;flex-wrap:wrap;margin-top:4px;align-items:center}
.dtag{font-size:9.5px;padding:2px 8px;border-radius:6px;border:1px solid var(--bdrm);color:var(--tx2);background:var(--bg)}
.dtag.type{border-style:dashed}
.dlink{font-size:10px;font-weight:500;padding:3px 10px;border:1px solid var(--bdrm);border-radius:7px;background:var(--bg);color:#2B6CB8;text-decoration:none}
.dlink:hover{background:#E8F0FB}
.dblurb{font-size:11px;line-height:1.5;color:var(--tx2);margin-top:8px;max-width:82ch}
.dblurb-lbl{font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--tx3);margin-top:10px}
.cref{border-bottom:1px dotted var(--tx3);cursor:help;color:var(--tx);font-family:'DM Mono',monospace;font-size:.9em;white-space:nowrap}
.cref:hover{background:#F1EFE8}
.rel{margin-top:11px;display:flex;flex-direction:column;gap:8px}
.relgrp h4{font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px;display:flex;align-items:center;gap:6px}
.relgrp h4 .cnt{font-family:'DM Mono',monospace;color:var(--tx3);font-weight:500}
.relgrp h4 svg{width:24px;height:8px}
.relrow{display:flex;flex-wrap:wrap;gap:4px}
.nbchip{display:inline-flex;align-items:center;gap:5px;font-size:10.5px;padding:3px 8px;border-radius:7px;border:1px solid;cursor:pointer;background:var(--bg);line-height:1.35;max-width:340px}
.nbchip:hover{filter:brightness(.97)}
.nbchip .c{font-family:'DM Mono',monospace;font-size:8.5px;opacity:.7}
.nbchip .n{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:280px}
footer{padding:5px 16px;font-size:9px;color:var(--tx3);border-top:1px solid var(--bdr);background:var(--sf);display:flex;justify-content:space-between;flex-wrap:wrap;gap:3px;flex-shrink:0}
.mono{font-family:'DM Mono',monospace}
</style>
</head>
<body>
<header>
  <div style="display:flex;align-items:center;gap:9px">
    <div class="logo"><svg viewBox="0 0 14 14" fill="none"><rect x="1" y="1" width="5" height="5" rx="1" fill="white" opacity=".9"/><rect x="8" y="1" width="5" height="5" rx="1" fill="white" opacity=".6"/><rect x="1" y="8" width="5" height="5" rx="1" fill="white" opacity=".6"/><rect x="8" y="8" width="5" height="5" rx="1" fill="white" opacity=".9"/></svg></div>
    <div><h1>Climate–Nature Governance · Relationship Explorer</h1><div class="subtitle" id="sub"></div></div>
  </div>
  <div class="linklegend" id="linklegend"></div>
  <div style="margin-left:auto;display:flex;gap:6px;align-items:center">
    <button class="infobtn" id="btnRail" onclick="togglePanel('rail')" title="Show/hide the filters panel (more room for the diagram)">&#9703;&nbsp;Filters</button>
    <button class="infobtn" id="btnDetail" onclick="togglePanel('detail')" title="Show/hide the detail panel (more room for the diagram)">&#9636;&nbsp;Details</button>
    <button class="infobtn" onclick="toggleHelp()" title="What this shows &amp; how to use it">&#9432;&nbsp;Help</button>
  </div>
</header>
<div class="main">
  <div class="rail">
    <div class="railtop">
      <div class="srch">
        <svg class="sico" viewBox="0 0 14 14"><circle cx="5.5" cy="5.5" r="4.2" stroke="currentColor" stroke-width="1.4" fill="none"/><path d="M9 9L12 12" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>
        <input class="si" id="srch" placeholder="Search — type e.g. 'climate'…" autocomplete="off"
               oninput="onSearch(this.value)" onkeydown="acKey(event)" onfocus="onSearch(this.value)">
        <div class="ac" id="ac"></div>
      </div>
      <div class="flbl">Record type</div>
      <div class="filterrow" id="famrow"></div>
      <div class="secblock">
        <div class="flbl">Policy sector</div>
        <div class="secwrap" id="secrow"></div>
      </div>
    </div>
    <div class="railcount" id="railcount"></div>
    <div class="idxlist" id="idxlist"></div>
  </div>
  <div class="stage">
    <div class="egowrap" id="egowrap">
      <svg id="ego"></svg>
      <div class="egoctrl" id="egoctrl">
        <div class="ebgrp" title="Navigation & view">
          <button class="eb" id="navBack" title="Back" onclick="navBack()">&#9664;</button>
          <button class="eb" id="navFwd" title="Forward" onclick="navFwd()">&#9654;</button>
          <button class="eb" title="Zoom out" onclick="zoomBy(1/1.25)">&#8722;</button>
          <button class="eb" title="Zoom in" onclick="zoomBy(1.25)">+</button>
          <button class="eb" title="Fit to window" onclick="fitView()">Fit</button>
        </div>
        <div class="ebgrp" title="Display options">
          <button class="eb" id="btnCollapse" title="Collapse all depth-2 expansions" onclick="collapseAll()">&#8709; depth</button>
          <button class="eb" id="btnSoft" title="Show/hide all soft (dashed) links: related, funded-by, international-soft" onclick="toggleSoft()">Soft</button>
          <button class="eb" id="btnEU" title="Show/hide EU law nodes" onclick="toggleEU()">EU</button>
        </div>
        <div class="ebgrp" title="Export">
          <button class="eb" title="Download SVG" onclick="exportImg('svg')">SVG</button>
          <button class="eb" title="Download PNG" onclick="exportImg('png')">PNG</button>
        </div>
      </div>
      <div class="empty" id="empty">Pick a record — from the list on the left, the search box, or a link chip below —<br>to see everything it links to, in category tiers with typed connectors.<br><span style="font-size:10.5px">Scroll to zoom, drag to pan. Click a neighbour&rsquo;s <b>+</b> to expand its own links (depth-2).<br>Deep-link with <span class="mono">#RECORD-ID</span> in the URL. SVG/PNG export saves the visible window.</span></div>
    </div>
    <div class="detail" id="detail"></div>
  </div>
</div>
<footer><span id="foot"></span><span id="foot2"></span></footer>
<div class="modal" id="helpModal" onclick="if(event.target===this)toggleHelp()">
  <div class="modalbox">
    <button class="modalx" onclick="toggleHelp()" title="Close">&#10005;</button>
    <h2>Climate–Nature Governance Explorer</h2>
    <p>An interactive map of how UK and international climate- and nature-related <b>governance connects</b>: the legislation, public bodies, policies/activities, international instruments and indicator frameworks that make up the system, and the typed links between them. It is built directly from the three canonical workbooks, so it always reflects their current version.</p>
    <h3>What you're looking at</h3>
    <p>Records are grouped into horizontal <b>tiers</b> (international treaties → international bodies/EU law → UK legislation → UK public bodies → UK policy &amp; activity → indicator frameworks). Colour shows the record's primary <b>policy sector</b>. Pick a record and the map shows everything it links to.</p>
    <h3>Reading the links</h3>
    <p>Line style shows link type; the <b>arrow points from the governing entity to what it governs</b> — enabling legislation → the body/policy it empowers, lead organisation → the policy it leads, parent → child, funder → funded.</p>
    <ul>
      <li><b>Solid</b> = hard links (enabling legislation, lead org/dept, parent/child).</li>
      <li><b>Dashed</b> = soft links (related / cross-reference, funded-by).</li>
      <li><b>Double line</b> = UK↔international bridge (solid = ratified/retained; dotted = thematic).</li>
      <li><b>Solid pink</b> = key instrument &mdash; the legislation, bodies and policies named in an indicator framework&rsquo;s policy purpose.</li>
      <li><b>Dotted</b> = indicator / monitoring (softer cross-references).</li>
    </ul>
    <p>Click any link type in the top legend to show/hide it.</p>
    <h3>How to use it</h3>
    <ul>
      <li><b>Find a record</b> — search box or the list on the left; or click any node.</li>
      <li><b>Expand</b> — click a neighbour's <b>+</b> to add its own links (depth-2).</li>
      <li><b>Hover</b> a node to see its full name; the bottom panel shows the selected record's details and narrative.</li>
      <li><b>Controls</b> (top-right of the map): <b>navigate/zoom/fit</b>, <b>display options</b> (collapse depth, toggle Soft links, toggle EU law), and <b>export</b> (SVG/PNG of the current view).</li>
      <li><b>More room</b> — the header's <b>&#9703; Filters</b> and <b>&#9636; Details</b> buttons hide the side and bottom panels to enlarge the diagram (handy on laptops).</li>
      <li><b>Deep-link</b> — the URL ends with <span class="mono">#RECORD-ID</span>; share it to reopen on that record.</li>
    </ul>
    <p style="margin-top:12px;color:var(--tx3)">Record IDs: LEG = UK legislation · ORG = UK public body · POL = UK policy/activity · INT-L/O/P = international treaty/body/policy · EU-L = EU law · IFW = indicator framework.</p>
  </div>
</div>
<script>
const D=/*DATA*/;
const N=D.nodes, PAL=D.pal, EDGES=D.edges;

const LT={
  enabling: {label:"Enabling legislation",           group:"Hard",       col:"#C1272D", w:2.6, dash:"",    arrow:true},
  lead:     {label:"Lead org / dept",                 group:"Hard",       col:"#0B7A3B", w:2.2, dash:"",    arrow:true},
  parent:   {label:"Parent / child",                  group:"Hard",       col:"#6A2FA0", w:2.2, dash:"",    arrow:true},
  related:  {label:"Related / cross-ref",             group:"Soft",       col:"#8A6D0B", w:1.8, dash:"6 4", arrow:false},
  funding:  {label:"Funded by",                       group:"Soft",       col:"#B85C00", w:1.9, dash:"2 3", arrow:true},
  intl_hard:{label:"Int'l \u2014 hard (ratified/retained)",group:"Bridge", col:"#0E7C86", w:2.2, dash:"",  arrow:false, dbl:true},
  intl_soft:{label:"Int'l \u2014 soft (thematic)",    group:"Bridge",     col:"#0D9AA8", w:1.8, dash:"2 3", arrow:false, dbl:true},
  key_inst: {label:"Key instrument (framework)",      group:"Monitoring", col:"#A61E4D", w:2.4, dash:"",    arrow:true},
  indicator:{label:"Indicator / monitoring",          group:"Monitoring", col:"#D6336C", w:1.9, dash:"1 4", arrow:true},
};
const LT_ORDER=["enabling","lead","parent","related","funding","intl_hard","intl_soft","key_inst","indicator"];
let ltOn={}; LT_ORDER.forEach(t=>ltOn[t]=true);

const BANDS=[
  {label:"International treaties & conventions", fams:["INT-L"]},
  {label:"International bodies \u00b7 policy \u00b7 EU law", fams:["INT-O","INT-P","EU-L"]},
  {label:"UK legislation",        fams:["LEG"]},
  {label:"UK public bodies",      fams:["ORG"]},
  {label:"UK policy & activity",  fams:["POL"]},
  {label:"Indicator frameworks",  fams:["IFW"]},
];
function bandOf(fam){for(let i=0;i<BANDS.length;i++)if(BANDS[i].fams.includes(fam))return i;return BANDS.length-1;}

const ADJ={}; Object.keys(N).forEach(k=>ADJ[k]=[]);
EDGES.forEach(e=>{ADJ[e.a].push({o:e.b,type:e.type});ADJ[e.b].push({o:e.a,type:e.type});});
// Directed lookup so arrow direction follows the stored edge, NOT which node is focal.
const DSET=new Set(EDGES.map(e=>e.a+'|'+e.b+'|'+e.type));
function semantic(s,o,t){
  if(DSET.has(s+'|'+o+'|'+t)) return [s,o,!!LT[t].arrow];   // stored s->o
  if(DSET.has(o+'|'+s+'|'+t)) return [o,s,!!LT[t].arrow];   // stored o->s
  return [s,o,false];
}

let selId=null, srchQ="", famFilter=null, secFilter=null, acItems=[], acHi=-1;
let expanded=new Set();
let hist=[], hp=-1, hashLock=false;
let CONTENT=null, VIEW=null, suppressClick=false;

function esc(s){return (s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function darkenRGB(hex){const h=hex.replace('#','');return `rgb(${parseInt(h.slice(0,2),16)*0.6|0},${parseInt(h.slice(2,4),16)*0.6|0},${parseInt(h.slice(4,6),16)*0.6|0})`;}
function shortName(n,max){let s=n.acr||n.label;max=max||34;if(s.length>max)s=s.slice(0,max-1)+"\u2026";return s;}

function edgeSvg(type){
  const s=LT[type];const y=4;
  let l=`<svg viewBox="0 0 26 8" preserveAspectRatio="none">`;
  if(s.dbl){
    l+=`<line x1="1" y1="2.4" x2="25" y2="2.4" stroke="${s.col}" stroke-width="1.3" ${s.dash?`stroke-dasharray="${s.dash}"`:""}/>`;
    l+=`<line x1="1" y1="5.6" x2="25" y2="5.6" stroke="${s.col}" stroke-width="1.3" ${s.dash?`stroke-dasharray="${s.dash}"`:""}/>`;
  }else{
    l+=`<line x1="1" y1="${y}" x2="${s.arrow?21:25}" y2="${y}" stroke="${s.col}" stroke-width="${Math.min(s.w,2.4)}" ${s.dash?`stroke-dasharray="${s.dash}"`:""}/>`;
    if(s.arrow)l+=`<path d="M21 1.6 L25 4 L21 6.4 Z" fill="${s.col}"/>`;
  }
  return l+`</svg>`;
}

function initLegend(){
  document.getElementById('sub').textContent=
    `UK v${D.versions.uk} \u00b7 International v${D.versions.intl} \u00b7 Indicators v${D.versions.ind} \u00b7 ${D.counts.nodes} records \u00b7 ${D.counts.edges} links`;
  document.getElementById('linklegend').innerHTML=LT_ORDER.map(t=>
    `<span class="ll" id="ll-${t}" onclick="toggleLT('${t}')" title="${LT[t].group}">${edgeSvg(t)}<span>${LT[t].label}</span></span>`).join("");
  document.getElementById('foot').textContent=
    `Generated ${D.generated} \u00b7 solid = hard \u00b7 dashed = soft \u00b7 double = international (solid hard / dotted soft) \u00b7 dotted = monitoring`;
  document.getElementById('foot2').innerHTML=
    Object.entries(D.counts.by_type).map(([k,v])=>`<span class="mono">${k}:${v}</span>`).join(" &nbsp; ");
}
function toggleLT(t){ltOn[t]=!ltOn[t];document.getElementById('ll-'+t).classList.toggle('off',!ltOn[t]);if(selId){drawEgo();renderDetail();}}

// Master toggles (default: everything on). Soft = all dashed link types together.
let showEU=true, showSoft=true;
const SOFT_TYPES=['related','funding','intl_soft'];
function toggleSoft(){showSoft=!showSoft;SOFT_TYPES.forEach(t=>{ltOn[t]=showSoft;const el=document.getElementById('ll-'+t);if(el)el.classList.toggle('off',!showSoft);});const b=document.getElementById('btnSoft');if(b)b.classList.toggle('off',!showSoft);if(selId){drawEgo();renderDetail();}}
function toggleEU(){showEU=!showEU;const b=document.getElementById('btnEU');if(b)b.classList.toggle('off',!showEU);if(selId){drawEgo();renderDetail();}}
function toggleHelp(){document.getElementById('helpModal').classList.toggle('show');}
function togglePanel(which){
  document.body.classList.toggle('no-'+which);
  const hidden=document.body.classList.contains('no-'+which);
  const b=document.getElementById(which==='rail'?'btnRail':'btnDetail');
  if(b)b.classList.toggle('off',hidden);
  // the diagram area changed size — re-fit
  setTimeout(()=>{if(selId)drawEgo();},60);
}
window.addEventListener('keydown',e=>{if(e.key==='Escape')document.getElementById('helpModal').classList.remove('show');});

function initFilters(){
  const fams=[["all","All"],["LEG","Legislation"],["ORG","Bodies"],["POL","UK policy"],["INT-L","Treaties"],["INT-O","Int'l bodies"],["INT-P","Int'l policy"],["EU-L","EU law"],["IFW","Indicators"]];
  document.getElementById('famrow').innerHTML=fams.map(([v,l])=>
    `<button class="chip${v==='all'?' on':''}" onclick="setFam('${v}',this)">${l}</button>`).join("");
  document.getElementById('secrow').innerHTML=D.sectors.filter(s=>s!=="Cross-cutting").map(s=>{
    const p=PAL[s];return `<button class="secchip" data-sec="${esc(s)}" style="border-color:${p.stroke};color:${p.text}" onclick="setSec(this.dataset.sec,this)">${esc(s)}</button>`;}).join("");
}
function setFam(v,btn){famFilter=(v==='all')?null:v;document.querySelectorAll('#famrow .chip').forEach(b=>b.classList.toggle('on',b===btn));renderIndex();}
function setSec(s,btn){
  const chips=document.querySelectorAll('#secrow .secchip');
  if(secFilter===s){secFilter=null;chips.forEach(b=>{b.style.background='transparent';b.style.color=PAL[b.dataset.sec].text;});}
  else{secFilter=s;chips.forEach(b=>{b.style.background='transparent';b.style.color=PAL[b.dataset.sec].text;});btn.style.background=PAL[s].stroke;btn.style.color='#fff';}
  renderIndex();
}

function onSearch(v){
  srchQ=v.trim().toLowerCase();renderIndex();
  const ac=document.getElementById('ac');
  if(!srchQ){ac.classList.remove('show');ac.innerHTML="";acItems=[];return;}
  acItems=Object.values(N).filter(n=>n.id.toLowerCase().includes(srchQ)||n.label.toLowerCase().includes(srchQ)||(n.acr||"").toLowerCase().includes(srchQ))
    .sort((a,b)=>{const ai=a.label.toLowerCase().startsWith(srchQ)?0:1,bi=b.label.toLowerCase().startsWith(srchQ)?0:1;return ai-bi||a.id.localeCompare(b.id,undefined,{numeric:true});}).slice(0,12);
  acHi=-1;
  if(!acItems.length){ac.innerHTML=`<div class="acr" style="cursor:default;color:var(--tx3)">No matches</div>`;ac.classList.add('show');return;}
  ac.innerHTML=acItems.map((n,i)=>{const p=PAL[n.sec]||PAL['Cross-cutting'];
    return `<div class="acr" data-i="${i}" onmousedown="acPick(${i})"><span class="d" style="background:${p.stroke}"></span><span class="i">${n.id}</span><span class="n">${esc(n.label)}</span><span class="f">${esc(D.families[n.fam]||'')}</span></div>`;}).join("");
  ac.classList.add('show');
}
function acPick(i){const n=acItems[i];if(!n)return;document.getElementById('ac').classList.remove('show');document.getElementById('srch').value="";srchQ="";renderIndex();select(n.id);}
function acKey(e){const ac=document.getElementById('ac');if(!ac.classList.contains('show'))return;
  if(e.key==='ArrowDown'){e.preventDefault();acHi=Math.min(acItems.length-1,acHi+1);acPaint();}
  else if(e.key==='ArrowUp'){e.preventDefault();acHi=Math.max(0,acHi-1);acPaint();}
  else if(e.key==='Enter'){e.preventDefault();acPick(acHi<0?0:acHi);}
  else if(e.key==='Escape'){ac.classList.remove('show');}}
function acPaint(){document.querySelectorAll('#ac .acr').forEach(r=>r.classList.toggle('hi',+r.dataset.i===acHi));const el=document.querySelector('#ac .acr.hi');if(el)el.scrollIntoView({block:'nearest'});}
document.addEventListener('click',e=>{if(!e.target.closest('.srch'))document.getElementById('ac').classList.remove('show');});

function matchFilter(n){
  if(famFilter && n.fam!==famFilter) return false;
  if(secFilter && !(n.secs||[]).includes(secFilter)) return false;
  if(srchQ && !n.id.toLowerCase().includes(srchQ) && !n.label.toLowerCase().includes(srchQ) && !(n.acr||"").toLowerCase().includes(srchQ)) return false;
  return true;
}
const FAM_ORDER=["POL","LEG","ORG","INT-L","INT-P","INT-O","EU-L","IFW"];
function renderIndex(){
  const list=Object.values(N).filter(matchFilter);
  document.getElementById('railcount').textContent=`${list.length} record${list.length===1?'':'s'}`;
  const byFam={};list.forEach(n=>{(byFam[n.fam]=byFam[n.fam]||[]).push(n);});
  let h="";
  FAM_ORDER.forEach(f=>{
    const items=(byFam[f]||[]).sort((a,b)=>a.id.localeCompare(b.id,undefined,{numeric:true}));
    if(!items.length)return;
    h+=`<div class="grphdr">${D.families[f]||f} \u00b7 ${items.length}</div>`;
    items.forEach(n=>{const p=PAL[n.sec]||PAL['Cross-cutting'];
      h+=`<div class="irow${n.id===selId?' sel':''}" onclick="select('${n.id}')"><span class="irdot" style="background:${p.stroke}"></span><span class="irid">${n.id}</span><span class="irnm">${esc(n.label)}</span></div>`;});
  });
  document.getElementById('idxlist').innerHTML=h||`<div class="railcount">No records match.</div>`;
}

function select(id){ if(id===selId){return;} pushHist(id); applySel(id); }
function pushHist(id){ hist=hist.slice(0,hp+1); hist.push(id); hp=hist.length-1; updateNav(); }
function applySel(id){
  selId=id; expanded.clear();
  hashLock=true; location.hash=id?('#'+id):''; setTimeout(()=>hashLock=false,0);
  document.getElementById('empty').style.display=id?'none':'flex';
  document.getElementById('egoctrl').classList.toggle('show',!!id);
  renderIndex();drawEgo();renderDetail();updateNav();
  const row=document.querySelector('.irow.sel');if(row)row.scrollIntoView({block:'nearest'});
}
function navBack(){if(hp>0){hp--;applySel(hist[hp]);}}
function navFwd(){if(hp<hist.length-1){hp++;applySel(hist[hp]);}}
function updateNav(){document.getElementById('navBack').disabled=hp<=0;document.getElementById('navFwd').disabled=hp>=hist.length-1;document.getElementById('btnCollapse').disabled=expanded.size===0;}
window.addEventListener('hashchange',()=>{if(hashLock)return;const id=decodeURIComponent(location.hash.slice(1));if(N[id]&&id!==selId)select(id);else if(!id&&selId){selId=null;applySel(null);}});

function toggleExpand(id){ if(expanded.has(id))expanded.delete(id); else expanded.add(id); drawEgo(); updateNav(); }
function collapseAll(){ expanded.clear(); drawEgo(); updateNav(); }

function nbTypes(id){const m=new Map();ADJ[id].forEach(a=>{if(!ltOn[a.type])return;if(!showEU && N[a.o] && N[a.o].fam==='EU-L')return;if(!m.has(a.o))m.set(a.o,new Set());m.get(a.o).add(a.type);});return m;}
function strongest(types){return [...types].sort((a,b)=>LT_ORDER.indexOf(a)-LT_ORDER.indexOf(b))[0];}

function drawEgo(){
  const svg=document.getElementById('ego'),wrap=document.getElementById('egowrap');
  if(!selId){svg.innerHTML="";return;}
  const W=wrap.clientWidth,H=wrap.clientHeight;
  const sources=[selId,...[...expanded].filter(x=>x!==selId)];
  const nbOf={}; const visible=new Set(sources);
  sources.forEach(s=>{const m=nbTypes(s);nbOf[s]=m;m.forEach((_,o)=>visible.add(o));});
  const vis=visible.size;
  const SZ = vis<=6?1.32 : vis<=12?1.16 : vis<=22?1.03 : vis<=40?0.94 : vis<=70?0.88 : 0.82;
  const fMain=10.5*SZ, fFocus=12.5*SZ, fId=7.6*SZ, chipH=26*SZ, focusH=30*SZ, rowH=(chipH+6), gap=10*SZ, labelH=16;
  const charW=fMain*0.60, charWF=fFocus*0.60;
  function cw(n,focus){const s=shortName(n,focus?42:32);return Math.max(46,s.length*(focus?charWF:charW)+16)+(focus?14:0);}
  const marginX=140, padY=14, availW=Math.max(240,W-marginX-24);
  const order=[...visible].sort((a,b)=>a.localeCompare(b,undefined,{numeric:true}));
  const buckets=BANDS.map(()=>[]);
  order.forEach(id=>{const role=id===selId?'focus':(expanded.has(id)?'src':'nb');buckets[bandOf(N[id].fam)].push({id,role});});
  const bandInfo=BANDS.map((B,bi)=>{
    const items=buckets[bi];const rows=[];let row=[],rw=0;
    items.forEach(it=>{const w=cw(N[it.id],it.role==='focus');if(rw+w+gap>availW&&row.length){rows.push(row);row=[];rw=0;}row.push({...it,w});rw+=w+gap;});
    if(row.length)rows.push(row);
    const h=labelH+(rows.length?rows.length*rowH:rowH*0.5)+6;
    return {bi,label:B.label,rows,h,empty:items.length===0};
  });
  let totalH=bandInfo.reduce((s,b)=>s+b.h,0)+Math.max(0,bandInfo.length-1)*gap;
  const extra=Math.max(0,H-padY*2-totalH);
  const bandGap=gap+(bandInfo.length>1?extra/(bandInfo.length-1):0);
  const svgH=Math.max(H,padY*2+totalH);
  CONTENT={w:W,h:svgH};
  svg.removeAttribute('width');svg.removeAttribute('height');
  svg.setAttribute('preserveAspectRatio','xMidYMid meet');
  const pos={};let y=padY;
  bandInfo.forEach(b=>{
    b._labelY=y;let ry=y+labelH+rowH/2;
    b.rows.forEach(row=>{const tot=row.reduce((s,c)=>s+c.w,0)+gap*(row.length-1);let x=marginX+(availW-tot)/2;
      row.forEach(c=>{pos[c.id]={x:x+c.w/2,y:ry,w:c.w,role:c.role};x+=c.w+gap;});ry+=rowH;});
    y+=b.h+bandGap;
  });
  let defs=`<defs>`;Object.keys(LT).forEach(t=>defs+=`<marker id="ar-${t}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="11" markerHeight="11" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0.5 0.8 L9.5 5 L0.5 9.2 Z" fill="${LT[t].col}"/></marker>`);defs+=`</defs>`;
  let bg="";
  bandInfo.forEach(b=>{
    bg+=`<rect x="0" y="${b._labelY-4}" width="${W}" height="${b.h}" fill="rgba(30,30,20,${b.empty?.008:.02})"/>`;
    bg+=`<text x="14" y="${b._labelY+11}" font-size="9.5" font-weight="700" fill="${b.empty?'#C4C4B4':'#9B9B88'}" font-family="DM Sans" letter-spacing=".5">${esc(b.label.toUpperCase())}${b.empty?' \u2014 (no links)':''}</text>`;
  });
  let lines="",topLines="";const drawn=new Set();const cx=W/2;
  // Exit point on a box's border toward (tx,ty), so connectors meet the boundary (arrowheads visible).
  const boxPt=(P,tx,ty)=>{const hw=P.w/2,hh=(P.role==='focus'?focusH:chipH)/2;let dx=tx-P.x,dy=ty-P.y;if(!dx&&!dy)return{x:P.x,y:P.y};const k=Math.min(hw/Math.max(Math.abs(dx),1e-6),hh/Math.max(Math.abs(dy),1e-6));return{x:P.x+dx*k,y:P.y+dy*k};};
  sources.forEach(s=>{if(!pos[s])return;
    nbOf[s].forEach((types,o)=>{if(!pos[o])return;
      const t=strongest(types);const key=[s,o].sort().join('|')+'|'+t;if(drawn.has(key))return;drawn.add(key);
      // Draw from the SEMANTIC source A to target B (arrow at B), independent of focal node.
      const sem=semantic(s,o,t),A=sem[0],B=sem[1],arrow=sem[2];
      const f=pos[A],q=pos[B];if(!f||!q)return;
      const st=LT[t];
      const inc=(A===selId||B===selId);
      const span=Math.abs(bandOf(N[A].fam)-bandOf(N[B].fam));
      // Bow connectors that cross an intervening band sideways, so a direct link arcs clear of it.
      const bow=span>=2 ? (((f.x+q.x)/2<cx?-1:1)*(30+20*(span-1))*SZ) : 0;
      const midy=(f.y+q.y)/2;
      const a=boxPt(f,f.x+bow,midy), b=boxPt(q,q.x+bow,midy);
      if(st.dbl){const dx=(b.y-a.y),dy=-(b.x-a.x),L=Math.hypot(dx,dy)||1,ox=1.5*dx/L,oy=1.5*dy/L;const op=inc?1:.7;
        lines+=`<path d="M${a.x+ox} ${a.y+oy} C ${a.x+ox+bow} ${midy}, ${b.x+ox+bow} ${midy}, ${b.x+ox} ${b.y+oy}" fill="none" stroke="${st.col}" stroke-width="1.35" ${st.dash?`stroke-dasharray="${st.dash}"`:""} opacity="${op}"/>`;
        lines+=`<path d="M${a.x-ox} ${a.y-oy} C ${a.x-ox+bow} ${midy}, ${b.x-ox+bow} ${midy}, ${b.x-ox} ${b.y-oy}" fill="none" stroke="${st.col}" stroke-width="1.35" ${st.dash?`stroke-dasharray="${st.dash}"`:""} opacity="${op}"/>`;
      }else{
        // Emphasise edges incident to the focus node; dim purely peripheral (depth-2) edges.
        const op=inc?1:(selId&&!expanded.has(A)&&!expanded.has(B)?.5:.75);
        const w=inc?st.w+0.7:st.w;
        const path=`<path d="M${a.x} ${a.y} C ${a.x+bow} ${midy}, ${b.x+bow} ${midy}, ${b.x} ${b.y}" fill="none" stroke="${st.col}" stroke-width="${w}" ${st.dash?`stroke-dasharray="${st.dash}"`:""} ${arrow?`marker-end="url(#ar-${t})"`:""} opacity="${op}"/>`;
        if(inc)topLines+=path;else lines+=path;
      }
    });
  });
  let chips="";
  Object.entries(pos).forEach(([id,q])=>{
    const n=N[id],p=PAL[n.sec]||PAL['Cross-cutting'];
    if(q.role==='focus'){
      chips+=`<g><title>${esc(n.label)}${n.acr?' ('+esc(n.acr)+')':''} · ${n.id}</title><rect x="${q.x-q.w/2}" y="${q.y-focusH/2}" width="${q.w}" height="${focusH}" rx="9" fill="${p.stroke}" stroke="${darkenRGB(p.stroke)}" stroke-width="1.6"/>
        <text x="${q.x}" y="${q.y-1}" text-anchor="middle" font-size="${fFocus}" font-weight="700" fill="#fff" font-family="DM Sans">${esc(shortName(n,42))}</text>
        <text x="${q.x}" y="${q.y+fId+3}" text-anchor="middle" font-size="${fId}" fill="#fff" opacity=".85" font-family="DM Mono">${n.id}</text></g>`;
    }else{
      const isSrc=q.role==='src';
      chips+=`<g style="cursor:pointer" onclick="select('${id}')"><title>${esc(n.label)}${n.acr?' ('+esc(n.acr)+')':''} · ${n.id}</title>
        <rect x="${q.x-q.w/2}" y="${q.y-chipH/2}" width="${q.w}" height="${chipH}" rx="7" fill="${p.fill}" stroke="${isSrc?darkenRGB(p.stroke):p.stroke}" stroke-width="${isSrc?2.2:1.2}"/>
        <text x="${q.x}" y="${q.y-2}" text-anchor="middle" font-size="${fMain}" font-weight="600" fill="${p.text}" font-family="DM Sans">${esc(shortName(n,32))}</text>
        <text x="${q.x}" y="${q.y+fId+1.5}" text-anchor="middle" font-size="${fId}" fill="${p.text}" opacity=".7" font-family="DM Mono">${id}</text></g>`;
      const bx=q.x+q.w/2-3, by=q.y-chipH/2+3, sym=isSrc?'\u2013':'+';
      chips+=`<g style="cursor:pointer" onclick="event.stopPropagation();toggleExpand('${id}')"><circle cx="${bx}" cy="${by}" r="${7*SZ}" fill="#fff" stroke="${p.stroke}" stroke-width="1.2"/><text x="${bx}" y="${by+3.2*SZ}" text-anchor="middle" font-size="${11*SZ}" font-weight="700" fill="${p.text}" font-family="DM Sans">${sym}</text></g>`;
    }
  });
  svg.innerHTML=defs+bg+lines+topLines+chips;
  const only=[...nbOf[selId].keys()].length;
  if(only===0)svg.innerHTML+=`<text x="${W/2}" y="${H/2}" text-anchor="middle" font-size="11" fill="#9B9B88">No links of the enabled types \u2014 toggle link types in the header.</text>`;
  fitView();
}

/* ---------- zoom / pan ---------- */
function applyView(){const svg=document.getElementById('ego');if(!VIEW)return;
  svg.setAttribute('viewBox',`${VIEW.x} ${VIEW.y} ${VIEW.w} ${VIEW.h}`);}
function fitView(){if(!CONTENT)return;VIEW={x:0,y:0,w:CONTENT.w,h:CONTENT.h};applyView();}
function zoomBy(f,fx,fy){
  if(!VIEW||!CONTENT)return;
  const minW=CONTENT.w/12, maxW=CONTENT.w*2.5;
  let nw=VIEW.w/f, nh=VIEW.h/f;
  if(nw<minW||nw>maxW)return;
  if(fx===undefined){fx=VIEW.x+VIEW.w/2;fy=VIEW.y+VIEW.h/2;}
  VIEW={x:fx-(fx-VIEW.x)/f, y:fy-(fy-VIEW.y)/f, w:nw, h:nh};
  applyView();
}
function toContent(e){
  const svg=document.getElementById('ego');const m=svg.getScreenCTM();if(!m)return null;
  const p=svg.createSVGPoint();p.x=e.clientX;p.y=e.clientY;const q=p.matrixTransform(m.inverse());
  return {x:q.x,y:q.y,a:m.a,d:m.d};
}
(function initPanZoom(){
  const wrap=document.getElementById('egowrap');
  let dragging=false,didDrag=false,lx=0,ly=0;
  wrap.addEventListener('wheel',e=>{
    if(!selId)return;e.preventDefault();
    const c=toContent(e);if(!c)return;
    zoomBy(e.deltaY<0?1.12:1/1.12,c.x,c.y);
  },{passive:false});
  wrap.addEventListener('mousedown',e=>{
    if(!selId||e.button!==0)return;
    dragging=true;didDrag=false;lx=e.clientX;ly=e.clientY;wrap.classList.add('grabbing');
  });
  window.addEventListener('mousemove',e=>{
    if(!dragging)return;
    const dx=e.clientX-lx, dy=e.clientY-ly;
    if(Math.abs(dx)>3||Math.abs(dy)>3)didDrag=true;
    const svg=document.getElementById('ego');const m=svg.getScreenCTM();if(!m)return;
    VIEW.x-=dx/m.a; VIEW.y-=dy/m.d; applyView();
    lx=e.clientX;ly=e.clientY;
  });
  window.addEventListener('mouseup',()=>{dragging=false;wrap.classList.remove('grabbing');
    if(didDrag){suppressClick=true;setTimeout(()=>suppressClick=false,0);}});
  wrap.addEventListener('click',e=>{if(suppressClick){e.stopPropagation();e.preventDefault();}},true);
})();

function exportImg(kind){
  if(!selId||!VIEW)return;
  const src=document.getElementById('ego');
  const clone=src.cloneNode(true);
  // export exactly the visible window: clip to the current viewBox
  const w=VIEW.w, h=VIEW.h;
  const rect=document.createElementNS('http://www.w3.org/2000/svg','rect');
  rect.setAttribute('x',VIEW.x);rect.setAttribute('y',VIEW.y);rect.setAttribute('width',w);rect.setAttribute('height',h);rect.setAttribute('fill','#F7F6F2');
  clone.insertBefore(rect,clone.firstChild);
  clone.setAttribute('viewBox',`${VIEW.x} ${VIEW.y} ${w} ${h}`);
  clone.setAttribute('xmlns','http://www.w3.org/2000/svg');clone.setAttribute('width',w);clone.setAttribute('height',h);
  const s=new XMLSerializer().serializeToString(clone);
  const name='governance_'+selId;
  if(kind==='svg'){dl(new Blob([s],{type:'image/svg+xml'}),name+'.svg');return;}
  const img=new Image();const svgUrl='data:image/svg+xml;base64,'+btoa(unescape(encodeURIComponent(s)));
  img.onload=()=>{const sc=2;const c=document.createElement('canvas');c.width=w*sc;c.height=h*sc;const ctx=c.getContext('2d');ctx.scale(sc,sc);ctx.drawImage(img,0,0);c.toBlob(b=>dl(b,name+'.png'),'image/png');};
  img.src=svgUrl;
}
function dl(blob,name){const u=URL.createObjectURL(blob);const a=document.createElement('a');a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000);}

// Narrative-column label per family (what the blurb actually is)
const BLURB_LBL={LEG:"Key provisions","EU-L":"Key provisions",ORG:"Remit & powers","INT-O":"Remit & powers",POL:"Scope & commitments","INT-L":"Key provisions","INT-P":"Key commitments",IFW:"Policy purpose"};
const CREF_RE=/\[((?:LEG|ORG|POL|IFW|INT-L|INT-O|INT-P|EU-L)-\d+)\]/g;
// Render narrative with [CODE] tokens as hover-tooltip chips (full record name on hover).
function codeHtml(text){return esc(text).replace(CREF_RE,(m,c)=>{const t=N[c];return t?`<span class="cref" title="${esc(t.label)}${t.acr?' ('+esc(t.acr)+')':''}">[${c}]</span>`:m;});}

function renderDetail(){
  const d=document.getElementById('detail');
  if(!selId){d.innerHTML=`<div style="color:var(--tx3);font-size:11px">No record selected \u2014 pick one from the list, search, or paste <span class="mono">#RECORD-ID</span> into the URL.</div>`;return;}
  const n=N[selId];
  const src=n.url?`<a class="dlink" href="${n.url}" target="_blank" rel="noopener">\u2197 source</a>`:"";
  let h=`<div class="dhead"><div style="flex:1;min-width:220px">
    <div class="did">${n.id} \u00b7 ${D.families[n.fam]||n.fam}</div>
    <div class="dtitle">${esc(n.label)} ${src}</div>
    <div class="dmeta">${n.type?`<span class="dtag type">${esc(n.type)}</span>`:""}
      ${(n.secs||[]).map(s=>{const pp=PAL[s]||PAL['Cross-cutting'];return `<span class="dtag" style="border-color:${pp.stroke};color:${pp.text};background:${pp.fill}">${esc(s)}</span>`;}).join("")}
      ${n.year?`<span class="dtag">${esc(n.year)}</span>`:""}
      ${n.status?`<span class="dtag">${esc(n.status)}</span>`:""}
      <span class="dtag mono">${n.deg} links</span></div></div></div>`;
  // Feature the narrative columns (the relationships are the diagram itself).
  const secs=[];
  if(n.blurb) secs.push([BLURB_LBL[n.fam]||"Notes", n.blurb]);
  (n.x||[]).forEach(pr=>secs.push(pr));
  if(secs.length){
    secs.forEach(([lbl,val])=>{h+=`<div class="dblurb-lbl">${esc(lbl)}</div><div class="dblurb">${codeHtml(val)}</div>`;});
  }else{
    h+=`<div class="dblurb" style="color:var(--tx3);font-style:italic">No narrative recorded for this record.</div>`;
  }
  d.innerHTML=h;
}

initLegend();initFilters();renderIndex();
const boot=decodeURIComponent(location.hash.slice(1));
if(N[boot]){select(boot);} else {applySel(null);}
new ResizeObserver(()=>{if(selId)drawEgo();}).observe(document.getElementById('egowrap'));
</script>
</body>
</html>"""

if __name__ == "__main__":
    build()
