# Dashboards — user guide

Two interactive dashboards sit in `Dashboards/`. Both are single HTML files that open in any modern
browser, offline, straight from the folder — nothing to install and no internet connection needed.

| Dashboard | File | Use it to |
|---|---|---|
| **Indicator Finder** | `indicator_finder_v4.html` | find environmental indicators, see how far each depends on climate data, see the policy that uses it, and export a list |
| **Governance Diagram** (Relationship Explorer) | `governance_diagram_v<N>.html` | see how legislation, public bodies, policies, international instruments and indicator frameworks link together |

**Keep the two files in the same folder.** The Finder's "⬡ diagram" links open the Diagram by its file
name; if the files are separated those links stop working, without any error. Copy or email both
together.

Each dashboard has an **ⓘ Help** button with a fuller explanation than this guide.

## Where the data comes from, and how current it is

Both dashboards are generated from the three canonical workbooks in `Data/canonical_files/` and are
rebuilt at every release (`Management/finalise.py`). They show the workbooks as they stood at that
release, never anything newer. The Finder's footer lists the version of each workbook it was built
from. To change what a dashboard shows, change the workbook and release — never edit the HTML data.

## Indicator Finder

**What it holds.** A catalogue of indicators from UK and international frameworks (the Framework
filter lists them). Each indicator has a sector, Natural Capital Framework category, geographic scope,
units, data source, the policy goal it informs, and a **climate score**.

**Finding indicators.**

- **Filters** (left): sector, NCF category, framework, climate score, geographic scope and policy-context
  type. Sectors are the same 14 classes the Diagram uses, so the two can be filtered in step.
- **Search** (free text) across name, framework, type, goal and category.
- **Sort** (top of the list) by climate score, name or framework.

**The climate score (0–3)** says how far an indicator's published value depends on weather and climate
data — whether such data enter its calculation, and whether year-to-year weather moves it. It is
**not** a measure of relevance to climate policy: heat-pump installations are *about* climate but score
0, because no climate data enter them.

- To find indicators **about** climate, use **Sector → Climate**.
- To find indicators that **climate or weather data would move**, use **Climate score ≥ 2**; for those
  built directly on climate data, **≥ 3**.
- A hatched badge means *not assessed*; it never passes a score filter.

Each indicator's reason for its score is shown in its detail panel. The full method is in
`outputs_other/CLIMATE_SCORE_METHOD.md`.

**Policy context.** Click an indicator to open its detail panel on the right, listing the legislation,
public bodies and policies its framework informs. A filled marker means a *designated monitoring*
relationship (the framework formally reports against that instrument); an open marker means
*policy-relevant*. Each item offers **↗ source** (the official page) and **⬡ diagram** (opens that record
in the Governance Diagram in a new tab). The links belong to the indicator's framework, so every
indicator from one framework shows the same context.

**Exporting.** **⤓ Export** (top right) saves the indicators currently listed — after filters, search
and sort — so filter first to export a subset.

- **Excel** — three sheets: export information (date, counts and the filters applied), the indicators,
  and lookups for framework codes and the climate-score scale.
- **CSV** — one table; the lookups sit in a comment header, so skip the first 24 lines when reading it
  into R or Python.
- Columns: ID, name, framework, sector, NCF category, scope, units, policy goal (with GBF and SDG
  target titles added), data source, climate score and rationale. Policy-context links are not exported.
- The suggested file name records the filters and the date.

## Governance Diagram

**What it shows.** Records are arranged in horizontal tiers: international treaties → international
bodies and EU law → UK legislation → UK public bodies → UK policies and activities → indicator
frameworks. Colour shows a record's main policy sector. Pick a record and the map shows everything
linked to it.

**Reading the links.** The arrow points from the governing entity to what it governs — enabling
legislation → the body or policy it empowers, lead organisation → the policy it leads, parent → child,
funder → funded.

| Line | Meaning |
|---|---|
| Solid | Hard link: enabling legislation, lead organisation, parent/child |
| Dashed | Soft link: related / cross-reference, funded by |
| Double | UK ↔ international bridge (solid = ratified or retained; dotted = thematic) |
| Solid pink | Key instrument named in an indicator framework's policy purpose |
| Dotted | Indicator / monitoring link |

Click a link type in the legend to show or hide it.

**Using it.**

- **Find a record** with the search box or the list on the left, or click any node.
- **Expand** a neighbour with its **+** to add its own links (two levels deep).
- **Hover** a node for its full name; the bottom panel shows the selected record's details and
  narrative (duties, powers, provisions, status), with codes in the text named on hover.
- **Controls** (top right of the map): move, zoom and fit; collapse depth; show or hide soft links and
  EU law; export the current view as **SVG** or **PNG**.
- **More room**: **◧ Filters** and **▤ Details** in the header hide the side and bottom panels.
- **Share a view**: the address ends with `#RECORD-ID`; send it and the Diagram reopens on that record.

**Record ID prefixes.** `LEG` UK legislation · `ORG` UK public body · `POL` UK policy or activity ·
`INT-L` / `INT-O` / `INT-P` international treaty / body / policy · `EU-L` EU law · `IFW` indicator
framework.

## Using the two together

Start in the **Finder** to identify indicators — for example, climate score ≥ 2 within the Marine
sector — then follow **⬡ diagram** from the policy context to see where that instrument sits in the
governance system. Start in the **Diagram** when the question is about an organisation, Act or policy,
and open an indicator framework's node to see what it reports against.

## Limits to keep in mind

- The links are curated from the workbooks and are not exhaustive; a missing link means the workbook
  does not record one, not that none exists.
- Policy context is held per framework, not per indicator.
- The dashboards are only as current as the last release; check the Finder's footer.
