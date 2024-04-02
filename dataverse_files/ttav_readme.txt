This readme was generated 2023-03-27 by Kelly O'Neill.

Title of dataset: The Tsar's Trans-Atlantic Voyagers
Authors: Vivian Wei, Imperiia Project research assistant; Dr. Kelly O'Neill, Imperiia Project Director, Davis Center for Russian and Eurasian Studies, Harvard University
Contact: koneill@fas.harvard.edu
Spatial coverage: 1834-1897
Geographic coverage: Belarus, Finland, Poland, Russian Federation, Ukraine
Project funding: Davis Center for Russian and Eurasian Studies, Harvard University

SHARING AND ACCESS
DOI: https://doi.org/10.7910/DVN/OJLQNO
License: CC BY-NC 4.0 (Attribution-NonCommercial 4.0 International)
Cite the data: Vivian Wei and Kelly O'Neill, 2023, The Tsar's Trans-Atlantic Voyagers, https://doi.org/10.7910/DVN/OJLQNO, Harvard Dataverse, version 1 (2023-03-29).
Original version: National Archives. Data Files Relating to the Immigration of Russians to the United States, created, ca. 1977 - 2002, documenting the period 1834 - 1897. Creator: Balch Institute for Ethnic Studies. Center for Immigration Research. https://aad.archives.gov/aad/fielded-search.jsp?dt=2126&tf=F

FILE FORMATS
data: csv (11 files)
geospatial: geojson (3 files) /shp (3 files)
data model: pdf (1 file)

FILE LIST
ttav_codebook (csv)
ttav_datamodel (pdf)
ttav_gender_indicator_fam (csv)
ttav_gender_indicator_fn (csv)
ttav_gender_indicator_occ (csv)
ttav_occupations (csv)
ttav_passengers (csv)
ttav_ports (csv; geojson; shp)
ttav_lkresidences (csv; geojson; shp)
ttav_routes (csv; geojson; shp)
ttav_ships (csv)
ttav_travelgroups (csv)
ttav_voyages (csv)

ATTRIBUTES: See Codebook.

FILE NOTES
Occupations: 681 occupation listings, 64 occupational categories derived from the 1897 census, 16 major groupings. Occupation names were preserved from original data. Category names dervied from the 1897 census data. The list of occupational group names was compiled and applied by VW & KO. All roles determined to describe family status (such as WIFE, SON, SPINSTER) were grouped into the "family relationship data" (code 681). Family relationship roles were migrated to separate passenger attribute.
Passengers: 527,394 passengers. We made no changes to the spelling of names or last residence designations. Ages of those less than one year were converted from NARA code to decimal. Age designations likely vary in reliability (see, for example, the case of Doni Michalowski, listed as a child, age 99). Values rendered in capital letters were rendered as such in the NARA tables.
Ports: 78 sites are listed as departure, interim, or arrival ports. Where the same port is referenced by various names in the original data we consolidated to a single feaure. 
Last known residences (LKR): Field value = "unknown" or "no data" in over 70% of passenger records. 14% of passengers identified a location within the Russian Empire as their LKR (the rest are included in the NARA data because of their declared country of origin). Coordinate locations are given for 182 LKRs, including 1) LKRs named by 75 or more passengers; 2) LKRs named fewer than 75 times but located within tsarist territory. 15,585 placenames are attested (give or take), 48% of which occur only once. Single occurrences are not included in the LKR file except in a handful of cases. In "resID" 244 = unmapped (because of low # of attestations or inability to determine GeoNames match); 245 = unknown. 
Routes: The csv lists all 150 routes. The geojson file include 145 routes. Routes 131 and 150 departed from ports whose location is ambiguous; routes 146, 147, and 148 are listed as departing from "unknown" ports. The routes are depicted with lines and polylines. The port sequence is a best guess: the order in which interim ports are listed in the NARA data is not reliable for establishing sequence. Note also that the routes are depicted with simple point-to-point lines that often run overland: the lines are schematic and do not reflect actual sailing routes.
Ships: 781 ships. In cases where a decade or more passed between sailings we decided that the two ships were unique. In the NARA data ship 781 was listed as the "TENTONIC". We assumed a spelling error and listed the ship as the "TEUTONIC" but made no other changes to the spelling of ship names.
Travel groups: 315,959 travel groups. "Travel group" refers to the quantity of passengers sharing a last name and MID (in other words, on the same voyage). Group size ranges from 1 to 161.
Voyages: 10,761 voyages attested in the NARA records. This file defines the voyage object as a compilation of route and ship, related through the MID.

USAGE NOTES
This is a relational database. Each feature in a table has a unique identifier. The most important connections across tables are made through the MID and RouteID. See the Data Model.
The spatial data files (ports and routes) contain the relevant data from the corresponding csv files (via spatial join).
Note on the "sex" designation ("passengers" file). In many cases there is an apparent discrepancy between the first name, sex, and occupation/family role. Users wanting to explore ratios of male/female immigrants should cross-check the "passenger" data using the 3 gender indicator files.

VERSIONING: All changes to this dataset will be documented in a changelog in this README file.
V1: March 27, 2023 (original publication)