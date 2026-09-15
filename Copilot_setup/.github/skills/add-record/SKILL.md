---
name: add-record
description: Add, amend or retire records in the canonical workbooks by following Management/protocols/WORKBOOK_WRITE_PROTOCOL.md — propose, verify, link map, write, version/changelog/archive, then the finalise.py gate. Use for any change to Data/canonical_files/*.xlsx, including approved rows from Data/pending_additions.md.
argument-hint: "<what to add/amend/retire, or pending-queue row(s) to write>"
user-invocable: true
---
# Change a workbook record

Read `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` in full first. This skill is its checklist,
not a replacement for it.

## Stage A — propose (write nothing)

1. Run `python3 Management/finalise.py --check`. If it fails, stop and report: never write onto a
   failing baseline.
2. Identify the target workbook and sheet, and read that sheet's columns and the `Data Dictionary`
   entries for them.
3. Allocate IDs: the next free integer in the family. Never reuse a retired ID (`POL-023`,
   `POL-024`).
4. Draft a **proposal table**:
   - new records: the ID, `Name` and every column value;
   - edits: the exact cells, as old → new.
   Leave a cell blank rather than guess. Bracket every cross-reference code.
5. Draft the **link map** (protocol §3): every other record and workbook the change touches,
   including reciprocal links. UK ↔ international links are mandatory in both directions.
6. Flag, rather than absorb:
   - any new controlled-vocabulary value (`Policy_Sector`, `General_Type`, …) as a schema
     decision;
   - any per-nation question — is this one UK record, or four national ones?

## Stage B — verify

For each factual value, confirm it against a primary source: gov.uk, legislation.gov.uk, gov.scot,
gov.wales, daera-ni.gov.uk, or the body or treaty's own site. Record the source URL and a
confidence level. Anything you cannot verify stays blank and is listed.

If the Verifier agent is available, hand the proposal to it. Then **stop and present the proposal,
the link map and the verification table for approval.** A concise approval ("go ahead") authorises
the full scope as described.

## Stage C — write (only after approval)

1. Load twice: `data_only=True` for values, and a plain load for hyperlinks.
2. Append trailing rows only, styled from a same-parity row. Never `insert_rows` on a striped sheet;
   for structural change, rewrite the region and re-stripe by row index. Exclude
   `Record_ID` / `Framework_ID` from any regex pass. Write no formulas.
3. Apply every reciprocal touch in the link map, including the `Cross-Reference Index`.
4. Bump `Changelog!B2`, and append one `Version | Date | Summary | Author` row.
5. Archive the prior canonical file to
   `Data/outdated_files/<name>_v<oldVersion>_superseded_<YYYY-MM-DD>.xlsx`, then save under the
   canonical filename.
6. Run `python3 Management/finalise.py`. It must exit 0. On exit 1, fix the workbook — never the
   checker.
7. If the change touches a framework's governance chain, check `FRAMEWORK_CTX` in
   `Dashboards/code/build_indicator_finder.py` and say whether it needs updating.
8. If the records came from `Data/pending_additions.md`, resolve those rows: set `Status` and put
   the new Record ID in `Resolution`.

## Reply

Report:
- what was written (IDs and sheets);
- the version bump and archive filename;
- the gate result;
- anything left blank or flagged for a decision.
