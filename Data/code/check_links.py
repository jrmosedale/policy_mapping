#!/usr/bin/env python3
"""check_links.py — referential-integrity checker for the climate-nature governance workbooks.

Validates every bracketed [CODE] cross-reference across the UK governance, international
governance, and biodiversity-indicators workbooks against a registry of all known Record_IDs
and Framework_IDs, enforces the UK<->international bidirectional and placement invariants, and validates every
Data_Type "Controlled" column against the vocabulary declared in each workbook's Data Dictionary.

Usage:
    python3 check_links.py [uk.xlsx] [international.xlsx] [indicators.xlsx]

With no arguments it uses the stable-named canonical files in the working directory
(e.g. uk_climate_nature_governance.xlsx), falling back to the highest _vN file if absent. Exit code 0 = all pass, 1 = issues found.
"""
import sys, re, glob, os
from collections import defaultdict
import openpyxl

CODE = re.compile(r'\[([A-Z]{2,4}-[A-Z]?-?\d{1,3})\]')
UK_FAM = ('LEG', 'ORG', 'POL')
INTL_FAM = ('INT-L', 'INT-O', 'INT-P', 'EU-L')
RETIRED = {'POL-023', 'POL-024', 'LEG-008', 'LEG-009'}  # LEG-008/009 retired v29 (not statutory instruments)


def fam(code):
    return code.rsplit('-', 1)[0]


def latest(pattern):
    """Highest _vN.xlsx match, ignoring _superseded_ archives."""
    files = [f for f in glob.glob(pattern) if '_superseded_' not in f and re.search(r'_v(\d+)\.xlsx$', f)]
    if not files:
        return None
    return max(files, key=lambda f: int(re.search(r'_v(\d+)\.xlsx$', f).group(1)))


def resolve(canonical, *glob_patterns):
    """Prefer the canonical stable-named file; else fall back to the highest version-suffixed file."""
    if os.path.exists(canonical):
        return canonical
    for pat in glob_patterns:
        hit = latest(pat)
        if hit:
            return hit
    return None


def load_ids(path, id_cols):
    """Return {record_id: (sheet, row)} for the given id column names, per workbook."""
    ids = {}
    wb = openpyxl.load_workbook(path, read_only=True)
    for sn in wb.sheetnames:
        ws = wb[sn]
        hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        idx = next((hdr.index(c) for c in id_cols if c in hdr), None)
        if idx is None:
            continue
        for r, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            v = row[idx]
            if v and isinstance(v, str) and re.match(r'^[A-Z]{2,4}-', v.strip()):
                ids[v.strip()] = (os.path.basename(path), sn, r)
    wb.close()
    return ids


def scan_refs(path, id_cols):
    """Yield (sheet, row, record_id, cell_col_name, code) for every bracketed code,
    excluding the record-id column itself."""
    wb = openpyxl.load_workbook(path, read_only=True)
    for sn in wb.sheetnames:
        ws = wb[sn]
        hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        id_idx = next((hdr.index(c) for c in id_cols if c in hdr), None)
        for r, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            rid = row[id_idx] if id_idx is not None else None
            for ci, val in enumerate(row):
                if ci == id_idx or not val:
                    continue
                for code in CODE.findall(str(val)):
                    yield sn, r, rid, hdr[ci] if ci < len(hdr) else f'col{ci}', code
    wb.close()


def uk_links_map(intl_path):
    """From international UK_Links -> {uk_code: {intl_id}} (UK-family codes only)."""
    m = defaultdict(set)
    wb = openpyxl.load_workbook(intl_path, read_only=True)
    for sn in wb.sheetnames:
        ws = wb[sn]
        hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        if 'UK_Links' not in hdr or 'Record_ID' not in hdr:
            continue
        ri, ui = hdr.index('Record_ID'), hdr.index('UK_Links')
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[ri] is None or not row[ui]:
                continue
            for c in CODE.findall(str(row[ui])):
                if fam(c) in UK_FAM:
                    m[c].add(row[ri])
    wb.close()
    return m


def intl_links_map(uk_path):
    """From UK Intl_Links -> {uk_code: {intl_id}}."""
    m = defaultdict(set)
    wb = openpyxl.load_workbook(uk_path, read_only=True)
    for sn in wb.sheetnames:
        ws = wb[sn]
        hdr = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
        if 'Intl_Links' not in hdr or 'Record_ID' not in hdr:
            continue
        ri, ii = hdr.index('Record_ID'), hdr.index('Intl_Links')
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[ri] and row[ii]:
                for c in CODE.findall(str(row[ii])):
                    m[row[ri]].add(c)
    wb.close()
    return m



# --- controlled-vocabulary invariant ------------------------------------------

# Vocabulary cells that describe a PATTERN rather than enumerate terms are skipped.
VOCAB_PATTERN_MARKERS = ('\u2026', '...', ' through ', 'Free text', 'N.N', 'semicolon-separated')
VOCAB_SEP = re.compile(r'\s*\|\s*')

# Columns reported as a WARNING rather than a failure, with the reason.
# An entry here is a debt, not a permanent exemption: it exists so a newly added invariant can be
# landed without blocking the release gate on a pre-existing problem that needs a human decision.
VOCAB_WARN_ONLY = {
    # Empty, and it should stay that way. The Policy_Sector entry that lived here was cleared on
    # 2026-09-18: the fork turned out to be confined to the derived Cross-Reference Index, which
    # rebuild_xref.py now regenerates, rather than a disagreement about the vocabulary itself.
}
SHEET_SCOPED = re.compile(r"^\s*([A-Za-z][A-Za-z &/'-]{2,40}?)\s*:\s*(.+)$", re.S)


def _parse_vocab(cell):
    """Return (flat_terms, {sheet_name: terms}); exactly one of the two is populated."""
    scoped, flat = {}, []
    for seg in [x for x in str(cell).split(';') if x.strip()]:
        m = SHEET_SCOPED.match(seg)
        if m and '|' in m.group(2):
            scoped[m.group(1).strip()] = [t.strip() for t in VOCAB_SEP.split(m.group(2)) if t.strip()]
        else:
            flat.extend(t.strip() for t in VOCAB_SEP.split(seg) if t.strip())
    return ([], scoped) if scoped else (flat, {})


def _term_ok(value, terms):
    """Exact match, or prefix match for terms carrying a [placeholder] e.g. 'Royal Assent [date]'."""
    if value in terms:
        return True
    for t in terms:
        if '[' in t:
            stem = t.split('[', 1)[0].strip()
            if stem and value.startswith(stem):
                return True
    return False


def _rule_applies(dd_sheet, sheet_name, all_sheets):
    """Does a Data Dictionary row's Sheet value cover this sheet?

    'All sheets' / 'All framework sheets' -> every sheet. An exact sheet name -> that sheet only.
    A slash-separated abbreviation list ('EIF / CCC / JNCC') -> any sheet starting with a token.
    Anything unrecognised falls back to applying everywhere, so a rule is never silently dropped.
    """
    if not dd_sheet or dd_sheet.lower().startswith('all '):
        return True
    if dd_sheet in all_sheets:
        return dd_sheet == sheet_name
    tokens = [t.strip() for t in dd_sheet.split('/') if t.strip()]
    if tokens and any(s in all_sheets or any(x.startswith(s) for x in all_sheets) for s in tokens):
        return any(sheet_name == t or sheet_name.startswith(t) for t in tokens)
    return True


def vocab_breaches(path):
    """Yield a message per cell value not present in its column's declared vocabulary."""
    wb = openpyxl.load_workbook(path, read_only=True)
    if 'Data Dictionary' not in wb.sheetnames:
        return
    dd_rows = list(wb['Data Dictionary'].iter_rows(values_only=True))
    dd_hdr = dd_rows[0]
    try:
        c_sheet = dd_hdr.index('Sheet')
        c_col = dd_hdr.index('Column_Name')
        c_type = dd_hdr.index('Data_Type')
        c_vocab = dd_hdr.index('Controlled_Vocabulary')
    except ValueError:
        return

    rules = []
    for r in dd_rows[1:]:
        if not r[c_col] or not r[c_type] or 'Controlled' not in str(r[c_type]):
            continue
        cell = r[c_vocab]
        if not cell or any(m in str(cell) for m in VOCAB_PATTERN_MARKERS):
            continue
        flat, scoped = _parse_vocab(cell)
        if flat or scoped:
            rules.append((str(r[c_sheet] or '').strip(), str(r[c_col]).strip(), flat, scoped))

    base = os.path.basename(path)
    for sn in wb.sheetnames:
        if sn in ('Data Dictionary', 'Changelog', 'Legend', 'NCF Legend',
                  'Cross-Reference Index'):
            continue
        ws = wb[sn]
        first = next(ws.iter_rows(min_row=1, max_row=1), None)
        if not first:
            continue
        hdr = [c.value for c in first]
        idcol = next((hdr.index(c) for c in ('Record_ID', 'Framework_ID') if c in hdr), None)
        for dd_sheet, col_name, flat, scoped in rules:
            if col_name not in hdr:
                continue
            if not _rule_applies(dd_sheet, sn, wb.sheetnames):
                continue
            terms = scoped.get(sn) or (flat or None)
            if not terms:
                continue        # sheet-scoped vocabulary with no group for this sheet
            ci = hdr.index(col_name)
            for rn, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                v = row[ci] if ci < len(row) else None
                if v is None or str(v).strip() == '':
                    continue
                rid = row[idcol] if idcol is not None and idcol < len(row) else f'row {rn}'
                for token in [t.strip() for t in VOCAB_SEP.split(str(v)) if t.strip()]:
                    if not _term_ok(token, terms):
                        yield (f"{base} :: {sn} row {rn} ({rid}) :: "
                               f"{col_name} = '{token}' not in declared vocabulary")
    wb.close()


def main():
    args = sys.argv[1:]
    uk = args[0] if len(args) > 0 else resolve(
        'uk_climate_nature_governance.xlsx', 'uk_climate_nature_governance_v*.xlsx')
    intl = args[1] if len(args) > 1 else resolve(
        'international_climate_nature_governance.xlsx', 'international_climate_nature_governance_v*.xlsx')
    ind = args[2] if len(args) > 2 else resolve(
        'indicators_climate_nature.xlsx',
        'indicators_climate_nature_v*.xlsx', 'biodiversity_indicators_manual_v*.xlsx')
    for label, p in [('UK', uk), ('international', intl), ('indicators', ind)]:
        if not p or not os.path.exists(p):
            print(f"FATAL: {label} workbook not found ({p}).")
            sys.exit(2)
    print(f"UK           : {os.path.basename(uk)}")
    print(f"International : {os.path.basename(intl)}")
    print(f"Indicators   : {os.path.basename(ind)}\n")

    ID_COLS = ('Record_ID', 'Framework_ID')
    registry = {}
    for p in (uk, intl, ind):
        registry.update(load_ids(p, ID_COLS))
    print(f"Registry: {len(registry)} Record_IDs / Framework_IDs across 3 workbooks.\n")

    issues = defaultdict(list)

    # 1. Orphan references: every bracketed code must resolve
    for p in (uk, intl, ind):
        for sn, r, rid, col, code in scan_refs(p, ID_COLS):
            if code not in registry:
                issues['orphan'].append(f"{os.path.basename(p)} :: {sn} row {r} ({rid}) :: {col} -> [{code}] not in registry")

    # 2. Placement invariant: UK_Links = UK codes only; Intl_Links = international codes only
    for sn, r, rid, col, code in scan_refs(intl, ID_COLS):
        if col == 'UK_Links' and fam(code) in INTL_FAM:
            issues['placement'].append(f"{os.path.basename(intl)} :: {sn} row {r} ({rid}) :: international [{code}] in UK_Links")
    for sn, r, rid, col, code in scan_refs(uk, ID_COLS):
        if col == 'Intl_Links' and fam(code) in UK_FAM:
            issues['placement'].append(f"{os.path.basename(uk)} :: {sn} row {r} ({rid}) :: UK [{code}] in Intl_Links")

    # 3. Bidirectional completeness UK<->international
    fwd = uk_links_map(intl)      # uk_code -> {intl_id}
    rev = intl_links_map(uk)      # uk_code -> {intl_id}
    for uk_code, iset in fwd.items():
        for iid in iset:
            if iid not in rev.get(uk_code, set()):
                issues['missing_reverse'].append(f"{iid} -> {uk_code} present in international UK_Links but no reverse in UK Intl_Links")
    for uk_code, iset in rev.items():
        for iid in iset:
            if iid not in fwd.get(uk_code, set()):
                issues['extra_reverse'].append(f"{uk_code} -> {iid} present in UK Intl_Links but no forward in international UK_Links")

    # 4. Controlled vocabulary: every value in a Data_Type "Controlled" column must be declared
    warnings = defaultdict(list)
    for p in (uk, intl, ind):
        for msg in vocab_breaches(p):
            col = msg.rsplit(':: ', 1)[-1].split(' = ', 1)[0].strip()
            if col in VOCAB_WARN_ONLY:
                warnings[col].append(msg)
            else:
                issues['vocab'].append(msg)

    # 5. Retired IDs must not reappear as records
    for rid in RETIRED:
        if rid in registry:
            issues['retired'].append(f"retired ID {rid} reused at {registry[rid]}")

    labels = {
        'orphan': 'Orphan references (code with no matching record)',
        'placement': 'Placement-invariant breaches (wrong link column)',
        'missing_reverse': 'Forward links with no reverse (UK<->intl)',
        'extra_reverse': 'Reverse links with no forward (UK<->intl)',
        'vocab': 'Controlled-vocabulary breaches (value not declared in Data Dictionary)',
        'retired': 'Retired Record_IDs reused',
    }
    total = sum(len(v) for v in issues.values())
    for key, title in labels.items():
        rows = issues.get(key, [])
        tag = 'PASS' if not rows else f'FAIL ({len(rows)})'
        print(f"[{tag}] {title}")
        for line in rows[:50]:
            print(f"        - {line}")
        if len(rows) > 50:
            print(f"        ... and {len(rows) - 50} more")

    for col, rows in warnings.items():
        print(f"[WARN] Controlled-vocabulary debt: {col} ({len(rows)} values)")
        print(f"        reason: {VOCAB_WARN_ONLY[col]}")
        for line in rows[:5]:
            print(f"        - {line}")
        if len(rows) > 5:
            print(f"        ... and {len(rows) - 5} more (not a gate failure)")

    print(f"\n{'ALL CHECKS PASSED' if total == 0 else f'{total} ISSUE(S) FOUND'}")
    sys.exit(0 if total == 0 else 1)


if __name__ == '__main__':
    main()
