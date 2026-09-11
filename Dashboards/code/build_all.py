#!/usr/bin/env python3
"""
Master rebuild script — regenerates the dashboard HTML from the current canonical workbooks.
Rewritten 2026-07-15 for the versioned, repo-relative layout.

Layout assumed (repo root = grandparent of this Dashboards/code/ directory):
    Data/canonical_files/   uk_climate_nature_governance.xlsx, international_...xlsx, indicators_...xlsx
    Dashboards/code/        the build_*.py scripts (this file)
    Dashboards/             the generated dashboards (both HTML files MUST stay in one directory)

Builders run as subprocesses (each is self-contained and can also be run on its own):
    diagram  -> build_governance_diagram.py   -> Dashboards/governance_diagram_vN.html
               (reads all three workbooks directly; auto-detects canonical filenames)
    finder   -> build_indicator_finder.py     -> Dashboards/indicator_finder_v4.html (in place)
               (reads the indicators workbook; also re-points the finder's "diagram" deep-links
                at the newest governance_diagram_v*.html — so build the diagram FIRST)

Order matters: diagram before finder, so the finder links to the newest diagram.

NOTE: build_climate_heatmap.py is NOT built here — it is currently unmaintained (its
POLICY_CONTEXT is hardcoded and it depends on utils.py, whose paths are stale). Revive it
separately if needed.

The governance diagram's output filename carries a version integer (…_vN.html). When its
DESIGN or the workbook data changes materially, bump the integer inside
build_governance_diagram.py (the `out = …_vN.html` line) and archive the prior file to
Data/outdated_files/ — same discipline as the workbooks (see WORKBOOK_WRITE_PROTOCOL.md).

Usage:
    python3 build_all.py            # rebuild diagram then finder
    python3 build_all.py diagram    # just the governance diagram
    python3 build_all.py finder     # just the indicator finder
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../Dashboards/code
DASH_DIR = HERE.parent                           # .../Dashboards  (the generated HTML lives here)
ROOT = DASH_DIR.parent                           # repo root
CANON_DIR = ROOT / "Data" / "canonical_files"

# key -> (script, argv, cwd). cwd matters: the diagram builder resolves canonical files
# relative to the working directory, so it runs from Data/canonical_files/.
BUILDERS = {
    "diagram": ("build_governance_diagram.py",
                ["--outdir", str(DASH_DIR)], CANON_DIR),
    "finder":  ("build_indicator_finder.py",
                [], HERE),
}
ORDER = ["diagram", "finder"]   # diagram first so the finder links to the newest diagram


def run_builder(key):
    script, extra, cwd = BUILDERS[key]
    print(f"── {key}: {script} ─────────────────────────────")
    t0 = time.time()
    r = subprocess.run([sys.executable, str(HERE / script), *extra],
                       cwd=str(cwd))
    ok = r.returncode == 0
    print(f"  {'✓' if ok else '✗'} {key} ({time.time() - t0:.1f}s)\n")
    return ok


def main():
    args = [a for a in sys.argv[1:] if a != "all"]
    bad = [a for a in args if a not in BUILDERS]
    if bad:
        print(f"Unknown targets: {bad}. Valid: {sorted(BUILDERS)} or 'all'.")
        sys.exit(1)
    targets = [k for k in ORDER if not args or k in args]

    print("=" * 54)
    print(f"Dashboard rebuild — {', '.join(targets)}")
    print("=" * 54 + "\n")
    results = {k: run_builder(k) for k in targets}

    passed = sum(results.values())
    print("=" * 54)
    print(f"Done — {passed} succeeded, {len(results) - passed} failed")
    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
