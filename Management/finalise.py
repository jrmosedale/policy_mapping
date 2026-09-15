#!/usr/bin/env python3
"""
finalise.py — the release gate. Run this after any workbook edit, before calling a version done.

Three steps, in order, each only if the one before it passed:

  1. check_links.py       — five referential-integrity invariants across the three canonical
                            workbooks. This is the project's only automated gate.
  2. build_all.py         — regenerates the governance diagram, then the indicator finder.
  3. export_release.py    — writes Exports/: one CSV per workbook sheet, the protocols, method,
                            user guide, handover and pending queue as .docx, and the YAML
                            templates as .txt, for tools that cannot read the workbooks, Markdown
                            or YAML directly (e.g. a Microsoft 365 Copilot agent).
                            Files are rewritten only when their content changes.

Why a wrapper rather than separate commands: the failure this catches is finalising a workbook
without rebuilding (and re-exporting) what depends on it, and the failure it prevents is
rebuilding dashboards from workbooks that do not pass the integrity check. Neither is caught by
running the scripts by hand, because by hand they are separate decisions and one gets skipped.

WHAT THIS DOES NOT DO — deliberately:
  * It does not bump a version integer. Whether a change is material enough to warrant a
    new `_vN` is a judgement call and stays human (WORKBOOK_WRITE_PROTOCOL.md §5, §7).
  * It does not archive superseded files, or write a changelog entry.
  * It never edits a source file. Exports/ is generated output; edit the workbooks and the
    Markdown, never the exports.
  * It regenerates dashboards IN PLACE. If the design or data change materially, bump the
    `out = ..._vN.html` line in build_governance_diagram.py and archive the prior HTML to
    Data/outdated_files/ yourself, then re-run this.

Usage:
    python3 Management/finalise.py            # check, then rebuild, then export
    python3 Management/finalise.py --check    # integrity check only, no rebuild or export
    python3 Management/export_release.py      # exports alone, e.g. after editing only a protocol

Exit code 0 = all three steps clean. 1 = integrity check failed (nothing was rebuilt).
2 = check passed but a build failed (nothing exported). 3 = check and build passed but the
export failed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON_DIR = ROOT / "Data" / "canonical_files"
CHECK = ROOT / "Data" / "code" / "check_links.py"
BUILD_ALL = ROOT / "Dashboards" / "code" / "build_all.py"
EXPORT = ROOT / "Management" / "export_release.py"


def banner(text):
    print(f"\n{'=' * 70}\n{text}\n{'=' * 70}", flush=True)


def main():
    ap = argparse.ArgumentParser(description="Integrity gate, then dashboard rebuild, then exports.")
    ap.add_argument("--check", action="store_true",
                    help="run the integrity check only; do not rebuild dashboards or export")
    args = ap.parse_args()

    for p in (CANON_DIR, CHECK, BUILD_ALL, EXPORT):
        if not p.exists():
            sys.exit(f"FATAL: expected path not found — {p}\n"
                     f"       finalise.py assumes the standard layout and lives in Management/.")

    banner("1/3  Integrity check — check_links.py")
    r = subprocess.run([sys.executable, str(CHECK)], cwd=str(CANON_DIR))
    if r.returncode != 0:
        print("\nFAILED: check_links.py reported issues. Nothing has been rebuilt.")
        print("Fix the workbooks and re-run. Do not finalise a version on a failing check.")
        return 1
    print("\nIntegrity check clean.")

    if args.check:
        print("--check given; stopping before the rebuild and export.")
        return 0

    banner("2/3  Dashboard rebuild — build_all.py")
    r = subprocess.run([sys.executable, str(BUILD_ALL)])
    if r.returncode != 0:
        print("\nFAILED: dashboard build did not complete. The workbooks are fine; "
              "the dashboards may now be stale or partly written. Nothing was exported.")
        return 2

    banner("3/3  Exports — export_release.py")
    r = subprocess.run([sys.executable, str(EXPORT)])
    if r.returncode != 0:
        print("\nFAILED: exports did not complete. Workbooks and dashboards are fine; Exports/ may "
              "be stale or partly written. Fix and re-run `python3 Management/export_release.py`.")
        return 3

    banner("Done")
    print("Workbooks pass all invariants, both dashboards are rebuilt from them, and Exports/ "
          "is current.")
    print("Still yours to do, if the change was material:")
    print("  * bump the workbook version integer and write the Changelog entry")
    print("  * archive the superseded workbook to Data/outdated_files/")
    print("  * bump the dashboard _vN and archive the prior HTML, if the design changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
