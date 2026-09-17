---
name: queue-finds
description: Records policies, activities, bodies or indicators that a run found but the workbooks do not hold, as a candidate file for the next policy scan. Use at the end of every assessment, and whenever someone finds something relevant that is not catalogued.
---
# Queue the daggered finds

1. **Never edit `Data/pending_additions.md`.** Two runs writing to it at once would lose rows.
   Write one new file per run instead, with the SharePoint tool:
   `Data/pending_inbox/<YYYY-MM-DD>_<short run name>.md`
   If that name exists, add `-2`, `-3` and so on.
2. The file holds a heading line (date, who ran it, what the run was) and then one Markdown table
   with exactly these columns:
   `| Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution |`
3. One row per daggered item:
   - **Added** — today's date, `YYYY-MM-DD`.
   - **Found by** — the assessment field, or the scan block.
   - **Family** — `LEG`, `ORG`, `POL`, `INT-L`, `INT-O`, `INT-P`, `EU-L`, `IND` or `IFW`.
   - **Source** — a primary source URL, never secondary reporting.
   - **Climate input** — for indicators, does the measured quantity take a climate input: yes / no /
     unclear. A "no" does not disqualify it.
   - **Overlap** — only a record of the same kind counts (check `Record_Type` and `General_Type`);
     name the Record ID, or "none".
   - **Confidence** — what is unverified, not how strongly you feel.
   - **Status** — `pending`. **Resolution** — leave blank.
4. Before writing, check the item is not already in `Data/pending_additions.md` or in another file
   in `Data/pending_inbox/`. If it is, say so and do not duplicate it.
5. Tell the user the file name and the row count, and say that a maintainer merges the inbox into
   `Data/pending_additions.md` at the next triage.
6. If the write fails, put the table in your reply as a copy-paste block labelled for
   `Data/pending_additions.md`, and say the write failed. Losing the finds is not an option.

> **The `Data Dictionary` sheet documents the CURRENT schema only.** It carries no history.
> If a change adds, renames, re-scopes or removes a column, edit or delete that row in place —
> never append a row recording the change. Version history belongs in `Changelog`.
