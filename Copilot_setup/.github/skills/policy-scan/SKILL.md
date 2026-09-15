---
name: policy-scan
description: Run a policy scan block by block following Management/protocols/POLICY_SCAN_PROTOCOL.md §6 — establish the window, work the pending queue, scan ministerial statements, enumerate each watchlist source, title-sweep, screen, and write the triage note and queue rows before moving to the next block. Proposes only; never writes to a workbook.
argument-hint: "[block=<1-8>|next] [from=YYYY-MM-DD] [to=YYYY-MM-DD]"
user-invocable: true
---
# Policy scan

Read `Management/protocols/POLICY_SCAN_PROTOCOL.md` in full before starting — §2.0 and §6.0 above
all. This skill enforces the parts that most often go wrong.

## Set-up (first block of a scan only)

1. **Window.**
   - Read each workbook's version from `Changelog!B2`.
   - The window starts at the date of the newest `outputs_other/policy_scan_*.md` and ends today,
     unless the user gives dates.
   - If a triage note for this scan already exists, its coverage table is the resumption point:
     continue from the first block not marked complete.
2. **Queue first.** List every `pending` row in `Data/pending_additions.md`. These outrank
   watchlist finds.
3. Create or open `outputs_other/policy_scan_<YYYY-MM-DD>.md`.

## One block per invocation

Blocks are listed in protocol §6.0:

1. Statements and Hansard
2. Defra
3. Core agencies
4. Other departments
5. legislation.gov.uk
6. Devolved administrations
7. CCC and OEP
8. International

Run the requested block, or the next incomplete one.

- **Enumerate first, search second.** List what each source actually published inside the window,
  then screen that list. Never start from keyword searches for what you expect to find.
  - gov.uk: use the date-filtered search API from protocol §2.0, loaded **in the browser tool**
    (a plain fetch can drop the query string and return the whole corpus).
  - Verify that the filter held: a total in the hundreds of thousands means enumeration failed —
    that is not a null result.
  - Atom feeds cap at 20 entries. Use them only for low-volume publishers, and record how far back
    each one reached.
- **Title-sweep** every document type not screened in full (protocol §2.0c). Never exclude a type
  outright.
- **Screen** each candidate with protocol §3, questions 1–4, in order, and ask question 5
  (framework refreshes) once per scan. Include retirements.
- **Overlap** must be a record of the same kind: check `Record_Type` / `General_Type`. Watch for the
  broken-chain pattern, where the body and the statute are held but not the policy between them.
- **Write before moving on.**
  - Append this block's candidates to `Data/pending_additions.md`, with `Status` = `pending`.
  - Append the block's findings and a coverage line to the triage note. For each document type,
    state whether it was screened in full, title-swept, or not reached, with item counts.
- **Report nulls with their method**: "enumerated Defra 6 Jul – 2 Sep, 388 items, none in scope".
  If a source could not be enumerated, say so against that source.
- **Never mark a block complete to finish a scan.** Partial is acceptable; partial recorded as
  complete is not. Stop when the quality of the work would degrade.

## Never

- Write to a workbook. Approved items go to `/add-record` (the Curator agent).
- Delete a queue row.

## Reply

Report:
- the block covered and its coverage counts;
- the candidates found, with confidence;
- what was not reached;
- the next block to run.
