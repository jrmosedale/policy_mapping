---
name: orphan-codes
description: Find [CODE] cross-references that appear only in narrative prose fields and are not captured by any typed link column, using Data/code/orphan_codes.py, then propose which to promote. Proposes only.
argument-hint: ""
user-invocable: true
---
# Orphan narrative codes

1. From `Data/canonical_files/`, run `python3 ../code/orphan_codes.py`. The script reads the
   workbooks from, and writes its report to, the current directory.
2. Move `orphan_narrative_codes.md` and `orphan_narrative_codes.csv` to `outputs_other/`,
   overwriting the previous report. Never leave them beside the workbooks.
3. Compare with `outputs_other/ORPHAN_CODES_promotion_analysis.md` so that settled decisions and
   the outstanding judgement calls are not re-argued.
4. For each new orphan, propose one of:
   - **promote**, naming the typed column it belongs in (use the column → edge table in
     `WORKBOOK_WRITE_PROTOCOL.md` §7);
   - **leave as prose**, where it is only a mention;
   - **judgement call**.

   Present the proposals as a table and stop for approval. Approved promotions go through
   `/add-record`, as edits.
