---
name: Workbooks and data
description: Rules for anything under Data/ — the canonical workbooks, the archive, the pending queue and the integrity tools.
applyTo: "Data/**"
---
# Working in Data/

- The three files in `Data/canonical_files/` are the single source of truth. Change them only by
  following `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` end to end, and only after the user
  has approved a proposal table (use `/add-record`).
- Run `python3 Management/finalise.py --check` before writing, to confirm a clean baseline.
- Filenames are stable. Never add a version suffix to a live workbook: the version lives in
  `Changelog!B2`.
- After writing, in this order: bump `Changelog!B2` by one; append one Changelog row
  (`Version | Date (YYYY-MM-DD) | Summary | Author`); archive the prior canonical file to
  `Data/outdated_files/<name>_v<oldVersion>_superseded_<YYYY-MM-DD>.xlsx`; then run
  `python3 Management/finalise.py`.
- openpyxl mechanics:
  - load twice when hyperlinks matter — `data_only=True` for values, a plain load for
    `.hyperlink.target`;
  - never `insert_rows` on a striped sheet; for structural change rewrite the region and re-stripe
    by final row index (even `FFFDFEFE`, odd `FFF4F6F7`);
  - append trailing rows or columns only, copying font, fill, border, alignment and number format
  - **`insert_cols` / `insert_rows` do not move hyperlinks** — the link stays anchored to the old
    coordinate and reappears in the new column. Append unless the sheet is known hyperlink-free.
    In the indicators workbook the only hyperlinks are `CCC Indicators` and `JNCC UK Biodiversity
    Indicators` cells `S15`, `S46`, `S64`.
  - **writes to a merged cell are discarded on save** — unmerge before rewriting a sheet
  - both of the above fail **silently**: the file saves without error. Always verify the result
    against the live headers after any structural edit.
    from a same-parity row or the sibling cell;
  - exclude `Record_ID` / `Framework_ID` from any bracketing or regex pass;
  - never write a formula.
- `Data/outdated_files/` is an archive. Never edit or overwrite a file there; never reuse a
  superseded name.
- `Data/pending_additions.md` is append-only. Add rows at the end of the Queue table using its
  columns. Resolve a row by changing `Status` and filling `Resolution`, never by deleting it. Use the
  `Status` values defined in the file's header; if you meet values that are not defined there, flag
  the inconsistency rather than normalising it silently.
- `Data/CANONICAL_FILES_GUIDE.md` is the short orientation to the workbooks; the write protocol governs.
- `Data/code/check_links.py` and `Data/code/check_legislation_links.py` are the automated gate.
  Changing either needs explicit approval, and weakening an invariant or the title match so that a
  check passes is never acceptable. A record deliberately named otherwise than its instrument goes in
  the link checker's `EXPECTED` table, with its reason, after approval.
- When you write a `Link`, open it and confirm the page is the instrument the record names.
- `Data/code/orphan_codes.py` reads the workbooks from, and writes its report to, the current
  directory. Run it from `Data/canonical_files/` (`python3 ../code/orphan_codes.py`), then move
  `orphan_narrative_codes.md` and `.csv` to `outputs_other/` — never leave them beside the
  workbooks.
