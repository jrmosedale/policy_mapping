# Climate score — method and provenance

*Nature Climate Indicators project · `indicators_climate_nature.xlsx` v27 · written 6 October 2026*

This is the reference for the `Climate_Score` column held on all nine indicator-framework sheets, and for the score shown in the Indicator Finder. The Finder's Help panel gives users a short summary of what the score measures; this document covers how the score is assigned, why, and where the evidence sits.

**Authoritative sources.** The scale and the scoring rules are on the workbook's `Legend` sheet. Every record's own justification is in its `Climate_Rationale` cell. The review that produced the current scores is `outputs_other/climate_score_harmonisation/climate_score_harmonisation_proposal.xlsx`. If this document and the Legend sheet ever disagree, the Legend sheet wins.

---

## 1. What the score measures

Each indicator carries a score from 0 to 3 — **none / low / medium / high** — for how far its **published value depends on weather and climate data**: whether such data enter its calculation, and whether year-to-year weather moves the number.

It is a **data-dependency** score. It is **not** a measure of how relevant an indicator is to climate policy. Heat-pump installations, or the number of countries with adaptation plans, are *about* climate but score 0, because no climate data enter them and weather cannot move them. Topical relevance is carried separately by `Policy_Sector = Climate`, which is what the Finder's Sector filter uses.

The distinction matters because the score answers the question this project exists to ask: *would a change in weather or climate data — the Met Office's product — change this indicator?*

| Score | Label | Meaning | Typical examples |
|---|---|---|---|
| **0** | None | Administrative, financial, legal or boundary data; weather cannot move the value. | Protected-area coverage, expenditure, EV sales, installed capacity, counts of NDCs, DRR strategies or adaptation plans |
| **1** | Low | Climate is a recognised long-run driver, but no climate data are used and weather does not materially move the annual value. | Red List Index, habitat condition, land-cover and habitat extent, invasive-species counts, GHG emission inventories, energy demand |
| **2** | Medium | Weather is a known, significant year-to-year confounder, or climate data enter indirectly through underlying models. | Breeding-bird and Living Planet indices, fish stock assessments, air-pollutant concentrations, renewable share of generation, water demand, harvest volumes, LULUCF carbon fluxes |
| **3** | High | Climate data are a direct input; the quantity is itself a climate or hydrological variable; it is defined by attribution to weather events; or it is designed to measure a climate response. | Temperature-adjusted emissions, Spring Index, butterfly flight-activity indices, fire-weather index, river flow, groundwater, sea level, ocean pH, heat-related mortality |

A blank score means **not assessed**. The Finder shows it as a hatched badge, and it never satisfies a "climate score ≥ N" filter, so an unscored record cannot pass as a zero. (Until September 2026 the builder read blanks as 0, which silently hid 173 unassessed SDG records among the genuine zeros.)

---

## 2. How a score is assigned

1. Identify the **measured quantity as published** — its units, data source and method — not its subject or the policy it serves.
2. Administrative, financial, legal, boundary-area, installed-stock or count-of-plans measures score **0**.
3. Status assessments, mapped extents, and emissions or energy inventories, where climate is only a background driver, score **1**.
4. If weather moves the annual value materially, or climate data enter through an underlying model, score **2**.
5. If climate or weather data are an explicit input, the quantity is a physical climate or hydrological variable, it is defined by attribution to weather or climate events or thresholds, or it is built to measure a climate-related biological response, score **3**.

### Special cases

- **Composites** — the component that defines the headline quantity governs; a climate-defined component named in the measure takes precedence ("river flows and ecological status" scores 3).
- **Same indicator, same score** — an indicator held under more than one framework (common where the GBF reuses SDG indicators) carries one score, unless the source methods differ, and then the rationale says how. UK agricultural emissions score 2 because the UK inventory uses rainfall-dependent emission factors; the EU series scores 1.
- **Weather-corrected series** score above raw ones: temperature-adjusted buildings emissions 3, the unadjusted series 1.
- **Targets** (the CCC adaptation framework, IFW-10) are scored on the quantity the target is expressed in, not on being adaptation targets.
- **Red List Index** scores 1 in every disaggregation except reef-building corals (2), whose assessments rest on climate-driven decline.

---

## 3. The scoring rules

These are held verbatim on the `Legend` sheet, below the 0–3 scale. Rule labels deliberately do not begin with a digit: `build_indicator_finder.py` lifts the scale from Legend rows matching `^[0-3]`, and a rule labelled "1." would be read as a scale level.

**Core principle.** Score the measured quantity as published: do weather or climate data enter its calculation, and does inter-annual weather materially move its value? Do not score topical relevance to climate policy (`Policy_Sector = Climate` carries that), the policy purpose of the measure (e.g. that it is an adaptation measure), or the fact that climate change is a long-run driver of the thing measured.

**Rule A — score 0.** Administrative, financial, legal, GIS-boundary, deployment/installed-capacity, certification and count-of-plans measures — including those whose subject is climate (NDCs, DRR strategies, adaptation plans, climate finance, carbon-credit registries, assets "assessed and adapted").

**Rule B — score 1.** Status assessments and extents from mapping or field survey, where climate is a recognised driver but no climate data enter and weather does not materially move the annual value: Red List Index and all its disaggregations, Red List of Ecosystems, STAR, phylogenetic-diversity loss, conservation status, habitat/site condition, INNS counts, land-cover and habitat extent (including mangrove, saltmarsh, seagrass, forest), and connectivity derived from land cover. *Exception:* reef-building corals RLI scores 2.

**Rule C — emissions and energy.** Emissions inventories (activity × emission factor), emission intensities, and energy demand or intensity score 1. A temperature-adjusted (weather-corrected) series scores 3. LULUCF and ecosystem carbon-flux estimates from models that take temperature or rainfall score 2.

**Rule D — score 2.** Quantities that inter-annual weather moves materially, or that are modelled with climate data indirectly: survey-based population indices (BBS, LPI, WBI), occupancy models for insects, fish stock assessments, plankton and trophic indices, measured or modelled air-pollutant concentrations, renewable-generation shares, water demand, leakage and abstraction compliance, surface-water extent, harvest volumes and yields at national scale, disease and pest incidence.

**Rule E — score 3** when (i) weather or climate data are a direct, explicit input (temperature adjustment, fire-weather index, reanalysis soil moisture, climate projections as primary input, DGVM or remote-sensing NPP driven by meteorology); (ii) the quantity is itself a physical climate-system or hydrological variable (temperature, sea level, ocean heat, pH, river flow, groundwater level, reservoir storage); (iii) the quantity is defined by attribution to weather or climate events or thresholds (heat-attributable mortality, weather-event disruption or loss, return-period standards, overheating thresholds); or (iv) it is designed to measure a climate-related biological response (phenology, butterfly/moth flight-activity indices, thermal community indices).

**Rule F — composites.** Score the component that defines the headline quantity; where a climate-defined component is a named part of the measure, it governs.

**Rule G — consistency.** The same measured quantity on more than one sheet takes one score, unless the source methodology genuinely differs — and then the rationale says how.

**Rule H — targets.** Targets (IFW-10) are scored on the quantity the target is expressed in, not on the target being an adaptation target.

### Writing the rationale

`Climate_Rationale` states the measured quantity, whether climate data enter it, and whether weather moves it, and ends by citing the level and rule, e.g. *"(Legend 1, rule B)"* or *"(Legend 2, rules D and G; aligned with [GBF-074])"*. Where rule G applies, name the sibling record. The rationale is shown in the Finder's detail panel and in both export formats, so it is the user-facing justification.

`Climate_Dependency` is the labelled form of the score (`0 – None`, `1 – Low`, `2 – Medium`, `3 – High`) and must always agree with `Climate_Score`.

---

## 4. Distribution

After harmonisation (v27), across 985 records:

| Sheet | Records | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|---:|
| EIF Indicators | 66 | 16 | 21 | 27 | 2 |
| CCC Indicators | 149 | 55 | 36 | 27 | 31 |
| JNCC UK Biodiversity Indicators | 77 | 27 | 18 | 22 | 10 |
| SoN 2023 Indicators | 32 | 4 | 18 | 9 | 1 |
| EEA Biodiversity Indicators | 62 | 16 | 18 | 15 | 13 |
| BIP Indicators | 81 | 38 | 21 | 18 | 4 |
| IPBES Indicators | 143 | 35 | 57 | 38 | 13 |
| CBD GBF Indicators | 202 | 116 | 56 | 26 | 4 |
| SDG Indicators | 173 | 128 | 24 | 19 | 2 |
| **All** | **985** | **435** | **269** | **201** | **80** |

The shape is what each framework should look like. The CCC sheet has the most 3s — adaptation targets defined in climatic terms, hydrological measures and weather-corrected emissions — and also many 0s, because mitigation deployment measures (installations, capacity, sales) take no climate data. The SDG and GBF sheets are dominated by social, financial and governance measures, so mostly 0. EEA carries a block of explicit climate indicators (temperature, sea level, ocean heat, drought, wildfire).

---

## 5. Provenance — the 2026 harmonisation

**Why it was needed.** When the SDG sheet was scored in September 2026 (v21), anchoring each SDG record on the identical record elsewhere exposed that the workbook already scored one measured quantity differently on different sheets:

| Indicator | Scores held before harmonisation |
|---|---|
| Total GHG emissions | 1 on CCC, JNCC and EEA; 3 at [GBF-184] and on the IPBES sheet |
| Annual mean PM2.5 / PM10 | 3 at [IND-E-003]; 2 at [GBF-074]; 1 on the IPBES sheet |
| Protected-area coverage | 0 on EIF, CBD GBF, BIP and IPBES; 3 on the CCC sheet |

Since the Finder's climate-score filter is the filter the dashboard is built around, three scores for one quantity meant it was not comparing like with like across frameworks.

**What the review found.** A record-by-record review of all 985 records showed the disagreements were about how the scale was read, not about the facts. Three readings were in use:

1. **The Legend as written** — data dependency. Followed by EIF, SoN, JNCC, EEA, the SDG sheet and the CCC mitigation rows.
2. **"Climate change threatens it"** — scored Red List, Red List of Ecosystems and habitat-extent measures 2 on the BIP, IPBES and GBF sheets, although the Legend's own example puts conservation status at 1.
3. **"It matters for climate policy"** — scored the 2023–25 CCC adaptation rows (IFW-11) 3 for protected-area extent, water-infrastructure capacity and carbon-code registries, and scored GHG emissions 3 at [GBF-184] and [IPBES-D-023].

**What was done (v27, 28 September 2026).** Reading 1 was adopted and written down as the Core principle and Rules A–H. 162 of 985 records were rescored — 145 down, 16 up; 98 at high and 64 at medium confidence — with `Climate_Dependency` and `Climate_Rationale` rewritten on each.

| Sheet | Changed |
|---|---:|
| CCC Indicators | 54 |
| CBD GBF Indicators | 31 |
| SDG Indicators | 19 |
| IPBES Indicators | 17 |
| EIF Indicators | 14 |
| BIP Indicators | 12 |
| JNCC UK Biodiversity Indicators | 8 |
| SoN 2023 Indicators | 4 |
| EEA Biodiversity Indicators | 3 |

Workbook distribution (0 / 1 / 2 / 3) moved from **396 / 233 / 228 / 128** to **435 / 269 / 201 / 80**. Resolved: GHG emission inventories 1 (temperature-adjusted series 3); air-pollutant concentrations 2; protected-area coverage 0; every Red List Index disaggregation 1 except corals; climate-policy administrative counts 0; renewable-generation shares 2.

**The review record.** `climate_score_harmonisation_proposal.xlsx` holds, for every changed record, the old and new score, the rule applied, the confidence, and the old and new rationale. Its sheets: *Rules*, *Proposed changes*, *Distribution*, *Kept – flagged*, *All records*. It is kept unchanged as the record of the decision.

---

## 6. Borderline cases deliberately left unchanged

| Record(s) and score | Why left unchanged | Confidence |
|---|---|---|
| IND-C-034, IND-C-073, IND-C-074 (2) vs IND-B-170 (1) | Agricultural GHG: the UK inventory uses country-specific N₂O factors that vary with rainfall; the EU series is activity × emission factor. A genuine method difference (rule G). Confirm the UK method before citing. | Medium |
| IND-C-105 (3) | Composite naming river flows; the hydrological component governs (rule F). | Medium |
| IND-C-110 (3) | Yield variability is designed to capture weather sensitivity (rule E iv). | High |
| IND-C-114 (3) | Area affected by drought, disease and windthrow is weather-event-defined (rule E iii). | Medium |
| IND-C-173 (3) | "Stocks sustainable under 2 °C" needs climate-projection modelling to evaluate (rule E i). Revisit when the CCC names the indicator. | Medium |
| IPBES-N-048/051/064/065 cSAR (2), IPBES-N-066 range size (2) | Could be 1 if the underlying range maps are expert polygons rather than climate-driven SDMs. Not verified. | Low |
| IPBES-N-052/078 Madingley (2) | Could be 3: temperature and NPP are explicit model inputs. Left at 2 because the outputs are biodiversity metrics, not climate fluxes. | Low |
| IND-B-178 free-flowing rivers (2) | Possibly 0–1 if the assessment is barrier-based only. Not verified. | Low |
| SDG-015, SDG-017 (2) | Global food-insecurity and wasting prevalence respond to drought shocks in many reporting countries. | Medium |
| GBF-150 inland fisheries threat (2) | Threat index includes flow and temperature layers; not verified. | Low |

---

## 7. Using and maintaining the score

**In the Finder.** The sidebar filter is a threshold: "climate score ≥ N". Use ≥ 2 for indicators that weather or climate data would move; ≥ 3 for indicators built on climate data. Use Sector → Climate for indicators *about* climate. The two answer different questions, and an indicator can satisfy either without the other.

**Scoring a new record.** Follow the steps in §2 against the rules in §3; check whether the same quantity is already held on another sheet (rule G) and anchor on it, citing the sibling; write the rationale as in §3. A new record must never be left blank: the builder prints a warning naming any unscored record.

**Changing a score.** Treat it as a workbook edit under `Management/protocols/WORKBOOK_WRITE_PROTOCOL.md` — propose, verify, write, bump the version, changelog, archive, `finalise.py`. If a change implies a rule is wrong, change the rule on the Legend sheet and this document together, and check every record the rule covers rather than the one in hand.

**Watch for.** The scale drifts towards topical relevance whenever records are scored in bulk from a framework's own description, because frameworks describe indicators by purpose. The September 2026 drift arose exactly that way, on the CCC adaptation and international biodiversity sheets.

---

## 8. Confidence and limits

- Scores judge each indicator's **published method from its documentation**, not from re-running the calculation. Where a method is undocumented, the score is an inference and the rationale should say so.
- 64 of the 162 changes in 2026 (≈40%) are **medium confidence**; the borderline cases in §6 are lower. The 1 vs 2 boundary — "background driver" against "known significant confounder" — is where reasonable scorers most often differ.
- The score describes the indicator, not its data source in a given year. An indicator whose methodology changes (for example, a new weather correction) should be rescored.

*Verified for this document:* the distribution tables were computed from the v27 workbook; the rules are copied from the Legend sheet; the change counts and borderline list are from the review workbook. *Inherited and not re-checked:* the methodological claims in individual rationales, which rest on each framework's documentation as read during the review.
