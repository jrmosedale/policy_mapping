# Pending additions — candidate workbook records

A standing, **append-only** queue of records that have been *found* but not yet *written* to the
canonical workbooks. Read and resolved at every policy scan
(`Management/protocols/POLICY_SCAN_PROTOCOL.md` §5–§6).

## How to use this file

**If you are running a policy assessment:** at the end of the run, append one row for every
activity and every indicator you marked `†` — everything relevant that you found and the workbooks
do not hold. **Append them; do not ask whether to.** Adding a row changes no workbook and needs no
approval; the queue is a candidate list, and every row still passes the screen and the triage
before anything is written. If you cannot reach this file, emit the rows as a copy-paste block
labelled for pasting here. Losing them is not an option.

**If you are running a policy scan:** work the `pending` rows first — they are already researched and
generally outrank anything the watchlist turns up. Then resolve each one.

**Concurrent appends** on separate git branches conflict at the end of the Queue table. Resolve by
keeping both sets of rows.

**Rows are never deleted.** Resolve by changing `Status`:

| Status | Meaning |
|---|---|
| `pending` | Not yet triaged. |
| `added` | Written to a workbook. Put the new Record ID in `Resolution`. |
| `rejected` | Triaged and declined. Put the reason in `Resolution` — this is what stops it being re-proposed and re-argued every quarter. |
| `duplicate` | Already held. Put the existing Record ID in `Resolution`. |
| `add` | Approved for writing, not yet written. Becomes `added` when written. |
| `defer` | Approved in principle or borderline; parked until a stated condition is met. |
| `investigate` | Needs a fact checked at source before a decision. |
| `done` | A framework-currency or update item completed on an existing record (no new record). |

**Column notes.** `Family` is the ID family it would join (`LEG`, `ORG`, `POL`, `INT-L`, `INT-O`,
`INT-P`, `EU-L`, `IND`, `IFW`). `Climate input` applies to indicators and is the project's core
relevance test — does the *measured quantity* take a climate input, or could it? A `no` does not
disqualify a record: the catalogue is broad and the dashboards filter (protocol §7.3). `Source`
must be a primary source. `Confidence` records what is unverified, not how strongly you feel.

---

## Queue

| Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-02 | scan 2026-09-02 | LEG | Natural Environment (Scotland) Act 2026 (2026 asp 6) | https://www.legislation.gov.uk/asp/2026/6/contents | Indirect now; likely yes once its mandated targets and indicators are set | Joins [LEG-032], [LEG-033], [LEG-034]; links [ORG-014], [ORG-034] | High — primary source; Royal Assent 12 Mar 2026 | added | **2026-10-06 — added (UK v27):** [LEG-068]. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 | LEG | Environment (Principles, Governance and Biodiversity Targets) (Wales) Act 2026 (2026 asc 4) | https://www.legislation.gov.uk/asc/2026/4/enacted | Indirect now; target-dependent later | None — Wales thinly represented in Legislation sheet | High — primary source; Royal Assent 27 Apr 2026 | added | **2026-10-06 — added (UK v27):** [LEG-069]. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 | ORG | Office of Environmental Governance Wales | https://www.gov.wales/environment-principles-governance-and-biodiversity-targets-wales-act-2026 | n/a — governance body | Peer of [ORG-007]; sibling of Environmental Standards Scotland | Medium — created in statute; needs check on operational status and commencement | added | **2026-10-06 — added (UK v27):** [ORG-046]. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 | ORG | Environmental Standards Scotland (ESS) | https://environmentalstandards.scot/about-us/what-we-do/ | n/a — governance body | Peer of [ORG-007]; links [ORG-034]; named as QA body in the Scotland Act above | High — operating since 2021; pre-existing gap, not a new development | added | **2026-10-06 — added (UK v27):** [ORG-045]. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 | POL | Nature Recovery Strategy for Northern Ireland to 2032 (DAERA) | https://www.daera-ni.gov.uk/consultations/draft-nature-recovery-strategy-extended-consultation-period | Unknown until adopted | None — NI least represented nation | Low — DRAFT, consultation extended and not concluded; do not add until adopted | add | **6 Oct 2026: still a draft (consultation closed spring 2026, no final strategy) — hold until adopted.** **Decided 2026-09-11 — add.** |
| 2026-09-02 | ocean heatwaves | IND | MCCIP sea-temperature evidence update (UK & Ireland) | https://www.mccip.org.uk/recent-updates | Yes — sea temperature is the measured quantity | MCCIP is catalogued as [POL-049] but has no indicator rows; blocked on the pending MCCIP scaffold decision | Medium — MCCIP publishes topic-level evidence with confidence ratings, not a quantitative indicator catalogue | added | **2026-10-06 — added (indicators v28):** covered by [IND-M-001] Sea temperature in the MCCIP block. **Decided 2026-09-11 — defer.** |
| 2026-09-02 | daily sunshine | POL | Solar Roadmap 2025 (DESNZ / Solar Taskforce / Solar Council) | https://www.gov.uk/government/publications/solar-roadmap | Yes — solar-resource climatology informs siting and yield | None; [POL-005] Clean Power 2030 and [POL-016] CfD mention solar but are different instruments | High — published 30 Jun 2025; 72 actions to reach 45-47 GW | defer | **Decided 2026-09-11 — defer.** Jonathan 2026-09-11: Borderline to scope |
| 2026-09-02 | daily sunshine | POL | Future Homes Standard (rooftop solar on new homes from 2027) | https://www.gov.uk/government/consultations/the-future-homes-and-buildings-standards-2023-consultation | Yes — location-specific sunshine climatology informs yield estimates | None | Medium — URL is the 2023 consultation; find the final standard before writing | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | land surface temperature | POL | Heat-Health Alerting System / Weather-Health Alerts (UKHSA - Met Office) | https://www.gov.uk/guidance/heat-health-alerting-system | Yes — runs on Met Office air-temperature forecasts | None as a policy record; [IND-C-130] covers the mortality outcome, not the alerting system | High | added | **2026-10-06 — added (UK v27):** [POL-072]. **Jonathan 2026-09-10 — D1+D2 UKHSA record and Operational service / System type agreed.** |
| 2026-09-02 | land surface temperature | POL | Adverse Weather and Health Plan (UKHSA) | https://www.gov.uk/government/publications/adverse-weather-and-health-plan | Yes — a NAP commitment underpinned by the Weather-Health Alerting System | None; sits under NAP3 [POL-002] | High | added | **2026-10-06 — added (UK v27):** [POL-073]. **Jonathan 2026-09-10 — D1+D2 UKHSA record and Operational service / System type agreed.** |
| 2026-09-02 | land surface temperature | POL | Building Regulations Part O (overheating in new residential buildings) | https://www.gov.uk/government/publications/overheating-approved-document-o | Yes — assessed against CIBSE design summer-year weather files | None. **Blocked**: needs the Building Act enabling-legislation LEG ID, an open schema decision in the handover | High on existence; the blocker is the LEG parent, not the record | added | **2026-10-06 — added (UK v27):** [POL-074], with parent [LEG-070] Building Act 1984. **Jonathan 2026-09-10 — D3 Building Act LEG ID agreed.** Jonathan: detailed policy actions in this field probably out of scope - keep the record high-level |
| 2026-09-02 | land surface temperature | POL | NSWWS Extreme Heat warnings (Met Office) | https://weather.metoffice.gov.uk/guides/warnings | Yes — air-temperature and impact based | None | Medium — an operational warning service; may need the 'Operational service / System' General_Type, itself an open schema decision | added | **2026-10-06 — added (UK v27):** [POL-075] — held at service level (NSWWS incl. Extreme Heat warnings). **Jonathan 2026-09-10 — D1+D2 UKHSA record and Operational service / System type agreed.** |
| 2026-09-02 | land surface temperature | IND | Heat mortality monitoring report, England (UKHSA Official Statistics) | https://www.gov.uk/government/publications/heat-mortality-monitoring-reports | Yes | **Overlaps [IND-C-130]** Heat-related mortality and morbidity (England and Wales) | Medium — the run itself flagged the overlap; this is the open schema decision on handling a UKHSA heat-mortality statistic | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: outside scope |
| 2026-09-02 | land surface temperature | ORG | UK Health Security Agency (UKHSA) | https://www.gov.uk/government/organisations/uk-health-security-agency | n/a — public body | Absent from Public Bodies, yet named in [IND-C-130], [IND-C-131], [IND-C-134] and owner of four queued policy candidates above | High — an open schema decision in the handover, now blocking five queued rows | added | **2026-10-06 — added (UK v27):** [ORG-047]; sponsor DHSC added as [ORG-049]. **Jonathan 2026-09-10 — D1 UKHSA ORG record agreed.** |
| 2026-09-02 | plant pest, pathogen & biosecurity | POL | GB Plant Health Risk Register / Defra plant health risk and horizon scanning | https://planthealthportal.defra.gov.uk/pests-and-diseases/uk-plant-health-risk-register/ | Yes — climate-suitability and degree-day outputs feed the establishment likelihood component | None | High — operational register; MO outputs already feed it | added | **2026-10-06 — added (UK v27):** [POL-076]. **Jonathan 2026-09-10 — D1+D2 UKHSA record and Operational service / System type agreed.** |
| 2026-09-02 | plant pest, pathogen & biosecurity | POL | Defra generic and pest-specific contingency plans / GB Plant Health Service outbreak response | https://planthealthportal.defra.gov.uk/pests-and-diseases/contingency-planning/ | Yes — Defra partners with the Met Office for predicted pest emergence dates | None; related to [POL-034] Plant Biosecurity Strategy | High — documented MO-Defra operational channel | added | **2026-10-06 — added (UK v27):** [POL-077]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | plant pest, pathogen & biosecurity | POL | Observatree (citizen-science tree-health surveillance) | https://www.observatree.org.uk/ | Possible — survey effort could be targeted using climate-suitability maps | **Mentioned within [POL-033] and [POL-034] but holds no record of its own** | Medium — decide whether a partnership programme warrants its own POL or stays a prose mention | defer | **Decided 2026-09-11 — defer.** Jonathan 2026-09-11: keep as mention for timebeing |
| 2026-09-02 | scan 2026-09-02 (corrected) | POL | 30by30 on land in England — commitment, criteria and delivery plan | https://www.gov.uk/government/publications/30by30-on-land-in-england-delivery-plan | Yes — the Management criterion requires monitoring of condition and trends of important habitats and species, and SSSIs count only if in favourable or recovering condition; habitat condition is climate-sensitive | **Not covered.** [POL-022] is the 30×30 Technical Working Group — a coordination body, not the policy, though its Link field points at the 30by30 page. Delivers GBF Target 3, measured by [GBF-013] 3.1 Coverage of protected areas and OECMs | High — primary source. Delivery plan and the assessment guidance both published 13 Jul 2026; criteria published 29 Oct 2024 at COP16, superseding the withdrawn Dec 2023 paper | added | **2026-10-06 — added (UK v27):** [POL-078]; reciprocal [INT-L-007] (intl v17). **Jonathan 2026-09-10 — D6 30by30 recorded per nation.** Also chase Wales and NI 30by30 commitments - neither yet scanned |
| 2026-09-02 | scan 2026-09-02 (corrected) | POL | 30by30 assessment standard for England — three criteria (Purpose / Protection / Management), Bronze / Silver / Gold tiers, central and partner assessment routes | https://www.gov.uk/government/publications/30by30-on-land-assessing-whether-land-can-contribute | Indirect — the criteria require monitoring of habitat and species condition, but the standard itself measures eligibility, not climate | **Corrected 2026-09-17 after checking the source: this is NOT a new indicator set.** It is an eligibility and assurance standard. It creates no new monitoring — central assessment runs on the existing SSSI Protected Sites regime, NNR records and Landscape Recovery scheme data. It produces one headline measure (share of England in Gold tier), already reported internationally through [GBF-013] 3.1 Coverage of protected areas and OECMs | High — read in full at source | added | **2026-10-06 — added (UK v27):** [POL-079] (Guidance / Methodology). **Decided 2026-09-11 — add.** Record type corrected 2026-09-17 from IFW to **POL**, `General_Type` **Guidance / Methodology** (or Standard / Code — Jonathan's call). Attach to the England 30by30 commitment record. If the *measure* is wanted, add ONE IND (% of England meeting the criteria), not a framework. **New scope item:** the guidance states separate approaches exist for Northern Ireland, Scotland, Wales **and at sea** — 30by30 marine has not been scanned at all. |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | Nature security assessment on global biodiversity loss, ecosystem collapse and national security (Defra) | https://hansard.parliament.uk/commons/2026-06-04/debates/CC1A879B-3B94-4B08-9B66-60AB047E06BC/GlobalBiodiversityLossAndEcosystemCollapseNationalSecurityAssessment | Yes — frames ecosystem collapse pathways, climate-driven | None | Medium — published Jan 2026; find the gov.uk landing page for the primary link before writing | added | **2026-10-06 — added (UK v27):** [POL-080] (published 20 Jan 2026). **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | Farming Roadmap 2050: Growing England's Future (CP 1611, Defra) | https://www.gov.uk/government/publications/farming-roadmap-2050 | Yes — agricultural land use and transition are climate-sensitive | None; relates to [POL-013] ELM, [POL-054] SFI, [POL-061] CSHT | High — June 2026, Command Paper | added | **2026-10-06 — added (UK v27):** [POL-081]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | Water White Paper 2026 (Defra) | https://www.gov.uk/government/publications/ | Yes — water resource and drought policy | None; regulators [ORG-006], [ORG-011], [ORG-022] present but the White Paper is not | Medium — published 2026 with a correction slip; confirm the gov.uk landing page and exact date | added | **2026-10-06 — added (UK v27):** [POL-082] — 'A new vision for water', CP 1940, 20 Jan 2026. **Decided 2026-09-11 — add.** Jonathan 2026-09-11: Borderline to scope but major LEG so add |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | National Drought Group / coordinated drought response | https://www.gov.uk/government/organisations/department-for-environment-food-rural-affairs.atom | Yes — drought is a climate impact; EIF F1-F3 resilience indicators relate | None | Medium — surfaced as Defra news 20 Aug 2026 ('Coordinated drought response intensifies amid extreme weather'); confirm whether the National Drought Group warrants a standing POL or is an operational response | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: assuming an operational response |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | Interactive Story Map on spatial evidence for climate and nature (14 Jul 2026) | https://hansard.parliament.uk/Lords/2026-07-14/debates/B660D9E1-AB48-4C94-864E-8C2B9AAEDCEB/StateOfClimateAndNature | Yes — spatial climate-nature evidence, directly relevant to the project's spatial-metrics question | None | Low — named in the statement; locate the actual product and assess before writing | investigate | **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | **CHECK, not an addition** — Land Use Framework: [POL-009] records 'Land Use Framework (LUF) 2025' but the 14 Jul 2026 statement refers to a 2026 Land Use Framework | https://hansard.parliament.uk/Lords/2026-07-14/debates/B660D9E1-AB48-4C94-864E-8C2B9AAEDCEB/StateOfClimateAndNature | n/a | [POL-009] | Medium — confirm whether a 2026 version supersedes the 2025 record; if so this is an amendment, not a new record | investigate | **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (pass 2) | POL | **CHECK, not an addition** — Carbon Budget and Growth Delivery Plan (Oct 2025) may supersede [POL-004] 'UK Net Zero Strategy / Carbon Budget Delivery Plan (CBDP) 2023' | https://hansard.parliament.uk/Lords/2026-07-14/debates/B660D9E1-AB48-4C94-864E-8C2B9AAEDCEB/StateOfClimateAndNature | n/a | [POL-004] | Medium — a retirement/supersession, which §3 warns is easier to miss than an addition | done | **2026-10-06 — done (UK v32):** Resolved: [POL-004] marked superseded and points to [POL-112]. **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (pass 2) | IND | **CHECK, not an addition** — EIF indicator data refreshed six times in 2026 (13 Feb, 17 Mar incl. new indicators, 15 Apr K1/F2/F3, 13 May, 3 Jul A2/K4, 19 Aug) | https://www.gov.uk/government/publications/environmental-indicator-framework-recent-updates | Yes | [IFW-01] and the 66 EIF indicator rows | High that updates occurred; unknown whether any EIF indicator was added or retired — the 17 Mar entry says 'new indicators updated'. Workbook EIF rows may be stale | added | **2026-10-06 — added (UK v27):** Done in indicators v17: EIF verified current, no indicator added or retired. **Decided 2026-09-11 — add.** Jonathan 2026-09-11: Update existing record - need also to ensure framework indicators updated? |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | **Environment Act target delivery plans — 13 plans plus an overview** (agriculture water quality; air quality; farm wildlife; habitat creation and restoration; marine protected areas; invasive non-native species; residual waste reduction; statutory species targets; tree canopy and woodland cover; water and abandoned metal mines; water demand; protected sites) | https://www.gov.uk/government/publications/overview-delivery-plans-for-our-environment-act-targets | Yes — habitat, species, tree canopy and water targets are all climate-sensitive | **None.** [LEG-004] Environment Act 2021 and [POL-001] EIP 2025 are held, but the statutory target *delivery* layer is entirely absent | High — all published 16 Jul 2026 (protected sites 20 Jul). Granularity decided | added | **2026-10-06 — added (UK v27):** [POL-083] overview + [POL-084]–[POL-096]. Correction: first published 1 Dec 2025 (16 Jul 2026 was the update); the 13th topic is wastewater. **Jonathan 2026-09-10 — D5 granularity = 13 records.** Create 13 POL records, one per target plan, plus the overview |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | IFW | Monitoring the condition of the natural environment (Defra) | https://www.gov.uk/government/publications/monitoring-the-condition-of-the-natural-environment | Yes | None. Published 16 Jul 2026 alongside the EIP progress report and the target delivery plans; likely describes the monitoring architecture behind [IFW-01] EIF | Medium | added | **2026-10-06 — added (UK v27):** [POL-071] (UK v26). **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | Government Estate Nature Plan (GENP) | https://www.gov.uk/government/publications/government-estate-nature-plan-genp | Yes | None. Relates to 30by30 and the National Estate for Nature named in the 30by30 delivery plan | High — 22 Jul 2026 | added | **2026-10-06 — added (UK v27):** [POL-097] (published 26 Jun 2026, not 22 Jul). **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | The UK's approach to deforestation regulations | https://www.gov.uk/government/publications/the-uks-approach-to-deforestation-regulations | Yes — forest loss and land use | Related to [POL-029] 2030 Strategic Framework for International Climate and Nature; no forest-risk-commodities record exists | High — 2 Sep 2026 | added | **2026-10-06 — added (UK v27):** [POL-098]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | Biodiverse Landscapes Fund | https://www.gov.uk/government/publications/biodiverse-landscapes-fund | Yes | None | High — 13 Aug 2026; international biodiversity funding programme | added | **2026-10-06 — added (UK v27):** [POL-099]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | Thames Estuary 2100 (TE2100) and its 15-year monitoring review | https://www.gov.uk/government/collections/thames-estuary-2100-te2100 | Yes — adaptive flood-risk management explicitly designed around sea-level rise | None | High — review published 6 Aug 2026. A rare worked example of adaptive climate management with a monitoring cycle; likely of direct interest to MO | added | **2026-10-06 — added (UK v27):** [POL-100]. **Decided 2026-09-11 — add.** Jonathan 2026-09-11: generally out of scope but including as example! |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | PFAS Plan | https://www.gov.uk/government/publications/pfas-plan | No — chemical pollution, no climate input | None | High — 17 Aug 2026. Catalogue under the tiered rule (§7.3) with climate relevance scored zero | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: pollution issues generally out of scope |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | Biodiversity gain statements for nationally significant infrastructure projects | https://www.gov.uk/government/collections/biodiversity-gain-statements-for-nationally-significant-infrastructure-projects | Indirect | Check against any existing biodiversity net gain record before writing | Medium — 31 Jul 2026 | investigate | **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | Future of Rural England Report | https://www.gov.uk/government/publications/future-of-rural-england-report | Indirect — rural land use | None | Low — 16 Jul 2026; assess whether it introduces commitments or is analysis only | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | LEG | **CHECK** — Fisheries Act 2020: Post-Legislative assessment (29 Jul 2026) and Fisheries management plans: policy information (30 Jul 2026) | https://www.gov.uk/government/publications/fisheries-act-2020-post-legislative-assessment | n/a | [LEG-052] Fisheries Act 2020, [POL-067] Fisheries Act climate change objective | Medium — may update the status or content of both records rather than adding one | investigate | **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (Defra enum) | POL | **CARRY FORWARD — open consultations, §3 excludes until concluded**: Biodiversity net gain brownfield exemption (2 Sep 2026); four proposed Fisheries Management Plans — Celtic Sea and Western Channel demersal, Celtic Sea and Western Channel pelagic, Seabream, Wrasses complex (28 Jul 2026) | https://www.gov.uk/government/consultations/biodiversity-net-gain-considering-a-targeted-exemption-for-brownfield-residential-development | Yes for the FMPs | FMPs relate to [POL-067] | High that they are open; revisit next scan | defer | **Decided 2026-09-11 — defer.** |
| 2026-09-02 | scan 2026-09-02 (stats sweep) | IND | Provisional Cormorant population indices for England 2026 | https://www.gov.uk/government/statistics/provisional-cormorant-population-indices-for-england-2026 | Yes — population index, climate-sensitive | **Answered 2026-09-17.** Not policy-target monitoring. The publication states the indices are released early as provisional "to enable their use for **operational purposes**" — i.e. Natural England licensing of fish-eating bird control to protect fisheries (licences A06/A07). It is an operational licensing input, not a biodiversity target measure | High — stated on the publication page | rejected | **Decided 2026-09-11 — rejected, confirmed 2026-09-17.** The underlying data are the BTO/RSPB/JNCC Wetland Bird Survey, which is already represented at the right level of generality by [IND-J-010] wetland birds and [IND-J-013] wintering waterbirds in the JNCC UKBI sheet — and wintering waterbird distribution is the established climate signal. Same reasoning as the Tyne/Tees/Wear fish counts: species- or site-specific operational cuts of a survey already held. |
| 2026-09-02 | scan 2026-09-02 (stats sweep) | IND | Flood and Coastal Erosion Risk Management in England: central government funding and performance | https://www.gov.uk/government/statistics/flood-and-coastal-erosion-risk-management-in-england-central-government-funding-and-performance | Yes — flood risk is a climate impact | [POL-045] holds the FCERM strategy but no indicator record exists for the statistic | High | rejected | **2026-10-06 — rejected:** Decided 18 Sep 2026: no action. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (stats sweep) | IND | UK farm animal genetic resources (FAnGR): breed inventory results | https://www.gov.uk/government/statistics/uk-farm-animal-genetic-resources-fangr-breed-inventory-results | Indirect | Genetic-diversity indicators exist in the CBD GBF sheet; check overlap before proposing | Medium | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (stats sweep) | IND | **CHECK — likely already held**: Butterfly populations UK/England (overlaps [IND-E-029], [IND-J-014]); UK and England's carbon footprint (overlaps [IND-E-057]); British survey of fertiliser practice (relates to [IND-E-035], [IND-C-038]) | https://www.gov.uk/government/statistics/butterflies-in-the-wider-countryside-uk | Yes | Held under framework indicator names rather than the statistic's own title | High — verify the workbook's data vintage matches these releases rather than adding duplicates | duplicate | **2026-10-06 — duplicate:** Closed 18 Sep 2026: held as [IND-J-014]–[IND-J-018], [IND-E-057], [IND-C-038]. **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (title sweep) | POL | The Blue Belt Programme | https://www.gov.uk/guidance/the-blue-belt-programme | Yes — marine protection in the UK Overseas Territories | **None** — no Blue Belt record exists | High. Found only by the title sweep, under `detailed_guide` | added | **2026-10-06 — added (UK v27):** [POL-101] (lead FCDO, delivered by Cefas and MMO). **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (title sweep) | POL | Marine Recovery Fund (terms and conditions for offshore wind developers) | https://www.gov.uk/government/publications/marine-recovery-fund-terms-and-conditions-for-offshore-wind-developers | Indirect — marine compensation for offshore wind | None | Medium — found under `guidance` | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: generally t&c out of scope |
| 2026-09-02 | scan 2026-09-02 (title sweep) | ORG | Local Nature Partnerships (collective) | https://www.gov.uk/government/publications/map-of-local-nature-partnerships | Indirect | [ORG-037] Local Authorities (collective) is the nearest analogue; [POL-014] LNRS relates | Medium — decide whether a collective LNP record is warranted, as for ORG-037 | added | **2026-10-06 — added (UK v27):** [ORG-048]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (title sweep) | POL | Peatland Restoration Sector Capacity Grant Scheme (England) | https://www.gov.uk/government/publications/peatland-restoration-sector-capacity-grant-scheme-privacy-notice | Yes — peatland condition and carbon | [POL-066] Peatland ACTION is Scotland; no England equivalent held | Medium — locate the scheme's own landing page, not the privacy notice, before writing | added | **2026-10-06 — added (UK v27):** [POL-102]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (title sweep) | POL | Farmer Collaboration Fund | https://www.gov.uk/government/publications/farmer-collaboration-fund | Indirect | Relates to the ELM cluster [POL-013], [POL-054], [POL-061] | Low | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (title sweep) | POL | **CHECK** — Sustainable Farming Incentive 2026 (SFI26) may supersede [POL-054] SFI; Land Use Framework actions confirms a 2026 LUF against [POL-009] LUF 2025 | https://www.gov.uk/government/publications/sustainable-farming-incentive-2026-sfi26 | n/a | [POL-054], [POL-009] | High that both are new iterations; supersessions, not additions | investigate | **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (statements) | POL | **CHECK** — Revised National Planning Policy Framework and further planning reform measures (MHCLG written statement, 1 Sep 2026) | https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=2026-07-06&DateTo=2026-09-02 | Indirect — planning policy governs land use and biodiversity net gain | [POL-050] National Planning Policy Framework | High that a revision was announced; confirm what changed for nature and BNG. Found in a **non-Defra** department's statements, which the watchlist would not have reached | investigate | **Decided 2026-09-11 — investigate.** |
| 2026-09-02 | scan 2026-09-02 (statements) | POL | Water Company Resilience to Heatwaves and Sustained Hot Weather (Defra written statement HCWS279/HLWS280, 16 Jul 2026) | https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=2026-07-06&DateTo=2026-09-02 | **Yes — directly climate-driven**; heatwave and sustained hot weather resilience of water supply | **No policy record.** Nearest indicators are [IND-E-040] efficient use of water and [IND-E-044] drought disruption; no drought or heatwave *policy* record exists at all | High. Read the statement in full — it likely names a resilience framework or Ofwat/EA requirement that is itself the record | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (statements) | POL | Carbon Border Adjustment Mechanism — July 2026 delivery update (HM Treasury, 14 Jul 2026) | https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=2026-07-06&DateTo=2026-09-02 | Yes — carbon pricing on imports | **None** — no CBAM record in either workbook. Relates to [ORG-013] UK ETS Authority; sectors Climate, Trade & Industry | High. A significant UK climate instrument, entirely absent | rejected | **Jonathan 2026-09-10 — D4 energy-system policy out of scope.** No clear nature dimension |
| 2026-09-02 | scan 2026-09-02 (statements) | POL | Illegal Tree Felling: reducing the restocking notice appeals backlog (Defra, 15 Jul 2026) | https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=2026-07-06&DateTo=2026-09-02 | Indirect — woodland extent and condition | [LEG-027] Forestry Act 1967 and [ORG-009] Forestry Commission hold the enforcement powers; no record of the appeals process or backlog measure | Medium — may be an operational update rather than a record | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: operational |
| 2026-09-02 | scan 2026-09-02 (statements) | POL | National Policy Statement for Ports (DfT, 6 Jul 2026); Review of National Policy Statements for Nuclear Energy Infrastructure (DESNZ, 16 Jul 2026) | https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=2026-07-06&DateTo=2026-09-02 | Indirect — NPSs govern consenting of infrastructure with marine and habitat effects | No NPS records held at all, though [POL-050] NPPF covers terrestrial planning policy | Medium — decide whether National Policy Statements are in scope as a class; if so there are several more | rejected | **2026-10-06 (UK v30):** Exclusion recorded in [POL-050]. **Jonathan 2026-09-10 — D7 NPSs not in scope.** Note the exclusion in [POL-050] NPPF so the next scan does not re-raise it |
| 2026-09-02 | scan 2026-09-02 (statements) | POL | **LOW PRIORITY / CONTEXT** — Annual Statement on National Resilience (Cabinet Office, 14 Jul); Internal Drainage Board Levy Support Grant 2026-27 (MHCLG, 15 Jul); Zane Gbangbola non-statutory inquiry (Defra, 13 Jul); Dartmoor ponies (Defra, 16 Jul) | https://questions-statements.parliament.uk/written-statements?SearchTerm=&DateFrom=2026-07-06&DateTo=2026-09-02 | Mixed | [ORG-041] Cabinet Office; [LEG-065] Land Drainage Act 1991 | Low — screened and recorded so they are not reconsidered next quarter. National Resilience may reference climate risk; check once | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | POL | National Framework for Water Resources 2025: water for growth, nature and a resilient future (Environment Agency, 27 Aug 2026) | https://www.gov.uk/government/publications/national-framework-for-water-resources-2025-water-for-growth-nature-and-a-resilient-future | Yes — water availability under climate change | **None.** [IND-C-144] covers strategic water supply capacity but no framework record exists | High. The most substantive Block 2 find | added | **2026-10-06 — added (UK v27):** [POL-103] (published 17 Jun 2025; 27 Aug 2026 was the update). **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | POL | Climate Change Agreements (CCA) scheme | https://www.gov.uk/government/publications/climate-change-agreements-cca-biennial-report | Yes — energy efficiency and emissions | **None in either workbook.** Relates to [ORG-013] UK ETS Authority | High — a long-standing UK climate instrument, entirely absent | rejected | **Jonathan 2026-09-10 — D4 energy-system policy out of scope.** No clear nature dimension |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | POL | Humber 2100+ (tidal flood risk strategy) and shoreline management planning | https://www.gov.uk/government/publications/humber-2100-understanding-tidal-risk | Yes — sea-level rise and tidal risk | **None**, and no shoreline management plan record of any kind. Sits alongside the queued Thames Estuary 2100 | Medium — confirm whether Humber 2100+ is a distinct strategy or part of FCERM [POL-045] | rejected | **2026-10-06 (UK v31):** Sentence folded into [POL-045]. **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: too specific - consider part of FCERM? |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | POL | Nature-based solutions for sustainable water resources — Environment Agency position statement (17 Aug 2026) | https://www.gov.uk/government/publications/nature-based-solutions-for-sustainable-water-resources-environment-agency-position-statement | Yes | No NbS policy record; only prose mentions in [ORG-005] and [ORG-019] | Medium — decide whether an agency position statement is a POL | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: agency position out of scope |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | POL | River basin management planning cycle — significant water management issues consultation, and 'Agriculture and rural land management: challenges for the water environment' | https://www.gov.uk/government/consultations/significant-water-management-issues-river-basin-management-plans | Yes | Only [LEG-047] Water Framework Directive (retained). **The RBMP statutory planning and monitoring cycle has no POL record** | High that the gap exists; the consultation itself is open, so §3 defers it, but the underlying RBMP cycle is a standing record | defer | **Decided 2026-09-11 — defer.** |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | POL | **LOW PRIORITY** — Natural England Action Plan 2026-27; NE designations programme for areas, sites and trails; Thames Regional Flood and Coastal Committee strategy; King Charles III England Coast Path | https://www.gov.uk/government/publications/natural-england-action-plan-2026-to-2027 | Mixed | None held; corporate or programme-level | Low — recorded so they are not reconsidered next quarter | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: too specific |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | IND | Dry weather and drought in England 2026 summary reports; Water situation national and area monthly reports; Rainfall and river flow weekly reports (all Environment Agency) | https://www.gov.uk/government/publications/dry-weather-and-drought-in-england-2026-summary-reports | **Yes — direct climate monitoring** | **No drought indicator or policy record exists.** [IND-C-105] covers freshwater quality and quantity; [IND-E-044] drought disruption. These are the operational hydrological monitoring series behind them | High. Agency monitoring outside any framework — exactly the §3 case | defer | **Decided 2026-09-11 — defer.** Jonathan 2026-09-11: For timebeing take river flow monitoring etc as outside scope |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | IND | River Tyne, Tees and Wear fish counts (Environment Agency statistical data sets) | https://www.gov.uk/government/statistical-data-sets/river-tyne-fish-counts | Yes — salmonid counts are strongly temperature- and flow-sensitive | **No match in any framework sheet** | Medium — decide whether river-specific series belong as records or as a data source on a national indicator | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: river-specific - needs to be more generalised |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | IND | **CHECK** — The Children's People and Nature Survey for England (Natural England, 2022-2025 updates) | https://www.gov.uk/government/statistics/the-childrens-people-and-nature-survey-for-england-2025-update | No — connection to nature, not a climate-input measure | Overlaps [IND-E-051] Health and wellbeing benefits | Medium — likely already the data source behind IND-E-051; verify rather than add | duplicate | **2026-10-06 — duplicate:** Closed 18 Sep 2026: [IND-E-051] names the People and Nature Survey. **Decided 2026-09-11 — investigate.** Jonathan 2026-09-11: Verify rather than add |
| 2026-09-02 | scan 2026-09-02 (Block 2 agencies) | IND | National assessment of flood and coastal erosion risk in England 2024 (NaFRA2) | https://www.gov.uk/government/publications/national-assessment-of-flood-and-coastal-erosion-risk-in-england-2024 | Yes | [IND-E-042] covers flooding disruption; NaFRA itself — the national risk assessment — has no record | Medium — a risk assessment rather than an indicator; may belong as an IFW or a data source | added | **2026-10-06 — added (UK v27):** [POL-070] (UK v26). **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | POL | **Drought orders and drought permits — the statutory drought response mechanism** (River Severn drought order application and public hearing; drought restriction notices for Teddington, Sunbury and Molesey, Penton Hook–Shepperton, Goring–Culham, St Johns–Osney, all 2026) | https://www.gov.uk/government/publications/notice-of-application-for-a-drought-order-river-severn | **Yes — the statutory instrument triggered by drought** | **None.** [LEG-025] Water Resources Act 1991 and [LEG-023] Water Act 2014 are held, but the drought order mechanism they enable has no record | High. **Third independent confirmation of the drought gap**, and the only one that is statutory. Found only by sweeping `notice`, the type nearly excluded as permit noise | rejected | **2026-10-06 (UK v30):** Mechanism now described in [LEG-025] and [LEG-023] Key_Provisions. **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: add mention to relevant LEG |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | POL | Energy Savings Opportunity Scheme (ESOS), phases 3 and 4 | https://www.gov.uk/guidance/energy-savings-opportunity-scheme-esos | Yes — energy efficiency and emissions | **None in either workbook.** Sits with the queued Climate Change Agreements as a second absent UK climate instrument administered by the EA | High | rejected | **Jonathan 2026-09-10 — D4 energy-system policy out of scope.** No clear nature dimension |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | POL | Storm overflow assessment framework 2025 (Environment Agency) | https://www.gov.uk/government/publications/storm-overflow-assessment-framework-2025 | Indirect — rainfall-driven spill frequency | **None** | Medium — an assessment framework; may be IFW rather than POL | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: primarily operational guidance so out of scope |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | POL | Species Recovery Programme (projects awarded funding 2026–2029; 'over 350 threatened species to benefit') | https://www.gov.uk/government/publications/species-recovery-programme-projects-awarded-funding-for-2026-to-2029 | Yes — species status under climate pressure | **None.** [BIP-019] and [BIP-051] are international species indicators, not this programme | High — a substantial NE delivery programme | added | **2026-10-06 — added (UK v27):** [POL-104]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | POL | Local Sites (Local Wildlife Sites) — selection, management and nature conservation guidance | https://www.gov.uk/guidance/selecting-and-managing-local-sites | Indirect | **None.** A whole tier of non-statutory site designation is absent, below SSSI level | Medium — decide whether the Local Sites system warrants a record | added | **2026-10-06 — added (UK v27):** [POL-105]. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | POL | Agroforestry funding and grants; Tree Production Innovation Fund; Tree Production Capital Grant (both currently closed) | https://www.gov.uk/government/publications/funding-and-grants-for-agroforestry | Yes — tree cover and carbon | No agroforestry record; [POL-055] EWCO and [POL-011] England Trees Action Plan are held | Medium — closed funds may warrant retired records rather than live ones | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: reject if closed fund no longer active |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | IND | UK bluefin tuna fishery (opened 2026; commercial fishery in UK waters) | https://www.gov.uk/guidance/bluefin-tuna-bft-commercial-fishery-within-uk-waters | **Yes — a range-shift signal**; bluefin tuna returning to UK waters is widely read as a warming indicator | **None** | Medium — decide whether a fishery is an indicator or a policy record; the *distribution shift* is the climate-relevant quantity | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: unless clear monitoring indicator |
| 2026-09-02 | scan 2026-09-02 (B2 title sweep) | IND | Marine ecological events surfaced in Block 2: South West octopus bloom (MMO tracking page opened); seaweed surveys finding species new to science; Atlantic salmon stocks in the Derwent catchment | https://www.gov.uk/guidance/mmo-updates-on-the-octopus-bloom | Yes — anomalous marine events are climate-linked | None | Low–medium — event reporting rather than indicators, but the octopus bloom prompted a standing MMO monitoring page, which may itself be a record | rejected | **Decided 2026-09-11 — rejected.** Jonathan 2026-09-11: event reporting out of scope |
| 2026-09-02 | scan 2026-09-02 (JNCC own site) | POL | JNCC Signpost Series — 'Integrating nature's value into land-use decisions across the UK' (2 Sep 2026) | https://jncc.gov.uk/news/ | Indirect — natural capital in land-use decisions | None; relates to [POL-009] Land Use Framework | Low–medium — an evidence report rather than a policy; assess whether the Signpost Series warrants a record | done | **2026-10-06 (UK v30):** Mention and series link added to [ORG-004]. **Decided 2026-09-11 — investigate.** Jonathan 2026-09-11: Add mention and link for whole series to JNCC entry |
| 2026-09-02 | scan 2026-09-02 (JNCC own site) | POL | JNCC evidence review on Northern Ireland peatland restoration, produced for DAERA (3 Aug 2026) | https://jncc.gov.uk/news/ | Yes — peatland condition and carbon | None. NI remains the least represented nation; no England or NI peatland record ([POL-066] Peatland ACTION is Scotland) | Medium | added | **2026-10-06 — added (UK v27):** [POL-106] Northern Ireland Peatland Strategy to 2040 — the strategy is the record; JNCC Report 828 cited in its prose. **Decided 2026-09-11 — add.** |
| 2026-09-02 | scan 2026-09-02 (JNCC own site) | IFW | **WATCH — UKBI 2026 not yet published.** [IFW-03] records 'JNCC UK Biodiversity Indicators **2025**'. No 2026 refresh appeared in the 6 Jul – 2 Sep window; UKBI is typically an autumn release | https://jncc.gov.uk/our-work/uk-biodiversity-indicators/ | Yes | [IFW-03] and its 77 JNCC indicator rows | High that no refresh has occurred yet. **Flag for the next scan**: a UKBI refresh changes indicator records wholesale and is the single highest-impact event on the horizon for the indicators workbook | investigate | **Decided 2026-09-11 — investigate.** Jonathan 2026-09-11: watch - nothing to decide? |
| 2026-09-02 | scan 2026-09-02 (Block 3 depts) | POL | **UK Emissions Trading Scheme (UK ETS)** — the scheme itself, plus its 2026 scope expansion to waste | https://www.gov.uk/government/publications/uk-emissions-trading-scheme-uk-ets-policy-overview | Yes | **Internal inconsistency, not a judgement call**: [ORG-013] UK ETS Authority exists *to administer the scheme* and [LEG-014] Energy Act 2023 and [LEG-030] GHG Emissions Trading Scheme Order underpin it, so the workbook already asserts a chain whose middle link has no record. `General_Type` would be Economic / market instrument | High — the strongest of the Block 3 rows, and the same adjacent-record pattern as 30by30/[POL-022] | defer | **Decided 2026-09-11 — defer.** Jonathan 2026-09-11: assume out of scope for moment |
| 2026-09-02 | scan 2026-09-02 (Block 3 depts) | POL | Greenhouse gas removals (GGR) programme — independent review and government response (2026) | https://www.gov.uk/government/publications/greenhouse-gas-removals-ggrs-independent-review | Yes | [IND-C-050] GGR portfolio indicator is held. **Note the weaker inference**: that indicator exists because the CCC's monitoring framework tracks GGR, which does not by itself establish that the GGR programme belongs in the governance workbook. Treat as a scope question, not a proven gap | **Medium, corrected down from High.** Decide alongside the energy-system scope question below; if DESNZ energy policy is in scope this is a clear add, if not it is a clear exclude | added | **2026-10-06 — added (UK v27):** [POL-107] — response covers nature-based removals and biomass land use. **Decided 2026-09-11 — add.** Jonathan 2026-09-11: includes policies with clear biodiversity / habitat implications? |
| 2026-09-02 | scan 2026-09-02 (Block 3 depts) | POL | Sustainable aviation fuel (SAF) revenue certainty mechanism — contract allocation strategy | https://www.gov.uk/government/publications/sustainable-aviation-fuel-saf-revenue-certainty-mechanism-contract-allocation-strategy | Yes | [IND-C-041] SAF blend rate indicator is held, for the same reason as GGR — the CCC tracks it. **Not by itself evidence that the mechanism belongs in the governance workbook** | **Medium, corrected down from High.** Same scope question as GGR | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (Block 3 depts) | POL | National Policy Statements as a class — ports NPS and proposed amendments (DfT); nuclear energy infrastructure NPS review (DESNZ) | https://www.gov.uk/government/publications/the-national-policy-statement-for-ports | Indirect — NPSs govern consenting of infrastructure with habitat and marine effects | Only [LEG-054] Planning Act 2008. **No NPS records at all** | Medium — a scope decision: if NPSs are in, several exist | rejected | **2026-10-06 (UK v30):** Exclusion recorded in [POL-050]. **Jonathan 2026-09-10 — D7 NPSs not in scope.** Note the exclusion in [POL-050] NPPF so the next scan does not re-raise it |
| 2026-09-02 | scan 2026-09-02 (Block 3 depts) | POL | **LOW PRIORITY** — Clean flexibility roadmap; Corporate Power Purchase Agreements; Ecodesign CE marking; Electric Vehicle Excise Duty; Net zero ports call for evidence | https://www.gov.uk/government/publications/clean-flexibility-roadmap | Yes but energy-system rather than nature-climate | [POL-005] Clean Power 2030 and [ORG-010] NESO are held | Low — decide how far energy-system policy belongs in a climate-*nature* catalogue; recorded so the question is not reopened each quarter | rejected | **Jonathan 2026-09-10 — D4 energy-system policy out of scope.** No clear nature dimension |
| 2026-09-02 | scan 2026-09-02 (legislation.gov.uk) | LEG | **Sustainable Aviation Fuel Act 2026** (2026 c. 9) | https://www.legislation.gov.uk/ukpga/2026/9 | Yes | [IND-C-041] SAF blend rate is held as a CCC framework indicator. **That does not establish that the Act belongs in the Legislation sheet** — the inference from indicator to statute is weak. What *does* stand on its own: it is a 2026 Act in the climate domain, and only 1 of 27 such Acts is currently held | **Medium, corrected down from High.** Justify on the legislative-backlog finding rather than on the indicator | defer | **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** SAF Act: hold pending the D4 boundary call - aviation fuel feedstock may be the 'energy crops' nature dimension |
| 2026-09-02 | scan 2026-09-02 (legislation.gov.uk) | LEG | Taxation (Energy and Vehicles) Act 2026 (2026 c. 26); Finance Act 2026 (2026 c. 11 — check for CBAM provisions) | https://www.legislation.gov.uk/ukpga/2026/26 | Yes — carbon and energy taxation | [LEG-031] Finance Act 2020 and [LEG-030] GHG Emissions Trading Scheme Order are held; the 2026 instruments are not | Medium — confirm which provisions are climate-relevant before writing | add | **6 Oct 2026: folded into the D8 legislative backlog audit — not yet run.** **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Fold into the backlog audit rather than adding piecemeal |
| 2026-09-02 | scan 2026-09-02 (legislation.gov.uk) | LEG | English Devolution and Community Empowerment Act 2026 (2026 c. 23) | https://www.legislation.gov.uk/ukpga/2026/23 | Indirect | Local government reorganisation changes the responsible authorities behind [POL-014] Local Nature Recovery Strategies and [ORG-037] Local Authorities | Medium — an amendment to existing records rather than a new one | add | **6 Oct 2026: folded into the D8 legislative backlog audit — not yet run.** **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Fold into the backlog audit rather than adding piecemeal |
| 2026-09-02 | scan 2026-09-02 (legislation.gov.uk) | LEG | **AUDIT FINDING — only one of the 27 UK Public General Acts of 2026 is held.** The Legislation sheet contains [LEG-010] BBNJ Act 2026 alone; c.1–c.27 were enumerated and at least four are climate- or nature-relevant | https://www.legislation.gov.uk/ukpga/2026 | n/a | Whole-sheet currency question | High. **Recommend a one-off legislative backlog audit covering 2024–2026**, alongside the devolved sweep already recommended | add | **6 Oct 2026: the D8 legislative backlog audit — not yet run.** **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Fold into the backlog audit rather than adding piecemeal |
| 2026-09-02 | scan 2026-09-02 (CCC) | IFW | **CURRENCY CHECK — CCC Adaptation Monitoring Framework published 20 May 2026.** [IFW-02] records 'CCC Mitigation & Adaptation Monitoring Framework / UK Net Zero Strategy' with 111 indicator rows | https://www.theccc.org.uk/publications/ | Yes | [IFW-02] and its 111 CCC indicator rows | High that a new Adaptation Monitoring Framework was published. **Second framework-currency question alongside the EIF** — verify whether the 111 rows reflect it | added | **2026-10-06 — added (UK v27):** Done: [IFW-10] and [IFW-11], indicators v17 and v23. **Decided 2026-09-11 — add.** Jonathan 2026-09-11: Update existing record - need also to ensure framework indicators updated? |
| 2026-09-02 | scan 2026-09-02 (CCC) | POL | Memorandum of Understanding between the CCC and Environmental Standards Scotland (23 Jul 2026) | https://www.theccc.org.uk/publications/ | n/a — governance relationship | **Links [ORG-003] CCC to Environmental Standards Scotland, which is itself queued as a missing ORG.** Supports adding ESS | Medium — an MoU may be a link rather than a record | added | **2026-10-06 — added (UK v27):** Recorded in [ORG-045] Remit_And_Powers — a relationship, not a record. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 (CCC) | POL | **LOW PRIORITY** — CCC supporting research in window: synergies between local climate mitigation and adaptation (25 Aug); local authorities and the Seventh Carbon Budget (8 Jul); letter to DAERA on agricultural policy (19 Aug) | https://www.theccc.org.uk/publications/ | Yes | Supporting research and correspondence, not records | Low — recorded as screened | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (OEP) | POL | **NIL RETURN IN WINDOW.** OEP published only corporate items 6 Jul – 2 Sep: whistleblowing report (19 Aug), Corporate Plan 2026/27–2027/28 (10 Aug), Annual Report and Accounts (9 Jul). Its neonicotinoid emergency-authorisation investigation (2 Jul) and NI natural-environment progress report (24 Jun) fall just before the window | https://www.theoep.org.uk/publications/reports-and-publications | n/a | [ORG-007] OEP | High — a clean negative, recorded so the source is demonstrably scanned | rejected | **Decided 2026-09-11 — rejected.** |
| 2026-09-02 | scan 2026-09-02 (devolved) | POL | **Scottish Biodiversity Strategy to 2045** and **Scottish Biodiversity Delivery Plan 2024–2030** | https://www.gov.scot/policies/biodiversity/ | Yes — the Strategy names climate change as a key pressure | **Neither is held.** Only [LEG-032] Nature Conservation (Scotland) Act 2004 mentions the strategy in passing. England's equivalents ([POL-001] EIP, [POL-003] NBSAP) are held, so Scotland's strategic layer is missing while England's is present | High — primary source. Pairs with the queued Natural Environment (Scotland) Act 2026, which mandates targets and indicators under this strategy | added | **2026-10-06 — added (UK v27):** [POL-108] Strategy and [POL-109] Delivery Plan 2024–2030. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 (devolved) | ORG | Scottish Biodiversity Programme (Scottish Government with NatureScot) | https://www.gov.scot/policies/biodiversity/ | n/a — coordination body | **None.** Analogous to [POL-022] 30×30 Technical Working Group | Medium | rejected | **2026-10-06 — rejected:** 6 Oct 2026: no body or programme of that name in the current strategy or delivery plan; governance (Strategic Biodiversity Council, delivery board) recorded in [POL-108] prose. **Jonathan 2026-09-10 — D8 legislative + devolved backlog audit commissioned.** Core of the devolved audit |
| 2026-09-02 | scan 2026-09-02 (devolved) | POL | Scotland's 30 by 30 commitment (distinct from England's, delivered via NatureScot) | https://www.gov.scot/policies/biodiversity/ | Yes | [POL-022] is the UK-level technical working group; the **England** 30by30 delivery plan is separately queued. **Scotland's commitment has no record** | Medium — confirms 30by30 needs per-nation records, not one | added | **2026-10-06 — added (UK v27):** [POL-110]; reciprocal [INT-L-007] (intl v17). **Jonathan 2026-09-10 — D6 30by30 recorded per nation.** Also chase Wales and NI 30by30 commitments - neither yet scanned |
| 2026-09-02 | correction 2026-09-02 | — | **METHOD CORRECTION affecting the three rows above.** An earlier framing claimed that holding an indicator without a corresponding policy or legislation record was 'positive evidence of a gap'. That is too strong. The indicators workbook catalogues *frameworks' indicators*: an indicator exists because a framework tracks that quantity, which is a statement about the framework, not about what the governance workbook should contain. The inference only holds where an indicator's `Policy_Goal` or `Indirect_Policy_Links` field **names a policy or Act that has no record** — then the workbook is internally inconsistent, which is a defect rather than a scope judgement. [ORG-013]/[LEG-014]/UK ETS meets that test; SAF and GGR do not | — | n/a | n/a | High | n/a | **Jonathan 2026-09-10 — record only.** Method note, not a candidate |
| 2026-10-06 | legislation link audit | LEG | **CHECK, not an addition** — [LEG-044] Plant Health (England) Order 2015 is marked **revoked** on legislation.gov.uk; the record's Status still reads 'In force (as amended)' | https://www.legislation.gov.uk/uksi/2015/610/contents | Indirect — the plant-health regime runs on climate-suitability risk scoring ([POL-076]) | Inbound from [ORG-020], [POL-033], [POL-034], [POL-052], [INT-L-023]; [POL-077] no longer cites it (v27) | High that it is revoked; the revoking instrument and current GB regime not yet identified | investigate | Jonathan 2026-10-06: keep the record unchanged for now. To do: identify the current GB plant-health legislation, decide repurpose vs retire, and whether the Legislation `Status` vocabulary needs a 'Revoked' stem. `check_legislation_links.py` warns on this record at every release until resolved. |

<!-- Append new rows directly above this comment. Keep the columns in order.
     Date format YYYY-MM-DD. "Found by" = the assessment field or "scan YYYY-MM-DD". -->

---

## Round-2 triage outcome (11 September 2026)

All 95 candidates now carry a decision: **42 add · 29 rejected · 11 investigate · 9 defer · 3 previously added · 1 method note**. No row remains `pending`.

Conditions and questions attached to decisions, which must be honoured when writing:

- **Drought orders** — rejected as a record, but "add mention to relevant LEG": note the drought-order mechanism in [LEG-025] Water Resources Act 1991 and [LEG-023] Water Act 2014.
- **JNCC Signpost Series** — add a mention and link for the whole series to the JNCC [ORG-004] entry rather than a record per report.
- **Agroforestry / Tree Production funds** — "reject if closed fund no longer active": confirm status before rejecting; the Tree Production funds are marked closed, agroforestry funding may not be.
- **Humber 2100+** — rejected as too specific; consider folding into [POL-045] FCERM rather than dropping.
- **National Policy Statements** — excluded as a class; record the exclusion in [POL-050] NPPF so later scans do not re-raise it.
- **EIF and CCC framework rows** — "update existing record, and ensure framework indicators up to date": these are the two framework-currency questions, and the indicator rows are the work, not the framework record.
- **TE2100** — added deliberately as an example despite being generally out of scope; note that reasoning on the record so it is not later removed as inconsistent.

## Two queries answered at source (17 September 2026)

**"Is the 30by30 assessment framework a new set of indicators?"** — **No.** It is an eligibility and assurance *standard*: three criteria, three tiers, two assessment routes. It creates no new monitoring, running instead on the existing SSSI Protected Sites regime, NNR records and Landscape Recovery scheme data. It yields one headline measure — the share of England in Gold tier — already reported internationally via [GBF-013]. **The queue row's record type has been corrected from `IFW` to `POL` / Guidance / Methodology.** My original classification was wrong.

**"Is the Cormorant index used to monitor policy targets?"** — **No.** The publication states the indices are released early as provisional *"to enable their use for operational purposes"*: Natural England licensing of fish-eating bird control to protect fisheries (A06/A07). The parent BTO/RSPB/JNCC Wetland Bird Survey is already held at the right level of generality as [IND-J-010] and [IND-J-013], and wintering waterbird distribution is the established climate signal. Rejection confirmed, on the same reasoning as the river fish counts.

**New scope item arising:** the 30by30 guidance states that separate approaches exist for Northern Ireland, Scotland, Wales **and at sea**. 30by30 marine has not been scanned at all, and is not in the queue.

## Framework currency check — EIF and CCC (17 September 2026)

Commissioned by the round-2 triage condition *"update existing record, and ensure framework indicators up to date"*. Sources read directly: the ten EIF theme pages on gov.uk, the EIF collection and Recent updates pages, and the CCC's Mitigation and Adaptation Monitoring Framework pages. Confidence **high** for EIF, **high** for the CCC adaptation finding, **medium** for the CCC mitigation finding (the CCC publishes no fixed enumerated mitigation indicator list to diff against).

### IFW-01 Environmental Indicator Framework — current. No indicator changes.

The published EIF is **66 indicators across themes A–K** (there is no theme I). All 66 held codes and names match the published set one for one: no additions, no retirements, no renumbering. The six 2026 updates (13 Feb, 17 Mar, 15 Apr, 13 May, 3 Jul, 19 Aug) were **data refreshes**, not structural changes — Defra moved the EIF off an annual cycle to rolling updates as data arrive, so "updated" on a theme page means new figures, not new indicators.

Three amendments to [IFW-01], all minor:

1. `Official_Link` is `https://oifdata.defra.gov.uk/`, which now redirects to the gov.uk collection page. Repoint to the collection: `https://www.gov.uk/government/collections/environmental-indicator-framework`.
2. **E5** published name is "Percentage of **the** annual growth of trees in English woodlands that is harvested"; [IND-E-037] omits "the".
3. **H1** published name is "Abatement of the number of invasive non-native species entering and establishing **against a baseline**"; [IND-E-052] omits the final three words.

**Implication for the scan protocol:** the EIF no longer has an annual refresh to watch for. The ad-hoc trigger "a new EIF indicator release" in `POLICY_SCAN_PROTOCOL.md` §1 should become a check of the *Recent updates* page, which is the only place a structural change would surface.

### IFW-02 CCC — materially out of date, and the record conflates two frameworks

The CCC now publishes these as **two separate monitoring frameworks**, on different cycles:

- **CCC Mitigation Monitoring Framework** — published 20 June 2025, updated June 2026.
- **CCC Adaptation Monitoring Framework** — published **20 May 2026**, replacing the Adaptation Monitoring Framework 2023–2025.

[IFW-02] covers both under one Framework_ID ("CCC Mitigation & Adaptation Monitoring Framework / UK Net Zero Strategy", 111 rows). **Recommend splitting into [IFW-02] mitigation and a new [IFW-10] adaptation**, since they now have separate sources, separate structures and separate update cycles, and a single Record_Count hides that one half is current and the other is not.

**Adaptation — 32 rows, superseded, and structurally incomplete.** All 32 adaptation rows cite *CCC Progress in Adapting to Climate Change 2023 Report to Parliament*. The May 2026 refresh is not an update but a rebuild: it is anchored on **CCRA4-IA** rather than CCRA3, it takes its ambition from the **21 national adaptation objectives** in *A Well-Adapted UK* (2026), and it restructures monitoring around **14 systems** — Health; Built environment and communities; Public services; Cultural heritage; Water and wastewater; Energy; Transport; Waste; Digital and telecoms; Land; Sea; Food security; Economy and finance; National security and international engagement — each with a published monitoring map of objective, targets, actions, enablers and policies.

Mapping the held sector labels onto those systems:

| Held sector | Rows | Current system | Status |
|---|---|---|---|
| Nature (Adaptation) | 8 | Land / Sea | Split across two systems |
| Working Lands & Seas (Adaptation) | 7 | Land / Sea | Split across two systems |
| Water Supply (Adaptation) | 7 | Water and wastewater | Narrower than the system (no wastewater) |
| Food Security (Adaptation) | 5 | Food security | Retained |
| Health (Adaptation) | 5 | Health | Retained |

Nine of the fourteen systems have **no held rows at all**: Built environment and communities, Public services, Cultural heritage, Energy, Transport, Waste, Digital and telecoms, Economy and finance, National security and international engagement. Several are out of this project's climate–nature scope and should stay that way, but Built environment, Energy, Transport and Economy and finance are not obviously so.

So the adaptation half is not stale, it is **structurally incomplete against the current framework**, and patching row by row will not fix it. The work is a re-extraction from the 14 system monitoring maps, with an explicit scope decision on which systems the project catalogues. That is a larger job than a triage row and should be queued as its own task.

**Mitigation — 79 rows, defensible but benchmarked on a superseded plan.** The mitigation framework publishes a *method*, not a fixed indicator list: indicators are selected per progress report. So the held rows are a synthesis rather than a transcription, and cannot be diffed. What has moved is the benchmark. The CCC now measures against the Government's **Carbon Budget and Growth Delivery Plan (CBGDP, October 2025)**, which replaced the Carbon Budget Delivery Plan 2023. **24 of the 111 rows** name the CBDP in `Source_Reference` or `Framework_Classification` and need their benchmark checked against the CBGDP; 47 cite "CCC Monitoring Framework 2025 – <sector>", which remains a valid citation given the June 2026 update, but the version should be stated.

Two vocabulary mismatches with the CCC's own sector definitions: held **"Waste & F-gases"** combines two sectors the CCC keeps separate, and held **"Fuel Supply / Hydrogen"** is the CCC's "Fuel supply". Both are the Government's groupings, not the CCC's.

### Knock-on to the governance workbook — found by this check, not previously queued

| Record | Held as | Position at 17 Sep 2026 | Action |
|---|---|---|---|
| [POL-017] | Climate Change Risk Assessment (CCRA3) 2022 | CCRA4-IA published 20 May 2026 as *A Well-Adapted UK*; the statutory CCRA4 follows | Add a CCRA4-IA record; mark [POL-017] superseded, do not delete |
| [POL-004] | UK Net Zero Strategy / Carbon Budget Delivery Plan (CBDP) 2023 | Superseded by the CBGDP, October 2025 | Add a CBGDP record; mark [POL-004] superseded |
| [POL-002] | National Adaptation Programme (NAP3) 2023–2028 | Still current; NAP4 due 2028 | No action |

New candidates arising, all confirmed at source:

| Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 | framework currency check | POL | A Well-Adapted UK — Fourth Independent Assessment of UK Climate Risk (CCRA4-IA), CCC, 20 May 2026. **Technical Report led by the Met Office (Prof Jason Lowe)** — a direct Met Office → policy channel | https://www.theccc.org.uk/publication/a-well-adapted-uk/ | Yes | Supersedes [POL-017] CCRA3 in part | High | added | **2026-10-06 — added (UK v32):** [POL-113].  |
| 2026-09-17 | framework currency check | POL | Carbon Budget and Growth Delivery Plan (CBGDP), October 2025 | https://www.theccc.org.uk/publication/ccc-monitoring-framework/ (CCC's citation; locate the primary DESNZ page before writing) | Yes | Supersedes [POL-004] CBDP 2023 | High | added | **2026-10-06 — added (UK v32):** [POL-112].  |
| 2026-09-17 | framework currency check | IFW | CCC Adaptation Monitoring Framework 2026 — split out of [IFW-02] | https://www.theccc.org.uk/publication/ccc-adaptation-monitoring-framework/ | Yes | [IFW-02] | High | done | **Completed indicators v17 (split) and v23 (re-extraction).** [IFW-10] holds the 38 proposed targets of the 2026 framework; [IFW-11] holds the superseded 2023–2025 set. |
| 2026-09-17 | framework currency check | POL | Progress in reducing emissions: 2026 report to Parliament, CCC, 24 June 2026 | https://www.theccc.org.uk/publication/progress-in-reducing-emissions-2026-report-to-parliament/ | Yes | Annual series — decide once whether the project holds the series or each edition | Medium | added | **2026-10-06 — added (UK v32):** [POL-114] — one record for the annual CCC progress-report series (decision 6 Oct 2026).  |
| 2026-09-17 | framework currency check | POL | Third Climate Change Adaptation Programme for Northern Ireland (NICCAP3), 2026 | https://www.theccc.org.uk/publication/ccc-adaptation-monitoring-framework/ (verify at DAERA before writing) | Yes | Devolved backlog (D8) | Medium | added | **2026-10-06 — added (UK v32):** [POL-115] (published 19 Mar 2026).  |
| 2026-09-17 | framework currency check | POL | Scotland's Climate Change Plan 2026–2040, March 2026 | https://www.theccc.org.uk/publication/ccc-monitoring-framework/ (verify at gov.scot before writing) | Yes | Devolved backlog (D8) | Medium | added | **2026-10-06 — added (UK v32):** [POL-116] (final plan 24 Mar 2026).  |

**Method note.** Both the NICCAP3 and Scotland Climate Change Plan rows were found in the CCC's own framework pages, not in a devolved-administration scan — which is the outstanding gap in the current scan. A secondary source naming a primary document is a legitimate *pointer*, but the record must be written from the primary. Do not write these two until gov.scot and DAERA have been read directly.

## Controlled vocabulary decision — General_Type (17 September 2026)

**Status: DECIDED by Jonathan, 17 September 2026. Ready to execute as a single edit.** This was the blocker on writing the 42 approved records.

### The finding that reframes it

The Data Dictionary cell for `General_Type` reads, literally:

> `Public Bodies: ... Devolved Administration | Devolved Public Body | Local Government (collective) | Government Unit / Authority | Executive Agency | Ministerial Department; Legislation: ...`

The leading `...` is **in the cell**. The six-term list was never a deliberate closed vocabulary — it is an elided one. So the 21 records on undeclared terms are not drift by the records; the dictionary lost terms. This is a dictionary repair, and the terms in use are, with two exceptions, the standard UK public-body taxonomy.

Corroborating this: `check_links.py` **does not validate `General_Type` against the Data Dictionary at all** — there is no reference to the column in the file. That is why 21 non-conforming records sat behind a passing release gate for however long. See the follow-on action below.

### Public Bodies — final vocabulary (closed, 12 terms, 44 records)

| Term | Records | Change |
|---|---|---|
| Ministerial Department | 7 | — |
| Non-Ministerial Department | 3 | **Declare** (was in use, undeclared) |
| Executive Agency | 6 | **Declare unchanged**; gains [ORG-017] Met Office |
| Executive NDPB | 7 | **Declare**; gains [ORG-007] OEP |
| Advisory NDPB | 3 | **Declare** |
| Independent Regulator | 4 | **Declare**; gains [ORG-040] FCA |
| Statutory corporation | 2 | **NEW TERM** |
| Devolved Administration | 3 | — |
| Devolved Public Body | 6 | — |
| Government Unit / Authority | 1 | — |
| Local Government (collective) | 1 | — |
| Non-governmental body / Partnership | 1 | **NEW TERM**, replacing "NGO Partnership / Coalition" |

**Retired terms:** `Independent Statutory Body` (4 records redistributed, term deleted), `Executive Agency / Trading Fund` (1 record moved, term deleted), `NGO Partnership / Coalition` (renamed).

**Definition to add for the new term:**

> **Statutory corporation** — a body corporate or corporation sole established by or under statute, which is not a department, executive agency or NDPB, and is not a servant or agent of the Crown.

### Record-level changes (6 records)

| Record | From | To | Basis |
|---|---|---|---|
| [ORG-007] Office for Environmental Protection | Independent Statutory Body | **Executive NDPB** | Jonathan's call |
| [ORG-040] Financial Conduct Authority | Independent Statutory Body | **Independent Regulator** | Jonathan's call. Note: technically a company limited by guarantee, not a statutory corporation — which is why a functional label fits it better than a constitutional one |
| [ORG-031] NI Climate Commissioner | Independent Statutory Body | **Statutory corporation** | SR 2025 No. 78 reg. 5: *"The person for the time being holding the office of the Commissioner is by that name a corporation sole… not to be regarded as the servant or agent of the Crown"* |
| [ORG-024] The Crown Estate | Independent Statutory Body | **Statutory corporation** | Body corporate under the Crown Estate Act 1961 as amended 2025 |
| [ORG-017] Met Office | Executive Agency / Trading Fund | **Executive Agency** | Compound token retired. Move the trading-fund status to `Remit_And_Powers` — it is a fact about the body, not a type of body, and a vocabulary that admits compounds will grow them |
| [ORG-042] State of Nature Partnership | NGO Partnership / Coalition | **Non-governmental body / Partnership** | Generalised so the term is not single-purpose |

### Legislation — one addition

`Retained EU Law` is in use on [LEG-047] Water Framework Directive (retained UK law) and is undeclared. **Declare it.** Legislation then reads: Primary Legislation (50) | Secondary Legislation (15) | Bill (pre-legislative) (1) | Retained EU Law (1).

**Policies & Activities needs no change** — nine terms declared, nine in use, no drift.

### Data Dictionary — exact replacement

Row `All sheets` / `General_Type`, column `Controlled_Vocabulary`, replace the whole cell with:

> `Public Bodies: Ministerial Department | Non-Ministerial Department | Executive Agency | Executive NDPB | Advisory NDPB | Independent Regulator | Statutory corporation | Devolved Administration | Devolved Public Body | Government Unit / Authority | Local Government (collective) | Non-governmental body / Partnership; Legislation: Primary Legislation | Secondary Legislation | Bill (pre-legislative) | Retained EU Law`

Replace the `Description` cell, which currently explains only one term, with:

> `Detailed classification within Record_Type. Public Bodies terms follow the standard UK public-body taxonomy, with three project-specific additions: "Independent Regulator" for economic and sectoral regulators; "Statutory corporation" for bodies corporate and corporations sole that are not departments, agencies or NDPBs and are not servants or agents of the Crown; and "Non-governmental body / Partnership" for non-public organisations held on this sheet. "Government Unit / Authority" covers joint cross-government units (e.g. NISTA, [ORG-023]). Note that the Public Bodies sheet holds a small number of non-public organisations; the sheet name understates its scope and is retained because the dashboard build scripts key on it.`

### Corrections to [ORG-031] found while verifying

The office was established by **The Northern Ireland Climate Commissioner Regulations (Northern Ireland) 2025, SR 2025 No. 78**, made by The Executive Office on 8 April 2025, in operation 9 April 2025, under s.50 of the Climate Change Act (Northern Ireland) 2022.

1. `Lead_Department` reads `[ORG-036] DAERA`. **Wrong** — the s.50 duty and the regulations both sit with **The Executive Office**. The Executive Office has no ORG record, so this is a missing record, not just a wrong value (queued below).
2. `Link` points at the 2022 Act. Repoint to the regulations.
3. `Statutory_Duties` reads as though the office existed from 2022. Note that establishment was April 2025.

### New records arising

| Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution |
|---|---|---|---|---|---|---|---|---|---|
| 2026-09-17 | vocabulary reconciliation | LEG | The Northern Ireland Climate Commissioner Regulations (Northern Ireland) 2025, SR 2025 No. 78 — Secondary Legislation | https://www.legislation.gov.uk/nisr/2025/78/contents/made | Indirect — establishes the NI climate oversight office | Authority for [ORG-031]; child of [LEG-059] | High | added | **2026-10-06 — added (UK v27):** [LEG-071]; now [ORG-031] Statutory_Role. Write alongside the [ORG-031] correction, not as a separate batch — it is the authority for the classification |
| 2026-09-17 | vocabulary reconciliation | ORG | The Executive Office (TEO), Northern Ireland | https://www.executiveoffice-ni.gov.uk/ | Indirect | Sponsor of [ORG-031]; a department of [ORG-036] | High | rejected | **Jonathan 2026-09-18 — no devolved departments.** Northern Ireland is held at administration level only. [ORG-036] was repurposed from DAERA to the **Northern Ireland Executive** (v23), so [ORG-031] Lead_Department now reads `[ORG-036] Northern Ireland Executive (The Executive Office)` and is correct without a TEO record. |

### Follow-on actions

1. **Add a controlled-vocabulary invariant to `check_links.py`** — a sixth check validating every `General_Type`, and any other `Data_Type: Controlled` column, against the Data Dictionary. Without it this class of drift stays invisible to the release gate, and the gate is the only thing standing between a proposed row and the workbooks. This is the single highest-value change arising from the whole exercise.
2. **UKHSA is unblocked.** It is an executive agency of DHSC and `Executive Agency` is already declared. The blocker was the untidiness of the vocabulary, not anything UKHSA-specific.

### Devolved tier — DECIDED 18 September 2026

The question raised above — [ORG-036] DAERA sitting in `Devolved Administration` alongside the Scottish and Welsh Governments, when it is a department rather than a government — is settled.

**Rule: the four UK administrations are held at administration level, and no devolved department is held as a record.** [ORG-034] Scottish Government, [ORG-035] Welsh Government and now [ORG-036] **Northern Ireland Executive**. Departments are named in prose, in brackets after the administration — `[ORG-036] Northern Ireland Executive (DAERA)`, `[ORG-036] Northern Ireland Executive (The Executive Office)` — so the department is still visible without becoming a node.

Implemented in UK governance **v23**. ORG-036 was repurposed rather than retired, because its fourteen inbound references had always meant "the Northern Ireland administration"; only its name sat at the wrong tier. Updated: ORG-004, ORG-016 (link and prose), ORG-031, LEG-038, LEG-039, LEG-040, LEG-059, POL-028, POL-052, POL-067, POL-069, Cross-Reference Index.

The rule is recorded in the ORG-036 `Remit_And_Powers` text so that a later scan finds it on the record rather than re-raising it. **A future candidate that is a devolved department is rejected on this rule**, and its substance folded into the administration record or into the prose of whatever it sponsors.

Two consequences worth noting:

- Defra sits in this company as England's lead department, which is an asymmetry — there is no "UK Government" or "England" administration record. It has not caused a problem, but it is the mirror image of the question just settled.
- [ORG-014] is still named "Scottish Natural Heritage". It was renamed **NatureScot** in 2020, and other records already refer to it by the new name. Not touched here; flagged as a one-cell correction for the next write.

## RESOLVED — Policy_Sector (18 September 2026)

Found by the new controlled-vocabulary invariant on its first run, and **closed the next day — with a different diagnosis from the one recorded below.**

**The vocabulary was never forked.** A record-sheet re-check found **zero** non-canonical tokens in any of the three workbooks: the 14-class migration made in indicators workbook v11 had been applied everywhere it mattered. What had not been updated was the **Cross-Reference Index** in each governance workbook — a derived sheet, read by nothing, never regenerated after the migration. It held 141 of 177 stale `Policy_Sector` values in the UK workbook and 87 of 103 in the international one, plus five superseded `General_Type` values and four records missing outright (ORG-042, INT-O-033, INT-O-034, INT-O-035).

So the three terms called homeless below — `Air Quality`, `International`, `Cross-cutting` — were **artefacts of a stale copy, not live classes**, and none of the three decisions listed at the end of this section needed making. The original diagnosis was wrong, and is kept here rather than deleted because the reasoning is what sent the fix in the wrong direction for a day.

**Fixed in UK governance v25 / international v16:** both indexes regenerated from source by the new `Data/code/rebuild_xref.py`, which `finalise.py` now runs as step 1 of 4; both Data Dictionaries now declare the 14 classes and document the index as derived; `VOCAB_WARN_ONLY` in `check_links.py` is empty, so `Policy_Sector` is a hard gate condition. The index can no longer drift, because it is rebuilt rather than maintained.

---

*Original entry, 17 September 2026 — superseded by the above.*

`WORKBOOK_WRITE_PROTOCOL.md` §2 states that `Policy_Sector` is one vocabulary of fourteen classes shared by all three workbooks and must not be forked per workbook. It has been forked, in both the dictionaries and the data.

- The **indicators** workbook declares the current fourteen classes and its records conform.
- The **UK governance** workbook declares twelve older slash-style terms; the **international** workbook declares ten.
- The **records** in both governance workbooks use a mixture of the two generations. `Nature & Biodiversity` (655 uses) sits alongside `Nature / Biodiversity` (171); `Land Use & Agriculture` (286) alongside `Land / Agriculture / Planning` (87); `Marine & Fisheries` (165) alongside `Marine` (47); `Governance, Society & Data` (249) alongside `Finance / Governance / Data` (24).

**25 distinct tokens are in use where the protocol specifies 14.** 390 cell values do not match their workbook's declaration.

This is not cosmetic: the governance diagram and the indicator finder both filter on `Policy_Sector`, so `Nature / Biodiversity` and `Nature & Biodiversity` are two separate filter entries today, and a user filtering on one silently misses the records tagged with the other.

**Why it was not fixed in this pass.** Most of the mapping is mechanical, but three terms in use have no home in the fourteen — `Air Quality` (5 uses), `International` (8) and `Cross-cutting` (24) — and two are compounds that would have to be split rather than renamed (`Finance / Governance / Data`, `Agriculture / Biosecurity`). Those are scope decisions, and migrating roughly 900 tokens on a guess would be worse than leaving the fork visible. The invariant therefore reports `Policy_Sector` as a **warning** rather than a gate failure, with the reason stated in `VOCAB_WARN_ONLY` in `check_links.py`.

**Decisions needed before this can be cleared:**

1. Do `Air Quality`, `International` and `Cross-cutting` become additional classes (making it 17), or fold into existing ones?
2. Does `Finance / Governance / Data` split into `Finance` + `Governance, Society & Data` on every record that carries it?
3. Is the three-per-record cap that applies to indicators also to apply to governance records after the split, or do governance records stay uncapped as they are now?

Once settled, the migration is a single scripted pass over two workbooks plus both dictionaries, followed by a dashboard rebuild, and `VOCAB_WARN_ONLY` is emptied.

## CCC benchmark re-derivation — buildings and surface transport done (18 September 2026)

Nine of the 24 CBDP-benchmarked rows on the `CCC Indicators` sheet have been re-derived against the **Carbon Budget and Growth Delivery Plan (October 2025)** and the **CCC Progress in reducing emissions 2026 report (24 June 2026)**. Indicators workbook **v18**.

Buildings and surface transport were taken first because the CCC states the CBGDP reduces emissions more slowly than the CBDP 2023 *in exactly these two sectors* — so this is where a stale benchmark was most likely to be wrong rather than merely out of date. Four of the nine turned out to be substantively wrong, not just stale:

| Record | Was | Now |
|---|---|---|
| IND-C-021 heat pumps | 600,000/year by 2028 (Heat & Buildings Strategy) | Warm Homes Plan: 450,000/year UK-wide by 2030, ~250,000 retrofit — which the CCC says is itself insufficient for the CBGDP. Balanced Pathway ~1.4m retrofit/year by 2035 |
| IND-C-022 EPC C | All homes EPC C by 2035 | No longer government policy. Planned MEES: private rented to EPC C on two metrics by 2030 (~1.8m homes); social rented one metric by 2030, two by 2039 (~1.1m / ~2.9m) |
| IND-C-023 insulation | "CBDP: significant scale-up required"; ECO4 scheme targets | No quantified government target. ECO closed with no replacement, having delivered ~a third of the retrofit market. CCC tracks cavity wall insulation coverage, on track |
| IND-C-027 non-residential | CBDP pathway | CBGDP buildings pathway; Public Sector Decarbonisation Scheme closed, non-residential MEES (EPC B by 2030) still unconfirmed since the 2019 consultation |

Three were pathway repoints only (IND-C-003, IND-C-019, IND-C-025: CBDP → CBGDP sectoral pathway). One was **confirmed unchanged** — IND-C-018, the 300,000 public charge points by 2030 target, which the CCC assesses as on track; the 2025 figure (88,000 devices) was added. IND-C-016 electric vans was rebenchmarked on CBGDP uptake assumptions with the 2025 actual (9.5% of new van sales, behind the CBGDP).

**UPDATE, same day — the remaining fifteen are done (indicators v19). The marker is cleared from all 24.**

Eleven are fully re-derived. Four of those were wrong rather than stale: IND-C-006 offshore wind (Clean Power 2030 is **43–50 GW by 2030**, not "50 GW including 5 GW floating"); IND-C-008 solar (**45–47 GW by 2030 is a government ambition**, which this row had mislabelled as a CCC pathway figure, and the 70 GW by 2035 Net Zero Strategy number is not the current benchmark); IND-C-035 peatland and IND-C-036 tree planting, both of which now benchmark against the **combined ambition of the four administrations** rather than the England-only figures previously held. IND-C-012 replaced an AR4 reference with AR7's record 8.2 GW. IND-C-028 was recast: the CBGDP sets no industrial energy-intensity target and makes electrification the primary route, so the benchmark is now the Balanced Pathway's 36% electric share of industrial energy demand by 2030 against 27% in 2024.

**Four were marked PARTIAL — and are now resolved (v20) by reading the CBGDP itself,** the Section 14 Report and its technical annex, rather than the CCC's commentary on it.

**The main finding is negative, and it matters more than the numbers.** For three of the four, *the CBGDP sets no target at all* — so the figures those rows carried were not out of date, they had no current government referent:

- **IND-C-031 hydrogen** — no capacity target. Production capacity is **derived from modelled demand**, assuming supply always equals demand, with CCUS-enabled plants at a 90% load factor and electrolytic at 60%. Delivery runs through allocation rounds (HAR1 11 projects funded, HAR2 27 shortlisted, HAR3 by 2026, HAR4 from 2028), and a new Hydrogen Strategy is in preparation to set out the scale government envisages. The 10 GW by 2030 came from the 2021 Hydrogen Strategy and is not restated.
- **IND-C-038 fertiliser** — no quantified target. Agricultural nitrous oxide is addressed through named advice-and-guidance policies with market-led uptake: agronomist-led nutrient management plans, precision farming with variable-rate nitrogen technology, grass and herbal leys, clover at 20%+ of mixed grassland, slurry nitrogen analysis.
- **IND-C-055 energy productivity** — the 15% final-energy-demand reduction target appears in **neither** the Section 14 Report **nor** the technical annex. The CBGDP works through sectoral policy lines (industrial energy efficiency, domestic energy efficiency) instead of an economy-wide demand target.

**IND-C-030 CCS** is the one row with a real number, and it is an order of magnitude below what the row carried. The Track-1 clusters enable up to **4 MtCO₂/year (East Coast) and 4.5 MtCO₂/year (HyNet) at full utilisation — about 8.5 MtCO₂/year combined** — against £9.4 billion allocated at Spending Review 2025, with Track-2 (Acorn, Viking) FID due later this Parliament and gas-terminal CCUS savings from 2034. The previous benchmark was 20–30 MtCO₂/year by 2030, from the Net Zero Strategy 2021.

**No row on the CCC Indicators sheet now carries a superseded or unverified benchmark.**

A method point worth keeping: three of these four could only be settled by reading the plan itself. The CCC's report says what the CBGDP does *differently*, not what it omits, so a benchmark with no successor looks identical to one the commentary simply did not mention. Where a row's benchmark cannot be found in the source plan, "no current target" is a finding to record, not a gap to leave blank.

**Also corrected, outside the original scope:** IND-C-014 read "ban on new petrol/diesel cars by 2035". The phase-out of new petrol and diesel **cars is 2030**; 2035 applies to vans. My earlier note in this file attributed that error to IND-C-015, which was wrong — IND-C-015 is cumulative electric car stock and is fine.

*(The note that previously stood here misidentified the row as IND-C-015; it was IND-C-014, and it has now been corrected in v19 — see the update above.)*

## SDG sheet climate-scored, and the dashboard's blank-vs-zero bug fixed (18 September 2026)

Indicators **v21**. All 173 SDG Indicators rows now carry `Climate_Score`, `Climate_Dependency` and `Climate_Rationale`. Distribution: **113 score 0, 36 score 1, 20 score 2, 4 score 3** — which is the shape the SDG framework should have, most of it being social, economic and statistical rather than environmental. The four 3s are 6.4.2 water stress, 6.6.1 water-related ecosystem extent, 11.6.2 PM2.5/PM10 and 14.3.1 marine acidity.

**The bug this closes.** `build_indicator_finder.py` read the score through `cell_int()`, which returns 0 for a blank cell. The 173 unassessed SDG records therefore rendered as climate score 0, indistinguishable from the 283 records that were assessed and genuinely scored zero. Anyone filtering the finder for climate relevance was silently excluding a sixth of the catalogue that nobody had ever looked at — and the catalogue gave no sign of it. A new `cell_score()` returns `None` for a blank, the page renders it as a hatched "not assessed" badge distinct from the cs-0 badge, an unassessed record never satisfies a "climate score ≥ N" filter, and the builder prints a warning naming any record that arrives unscored. The guard stays useful even now that nothing is blank, because it makes the next unscored import visible at build time instead of invisible for months.

**Method.** The Legend scale was applied as a **measured-quantity test** — does climate or weather data enter the calculation, or does inter-annual weather move the value — not as a topical-relevance test. So 14.5.1 marine protected area coverage scores 0 (a GIS area) while 6.4.2 water stress scores 3 (the denominator is computed from precipitation and runoff). **29 of the 173 are the same indicator as a record already scored elsewhere in this workbook**, because the GBF monitoring framework reuses SDG indicators; those were anchored on the existing score rather than rescored, marked `A:` and citing the sibling record.

### Two cross-sheet inconsistencies found — logged, not resolved

Anchoring exposed that the workbook already scores the same measured quantity differently on different sheets:

| Indicator | Scores held |
|---|---|
| Total GHG emissions | **1** on CCC [IND-C-001], JNCC [IND-J-034] and EEA [IND-B-165]; **3** at [GBF-184] (CO₂ per unit value added) and on the IPBES sheet |
| Annual mean PM2.5 / PM10 | **3** at [IND-E-003]; **2** at [GBF-074]; **1** on the IPBES sheet |
| Protected area coverage | **0** on EIF, CBD GBF, BIP and IPBES; **3** on the CCC sheet |

I chose within-sheet coherence over importing the divergence: the SDG emissions rows follow the 1, and PM2.5 follows the 3. But three scores for one measured quantity means the climate-score filter is not comparing like with like across frameworks, which is the filter the whole indicator finder is built around.

**A harmonisation pass across all nine sheets is the right fix**, and it is a bigger job than it looks: 947 records, and the disagreements are about how the scale is read, not about the facts. Worth doing before the climate score is used for anything consequential.

**Done — indicators v27 (28 September 2026).** All 985 records reviewed; 162 changed (145 down, 16 up), with Climate_Dependency and Climate_Rationale rewritten on each. The Legend as written (a data-dependency test) is the adopted reading; topical climate relevance is carried by `Policy_Sector = Climate`. A Core principle and Rules A–H now sit on the Legend sheet below the 0–3 scale. The three inconsistencies above resolve to: GHG emission inventories 1 (temperature-adjusted series 3), air-pollutant concentrations 2, protected-area coverage 0. Distribution 0/1/2/3 moved from 396/233/228/128 to 435/269/201/80. Full review record, including ten borderline records deliberately left unchanged: `outputs_other/climate_score_harmonisation/climate_score_harmonisation_proposal.xlsx`.

### NCF_Category and Indicator_Type now populated too (v22)

Both columns are filled on all 173 rows. **`NCF_Category` is a controlled five-term vocabulary**, so these rows are now validated by the check_links controlled-vocabulary invariant for the first time. Distribution: Enabling 128, Benefit 18, Pressure 18, State – Habitats 6, State – Species 3.

The weighting to **Enabling** is correct rather than lazy. The NCF Legend defines it as "policy responses, governance metrics, funding, data, public engagement and other enabling conditions", and most of the SDG framework is social, economic, financial or statistical. It matches how the workbook already treats its siblings — CBD GBF is 102 of 202 Enabling, BIP 34 of 81. For the 29 rows duplicating a GBF or BIP record, NCF was **anchored on the sibling**, and every anchor agreed with the value I had derived independently, which is a useful check on the derivation.

**`Indicator_Type` was deliberately not anchored.** The CBD GBF sheet stores the GBF monitoring-framework *tier* in that column — Headline / Component / Complementary / Binary — which is a framework tier, not a type. Carrying those onto SDG rows would have been meaningless. The cross-sheet generic typology was used instead.

### Two new Indicator_Type terms — please confirm

`Indicator_Type` is declared **free text** in the Data Dictionary, so neither coinage required vocabulary approval. But coining terms across 57 records is the kind of thing that should be visible rather than absorbed, so both are flagged here:

| New term | Rows | Why nothing existing fitted |
|---|---|---|
| **Socio-economic statistic** | 52 | Poverty, employment, income, trade, macroeconomic and statistical measures. These are not policy or governance metrics — an unemployment rate is not a policy response — and they are not natural-capital measures either. Every existing term in the workbook is one or the other. |
| **Hazard impact** | 5 | The Sendai disaster mortality and economic-loss indicators, which appear three times each across goals 1, 11 and 13. The nearest existing terms are EEA's "Hazard frequency" (frequency, not impact) and "Impact index" (a composite index, which these are not). |

If you would rather fold either into an existing term, it is a one-line change across the affected rows.

### Still open on this sheet

`GBF_Targets_Clean` is absent from the sheet entirely. That is a column addition plus a mapping exercise rather than a fill, and it is the same job as the IFW-04 State of Nature gap (32 rows) — worth doing as one piece of work across both sheets.

## IFW-10 re-extracted; ID-gap audit closed (18 September 2026)

Indicators **v23**.

### The ID-gap audit — closed as intentional

Jonathan, 18 September: no record of when or why the `IND-B` and `IND-C` numbers were removed, but the gaps predate July, so **treat them as intentional removal or reorganisation unless contrary evidence appears**. 35 unused numbers in `IND-C` (below 147) and 141 in `IND-B` are therefore accepted, not investigated. New `IND-C` records continue from the maximum, not from the gaps — the never-reuse-a-retired-ID rule applies to them by default.

### IFW-10 — the finding is structural, not a data refresh

**The current CCC adaptation framework publishes no indicator list.** Its fourteen system monitoring maps publish an objective, proposed targets, actions, enablers and policies; the CCC then selects indicators against those targets separately in each adaptation progress report. So the 32 held rows could not be refreshed indicator-for-indicator — there is nothing to refresh them against.

What the framework does publish, and what is now held, are the **proposed targets**: measurable, time-bound, and the closest analogue to the target rows already on the CCC sheet. **38 new records, IND-C-147 to IND-C-184**, one per target:

| System | Targets | | System | Targets |
|---|---:|---|---|---:|
| Economy & finance | 7 | | Waste | 2 |
| Land | 4 | | Sea | 2 |
| Health | 3 | | Food security | 2 |
| Public services | 3 | | Cultural heritage | 2 |
| Water & wastewater | 3 | | Energy | 2 |
| Transport | 3 | | Built environment & communities | 2 |
| National security & international | 2 | | Digital & telecoms | 1 |

**Scope decision, taken rather than re-asked:** all fourteen systems, not a climate–nature subset, applying the tiered triage rule already settled for the policy scan — catalogue broadly, score climate relevance at entry, let the dashboards filter. Nine of the fourteen had no representation at all before this.

Climate scores are high, as they should be: **24 at 3, 10 at 2, 4 at 1**. Most adaptation targets are defined in directly climatic terms — excess heat-related mortality, resilience to a 1 in 500-year drought, flood probability thresholds, fish stocks sustainable under 2°C of warming. The four 1s are the governance and finance targets (business access to information, company adaptation plans, international climate finance).

**`Data_Source` reads "to be confirmed" on all 38, deliberately.** The framework names no data series for these targets. Inventing one would be a guess, and the blank-over-guess rule applies.

### The 32 legacy rows kept, with their own register record

They are now **[IFW-11] "CCC Adaptation Monitoring Framework 2023–2025 (superseded)"**, so the register shows both vintages honestly rather than one record spanning two frameworks. They remain the basis on which the CCC assessed adaptation progress in 2023 and 2025, and the project marks supersession rather than deleting. Sheet total rises 947 → 985; the register reads 11 frameworks across 9 sheets.

### Two things to watch

- **20 objectives were captured across the fourteen systems; the CCC states 21** in A Well-Adapted UK. The published system pages do not separately distinguish the twenty-first. Worth one check against the report PDF before anyone cites the objective count.
- **When the next CCC adaptation progress report lands**, it will carry the indicator set selected against these targets. That is the point at which IFW-10 can hold indicators rather than targets, and it should trigger a re-visit. Added to the scan protocol's ad-hoc triggers is the sensible home for this.

## Decisions of 18 September 2026, and the MCCIP proposal

### Settled

| Item | Decision |
|---|---|
| **Agency monitoring statistics** (EA drought, water situation, rainfall and river flow) | **Out of scope.** Written into the handover §8 as a standing scope rule, with the accepted cost stated: drought and water availability remains the catalogue's largest thematic gap. The earlier note that these would "eventually" get an indicators worksheet is superseded. |
| **Level of generality** | **Rule written down**, in handover §8 and cross-referenced from the scan protocol §3, so the Cormorant indices, river fish counts, bluefin fishery and marine event reporting are not re-raised. |
| **NaFRA2** | **Added as [POL-070]**, UK governance v26, with a reciprocal link on [POL-045] and on [IND-E-042], which already named NaFRA as a data source. |
| **Monitoring the condition of the natural environment** | **Added as [POL-071]**, the Environment Act 2021 s.16 statutory statement. Date corrected: first published 23 May 2022, last updated 16 July 2026 — the queue had recorded the update date as the publication date. |
| **FCERM funding and performance statistic** | **No action.** |

### Verifications — all three "investigate" rows close with no addition

- **Butterflies** — held seven times over on the JNCC sheet under UKBI 2025 indicator names ([IND-J-014] to [IND-J-018], plus [IND-J-033] and [IND-J-074] for connectivity), sourced to the UK Butterfly Monitoring Scheme. Nothing to add.
- **UK carbon footprint** — held as [IND-E-057], sourced to Defra/ONS consumption-based emissions statistics. Nothing to add.
- **British Survey of Fertiliser Practice** — it is a *data source*, not a missing indicator: it is named on [IND-C-038], and [IND-C-083] and [IND-C-087] carry the related fertiliser and nutrient-management measures. Nothing to add.
- **Children's People and Nature Survey** — [IND-E-051] already names the People and Nature Survey as a data source, alongside MENE. The *children's* variant is not separately named. One-cell improvement if wanted, not a record.

---

## RESOLVED — the MCCIP indicator block (written 6 October 2026)

**Done in indicators v28:** [IFW-12] and the `MCCIP Indicators` sheet, IND-M-001 to IND-M-016 — the 16 physical-environment and ecosystem-change topics, as recommended below; the six societal-impact topics excluded. Scores checked against `outputs_other/CLIMATE_SCORE_METHOD.md`. The proposal is kept below as written.

### The proposal as put (18 September 2026)

**Not written. This is the proposal you asked for.**

### What MCCIP actually publishes

MCCIP is held as [POL-049] with no indicator rows. Its UK evidence hub publishes **22 topics** in three groups, each topic a standing evidence review rather than a data series:

| Group | Topics |
|---|---|
| **Physical environment** (10) | Temperature · Dissolved oxygen · Stratification · Salinity · Sea level · Storms and waves · Coastal geomorphology · Ocean acidification · Ocean circulation · Arctic sea ice |
| **Ecosystem change** (6) | Coastal and intertidal habitats · Shallow subtidal, shelf and deep-sea habitats · Plankton · Fish · Seabirds and waterbirds · Marine mammals |
| **Societal impact** (6) | Fisheries · Aquaculture · Harmful species · Coastal flooding · Transport and infrastructure · Cultural heritage |

Each topic carries a dated full review paper, a **"What is already happening?"** statement with quantified observed trends, a **confidence level for the observed evidence**, a **"What could happen in the future?"** statement with quantified projections, and a **separate confidence level for the projections**. The sea temperature topic, for example, gives 0.3 °C per decade over 40 years at HIGH confidence (high evidence, high consensus) for observed, and up to 3.11 ± 0.98 °C by 2079–98 under RCP8.5 at MEDIUM confidence for projected.

### The precedent this follows

**[IFW-07] IPBES Global Assessment** — 143 rows drawn from an assessment rather than a monitoring framework, whose Policy_Purpose already says its "role is to inform policy, not to set or track targets". MCCIP is the same shape, for UK marine. It is *not* like [IFW-01] EIF or [IFW-02] CCC, which track targets.

### Proposed shape

- **New framework record [IFW-12]**, "MCCIP UK Marine Climate Change Impacts Evidence Hub", `Sheet_Name` **MCCIP Indicators** (a new sheet), Record_Count 22, Scope UK, Lead_Organisation [POL-049] MCCIP partnership.
- **22 records, IND-M-001 to IND-M-022.** New `IND-M` family — the first new indicator family since the workbook was built, and the decision that most deserves a second opinion.
- Column mapping: `Indicator_Name` = topic; `Units_Measure` = the observed quantity where the review gives one; `Climate_Rationale` = the observed-trend statement; `Source_Reference` = the dated review paper; `Source_URL` = the topic page; `Framework_Classification` = `Role: Evidence review; Observed confidence: <level>; Projection confidence: <level>`, which preserves MCCIP's dual confidence rating, the thing that makes it distinctive.
- Climate scores would run high — most physical-environment topics are climate variables outright, so 3.

### Why it is worth doing, and the case against

**For.** MCCIP is a UK marine climate evidence partnership co-led by Cefas with heavy Met Office involvement; sea temperature, marine heatwaves and sea-level projections are squarely the Met Office → policy channel this project exists to map. The catalogue currently has no UK marine *climate* evidence block at all — [IFW-01] Theme C covers marine state, not climate drivers. Two of the four completed assessments (ocean heatwaves, land surface temperature) would have drawn on it directly.

**Against.** Only about half the 22 topics are measured quantities; the societal-impact six are qualitative impact reviews with no series behind them. A new sheet and a new ID family is real structural change for 22 rows. And the confidence ratings do not map onto `Climate_Score`, so the sheet would carry a grading scheme nothing else uses.

**My recommendation: do it, but only the 16 physical-environment and ecosystem-change topics**, leaving the societal-impact six out under the level-of-generality rule just adopted — they are impact narratives, not measures. That gives a 16-row block of genuine marine climate evidence without importing a qualitative tail.

## Resolved — historical record

Rows move here once resolved, keeping the same columns. Nothing is ever removed from the file.

| Added | Found by | Family | Proposed name | Source | Climate input | Overlap | Confidence | Status | Resolution |
|---|---|---|---|---|---|---|---|---|---|
| 2026-07 (pre-queue) | ocean heatwaves | POL | Fisheries Act 2020 climate change objective - JFS and FMPs | https://www.legislation.gov.uk/ukpga/2020/22/contents | Yes | — | High | added | [POL-067] |
| 2026-07 (pre-queue) | ocean heatwaves | POL | Shellfish official-control and HAB / biotoxin monitoring (Cefas for FSA / FSS) | https://www.cefas.co.uk/ | Yes | — | High | added | [POL-068]; also added [ORG-043] FSA and [ORG-044] FSS. **RESOLVED 2026-09-17 — RETAIN.** Jonathan: keep POL-068, ORG-043 and ORG-044 in. Harmful algal blooms are strongly driven by sea surface temperature and climate, so this is a climate-sensitive monitoring regime, not general pollution monitoring. The earlier 'rejected' mark arose from this already-actioned row appearing in the round-2 triage sheet in error. **Precedent: 'pollution monitoring out of scope' does not extend to monitoring whose trigger is climatic.** |
| 2026-07 (pre-queue) | ocean heatwaves | POL | UK Blue Carbon Evidence Partnership (UKBCEP) | https://uk-bcep.org/ | Indirect | — | High | added | [POL-069] |
