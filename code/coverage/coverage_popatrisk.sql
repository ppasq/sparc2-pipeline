SELECT
    LSIB.iso_alpha3 as iso_alpha3,
    G.admin0_code,
    G.admin0_name,
    CASE WHEN CYCLONE.iso3 IS NULL THEN 0 ELSE 1 END as cyclone,
    0 as drought,
    CASE WHEN FLOOD.iso3 IS NULL THEN 0 ELSE 1 END as flood,
    CASE WHEN LANDSLIDE.iso3 IS NULL THEN 0 ELSE 1 END as landslide
FROM lsibdjango_geographicthesaurusentry as LSIB
LEFT JOIN gauldjango_gauladmin0 as G ON LSIB.gaul = G.admin0_code
LEFT JOIN wfppresencedjango_wfpcountry as W ON LSIB.id = W.thesaurus_id
LEFT JOIN ( SELECT iso3 FROM cyclone.admin2_popatrisk GROUP BY iso3 ORDER BY iso3 ) as CYCLONE ON LSIB.iso_alpha3 = CYCLONE.iso3
LEFT JOIN ( SELECT iso3 FROM flood.admin2_popatrisk GROUP BY iso3 ORDER BY iso3 ) as FLOOD ON LSIB.iso_alpha3 = FLOOD.iso3
LEFT JOIN ( SELECT iso3 FROM landslide.admin2_popatrisk GROUP BY iso3 ORDER BY iso3 ) as LANDSLIDE ON LSIB.iso_alpha3 = LANDSLIDE.iso3
WHERE LSIB.iso_alpha3 IS NOT NULL and W.id IS NOT NULL
GROUP BY LSIB.iso_alpha3, G.admin0_code, G.admin0_name, CYCLONE.iso3, FLOOD.iso3, LANDSLIDE.iso3
ORDER BY LSIB.iso_alpha3
