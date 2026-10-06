---
name: triage-pending
description: Work the candidate queue in Data/pending_additions.md — screen each pending row against POLICY_SCAN_PROTOCOL.md §3, check for same-kind overlap in the workbooks, and present a decision table for approval. Records approved decisions in the queue; hands approved additions to /add-record.
argument-hint: "[rows or filter, e.g. family=POL, found-by=ocean heatwaves]"
user-invocable: true
---
# Triage the pending queue

1. Read `Data/pending_additions.md`: its header, column notes and every row. Select the `pending`
   rows, or those matching the user's filter.
2. Status vocabulary: use the values defined in the file header (`pending`, `added`, `rejected`,
   `duplicate`). If rows use other values (for example `add`, `defer`), treat them as
   decided-but-not-written, and flag the vocabulary inconsistency once rather than rewriting it.
3. For each row:
   - **Screen** it with `POLICY_SCAN_PROTOCOL.md` §3: does it introduce or retire a record? Is it
     in scope? For indicators, does the measured quantity take a climate input?
   - **Check overlap** in the workbooks — or `Exports/csv/` — by name, acronym and URL. Only a
     record of the same kind counts: check `Record_Type` / `General_Type`.
   - **Re-verify** the source is primary and current. Note what is still unverified.
   - Note whether it needs a **schema decision** (a new vocabulary value, a missing parent
     `LEG` / `ORG`) or a **per-nation** split.
4. Present one table: `Row | Proposed decision (add / reject / duplicate / defer) | Reason | Overlap | Blockers | Confidence`.
   Stop for approval.
5. After approval, update `Status` and `Resolution` in place. Record rejections with their reason;
   never delete a row. Hand approved additions to `/add-record`.
