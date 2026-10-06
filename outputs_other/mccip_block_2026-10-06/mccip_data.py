"""MCCIP indicator block — 16 topics (physical environment + ecosystem change) as [IFW-12] on a new
'MCCIP Indicators' sheet, IND-M family. Source: MCCIP Impacts Hub topic pages, read 6 Oct 2026.
_conf is verification metadata, not written."""
SF = "MCCIP UK Marine Climate Change Impacts Evidence Hub"
HUB = "https://www.mccip.org.uk/all-uk/uk-impacts/hub"
COLS = ["Record_ID","Indicator_Name","Source_Framework","NCF_Category","Policy_Sector","Indicator_Type","Units_Measure",
        "Scope","Policy_Goal","Source_Reference","Data_Source","Climate_Score","Climate_Dependency","Climate_Rationale",
        "Policy_Links","Framework_Classification","Source_URL"]
DEP = {0:"0 – None",1:"1 – Low",2:"2 – Medium",3:"3 – High"}
GOAL_PHYS = "UK marine climate evidence for adaptation and marine policy: informs CCRA4-IA and the National Adaptation Programmes, and UK Marine Strategy assessments of good environmental status."
GOAL_ECO = "UK marine climate evidence on ecosystem change: informs CCRA4-IA, the UK Marine Strategy (good environmental status) and marine nature recovery."
def conf(level, ev): return f"{level} ({ev})"
T = [
# id, name, group, ncf, sectors, itype, units, score, rule, observed, projected, obs_conf, proj_conf, review, slug, links
("IND-M-001","Sea temperature","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Sea-surface and bottom temperature, °C; trend °C per decade",3,"Rule E(ii): a physical climate-system variable",
 "UK sea-surface temperature has warmed by around 0.3°C per decade over the last 40 years, most in the southern North Sea.",
 "Annual mean SST up to 3.11°C (±0.98°C) higher by 2079–2098 than 2000–2019 under RCP8.5; bottom temperature up to 2.49°C (±0.94°C).",
 conf("High","high evidence, high consensus"),conf("Medium","medium evidence, high consensus"),"MCCIP Sea Temperature topic review, update October 2025","temperature","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-002","Dissolved oxygen","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Dissolved oxygen concentration; % change",3,"Rule E(ii): a physical-chemical ocean variable",
 "Global ocean oxygen content has fallen by more than 2% since the 1960s; seasonal oxygen depletion is more frequent in the North Sea and has been detected in the Celtic Sea.",
 "UK shelf declines strongest in the North Sea and western English Channel (3–4% by 2100); about 2% in deeper regions exchanging with the open ocean.",
 conf("Low","low evidence, medium consensus"),conf("Medium","medium evidence, medium consensus"),"MCCIP Oxygen topic review, update August 2025","oxygen","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-003","Shelf-sea stratification","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Thermal stratification strength and timing (onset, breakdown, duration in weeks)",3,"Rule E(ii): a physical ocean variable derived from temperature and salinity profiles",
 "Earlier onset of seasonal stratification in UK shelf seas, with tentative evidence of long-term strengthening; no discernible trend in coastal waters.",
 "By 2100 thermal stratification in UK shelf seas lasts about two weeks longer and is stronger, with consequences for nutrient mixing, primary production and bottom-water oxygen.",
 conf("Low","low evidence, medium consensus"),conf("Low","low evidence, low agreement"),"MCCIP Stratification topic review (draws on Tinker et al. 2024)","stratification","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-004","Salinity","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Salinity of UK shelf seas and adjacent Atlantic",3,"Rule E(ii): a physical ocean variable",
 "UK shelf-sea and adjacent Atlantic salinity is highly variable on annual and decadal timescales with no clear long-term trend; recent marked freshening of eastern North Atlantic waters west of the UK.",
 "Most 21st-century projections show UK shelf seas and the adjacent Atlantic becoming less saline, driven by ocean-circulation change; larger decreases in the North Sea than the Irish and Celtic Seas.",
 conf("Medium","medium evidence, high agreement"),conf("Medium","medium evidence, medium agreement"),"MCCIP Salinity topic review","salinity","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-005","Sea level","Physical environment","Pressure","Climate | Marine & Fisheries | Water","Pressure / threat index",
 "Mean sea level, cm (observed) and m (projected)",3,"Rule E(ii): a physical climate-system variable",
 "Mean sea level around the UK has risen by about 12–16 cm since 1900, faster in the 20th century than the 19th.",
 "By 2100: London 0.45–0.78 m, Cardiff 0.43–0.76 m, Belfast 0.26–0.58 m, Edinburgh 0.23–0.54 m, depending on emissions scenario.",
 conf("High","high evidence, high agreement"),conf("Medium","medium evidence, high agreement"),"MCCIP Sea-level Rise topic review (2020)","sea-level-rise","[POL-049]; [POL-113]; [POL-045]"),
("IND-M-006","Storms and waves","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Significant wave height (m); storminess",3,"Rule E(ii): a physical climate-system variable",
 "Mean significant wave height has decreased over the last 30 years in northern UK waters and increased in the south.",
 "The most severe waves could be higher by 2100 under high emissions, with an overall reduction possible in North Atlantic mean significant wave height.",
 conf("Medium","high evidence, medium consensus"),conf("Low","medium evidence, low consensus"),"MCCIP Storms and Waves topic review, update May 2025","storms-and-waves","[POL-049]; [POL-113]; [POL-045]"),
("IND-M-007","Coastal geomorphology","Physical environment","Pressure","Climate | Marine & Fisheries | Land Use & Agriculture","Pressure / threat index",
 "Share of coastline eroding (%); erosion rates",2,"Rule D: mapped and surveyed erosion that storms and sea level move materially year to year; no climate data enter the measure directly",
 "About 17% of the UK coastline is currently affected by erosion.",
 "Coastal erosion rate and extent expected to increase with relative sea-level rise and reduced sediment supply; Scotland's firths face increased erosion.",
 conf("High","high evidence, high agreement"),conf("Medium","medium evidence, medium agreement"),"MCCIP Coastal Geomorphology topic review (2020)","coastal-geomorphology","[POL-049]; [POL-113]; [POL-045]"),
("IND-M-008","Ocean acidification","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Seawater pH; carbonate saturation state; atmospheric CO2 (ppm)",3,"Rule E(ii): a physical-chemical ocean variable (pH)",
 "Atmospheric CO2 exceeded 420 ppm in 2024, rising about 2.5 ppm a year over the last decade; North Atlantic pH continues to decline.",
 "Shelf-sea pH declines at the current rate to 2050 and then faster; by 2100 up to 90% of north-west European shelf seas may be undersaturated in aragonite for at least one month a year.",
 conf("High","high evidence, high consensus"),conf("Medium","medium evidence, medium agreement"),"MCCIP Ocean Acidification topic review, update February 2025","ocean-acidification","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-009","Ocean circulation (AMOC)","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "Atlantic Meridional Overturning Circulation strength, Sv; trend Sv per decade",3,"Rule E(ii): a physical climate-system variable",
 "The AMOC strengthened in the 1990s, weakened to the early 2010s, recovered slightly, and has weakened again recently; observed trend since 2004 about −1 Sv per decade.",
 "AMOC weakening by 2100 is a robust projection, consistent in magnitude with the observed trend.",
 conf("High","high evidence, high agreement"),conf("Medium","medium evidence, high agreement"),"MCCIP Ocean Circulation topic review, update September 2025","ocean-circulation","[POL-049]; [POL-113]"),
("IND-M-010","Arctic sea ice","Physical environment","Pressure","Climate | Marine & Fisheries","Pressure / threat index",
 "September sea-ice extent, km²; % change per decade",3,"Rule E(ii): a physical climate-system variable",
 "September minimum Arctic sea-ice extent has fallen by about 79,000 km² a year since 1979, around 12% per decade relative to the 1981–2010 mean.",
 "The Arctic becomes practically ice-free at the seasonal minimum at least once before 2050 under any emissions scenario.",
 conf("High","high evidence, high agreement"),conf("High","high evidence, high agreement"),"MCCIP Impacts of Climate Change on Arctic Sea Ice topic review (2023); Met Office leads this topic","sea-ice","[POL-049]; [POL-113]"),
("IND-M-011","Coastal and intertidal habitats","Ecosystem change","State – Habitats","Marine & Fisheries | Nature & Biodiversity | Climate","Habitat extent / condition",
 "Saltmarsh extent (% change); dune and soft-cliff erosion rates",1,"Rule B: habitat extent from mapping and survey (saltmarsh named in the rule); climate is a driver but no climate data enter the measure",
 "Relative sea-level rise and coastal hazards are affecting saltmarshes: more erosion from stronger wave action, more frequent flooding of low marsh, and landward migration of habitats.",
 "An estimated 11% loss of UK saltmarsh by 2060 without restoration; dune erosion continues to increase; soft-cliff retreat three to seven times faster in North Devon and Yorkshire by 2100.",
 conf("High","high evidence, high consensus — saltmarsh"),conf("High","high evidence, high consensus — saltmarsh"),"MCCIP Coastal and Intertidal Habitats topic review, update May 2026","coastal-and-intertidal-habitats","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-012","Shallow subtidal, shelf and deep-sea habitats","Ecosystem change","State – Habitats","Marine & Fisheries | Nature & Biodiversity | Climate","Habitat extent / condition",
 "Benthic community composition and species distributions; kelp assemblages; seafloor biomass (%)",2,"Rule D: survey-based community and distribution measures that inter-annual sea temperature moves; habitat-suitability work uses climate data indirectly",
 "North Sea infaunal species have shifted distribution with warming but most cannot keep pace; UK kelp assemblages have changed; plankton changes are reducing organic carbon flux to the seabed; deep-sea sponge communities show resilience.",
 "Significant kelp range shifts by 2050; restructured North Sea benthic communities by 2100; only 30–42% of present habitat for the reef-forming coral Desmophyllum pertusum persisting as refugia; global seafloor biomass down 3% by 2050 and 5.9% by 2080.",
 conf("Low","shelf: medium evidence, low consensus; deep sea: low evidence, medium consensus"),conf("Low","shelf and deep sea"),"MCCIP Shallow Subtidal, Shelf and Deep-sea Habitats topic review, update June 2026","shallow-shelf-and-deep-sea-habitats","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-013","Plankton and pelagic habitats","Ecosystem change","State – Species","Marine & Fisheries | Nature & Biodiversity | Climate","Species index / trend",
 "Plankton biomass and community composition (size classes); bloom timing; distribution shifts",2,"Rule D: plankton and trophic indices",
 "Large phyto- and zooplankton are declining in oceanic waters beyond the shelf, while smaller plankton and microbial species dominate in warmer, stratified shelf waters.",
 "Earlier and longer spring blooms in some regions, further northward shifts of plankton and fish, reduced overall primary productivity and more dominance by smaller phytoplankton.",
 conf("Medium","high evidence, medium consensus"),conf("Medium","medium evidence, low consensus"),"MCCIP Plankton and Pelagic Habitats topic review, update 2026","plankton","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-014","Fish","Ecosystem change","State – Species","Marine & Fisheries | Nature & Biodiversity | Climate","Species index / trend",
 "Species distribution and abundance; habitat suitability; thermal thresholds (°C)",2,"Rule D: fish survey and stock-assessment measures, which inter-annual sea temperature moves",
 "Warm-water fish species continue to increase in UK waters, with local declines of some cold-affinity species; several cephalopods have increased in abundance and range; Atlantic cod reproductive success falls above 9.6°C.",
 "Continued warming changes species composition in shallow areas such as the southern North Sea; by 2100 conditions may suit Mediterranean horse mackerel and bogue as far north as the mid Irish and North Seas; cod habitat shifts north.",
 conf("Medium","high evidence, medium agreement"),conf("Medium","medium evidence, medium agreement"),"MCCIP Fish topic review (Wright et al. 2020, updated 2023)","fish","[POL-049]; [POL-113]; [POL-067]"),
("IND-M-015","Seabirds and waterbirds","Ecosystem change","State – Species","Marine & Fisheries | Nature & Biodiversity | Climate","Species index / trend",
 "Population indices; breeding numbers and distribution; productivity and survival",2,"Rule D: survey-based population indices",
 "UK and Ireland seabird and waterbird indices have declined since the 1990s, linked to climate-driven changes in fish prey and to extreme weather affecting breeding success.",
 "Mixed impacts on breeding and non-breeding numbers; Arctic and sub-Arctic waterbirds wintering in the UK and Ireland are particularly vulnerable; many UK seabird populations lack resilience.",
 conf("Medium","medium evidence, medium agreement"),conf("Low","low evidence, low agreement"),"MCCIP Seabirds and Waterbirds topic review (2023)","seabirds-and-waterbirds","[POL-049]; [POL-113]; [POL-028]"),
("IND-M-016","Marine mammals","Ecosystem change","State – Species","Marine & Fisheries | Nature & Biodiversity | Climate","Species index / trend",
 "Range and distribution shifts; disease prevalence; habitat suitability (largely qualitative)",2,"Rule D: survey-based distribution measures that inter-annual ocean conditions move",
 "Apparent northward shift of some warmer-water cetaceans around the UK; range shifts, habitat loss, food-web change and more disease are documented.",
 "Species tied to breeding grounds face habitat and behavioural change; disease and thermal stress may increase; breeding timing may shift.",
 conf("Medium","medium evidence, medium consensus"),conf("Medium","low evidence, medium consensus"),"MCCIP Climate Change Impacts on Marine Mammals around the UK and Ireland topic review (2023)","marine-mammals","[POL-049]; [POL-113]; [POL-028]"),
]
ROWS = []
for (rid,name,grp,ncf,sec,itype,units,score,rule,obs,proj,oc,pc,rev,slug,links) in T:
    ROWS.append({"Record_ID":rid,"Indicator_Name":name,"Source_Framework":SF,"NCF_Category":ncf,"Policy_Sector":sec,
      "Indicator_Type":itype,"Units_Measure":units,"Scope":"UK | Ireland","Policy_Goal":GOAL_PHYS if grp=="Physical environment" else GOAL_ECO,
      "Source_Reference":rev,"Data_Source":"MCCIP evidence synthesis of published observations and model studies (topic review; Impacts Hub)",
      "Climate_Score":str(score),"Climate_Dependency":DEP[score],
      "Climate_Rationale":f"Scored on the topic's headline measured quantity ({rule}). Observed: {obs} Projected: {proj}",
      "Policy_Links":links,"Framework_Classification":f"Role: Evidence review; Group: {grp}; Observed confidence: {oc}; Projection confidence: {pc}",
      "Source_URL":f"https://www.mccip.org.uk/{slug}"})
from collections import Counter
REGISTER = {"Framework_ID":"IFW-12","Source_Framework":SF,"Sheet_Name":"MCCIP Indicators","Record_Count":str(len(ROWS)),"Scope":"UK | Ireland",
 "Lead_Organisation":"[ORG-018] Cefas (MCCIP secretariat); [POL-049] MCCIP partnership",
 "Indicator_Types_Summary":"; ".join(f"{k} ({v})" for k,v in Counter(r["Indicator_Type"] for r in ROWS).most_common()),
 "NCF_Categories":"; ".join(f"{k} ({v})" for k,v in Counter(r["NCF_Category"] for r in ROWS).most_common()),
 "GBF_Coverage":"0/16",
 "Policy_Purpose":"The Marine Climate Change Impacts Partnership [POL-049] is a UK partnership of scientists, government, agencies and NGOs, with its secretariat at Cefas and the Met Office among its partners, that provides co-ordinated, quality-assured evidence on how climate change is affecting UK and Irish seas and coasts. Its Impacts Hub publishes standing topic reviews in three groups — physical environment, ecosystem change and societal impact — each stating what is already happening and what could happen, with separate confidence ratings (evidence and consensus) for the observed and projected statements. Its role is to inform adaptation and marine policy — the Climate Change Risk Assessment and national adaptation programmes, and the UK Marine Strategy — not to set or track targets: an assessment-derived framework like [IFW-07]. Sixteen topics are held, the physical-environment and ecosystem-change groups; the six societal-impact topics are excluded as impact narratives without a measured series (level-of-generality rule).",
 "Official_Link":HUB,"Indirect_Policy_Links":"[POL-113] CCRA4-IA; [POL-002] NAP3; [POL-028] UK Marine Strategy","Key_Instruments":"[POL-049]; [ORG-018]"}

# ---- Scoring checked against outputs_other/CLIMATE_SCORE_METHOD.md (6 Oct 2026) ----------------
# Rationale format per method §3: measured quantity; do climate data enter; does weather move it;
# then Observed / Projected; ending with "(Legend N, rule X; aligned with [sibling])" (rule G).
SCORING = {
 "IND-M-001":(3,"Measured quantity: sea-surface and bottom temperature — itself a physical climate-system variable.","(Legend 3, rule E ii; aligned with [IND-B-162])"),
 "IND-M-002":(3,"Measured quantity: dissolved-oxygen concentration — a physical-chemical ocean variable of the same kind as pH.","(Legend 3, rule E ii)"),
 "IND-M-003":(3,"Measured quantity: strength and timing of thermal stratification, computed from temperature and salinity profiles — a physical ocean variable.","(Legend 3, rule E ii)"),
 "IND-M-004":(3,"Measured quantity: salinity of shelf seas and the adjacent Atlantic — a physical ocean variable.","(Legend 3, rule E ii)"),
 "IND-M-005":(3,"Measured quantity: mean sea level — itself a physical climate-system variable.","(Legend 3, rule E ii; aligned with [IND-B-160])"),
 "IND-M-006":(3,"Measured quantity: significant wave height and storminess — physical climate-system variables.","(Legend 3, rule E ii)"),
 "IND-M-007":(1,"Measured quantity: share of coastline affected by erosion, from mapping and survey programmes. No climate data enter it, and the mapped share does not move materially year to year, although sea level and storms drive erosion over time; a storm-year erosion-rate series would score 2.","(Legend 1, rule B)"),
 "IND-M-008":(3,"Measured quantity: seawater pH and carbonate saturation state — a physical-chemical climate variable.","(Legend 3, rule E ii; aligned with [IND-B-197], [GBF-168], [SDG-128])"),
 "IND-M-009":(3,"Measured quantity: strength of the Atlantic Meridional Overturning Circulation (Sv) — a physical climate-system variable.","(Legend 3, rule E ii)"),
 "IND-M-010":(3,"Measured quantity: Arctic September sea-ice extent — a physical climate-system variable.","(Legend 3, rule E ii)"),
 "IND-M-011":(1,"Measured quantity: saltmarsh and other coastal habitat extent, from mapping. No climate data enter it and weather does not materially move the annual value; sea level and storms are long-run drivers.","(Legend 1, rule B; aligned with [GBF-101], [IND-S-026])"),
 "IND-M-012":(1,"Measured quantity: benthic community composition, species distributions and kelp assemblages, from field survey. No climate data enter the measures and they integrate change over years rather than responding materially to a single year's weather; ocean warming is the recognised long-run driver. Projections use habitat-suitability modelling with climate data, but the observed measures do not.","(Legend 1, rule B)"),
 "IND-M-013":(2,"Measured quantity: plankton biomass, community composition and bloom timing from long-term survey and monitoring. Inter-annual sea temperature and stratification move the values materially; climate data are not an input to the indices.","(Legend 2, rule D; aligned with [GBF-111])"),
 "IND-M-014":(2,"Measured quantity: fish distribution, abundance and stock status from surveys and stock assessments, in which sea temperature enters productivity and recruitment models indirectly.","(Legend 2, rule D; aligned with [IND-E-024], [IND-C-115], [IND-B-129])"),
 "IND-M-015":(3,"Measured quantity: seabird and waterbird population indices. The seabird component alone would score 2 (survey index moved by weather, [IND-J-011]); the wintering-waterbird component is analysed with cold-weather movements in mind and scores 3 ([IND-J-013]). Waterbirds are a named part of the measure, so the climate-defined component governs.","(Legend 3, rules F and G; aligned with [IND-J-013]; seabird component as [IND-J-011])"),
 "IND-M-016":(2,"Measured quantity: marine-mammal distribution and range shifts, from surveys and sightings; inter-annual ocean conditions and prey move distribution materially; no climate data enter the measures.","(Legend 2, rule D; aligned with [IND-E-017]; differs from [IND-S-007] cetacean abundance index, an effort-corrected abundance measure scored 1)"),
}
_obs = {t[0]:(t[9],t[10]) for t in T}
for r in ROWS:
    s,basis,cite = SCORING[r["Record_ID"]]
    obs,proj = _obs[r["Record_ID"]]
    r["Climate_Score"]=str(s); r["Climate_Dependency"]=DEP[s]
    r["Climate_Rationale"]=f"{basis} Observed: {obs} Projected: {proj} {cite}"
