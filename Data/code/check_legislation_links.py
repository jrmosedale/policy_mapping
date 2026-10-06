#!/usr/bin/env python3
"""check_legislation_links.py — does each Legislation record's Link open the instrument it names?

check_links.py validates bracketed codes; it cannot tell whether a URL resolves to the named Act
or SI. Two such errors were found on 6 October 2026 (LEG-034 opened the Bail and Release from
Custody (Scotland) Act 2023; LEG-013 opened the Arbitration Act 2025) and three more by a manual
audit (outputs_other/legislation_link_audit_2026-10-06.md). This script makes that audit
repeatable and puts it in the release gate (finalise.py step 3 of 5).

For every record on the UK workbook's `Legislation` sheet whose Link is on legislation.gov.uk, it
fetches the instrument's metadata (<base>/data.xml), reads dc:title, and compares it with the
record's Name. Links elsewhere (gov.uk guidance, bills.parliament.uk) are listed as not checkable.

Matching (deliberately lenient on presentation, strict on identity):
  * case, a leading "The", dashes, quotes and whitespace are normalised on both sides;
  * the record Name may carry trailing annotations the official title lacks —
    "(SI 2015/610)", "(NERC Act)", "(as amended)", "(s.26 – carbon lock-in)" — so a Name that
    begins with the official title counts as a match;
  * records whose Name is intentionally not the instrument title are listed in EXPECTED with the
    text the official title must contain instead, and the reason.
A title reported as revoked or repealed is a warning, not a failure: the record may be held
deliberately for history, but its Status should say so.

Politeness and offline use. legislation.gov.uk rate-limits (HTTP 429). Requests are spaced
(DELAY seconds) and results cached in `.legislation_title_cache.json` beside this script for
CACHE_DAYS, so a routine release re-fetches only new or changed links. If the site cannot be
reached at all, the check reports WARNING and exits 0 — an unreachable network must not block a
release made offline — and says how many links went unchecked. A title mismatch exits 1.

Usage (run from anywhere; the workbook path is resolved from this file's location):
    python3 Data/code/check_legislation_links.py              # check, using the cache
    python3 Data/code/check_legislation_links.py --refresh    # ignore the cache
    python3 Data/code/check_legislation_links.py --offline    # cache only, no network
    python3 Data/code/check_legislation_links.py --titles-json FILE   # titles supplied as {url: title} (testing)

Exit code 0 = no mismatches (warnings allowed). 1 = at least one Link opens a different instrument.
"""
import argparse, datetime, json, re, sys, time, unicodedata, urllib.error, urllib.request
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
UK = HERE.parent / "canonical_files" / "uk_climate_nature_governance.xlsx"
CACHE = HERE / ".legislation_title_cache.json"
CACHE_DAYS = 30
DELAY = 2.0          # seconds between live requests
TIMEOUT = 20
UA = "MetOffice-nature-climate-indicators link check (python urllib)"

# Records whose Name is not, and should not be, the official title of the linked instrument.
# Value: (text the official title must contain, reason).
EXPECTED = {
    "LEG-003": ("Carbon Budget Order", "Record covers the 1st–7th Carbon Budget Orders; the Link is one of them"),
    "LEG-047": ("Directive 2000/60/EC", "Record names the Water Framework Directive by its common name"),
}

DROP_SUFFIX = re.compile(r"\s*\((?:revoked|repealed)\)\s*$", re.I)


def norm(s):
    s = unicodedata.normalize("NFKC", str(s or ""))
    s = s.replace("–", "-").replace("—", "-").replace("’", "'").replace("‘", "'")
    s = re.sub(r"\s+", " ", s).strip().lower()
    s = re.sub(r"^the ", "", s)
    return s


def base_url(link):
    """legislation.gov.uk URL -> document base (no /contents, /enacted, /made, trailing slash)."""
    m = re.match(r"https?://(?:www\.)?legislation\.gov\.uk/(.+)$", link.strip())
    if not m:
        return None
    path = m.group(1).split("?")[0].split("#")[0].strip("/")
    path = re.sub(r"/(contents|introduction|data\.\w+)(/.*)?$", "", path)
    path = re.sub(r"/(enacted|made)$", "", path)
    return "https://www.legislation.gov.uk/" + path


def fetch_title(base):
    req = urllib.request.Request(base + "/data.xml", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        xml = r.read().decode("utf-8", "replace")
    m = re.search(r"<dc:title[^>]*>(.*?)</dc:title>", xml, re.S)
    if not m:
        raise ValueError("no dc:title in data.xml")
    title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    revoked = bool(re.search(r'\bStatus="(?:Revoked|Repealed)"', xml)) or bool(DROP_SUFFIX.search(title))
    return title, revoked


def matches(rid, name, title):
    t = norm(DROP_SUFFIX.sub("", title))
    if rid in EXPECTED:
        return norm(EXPECTED[rid][0]) in t
    n = norm(name)
    return n == t or n.startswith(t + " (") or n.startswith(t + ",")


def records():
    wb = openpyxl.load_workbook(UK, read_only=True, data_only=True)
    rows = list(wb["Legislation"].iter_rows(values_only=True))
    h = list(rows[0])
    i_id, i_name, i_link = h.index("Record_ID"), h.index("Name"), h.index("Link")
    return [(r[i_id], r[i_name], (r[i_link] or "").strip()) for r in rows[1:] if r[i_id]]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--refresh", action="store_true", help="ignore cached titles")
    ap.add_argument("--offline", action="store_true", help="use cached titles only; no network")
    ap.add_argument("--titles-json", help="JSON {url: title} used instead of the network (testing)")
    a = ap.parse_args()

    supplied = json.loads(Path(a.titles_json).read_text()) if a.titles_json else None
    try:
        cache = {} if a.refresh else json.loads(CACHE.read_text())
    except (FileNotFoundError, ValueError):
        cache = {}
    today = datetime.date.today()
    fresh = lambda e: (today - datetime.date.fromisoformat(e["checked"])).days <= CACHE_DAYS

    mismatch, revoked, unchecked, offsite, ok = [], [], [], [], 0
    network_down = a.offline
    fetched = 0
    for rid, name, link in records():
        base = base_url(link) if link else None
        if not base:
            offsite.append((rid, link or "(no link)"))
            continue
        title = is_revoked = None
        if supplied is not None:
            if base in supplied:
                title, is_revoked = supplied[base], bool(DROP_SUFFIX.search(supplied[base]))
        elif base in cache and fresh(cache[base]):
            title, is_revoked = cache[base]["title"], cache[base]["revoked"]
        elif not network_down:
            try:
                time.sleep(DELAY)
                title, is_revoked = fetch_title(base)
                cache[base] = {"title": title, "revoked": is_revoked, "checked": today.isoformat(),
                               "source": "data.xml"}
                fetched += 1
            except urllib.error.HTTPError as e:
                if e.code == 429:
                    print(f"  rate-limited at {rid}; stopping live requests for this run")
                    network_down = True
                unchecked.append((rid, f"HTTP {e.code}"))
                continue
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                print(f"  legislation.gov.uk unreachable ({getattr(e, 'reason', e)}); continuing from cache only")
                network_down = True
                unchecked.append((rid, "unreachable"))
                continue
            except ValueError as e:
                unchecked.append((rid, str(e)))
                continue
        if title is None:
            unchecked.append((rid, "not cached" if network_down or supplied is not None else "no title"))
            continue
        if matches(rid, name, title):
            ok += 1
        else:
            mismatch.append((rid, name, title, link))
        if is_revoked:
            revoked.append((rid, name, title))

    if fetched:   # never rewrite the cache from a run that fetched nothing (e.g. --refresh while offline)
        CACHE.write_text(json.dumps(cache, indent=1, sort_keys=True, ensure_ascii=False))

    print(f"Legislation links: {ok} match, {len(mismatch)} mismatch, {len(revoked)} revoked/repealed, "
          f"{len(unchecked)} unchecked, {len(offsite)} not on legislation.gov.uk")
    for rid, name, title, link in mismatch:
        print(f"[FAIL] {rid}: Name '{name}' but the Link opens '{title}'\n         {link}")
    for rid, name, title in revoked:
        print(f"[WARN] {rid}: '{title}' is marked revoked/repealed — check the record's Status")
    by_reason = {}
    for rid, why in unchecked:
        by_reason.setdefault(why, []).append(rid)
    for why, ids in by_reason.items():
        print(f"[WARN] not checked ({why}): {len(ids)} — {', '.join(ids)}")
    for rid, link in offsite:
        print(f"[INFO] {rid}: not checkable here — {link}")
    if mismatch:
        print("\nLINK CHECK FAILED: a Link opens a different instrument from the one the record names.")
        return 1
    print("\nLink check clean" + (" (with warnings)." if (revoked or unchecked) else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
