---
name: release
description: Release after a workbook change — confirm the version/changelog/archive steps, run Management/finalise.py (integrity check → dashboard rebuild → Exports refresh), interpret the result and report what changed. Use when a workbook edit is finished, or to rebuild dashboards and exports.
argument-hint: "[--check]"
user-invocable: true
---
# Release

1. **Confirm the manual steps are done** (`WORKBOOK_WRITE_PROTOCOL.md` §5) for every workbook that
   changed:
   - `Changelog!B2` has been bumped;
   - a Changelog row has been added;
   - the prior file has been archived to `Data/outdated_files/` with the `_superseded_` name.

   If any is missing, say so and stop. Whether a change is material is the user's call, not yours.
2. Run `python3 Management/finalise.py`. With `--check`, run only the integrity check.
3. Interpret the exit code:
   - `0` — check clean, dashboards rebuilt, `Exports/` refreshed;
   - `1` — the integrity check failed and nothing was rebuilt. Quote the failing invariant and
     record IDs, and propose the workbook fix. Never modify `check_links.py` to pass;
   - `2` — the check passed but a build failed. Report the builder's error. Nothing was exported;
   - `3` — the check and build passed but the export failed. Re-run with
     `python3 Management/export_release.py` after fixing.
4. If the dashboard design or the data changed materially, remind the user of two things: bump
   `out = …_vN.html` in `build_governance_diagram.py`, and archive the prior HTML. If any governance
   chain behind a framework changed, check `FRAMEWORK_CTX`.
5. Summarise the changes (`git status --short`, if the folder is a git repository) and suggest a
   one-line commit message. Do not commit or push unless asked.
