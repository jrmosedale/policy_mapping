/* =============================================================================
   indicator_export.js  —  PROTOTYPE v2  (Excel + CSV, single combined table)
   Client-side export of the currently-filtered indicator list.
   Zero external dependencies: no CDN, no bundled library. Works offline and
   from file:// . Designed to be pasted verbatim into indicator_finder_v4.html
   immediately before the closing </script>, so build_indicator_finder.py
   (which re-injects only `const INDICATORS`) preserves it on rebuild.

   v2 changes: Word output dropped; policy-context columns and the separate
   policy-context sheet dropped; one combined indicator table in both formats.

   Public entry point:  IndicatorExport.runExport(format, filename)
   Requires from the host page:  INDICATORS, applyFilters(), applySort(), F, CS_LBL
   ============================================================================= */
(function (global) {
'use strict';

/* ── 1. ZIP writer ─────────────────────────────────────────────────────────
   .xlsx is a ZIP of XML parts. Native CompressionStream('deflate-raw') where
   available (Chrome 80+, Edge 80+, Firefox 113+, Safari 16.4+), else STORED.  */

const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buf) {
  let c = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xFF] ^ (c >>> 8);
  return (c ^ 0xFFFFFFFF) >>> 0;
}

async function deflateRaw(bytes) {
  if (typeof CompressionStream === 'undefined') return null;
  try {
    const cs = new CompressionStream('deflate-raw');
    const stream = new Blob([bytes]).stream().pipeThrough(cs);
    return new Uint8Array(await new Response(stream).arrayBuffer());
  } catch (e) { return null; }
}

async function makeZip(files) {          // files: [{name, data:Uint8Array}]
  const enc = new TextEncoder();
  const chunks = [], central = [];
  let offset = 0;

  for (const f of files) {
    const nameBytes = enc.encode(f.name);
    const crc = crc32(f.data);
    const deflated = await deflateRaw(f.data);
    const useDeflate = deflated && deflated.length < f.data.length;
    const payload = useDeflate ? deflated : f.data;
    const method = useDeflate ? 8 : 0;

    const lh = new DataView(new ArrayBuffer(30));
    lh.setUint32(0, 0x04034B50, true); lh.setUint16(4, 20, true);
    lh.setUint16(6, 0x0800, true);                          // UTF-8 filename flag
    lh.setUint16(8, method, true);
    lh.setUint16(10, 0, true); lh.setUint16(12, 0, true);   // time / date
    lh.setUint32(14, crc, true);
    lh.setUint32(18, payload.length, true);
    lh.setUint32(22, f.data.length, true);
    lh.setUint16(26, nameBytes.length, true); lh.setUint16(28, 0, true);
    chunks.push(new Uint8Array(lh.buffer), nameBytes, payload);

    const ch = new DataView(new ArrayBuffer(46));
    ch.setUint32(0, 0x02014B50, true); ch.setUint16(4, 20, true);
    ch.setUint16(6, 20, true); ch.setUint16(8, 0x0800, true);
    ch.setUint16(10, method, true);
    ch.setUint16(12, 0, true); ch.setUint16(14, 0, true);
    ch.setUint32(16, crc, true);
    ch.setUint32(20, payload.length, true);
    ch.setUint32(24, f.data.length, true);
    ch.setUint16(28, nameBytes.length, true);
    ch.setUint32(42, offset, true);
    central.push(new Uint8Array(ch.buffer), nameBytes);

    offset += 30 + nameBytes.length + payload.length;
  }

  let cdSize = 0;
  for (const c of central) cdSize += c.length;
  const eocd = new DataView(new ArrayBuffer(22));
  eocd.setUint32(0, 0x06054B50, true);
  eocd.setUint16(8, files.length, true); eocd.setUint16(10, files.length, true);
  eocd.setUint32(12, cdSize, true); eocd.setUint32(16, offset, true);

  return new Blob([...chunks, ...central, new Uint8Array(eocd.buffer)]);
}

const U8 = s => new TextEncoder().encode(s);
const X  = s => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;').replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '');

/* ── 2. Column schema ──────────────────────────────────────────────────────
   ONE definition, shared by Excel and CSV. Order follows the right-hand detail
   panel. Policy-context fields are deliberately excluded (v2).               */

const CSL_LOCAL = ['none', 'low', 'medium', 'high'];
const csLabel = n => (typeof CS_LBL !== 'undefined' ? CS_LBL : CSL_LOCAL)[n] || '';

const COLS = [
  { h: 'Record ID',         w: 13, get: r => r.id },
  { h: 'Indicator name',    w: 48, get: r => r.name, wrap: 1 },
  { h: 'Framework',         w: 10, get: r => r.fw },
  { h: 'Framework (full)',  w: 34, get: r => r.fw_full, wrap: 1 },
  { h: 'NCF category',      w: 16, get: r => r.ncf },
  { h: 'Geographic scope',  w: 18, get: r => r.scope },
  { h: 'Units / measure',   w: 32, get: r => r.units, wrap: 1 },
  { h: 'Policy goal',       w: 46, get: r => r.goal, wrap: 1 },
  { h: 'Data source',       w: 36, get: r => r.datasrc, wrap: 1 },
  { h: 'Climate score',     w:  9, get: r => r.cs, num: 1, csCol: 1 },
  { h: 'Climate relevance', w: 14, get: r => csLabel(r.cs) },
  { h: 'Climate rationale', w: 64, get: r => r.rat, wrap: 1 },
];

/* ── 3. Export metadata ────────────────────────────────────────────────── */

function filterSummary() {
  const sortSel = document.getElementById('sort-sel');
  const sortTxt = sortSel ? sortSel.options[sortSel.selectedIndex].text : '';
  const ctxLbl = { all: 'All', monitoring: 'Designated monitoring only', relevant: 'Policy-relevant only' };
  return [
    ['Sector',                 F.sector === 'all' ? 'All sectors' : F.sector],
    ['NCF category',           F.ncf    === 'all' ? 'All' : F.ncf],
    ['Framework',              F.fw     === 'all' ? 'All' : F.fw],
    ['Climate score',          F.cs ? `≥ ${F.cs} (${csLabel(F.cs)}+)` : 'Any (0+)'],
    ['Geographic scope',       F.scope  === 'all' ? 'All' : F.scope],
    ['Policy-context filter',  ctxLbl[F.ctxf] || F.ctxf],
    ['Free-text search',       F.search ? `"${F.search}"` : '(none)'],
    ['Sort order',             sortTxt],
  ];
}

function stamp() {
  const d = new Date(), p = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`;
}
const PROVENANCE = 'indicators_climate_nature.xlsx (v10) via indicator_finder_v4.html';

/* ── 4. CSV ────────────────────────────────────────────────────────────── */

function buildCSV(rows) {
  const q = v => {
    const s = String(v == null ? '' : v);
    return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  };
  const L = [];
  L.push(q('# UK Climate–Nature Indicator Finder — indicator export'));
  L.push([q(`# Exported ${stamp()}`), q(`${rows.length} of ${INDICATORS.length} indicators`)].join(','));
  L.push(q('# Filters: ' + filterSummary().map(f => `${f[0]}=${f[1]}`).join('; ')));
  L.push(q('# Source: ' + PROVENANCE));
  L.push('');
  L.push(COLS.map(c => q(c.h)).join(','));
  rows.forEach(r => L.push(COLS.map(c => q(c.get(r))).join(',')));
  return new Blob(['﻿' + L.join('\r\n')], { type: 'text/csv;charset=utf-8' });
}

/* ── 5. XLSX ───────────────────────────────────────────────────────────── */

const COL_LETTER = n => { let s = ''; n++; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = (n - m - 1) / 26; } return s; };

const STYLES_XML = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="5">
<font><sz val="10"/><name val="Calibri"/></font>
<font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>
<font><sz val="9.5"/><name val="Calibri"/></font>
<font><b/><sz val="16"/><color rgb="FF2F5D50"/><name val="Calibri"/></font>
<font><b/><sz val="9.5"/><name val="Calibri"/></font>
</fonts>
<fills count="7">
<fill><patternFill patternType="none"/></fill>
<fill><patternFill patternType="gray125"/></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FF2F5D50"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFEFEEE9"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFF6E7C8"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFF2D2AE"/><bgColor indexed="64"/></patternFill></fill>
<fill><patternFill patternType="solid"><fgColor rgb="FFF3C0BC"/><bgColor indexed="64"/></patternFill></fill>
</fills>
<borders count="2"><border/><border><left/><right/><top/><bottom style="thin"><color rgb="FFD8D5CC"/></bottom><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="9">
<xf xfId="0" numFmtId="0" fontId="0" fillId="0" borderId="0"/>
<xf xfId="0" numFmtId="0" fontId="1" fillId="2" borderId="0" applyFont="1" applyFill="1" applyAlignment="1"><alignment vertical="center" wrapText="1"/></xf>
<xf xfId="0" numFmtId="0" fontId="2" fillId="0" borderId="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top"/></xf>
<xf xfId="0" numFmtId="0" fontId="2" fillId="0" borderId="1" applyFont="1" applyBorder="1" applyAlignment="1"><alignment vertical="top" wrapText="1"/></xf>
<xf xfId="0" numFmtId="0" fontId="4" fillId="3" borderId="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf xfId="0" numFmtId="0" fontId="4" fillId="4" borderId="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf xfId="0" numFmtId="0" fontId="4" fillId="5" borderId="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf xfId="0" numFmtId="0" fontId="4" fillId="6" borderId="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="top"/></xf>
<xf xfId="0" numFmtId="0" fontId="3" fillId="0" borderId="0" applyFont="1"/>
</cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>`;

const S = { HDR: 1, BODY: 2, BODY_WRAP: 3, CS: [4, 5, 6, 7], TITLE: 8 };

function cellXml(ref, cell) {
  const s = cell.s ? ` s="${cell.s}"` : '';
  if (cell.n) return `<c r="${ref}"${s} t="n"><v>${Number(cell.v) || 0}</v></c>`;
  if (cell.v === '' || cell.v == null) return `<c r="${ref}"${s}/>`;
  return `<c r="${ref}"${s} t="inlineStr"><is><t xml:space="preserve">${X(cell.v)}</t></is></c>`;
}

function sheetXml(grid, colWidths, freeze, autofilter) {
  const cols = colWidths.length
    ? '<cols>' + colWidths.map((w, i) => `<col min="${i + 1}" max="${i + 1}" width="${w}" customWidth="1"/>`).join('') + '</cols>' : '';
  const rows = grid.map((row, ri) =>
    `<row r="${ri + 1}"${ri === 0 && freeze ? ' ht="30" customHeight="1"' : ''}>` +
    row.map((cell, ci) => cell == null ? '' : cellXml(COL_LETTER(ci) + (ri + 1), cell)).join('') + '</row>').join('');
  const pane = freeze
    ? `<sheetView workbookViewId="0"><pane xSplit="2" ySplit="1" topLeftCell="C2" activePane="bottomRight" state="frozen"/></sheetView>`
    : `<sheetView workbookViewId="0"/>`;
  const af = autofilter ? `<autoFilter ref="${autofilter}"/>` : '';
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetViews>${pane}</sheetViews>${cols}<sheetData>${rows}</sheetData>${af}</worksheet>`;
}

async function buildXLSX(rows) {
  /* Sheet 1 — Export info */
  const info = [
    [{ v: 'UK Climate–Nature Indicator Finder', s: S.TITLE }],
    [{ v: 'Indicator export' }], [],
    [{ v: 'Exported', s: S.BODY }, { v: stamp(), s: S.BODY }],
    [{ v: 'Indicators in export', s: S.BODY }, { v: rows.length, n: 1, s: S.BODY }],
    [{ v: 'Indicators in catalogue', s: S.BODY }, { v: INDICATORS.length, n: 1, s: S.BODY }],
    [{ v: 'Columns', s: S.BODY }, { v: COLS.length, n: 1, s: S.BODY }],
    [{ v: 'Source', s: S.BODY }, { v: PROVENANCE, s: S.BODY }],
    [],
    [{ v: 'FILTERS APPLIED', s: S.HDR }, { v: '', s: S.HDR }],
  ].concat(filterSummary().map(f => [{ v: f[0], s: S.BODY }, { v: f[1], s: S.BODY }]));

  /* Sheet 2 — Indicators (single combined table) */
  const g2 = [COLS.map(c => ({ v: c.h, s: S.HDR }))];
  rows.forEach(r => g2.push(COLS.map(c => {
    const v = c.get(r);
    if (c.csCol) return { v, n: 1, s: S.CS[Math.max(0, Math.min(3, r.cs))] };
    return { v, n: c.num ? 1 : 0, s: c.wrap ? S.BODY_WRAP : S.BODY };
  })));

  const sheets = [
    { name: 'Export info', xml: sheetXml(info, [26, 60], false, null) },
    { name: 'Indicators',  xml: sheetXml(g2, COLS.map(c => c.w), true,
                                         `A1:${COL_LETTER(COLS.length - 1)}${rows.length + 1}`) },
  ];

  const ct = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
${sheets.map((s, i) => `<Override PartName="/xl/worksheets/sheet${i + 1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>`).join('')}
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>`;
  const rels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>`;
  const wb = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>
${sheets.map((s, i) => `<sheet name="${X(s.name)}" sheetId="${i + 1}" r:id="rId${i + 1}"/>`).join('')}
</sheets></workbook>`;
  const wbRels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
${sheets.map((s, i) => `<Relationship Id="rId${i + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet${i + 1}.xml"/>`).join('')}
<Relationship Id="rId${sheets.length + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>`;

  return makeZip([
    { name: '[Content_Types].xml',        data: U8(ct) },
    { name: '_rels/.rels',                data: U8(rels) },
    { name: 'xl/workbook.xml',            data: U8(wb) },
    { name: 'xl/_rels/workbook.xml.rels', data: U8(wbRels) },
    { name: 'xl/styles.xml',              data: U8(STYLES_XML) },
    ...sheets.map((s, i) => ({ name: `xl/worksheets/sheet${i + 1}.xml`, data: U8(s.xml) })),
  ]);
}

/* ── 6. Save ───────────────────────────────────────────────────────────── */

async function saveBlob(blob, filename, ext, desc, mime) {
  if (global.showSaveFilePicker) {                 // Chrome / Edge: true Save-As dialog
    try {
      const handle = await global.showSaveFilePicker({
        suggestedName: filename + ext,
        types: [{ description: desc, accept: { [mime]: [ext] } }],
      });
      const w = await handle.createWritable();
      await w.write(blob); await w.close();
      return handle.name;
    } catch (e) { if (e.name === 'AbortError') return null; }
  }
  const a = document.createElement('a');           // Firefox / Safari fallback
  a.href = URL.createObjectURL(blob);
  a.download = filename + ext;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
  return filename + ext;
}

/* ── 7. Suggested filename ─────────────────────────────────────────────── */

function suggestName() {
  const bits = ['indicators'];
  if (F.sector !== 'all') bits.push(F.sector.replace(/[^A-Za-z]+/g, ''));
  if (F.fw     !== 'all') bits.push(F.fw);
  if (F.ncf    !== 'all') bits.push(F.ncf.replace(/[^A-Za-z]+/g, ''));
  if (F.scope  !== 'all') bits.push(F.scope);
  if (F.cs) bits.push('cs' + F.cs + 'plus');
  if (F.search) bits.push(F.search.replace(/[^A-Za-z0-9]+/g, '-').slice(0, 20));
  bits.push(new Date().toISOString().slice(0, 10));
  return bits.join('_');
}

/* ── 8. Public API ─────────────────────────────────────────────────────── */

async function runExport(format, filename) {
  const rows = applySort(applyFilters());
  const spec = {
    csv:  { ext: '.csv',  mime: 'text/csv', desc: 'CSV file',
            make: () => buildCSV(rows) },
    xlsx: { ext: '.xlsx', mime: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            desc: 'Excel workbook', make: () => buildXLSX(rows) },
  }[format];
  const blob = await spec.make();
  return { name: await saveBlob(blob, filename, spec.ext, spec.desc, spec.mime), n: rows.length };
}

global.IndicatorExport = { runExport, buildCSV, buildXLSX, suggestName, COLS,
                           _internal: { makeZip, crc32 } };

})(typeof window !== 'undefined' ? window : globalThis);

if (typeof module !== 'undefined') module.exports = globalThis.IndicatorExport;
