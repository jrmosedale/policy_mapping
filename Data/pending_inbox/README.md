# Pending inbox — one file per run

Candidate records found by an assistant that cannot safely edit `Data/pending_additions.md`.

**Why this folder exists.** The Copilot Studio agent writes to SharePoint through a connector that
replaces a whole file. If two runs appended to `pending_additions.md` at the same time, one set of
rows would be lost silently. So each run writes its own file here instead, and nothing is
overwritten.

**File name:** `<YYYY-MM-DD>_<short run name>.md` — e.g. `2026-09-14_soil-moisture-applied.md`.

**Contents:** a heading line (date, who ran it, what the run was), then one Markdown table with the
same columns as the Queue table in `Data/pending_additions.md`:

`| Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution |`

Rows arrive with `Status` = `pending` and an empty `Resolution`.

**Merging.** At the start of each triage — `Management/protocols/POLICY_SCAN_PROTOCOL.md` §5 — a
maintainer appends every row here to the Queue table in `Data/pending_additions.md`, drops exact
duplicates, then deletes the merged file. Merge before working the queue, so the queue stays the
single place decisions are recorded.

**This folder is not the queue.** Nothing here has been screened. Decisions are only recorded in
`Data/pending_additions.md`.
