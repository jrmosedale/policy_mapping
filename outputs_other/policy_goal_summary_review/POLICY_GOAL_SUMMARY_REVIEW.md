# `Policy_Goal_Summary` — original vs proposed

**Sheet:** `Indicator Framework`, workbook `indicators_climate_nature.xlsx` v14
**Drafted:** 17 September 2026 · **Nothing has been written to the workbook**

Proposed values are written from each framework's own primary documentation, describing what the
framework is *for* and how wide its policy range is. They do not aggregate the `Policy_Goal` field
of individual indicators.

---

## What is wrong with the current column

Three things, all visible once the nine values are read together:

1. **They are not summaries.** Every one is a semicolon-delimited list of policy instruments — the
   same form as the `Policy_Goal` field on an individual indicator row. The column name promises
   prose describing scope and purpose; the content is a bibliography of targets.

2. **Indicator-level detail has bubbled up to framework level.** IFW-02 ends
   *"Minimise climate change impacts on biodiversity (GBF-T8)"* — that is the policy goal of some
   individual CCC records, not a statement about the CCC's monitoring framework. IFW-07 is worse:
   *"GBF Goal A and Targets 2, 8, 11; SDG 15.5"* describes which targets a handful of IPBES
   indicators happen to map to, and says nothing about what IPBES is. This is the artefact you
   suspected.

3. **One is misleading.** IFW-04 reads *"State of Nature Partnership; JNCC UK Biodiversity
   Indicators; Kunming-Montreal GBF"*, which implies State of Nature reports against the GBF. It
   does not. It is an independent NGO-led assessment with no statutory targets and no reporting
   duty — which is arguably the single most important thing to know about it.

**What is lost.** The current values do carry real information: the specific instruments each
framework serves. If that matters to you, the cleanest answer is to keep it in a separate column
(`Key_Instruments`, say) rather than lose it — see the note at the end.

---

## IFW-01 · Environmental Indicator Framework (EIF) · England · 66 records

**Original**
> Environmental Improvement Plan (EIP) 2025; 30×30 land and sea protection; Kunming-Montreal GBF targets (vary by indicator); Environment Act 2021 (statutory basis)

**Proposed**
> Defra's Environmental Indicator Framework (formerly the Outcome Indicator Framework) tracks
> environmental change in England against the ten goals of the Environmental Improvement Plan, the
> statutory plan required under the Environment Act 2021. Its indicators form the evidence base for
> Defra's annual EIP progress report, which the Office for Environmental Protection scrutinises
> independently. Coverage is deliberately broad — air, water, land, seas, wildlife, resource
> efficiency, biosecurity and people's engagement with nature — rather than biodiversity alone.

*Sources: [Environmental Indicator Framework](https://oifdata.defra.gov.uk/), [Guide to EIF assessments](https://www.gov.uk/government/publications/guide-to-environmental-indicator-framework-assessments/guide-to-environmental-indicator-framework-assessments), [EIP 2025](https://www.gov.uk/government/publications/environmental-improvement-plan-2025/environmental-improvement-plan-eip-2025)*

---

## IFW-02 · CCC Mitigation & Adaptation Monitoring Framework · UK / GB · 111 records

**Original**
> UK Climate Change Act 2008 carbon budgets; Third National Adaptation Programme (NAP3) 2023; CCRA3; Minimise climate change impacts on biodiversity (GBF-T8)

**Proposed**
> The Climate Change Committee's monitoring frameworks support its statutory duty under the Climate
> Change Act 2008 to report annually to Parliament on UK progress. The mitigation framework tracks
> emissions against the legally binding five-year carbon budgets on the path to net zero by 2050,
> and does so through indicators of the underlying drivers — deployment rates, technology uptake and
> market activity — rather than emissions alone. The adaptation framework separately evaluates
> delivery of the National Adaptation Programme for England against the risks identified in the
> Climate Change Risk Assessment. Scope is economy-wide: power, buildings, surface transport,
> aviation and shipping, industry, agriculture and land use, waste and F-gases, and engineered
> removals.

*Sources: [CCC Mitigation Monitoring Framework](https://www.theccc.org.uk/publication/ccc-monitoring-framework/), [About the CCC](https://www.theccc.org.uk/about/), [CCC Insights Briefing 1 — The UK Climate Change Act](https://www.theccc.org.uk/wp-content/uploads/2020/10/CCC-Insights-Briefing-1-The-UK-Climate-Change-Act.pdf)*

---

## IFW-03 · JNCC UK Biodiversity Indicators 2025 · UK / GB · 77 records

**Original**
> UK National Biodiversity Strategy and Action Plan (NBSAP) 2025; Environment Act 2021 species targets; 30×30 land and sea protection; GBF targets (vary by indicator)

**Proposed**
> The UK Biodiversity Indicators are an accredited official statistics compendium produced by JNCC
> and Defra, giving an annual snapshot of the status of UK biodiversity and how it is changing.
> They serve two reporting purposes. Internationally, they are the UK's principal evidence for
> national reporting to the Convention on Biological Diversity, and the 2025 suite was revised
> specifically to align with the Kunming-Montreal Global Biodiversity Framework ahead of the 2026
> and 2029 national reports. Domestically, the parallel England suite feeds Defra's Environmental
> Indicator Framework. Coverage spans species and habitat status, the pressures acting on them,
> ecosystem services, and enabling conditions such as finance, data and public engagement.

*Sources: [UK Biodiversity Indicators](https://jncc.gov.uk/our-work/uk-biodiversity-indicators/) (data last updated December 2025)*

---

## IFW-04 · State of Nature 2023 Report · UK / GB / England / NI · 32 records

**Original**
> State of Nature Partnership; JNCC UK Biodiversity Indicators; Kunming-Montreal GBF

**Proposed**
> State of Nature is a periodic assessment of UK wildlife produced by a partnership of more than 60
> conservation NGOs, research institutes and statutory nature conservation bodies, drawing on
> biological recording and monitoring data collected largely by volunteers. It is not a government
> reporting framework and carries no statutory targets: its purpose is to provide an independent
> benchmark for the status of UK species and habitats, to set that against the pressures acting on
> nature, and to assess the conservation responses being made. The 2023 edition reports UK-level
> trends with separate summaries for England, Scotland, Wales and Northern Ireland.

*Sources: [State of Nature 2023](https://stateofnature.org.uk/), [Partners](https://stateofnature.org.uk/partners/), [main report PDF](https://stateofnature.org.uk/wp-content/uploads/2023/09/TP25999-State-of-Nature-main-report_2023_FULL-DOC-v12.pdf)*

---

## IFW-05 · CBD Global Biodiversity Framework (GBF) · International · 202 records

**Original**
> Kunming-Montreal GBF — all 23 targets and 4 goals; Monitoring Framework from CBD/COP/16/L.26/Rev.1 (Feb 2025)

**Proposed**
> The Kunming-Montreal Global Biodiversity Framework, adopted at CBD COP15 in December 2022, sets
> four goals for 2050 and 23 targets for 2030 on a pathway to the Convention's vision of living in
> harmony with nature. The targets divide into three groups: reducing threats to biodiversity
> (1–8), meeting people's needs through sustainable use and benefit-sharing (9–13), and tools for
> implementation and mainstreaming (14–23). The accompanying monitoring framework, finalised at
> COP16, defines headline, component, binary and complementary indicators against which all Parties
> — the UK among them — report at least every five years.

*Sources: [CBD COP15 final text](https://www.cbd.int/article/cop15-final-text-kunming-montreal-gbf-221222), [2030 Targets with guidance notes](https://www.cbd.int/gbf/targets), [Monitoring framework CBD/COP/16/L.26/Rev.1](https://www.cbd.int/doc/c/1e13/f20d/81cd8447744640bbd21e008f/cop-16-l-26-rev1-en.pdf)*

---

## IFW-06 · Biodiversity Indicators Partnership (BIP) · International / Global · 81 records

**Original**
> Kunming-Montreal GBF; SDG 15 (Life on Land); SDG 14 (Life Below Water); Post-2020 biodiversity targets

**Proposed**
> The Biodiversity Indicators Partnership is a global initiative, with a secretariat hosted at
> UNEP-WCMC, that coordinates the development and delivery of biodiversity indicators for use across
> the international policy system. Its indicators are built to serve the Convention on Biological
> Diversity and other biodiversity-related conventions, IPBES, and the Sustainable Development
> Goals, rather than any single instrument. It convenes more than sixty contributing organisations
> and also works to strengthen national capacity to use indicators in National Biodiversity
> Strategies and Action Plans and in SDG reporting.

*Sources: [About the BIP](https://www.bipindicators.net/about)*

---

## IFW-07 · IPBES Global Assessment · International / Global · 143 records

**Original**
> Kunming-Montreal GBF Goal A and Targets 2, 8, 11; UN SDGs (SDG 15.5); IPBES Global Assessment monitoring framework

**Proposed**
> IPBES is the intergovernmental science-policy platform tasked with assessing the state of
> knowledge on biodiversity and ecosystem services for decision-makers. The 2019 Global Assessment,
> compiled by 145 expert authors from a systematic review of around 15,000 scientific and government
> sources and drawing for the first time at this scale on indigenous and local knowledge, assessed
> five decades of change in nature, its contributions to people, and the causes behind them. The
> indicators drawn from it characterise the five direct drivers of biodiversity loss — land- and
> sea-use change, direct exploitation of species, climate change, pollution and invasive alien
> species — together with the indirect economic and demographic drivers behind them. Its role is to
> inform policy, not to set or track targets.

*Sources: [IPBES Global Assessment](https://www.ipbes.net/global-assessment), [Summary for Policymakers](https://files.ipbes.net/ipbes-web-prod-public-files/inline/files/ipbes_global_assessment_report_summary_for_policymakers.pdf)*

---

## IFW-08 · UN Sustainable Development Goals (SDGs) · International / Global · 173 records

**Original**
> UN 2030 Agenda for Sustainable Development; all 17 SDG Goals — nature-relevant subset (revised IAEG-SDGs post-2020 indicator framework, A/RES/71/313)

**Proposed**
> The global indicator framework for the 2030 Agenda for Sustainable Development was developed by
> the Inter-agency and Expert Group on SDG Indicators and adopted by the UN General Assembly in
> resolution A/RES/71/313. It is the statistical apparatus for monitoring progress, informing policy
> and holding stakeholders accountable across the 17 Goals and 169 targets, and is refined annually
> with comprehensive reviews by the UN Statistical Commission — most recently in 2025. The framework
> spans the full social, economic and environmental agenda; the records held here are the
> nature- and climate-relevant subset.

*Sources: [IAEG-SDGs](https://unstats.un.org/sdgs/iaeg-sdgs/), [Global indicator framework after 2025 review](https://unstats.un.org/sdgs/indicators/indicators-list/)*

---

## IFW-09 · EEA Biodiversity Strategy Indicators · EU / Europe / Global · 62 records

**Original**
> EU Biodiversity Strategy 2030; EU Nature Restoration Law 2024; EU Climate Law 2021; EU Adaptation Strategy 2021; 8th Environmental Action Programme

**Proposed**
> The European Environment Agency maintains the indicator set used to monitor Europe's progress on
> biodiversity and ecosystem health, principally against the EU Biodiversity Strategy for 2030 and
> the 8th Environment Action Programme, with the EU Biodiversity Strategy dashboard as the main
> reporting vehicle. The indicators cover the conservation status of species and habitats under the
> Habitats Directive, protected-area coverage towards the 30% land and sea target, ecosystem extent
> and condition, and the pressures of land-use change, pollution and climate change. Several double
> as EU-level reporting for SDG 14 and SDG 15, and the Nature Restoration Regulation (EU 2024/1991)
> adds restoration-progress reporting to the same set.

*Sources: [EEA biodiversity indicators](https://www.eea.europa.eu/themes/biodiversity/indicators), [EU Biodiversity Strategy for 2030](https://www.eea.europa.eu/policy-documents/eu-biodiversity-strategy-for-2030-1), [8th EAP monitoring report 2025](https://www.eea.europa.eu/en/analysis/publications/monitoring-report-on-progress-towards-the-8th-eap-objectives-2025)*

---

## Notes and judgement calls

**Length.** Originals average 132 characters; proposals average roughly 650. That is the cost of
prose. If you want them shorter, the second and third sentences are the ones to cut — the first
sentence of each carries the purpose.

**Row heights and column width.** The `Indicator Framework` sheet's dimensions were recomputed in
v13 against the current short values. Adopting these would need that redone for the sheet, or the
`Policy_Goal_Summary` rows will clip.

**Two things I could not verify to primary-source standard, flagged rather than asserted:**

- IFW-01 — I have stated that the OEP scrutinises Defra's EIP progress report. The OEP's annual
  progress assessment is well established, but I did not find it stated on the EIF pages themselves.
  Medium confidence; drop the clause if you want the sentence tied only to Defra sources.
- IFW-09 — the EEA does not publish a single named "Biodiversity Strategy Indicators" set under that
  title. The proposal describes the indicator set as the EEA actually presents it (biodiversity
  indicators feeding the EU Biodiversity Strategy dashboard and the 8th EAP monitoring report).
  **You may want to rename `Source_Framework` for IFW-09 to match.**

**The instrument lists.** If you want to keep them, add a `Key_Instruments` column to the
`Indicator Framework` sheet and move the current values there verbatim. That keeps the
cross-reference value while letting `Policy_Goal_Summary` do what its name says. It is a schema
change, so it needs your decision — and per the new Data Dictionary convention it would be
documented by editing that sheet in place, not appending.
