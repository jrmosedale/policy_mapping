#!/usr/bin/env python3
"""
finalise.py — the release gate. Run this after any workbook edit, before calling a version done.

Two steps, in order, and the second only runs if the first passes:

  1. check_links.py   — five referential-integrity invariants across the three canonical
                        workbooks. This is the project's only automated gate.
  2. build_all.py     — regenerates the governance diagram, then the indicator finder.

Why a wrapper rather than two commands: the failure this catches is finalising a workbook
without rebuilding what depends on it, and the failure it prevents is rebuilding dashboards
from workbooks that do not pass the integrity check. Neither is caught by running the two
scripts by hand, because by hand they are two decisions and one of them gets skipped.

WHAT THIS DOES NOT DO — deliberately:
  * It does not bump a version integer. Whether a change is material enough to warrant a
    new `_vN` is a judgement call and stays human (WORKBOOK_WRITE_PROTOCOL.md §5, §7).
  * It does not archive superseded files, or write a changelog entry.
  * It regenerates dashboards IN PLACE. If the design or data change materially, bump the
    `out = ..._vN.html` line in build_governance_diagram.py and archive the prior HTML to
    Data/outdated_files/ yourself, then re-run this.

Usage:
    python3 Management/finalise.py            # check, then rebuild
    python3 Management/finalise.py --check    # integrity check only, no rebuild

Exit code 0 = both steps clean. 1 = integrity check failed (nothing was rebuilt).
2 = check passed but a build failed.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON_DIR = ROOT / "Data" / "canonical_files"
CHECK = ROOT / "Data" / "code" / "check_links.py"
BUILD_ALL = ROOT / "Dashboards" / "code" / "build_all.py"


def banner(text):
    print(f"\n{'=' * 70}\n{text}\n{'=' * 70}")


def main():
    ap = argparse.ArgumentParser(description="Integrity gate, then dashboard rebuild.")
    ap.add_argument("--check", action="store_true",
                    help="run the integrity check only; do not rebuild dashboards")
    args = ap.parse_args()

    for p in (CANON_DIR, CHECK, BUILD_ALL):
        if not p.exists():
            sys.exit(f"FATAL: expected path not found — {p}\n"
                     f"       finalise.py assumes the standard layout and lives in Management/.")

    banner("1/2  Integrity check — check_links.py")
    r = subprocess.run([sys.executable, str(CHECK)], cwd=str(CANON_DIR))
    if r.returncode != 0:
        print("\nFAILED: check_links.py reported issues. Nothing has been rebuilt.")
        print("Fix the workbooks and re-run. Do not finalise a version on a failing check.")
        return 1
    print("\nIntegrity check clean.")

    if args.check:
        print("--check given; stopping before the rebuild.")
        return 0

    banner("2/2  Dashboard rebuild — build_all.py")
    r = subprocess.run([sys.executable, str(BUILD_ALL)])
    if r.returncode != 0:
        print("\nFAILED: dashboard build did not complete. The workbooks are fine; "
              "the dashboards may now be stale or partly written.")
        return 2

    banner("Done")
    print("Workbooks pass all invariants and both dashboards are rebuilt from them.")
    print("Still yours to do, if the change was material:")
    print("  * bump the workbook version integer and write the Changelog entry")
    print("  * archive the superseded workbook to Data/outdated_files/")
    print("  * bump the dashboard _vN and archive the prior HTML, if the design changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
