---
name: sanity-check-inputs
description: Confirms an assessment has everything it needs before the research starts — field, mode, bibliography, flagship tool and workbook versions. Use at the start of any assessment request, or when a user asks what you need from them.
---
# Sanity-check the inputs

1. Check and report, in one short block:
   - **Research field** — stated?
   - **Mode** — applied or gap? If unstated, infer it from the request and say which you inferred
     and why.
   - **Bibliography** — uploaded, or present in `PA_toolkit/bibliographies/`? Name it. In gap mode
     it should be external literature, not Met Office publications — flag it if it looks wrong for
     the mode.
   - **Flagship Met Office tool or URL** — given, or none.
   - **Output basename.**
2. Report the version of each workbook you will use, read from the `Changelog` sheet, cell B2, and
   the date of the newest file in `Data/pending_inbox/`, if any.
3. Say whether web access is working, with one check against a gov.uk page. If it is not, warn that
   every claim, date and URL will be marked unverified and the assessment will be weaker.
4. Ask once, in a single message, for anything missing. Then hand over to `run-assessment`.
