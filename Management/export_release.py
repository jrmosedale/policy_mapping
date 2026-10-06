#!/usr/bin/env python3
"""
export_release.py — plain-format exports of the canonical workbooks and the governing documents.

Run by finalise.py as its third step, after the integrity gate and the dashboard rebuild. Can also
be run on its own. Writes, under Exports/ at the project root:

  Exports/csv/<workbook>/<Sheet_Name>.csv   one CSV per sheet of each canonical workbook
  Exports/csv/_manifest.csv                 one row per CSV: version, rows, columns, record count
  Exports/docx/<NAME>.docx                  the protocols, method, user guide, handover, pending queue
                                            and climate-score method
  Exports/README.txt                        what these files are and how to read them

Why: the workbooks and Markdown files are the source of truth, but not every reader handles them
well. GitHub Copilot and other text-based tools read a single-table CSV directly, whereas an .xlsx
needs a script; pandas reads a CSV more reliably than a styled workbook; git shows a readable diff
of a CSV where it can only report that an .xlsx changed; and colleagues without a Markdown viewer
read the governing documents as Word files. Nothing here is ever edited by hand — every file is
regenerated from its source, and editing an export changes nothing upstream.

Design rules:
  * Deterministic output. No timestamps are written into any file, and a file is only rewritten
    when its content would change, so an unchanged sheet or document produces no git diff and no
    OneDrive re-sync.
  * Faithful export. Every sheet is exported as stored — banner rows, merged-cell remnants and the
    Changelog key/value block included. Nothing is filtered or reinterpreted; where a sheet needs a
    counting rule (the CBD GBF banner rows), the manifest and README state it instead.
  * Stale exports are removed. A CSV or DOCX whose source sheet or document no longer exists is
    deleted, so the folder never offers an agent a sheet that has gone. If deletion is not
    permitted, the file is named in a warning and the run still succeeds.
  * No new dependencies: openpyxl (already required by the builders) and python-docx (already
    required by the render kit).

Usage:
    python3 Management/export_release.py

Exit code 0 = all exports written or already current. 1 = an export failed.
"""
import csv
import hashlib
import os
import io
import re
import sys
from pathlib import Path

try:
    import openpyxl
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError as e:  # pragma: no cover
    sys.exit(f"FATAL: missing dependency ({e.name}). Install openpyxl and python-docx:\n"
             f"       pip install openpyxl python-docx")

ROOT = Path(__file__).resolve().parent.parent
CANON_DIR = ROOT / "Data" / "canonical_files"
EXPORT_DIR = ROOT / "Exports"
CSV_DIR = EXPORT_DIR / "csv"
DOCX_DIR = EXPORT_DIR / "docx"

WORKBOOKS = [
    "uk_climate_nature_governance.xlsx",
    "international_climate_nature_governance.xlsx",
    "indicators_climate_nature.xlsx",
]

# Documents exported to DOCX. Every protocol is picked up automatically; add others here.
DOC_SOURCES = sorted((ROOT / "Management" / "protocols").glob("*.md")) + [
    ROOT / "PA_toolkit" / "METHOD_AND_SCORING.md",
    ROOT / "PA_toolkit" / "ASSESSMENT_TOOLKIT_USER_GUIDE.md",
    ROOT / "Management" / "PROJECT_HANDOVER_Nature_Climate_Indicators.md",
    ROOT / "Data" / "pending_additions.md",
    ROOT / "outputs_other" / "CLIMATE_SCORE_METHOD.md",
    ROOT / "Data" / "CANONICAL_FILES_GUIDE.md",
]

# Bump when the Markdown -> DOCX conversion changes, so every DOCX is regenerated once.
CONVERTER_VERSION = "1"

FONT = "Arial"          # matches the render kit's default Word font
MONO = "Consolas"
TEXT_SIZE = Pt(10.5)
TABLE_SIZE = Pt(9)
CODE_SIZE = Pt(8.5)
LINK_COLOUR = "0B5563"


# --------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------

def rel(p):
    return p.relative_to(ROOT).as_posix()


def replace_bytes(path, data):
    """Write `data` to `path` via a sibling temp file and an atomic rename.

    Renaming over the old file never reads or opens it, so this also works when the old file is
    an online-only OneDrive placeholder, where opening it fails with OSError errno 35 ("Resource
    deadlock avoided") in a sandbox that cannot trigger the download (fixed 2026-10-06).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def write_if_changed(path, data):
    """Write bytes only if they differ from what is on disk. Returns 'written' or 'unchanged'.

    An existing file that cannot be read (e.g. an online-only OneDrive placeholder) is treated as
    changed and replaced, rather than aborting the whole export: before 2026-10-06 one such file
    stopped every release at the CSV step.
    """
    if path.exists():
        try:
            if path.read_bytes() == data:
                return "unchanged"
        except OSError as e:
            print(f"  {'unreadable':<10} {path.name}: {e.strerror or e} - replacing")
    replace_bytes(path, data)
    return "written"


def sheet_slug(name):
    s = name.replace("&", "and")
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s or "sheet"


def remove_stale(root, pattern, keep):
    """Delete generated files under root that this run did not produce. Returns warnings."""
    warnings = []
    if not root.exists():
        return warnings
    for p in sorted(root.rglob(pattern)):
        if p.resolve() in keep:
            continue
        try:
            p.unlink()
            print(f"  removed stale  {rel(p)}")
        except OSError as e:
            warnings.append(f"stale export could not be removed ({e.strerror}): {rel(p)}")
    return warnings


# --------------------------------------------------------------------------------------------
# Workbooks -> CSV
# --------------------------------------------------------------------------------------------

def cell_text(value, link):
    """Text for one cell. Hyperlink targets are kept if the cell's text does not already show them."""
    text = "" if value is None else str(value)
    if link and link not in text:
        text = f"{text} <{link}>" if text else link
    return text


def sheet_rows(ws_val, ws_raw):
    """All rows of a sheet as lists of strings, trimmed to the last non-empty row and column."""
    links = {}
    for row in ws_raw.iter_rows():
        for c in row:
            if c.hyperlink is not None and c.hyperlink.target:
                links[(c.row, c.column)] = c.hyperlink.target
    rows = []
    for r_idx, row in enumerate(ws_val.iter_rows(values_only=True), start=1):
        rows.append([cell_text(v, links.get((r_idx, c_idx)))
                     for c_idx, v in enumerate(row, start=1)])
    while rows and not any(rows[-1]):
        rows.pop()
    width = max((max((i + 1 for i, v in enumerate(r) if v), default=0) for r in rows), default=0)
    return [r[:width] + [""] * (width - len(r[:width])) for r in rows], len(links)


def sheet_stats(rows, merged):
    """Row counts and notes for the manifest."""
    header = rows[0] if rows else []
    data = [r for r in rows[1:] if any(r)]
    stats = {"columns": len(header), "data_rows": len(data), "records": "", "notes": []}
    if "Record_ID" in header:
        i_id = header.index("Record_ID")
        i_name = header.index("Indicator_Name") if "Indicator_Name" in header else None
        keyed = [r for r in data if r[i_id]]
        if i_name is not None:
            banners = [r for r in keyed if not r[i_name]]
            recs = [r for r in keyed if r[i_name]]
            stats["records"] = len(recs)
            if banners:
                stats["notes"].append(
                    f"{len(banners)} section-banner row(s) have Record_ID but no Indicator_Name; "
                    f"not indicator records")
        else:
            stats["records"] = len(keyed)
    elif header[:1] == ["Workbook"]:
        stats["notes"].append("key/value block (Workbook, Version, Last updated), then a "
                              "Version|Date|Summary|Author table; row 1 is not a header")
    if merged:
        stats["notes"].append(f"{merged} merged range(s): the text sits in the first cell of "
                              f"each merged range; the other cells are empty")
    return stats


def export_workbooks():
    manifest = [["workbook", "workbook_version", "sheet", "csv_file", "columns", "data_rows",
                 "records", "notes"]]
    produced, versions, counts = set(), {}, {"written": 0, "unchanged": 0}
    indicator_records = 0
    for name in WORKBOOKS:
        path = CANON_DIR / name
        if not path.exists():
            raise FileNotFoundError(f"canonical workbook not found: {rel(path)}")
        wb_val = openpyxl.load_workbook(path, data_only=True)   # values (no formulas by rule)
        wb_raw = openpyxl.load_workbook(path)                   # second load for hyperlink targets
        version = ""
        if "Changelog" in wb_val.sheetnames:
            v = wb_val["Changelog"]["B2"].value
            version = "" if v is None else str(v)
        versions[name] = version
        stem = Path(name).stem
        used = set()
        for ws in wb_val.worksheets:
            slug = sheet_slug(ws.title)
            while slug.lower() in used:          # guard: two titles slugging to the same name
                slug += "_"
            used.add(slug.lower())
            out = CSV_DIR / stem / f"{slug}.csv"
            rows, n_links = sheet_rows(ws, wb_raw[ws.title])
            buf = io.StringIO()
            csv.writer(buf, lineterminator="\n").writerows(rows)
            state = write_if_changed(out, buf.getvalue().encode("utf-8"))
            counts[state] += 1
            produced.add(out.resolve())
            st = sheet_stats(rows, len(ws.merged_cells.ranges))
            if name == "indicators_climate_nature.xlsx" and st["records"] != "" \
                    and "Indicator_Name" in (rows[0] if rows else []):
                indicator_records += st["records"]
            manifest.append([name, version, ws.title, out.relative_to(EXPORT_DIR).as_posix(),
                             st["columns"], st["data_rows"], st["records"], "; ".join(st["notes"])])
            print(f"  {state:<10} {rel(out)}  ({st['data_rows']} rows)")
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(manifest)
    mpath = CSV_DIR / "_manifest.csv"
    counts[write_if_changed(mpath, buf.getvalue().encode("utf-8"))] += 1
    produced.add(mpath.resolve())
    warnings = remove_stale(CSV_DIR, "*.csv", produced)
    return versions, indicator_records, counts, warnings


# --------------------------------------------------------------------------------------------
# Markdown -> DOCX (the subset these documents use: headings, paragraphs, bullet and numbered
# lists with continuation lines, pipe tables, fenced code, block quotes, rules, and inline
# **bold**, *italic*, `code` and [links](url)). Underscores are never emphasis — too many
# identifiers such as Record_ID contain them.
# --------------------------------------------------------------------------------------------

INLINE = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<bold>\*\*(?P<bold_t>.+?)\*\*)"
    r"|(?P<link>\[(?P<link_t>[^\]]+)\]\((?P<link_u>[^)\s]+)\))"
    r"|(?P<ital>\*(?=\S)(?P<ital_t>.+?)(?<=\S)\*)"
)


def _shade(element, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    element.append(shd)


def _hyperlink(par, text, url, size=None):
    r_id = par.part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement("w:hyperlink")
    h.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    colour = OxmlElement("w:color")
    colour.set(qn("w:val"), LINK_COLOUR)
    underline = OxmlElement("w:u")
    underline.set(qn("w:val"), "single")
    rpr.append(colour)
    rpr.append(underline)
    if size is not None:
        sz = OxmlElement("w:sz")
        sz.set(qn("w:val"), str(int(size.pt * 2)))
        rpr.append(sz)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    h.append(run)
    par._p.append(h)


def add_inline(par, text, bold=False, italic=False, size=None):
    pos = 0
    for m in INLINE.finditer(text):
        if m.start() > pos:
            _run(par, text[pos:m.start()], bold, italic, size)
        if m.group("code"):
            r = _run(par, m.group("code")[1:-1], bold, italic, size)
            r.font.name = MONO
        elif m.group("bold"):
            add_inline(par, m.group("bold_t"), True, italic, size)
        elif m.group("link"):
            _hyperlink(par, m.group("link_t"), m.group("link_u"), size)
        else:
            add_inline(par, m.group("ital_t"), bold, True, size)
        pos = m.end()
    if pos < len(text):
        _run(par, text[pos:], bold, italic, size)


def _run(par, text, bold, italic, size):
    r = par.add_run(text)
    r.bold = bold or None
    r.italic = italic or None
    if size is not None:
        r.font.size = size
    return r


def _split_row(line):
    """Split a pipe-table row into cells, ignoring pipes inside `code` spans."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells, cur, in_code = [], [], False
    for ch in s:
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
BULLET = re.compile(r"^(\s*)[-*+]\s+(.*)$")
NUMBER = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
RULE = re.compile(r"^\s*(-{3,}|\*{3,}|_{3,})\s*$")
FENCE = re.compile(r"^\s*```")


class DocBuilder:
    def __init__(self, title, source_rel, digest):
        self.doc = Document()
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)      # A4
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(sec, side, Cm(2.0))
        normal = self.doc.styles["Normal"]
        normal.font.name = FONT
        normal.font.size = TEXT_SIZE
        normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
        for lvl in range(1, 5):
            st = self.doc.styles[f"Heading {lvl}"]
            st.font.name = FONT
            st.font.color.rgb = RGBColor.from_string("0B5563")
        cp = self.doc.core_properties
        cp.title = title
        cp.subject = source_rel
        cp.comments = digest          # read back to skip regeneration when the source is unchanged
        cp.author = "export_release.py"
        cp.keywords = "generated; do not edit"
        note = self.doc.add_paragraph()
        _run(note, f"Generated from {source_rel} by Management/export_release.py. Do not edit "
                   f"this file: edit the Markdown source and re-run finalise.py.",
             False, True, Pt(8.5))
        self.item = None      # last list-item paragraph, for continuation lines
        self.item_indent = 0

    # blocks -------------------------------------------------------------------------------
    def heading(self, level, text):
        h = self.doc.add_heading(level=min(level, 4))
        add_inline(h, text)
        self.item = None

    def paragraph(self, text, indent=None):
        p = self.doc.add_paragraph()
        if indent:
            p.paragraph_format.left_indent = indent
        add_inline(p, text)
        return p

    def bullet(self, depth, text):
        style = "List Bullet" if depth == 0 else f"List Bullet {min(depth + 1, 3)}"
        p = self.doc.add_paragraph(style=style)
        add_inline(p, text)
        self.item, self.item_indent = p, Cm(0.63 * (depth + 1))

    def numbered(self, depth, number, text):
        # Literal numbers, not Word auto-numbering: python-docx's "List Number" continues one
        # sequence through the whole document, which would renumber every later list.
        indent = Cm(0.8 * (depth + 1))
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent, pf.first_line_indent = indent, -Cm(0.8)
        pf.space_after = Pt(3)
        pf.tab_stops.add_tab_stop(indent)
        _run(p, f"{number}.\t", False, False, None)
        add_inline(p, text)
        self.item, self.item_indent = p, indent

    def code(self, lines):
        p = self.doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Cm(0.4)
        pf.space_before, pf.space_after = Pt(3), Pt(6)
        _shade(p._p.get_or_add_pPr(), "F2F4F5")
        for i, line in enumerate(lines):
            r = p.add_run(line)
            r.font.name, r.font.size = MONO, CODE_SIZE
            if i < len(lines) - 1:
                r.add_break()
        self.item = None

    def quote(self, text):
        try:
            p = self.doc.add_paragraph(style="Intense Quote")
        except KeyError:
            p = self.doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.8)
        add_inline(p, text)
        self.item = None

    def rule(self):
        p = self.doc.add_paragraph()
        pbdr = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "A0A8AD")):
            bottom.set(qn(f"w:{k}"), v)
        pbdr.append(bottom)
        p._p.get_or_add_pPr().append(pbdr)
        self.item = None

    def table(self, rows):
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        t = self.doc.add_table(rows=len(rows), cols=width)
        t.style = "Table Grid"
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        for i, row in enumerate(rows):
            for j, text in enumerate(row):
                cell = t.cell(i, j)
                par = cell.paragraphs[0]
                add_inline(par, text, bold=(i == 0), size=TABLE_SIZE)
                if i == 0:
                    _shade(cell._tc.get_or_add_tcPr(), "DCE6E8")
        self.doc.add_paragraph()
        self.item = None

    def save(self):
        buf = io.BytesIO()
        self.doc.save(buf)
        return buf.getvalue()


def md_to_docx(md_text, title, source_rel, digest):
    b = DocBuilder(title, source_rel, digest)
    lines = md_text.splitlines()
    para = []
    i, n = 0, len(lines)

    def flush():
        nonlocal para
        if para:
            b.paragraph(" ".join(s.strip() for s in para))
            b.item = None
            para = []

    while i < n:
        line = lines[i]
        if not line.strip():
            flush()
            i += 1
            continue
        if FENCE.match(line):
            flush()
            i += 1
            block = []
            while i < n and not FENCE.match(lines[i]):
                block.append(lines[i].rstrip())
                i += 1
            i += 1  # closing fence
            b.code(block)
            continue
        m = HEADING.match(line)
        if m:
            flush()
            b.heading(len(m.group(1)), m.group(2))
            i += 1
            continue
        if RULE.match(line):
            flush()
            b.rule()
            i += 1
            continue
        if line.lstrip().startswith("|") and i + 1 < n and TABLE_SEP.match(lines[i + 1]):
            flush()
            rows = [_split_row(line)]
            i += 2
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(_split_row(lines[i]))
                i += 1
            b.table(rows)
            continue
        if line.lstrip().startswith(">"):
            flush()
            q = []
            while i < n and lines[i].lstrip().startswith(">"):
                q.append(lines[i].lstrip()[1:].strip())
                i += 1
            b.quote(" ".join(q))
            continue
        m = BULLET.match(line)
        if m:
            flush()
            item_lines = [m.group(2)]
            i += 1
            while i < n and lines[i].strip() and not _starts_block(lines[i]):
                item_lines.append(lines[i].strip())
                i += 1
            b.bullet(len(m.group(1).expandtabs(4)) // 2, " ".join(item_lines))
            continue
        m = NUMBER.match(line)
        if m:
            flush()
            item_lines = [m.group(3)]
            i += 1
            while i < n and lines[i].strip() and not _starts_block(lines[i]):
                item_lines.append(lines[i].strip())
                i += 1
            b.numbered(len(m.group(1).expandtabs(4)) // 3, m.group(2), " ".join(item_lines))
            continue
        # Indented text after a list item (even across a blank line) continues that item.
        if b.item is not None and line.startswith("  ") and not para:
            cont = [line.strip()]
            i += 1
            while i < n and lines[i].strip() and not _starts_block(lines[i]):
                cont.append(lines[i].strip())
                i += 1
            p = b.paragraph(" ".join(cont), indent=b.item_indent)
            p.paragraph_format.space_before = Pt(0)
            continue
        para.append(line)
        i += 1
    flush()
    return b.save()


def _starts_block(line):
    """True if a line opens a new block rather than continuing the current one."""
    s = line.lstrip()
    return bool(HEADING.match(line) or FENCE.match(line) or s.startswith("|") or s.startswith(">")
                or RULE.match(line) or NUMBER.match(line) or BULLET.match(line))


def export_documents():
    produced, counts, warnings = set(), {"written": 0, "unchanged": 0}, []
    for src in DOC_SOURCES:
        if not src.exists():
            warnings.append(f"document source not found, skipped: {rel(src)}")
            continue
        raw = src.read_bytes()
        digest = hashlib.sha256(raw + CONVERTER_VERSION.encode()).hexdigest()
        out = DOCX_DIR / f"{src.stem}.docx"
        produced.add(out.resolve())
        if out.exists():
            try:
                if Document(str(out)).core_properties.comments == digest:
                    counts["unchanged"] += 1
                    print(f"  {'unchanged':<10} {rel(out)}")
                    continue
            except Exception:
                pass    # unreadable or foreign file: regenerate it
        text = raw.decode("utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.M)
        title = m.group(1).strip() if m else src.stem
        data = md_to_docx(text, title, rel(src), digest)
        replace_bytes(out, data)
        counts["written"] += 1
        print(f"  {'written':<10} {rel(out)}")
    warnings += remove_stale(DOCX_DIR, "*.docx", produced)
    return counts, warnings


# --------------------------------------------------------------------------------------------
# README
# --------------------------------------------------------------------------------------------

def write_readme(versions, indicator_records):
    vlines = "\n".join(f"  {name:<48} Version {versions.get(name) or '(not found)'}"
                       for name in WORKBOOKS)
    docs = "\n".join(f"  docx/{s.stem}.docx  <-  {rel(s)}" for s in DOC_SOURCES if s.exists())
    text = f"""EXPORTS - GENERATED FILES, DO NOT EDIT
=====================================

Everything in this folder is regenerated by Management/export_release.py, which
Management/finalise.py runs after every release (integrity check passed, dashboards rebuilt).
Editing a file here changes nothing upstream and is overwritten at the next release.

Sources of truth
  Workbooks  Data/canonical_files/*.xlsx
  Documents  the Markdown files listed below

Workbook versions in this export
{vlines}

Layout
  csv/<workbook>/<Sheet_Name>.csv   one file per sheet, exported as stored
  csv/_manifest.csv                 one row per CSV: workbook version, sheet, columns, data rows,
                                    record count and notes on sheet quirks
{docs}

Reading the CSVs
  * UTF-8 without a byte-order mark, comma-separated, RFC 4180 quoting, LF line endings.
    Cells can contain line breaks inside quotes.
  * Row 1 is the header on every sheet except each workbook's Changelog, which starts with a
    Workbook / Version / Last updated block and has its table further down.
  * Sheets are exported faithfully: section-banner rows and merged-cell remnants are kept.
  * Counting indicators: a row is an indicator record only if BOTH Record_ID and Indicator_Name
    are non-empty. The CBD GBF sheet has section-banner rows with a Record_ID but no
    Indicator_Name. Counted this way the indicators workbook holds {indicator_records} records;
    counting non-empty Record_ID alone overstates it.
  * Cross-references are bracketed codes, e.g. [LEG-NNN], [ORG-NNN], [IFW-NN]. Record_ID and
    Framework_ID key columns are never bracketed. Strip brackets before joining on IDs.
  * A cell whose hyperlink target is not already its text has the target appended as <url>.
"""
    return write_if_changed(EXPORT_DIR / "README.txt", text.encode("utf-8"))


# --------------------------------------------------------------------------------------------

def main():
    print("Workbooks -> CSV")
    versions, indicator_records, c_counts, w1 = export_workbooks()
    print("\nDocuments -> DOCX")
    d_counts, w2 = export_documents()
    state = write_readme(versions, indicator_records)
    print(f"\n  {state:<10} {rel(EXPORT_DIR / 'README.txt')}")
    print(f"\nCSV: {c_counts['written']} written, {c_counts['unchanged']} unchanged.  "
          f"DOCX: {d_counts['written']} written, {d_counts['unchanged']} unchanged.  "
          f"Indicator records: {indicator_records}.")
    for w in w1 + w2:
        print(f"WARNING: {w}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nFAILED: {type(e).__name__}: {e}")
        sys.exit(1)
