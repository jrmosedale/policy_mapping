# Canonical files — a short guide

The three Excel workbooks in `Data/canonical_files/` are the single source of truth for this project.
The dashboards, the CSV and Word exports and the assessment toolkit's policy context are all generated
from them. This guide says what each holds, how versions and archives work, and the rules for reading
and changing them.

Current version numbers and record counts are deliberately not given here, because they change. Read
them from each workbook's `Changelog` sheet (cell `B2` holds the version) or from
`Exports/csv/_manifest.csv`, which is regenerated at every release.

## The three workbooks

| File | Holds | Main record sheets |
|---|---|---|
| `uk_climate_nature_governance.xlsx` | UK legislation, public bodies, and policies and activities across the four administrations | `Legislation` (`LEG-`), `Public Bodies` (`ORG-`), `Policies & Activities` (`POL-`) |
| `international_climate_nature_governance.xlsx` | Conventions and treaties, EU legislation, international bodies and international policies | `Conventions & Treaties` (`INT-L-`), `EU Legislation` (`EU-L-`), `Associated Bodies` (`INT-O-`), `Intl Policies & Activities` (`INT-P-`) |
| `indicators_climate_nature.xlsx` | Indicator frameworks and their indicators, with a climate score for each indicator | `Indicator Framework` (`IFW-`, one row per framework) and the framework indicator sheets (a sheet can hold more than one framework) |

Every workbook also has:

- **`Data Dictionary`** — the current schema: one row per column, its meaning, and for `Controlled`
  columns the permitted values. It records no history.
- **`Changelog`** — the version number in `B2`, the last-updated date, and one row per version saying
  what changed and why.

The two governance workbooks also have a **`Cross-Reference Index`**. It is derived: it is regenerated
from the record sheets at every release, and any hand edit to it is overwritten. The indicators
workbook also has lookup sheets (GBF targets, SDG goals and targets) and legends for the climate score
and the Natural Capital Framework categories.

## How the workbooks link together

Records refer to one another with bracketed codes: `[LEG-004]`, `[ORG-001]`, `[IFW-01]`, `[INT-L-007]`.
The brackets are what makes a reference machine-readable; an unbracketed code is invisible to the
integrity check and the dashboards. The one exception is the `Record_ID` / `Framework_ID` key column,
which is never bracketed.

Links between UK and international records must run both ways: a UK record's `Intl_Links` and the
international record's `UK_Links` must name each other. The integrity check enforces this.

## Filenames, versions and archives

- **Filenames never change.** No version number appears in a filename, so every script, protocol and
  dashboard can rely on the same three names.
- **The version lives inside the workbook**, in `Changelog!B2`. It goes up by one for each released
  change, with a matching `Changelog` row.
- **The previous file is archived before it is overwritten**, to `Data/outdated_files/` as
  `<name>_v<oldVersion>_superseded_<YYYY-MM-DD>.xlsx`. Archives are never edited, overwritten or
  reused. `Data/outdated_files/` is not in git; git history also holds every committed version.

## Reading the workbooks

- **There are no formula cells**, and there must never be any. Read with openpyxl
  `load_workbook(..., data_only=True)` or pandas; every value is static.
- **Counting indicators:** a row is an indicator record only if both `Record_ID` and `Indicator_Name`
  are filled. Some sheets carry section-banner rows with a `Record_ID` but no name; counting `Record_ID`
  alone overstates the total.
- **Prefer the exports for quick reading.** `Exports/csv/<workbook>/<Sheet_Name>.csv` holds one CSV per
  sheet, regenerated at every release. They are read-only copies; editing them changes nothing.
- **Some IDs are retired and never reused.** The list is `RETIRED` in `Data/code/check_links.py`.

## Changing the workbooks

Every change follows `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md`. In outline:

1. **Propose** the change as a table — every new value, every edited cell, every record it touches —
   and get it approved before writing anything.
2. **Verify** each value against a primary source, and open every link you write to confirm it is the
   instrument or document the record names. Leave a cell blank rather than guess.
3. **Write** with openpyxl by appending rows; never insert rows or columns in the middle of a sheet,
   because that silently moves hyperlinks and breaks the row shading. New controlled-vocabulary terms
   need approval first.
4. **Bump the version, add a `Changelog` row and archive** the previous file.
5. **Run `python3 Management/finalise.py`.** It regenerates the derived index, runs the integrity check
   and the legislation link-title check, and only if both pass rebuilds the dashboards and exports.
   A version is not done until it exits 0.

## Do not

- rename, move or copy the canonical files elsewhere and edit the copy;
- add formulas, merged cells, or columns in the middle of a sheet;
- edit the `Cross-Reference Index` or anything in `Exports/` by hand;
- reuse a retired ID, or bracket a key column;
- weaken a check in `Data/code/` so that a workbook passes.

If the folder is synced by OneDrive, set it to keep files on this device: a cloud-only placeholder
cannot be read by the scripts.
