--DROP INDEX IF EXISTS gaul_admin0_with_isoalpha3_geom_id;
--DROP MATERIALIZED VIEW gaul_admin0_with_isoalpha3;

CREATE MATERIALIZED VIEW gaul_admin0_with_isoalpha3 AS
SELECT
    LSIB.iso_alpha3 as iso_alpha3,
    G.admin0_code,
    G.admin0_name,
    st_buffer(st_collect(st_simplify(G.mpoly, 0.005)), 0) as geom
FROM lsibdjango_geographicthesaurusentry as LSIB
LEFT JOIN gauldjango_gauladmin0 as G ON LSIB.gaul = G.admin0_code
LEFT JOIN wfppresencedjango_wfpcountry as W ON LSIB.id = W.thesaurus_id
WHERE LSIB.iso_alpha3 IS NOT NULL and W.id IS NOT NULL
GROUP BY LSIB.iso_alpha3, G.admin0_code, G.admin0_name
ORDER BY LSIB.iso_alpha3;
CREATE INDEX gaul_admin0_with_isoalpha3_geom_id ON gaul_admin0_with_isoalpha3 USING gist(geom);

-- If refreshing
--REFRESH MATERIALIZED VIEW gaul_admin0_with_isoalpha3;
--DROP INDEX IF EXISTS gaul_admin0_with_isoalpha3_geom_id;
--CREATE INDEX gaul_admin0_with_isoalpha3_geom_id ON gaul_admin0_with_isoalpha3 USING gist(geom);

SELECT
    iso_alpha3,
    admin0_code,
    admin0_name,
    CASE WHEN length(array_to_string(array_agg(CYCLONE.ogc_fid),',')) > 0 THEN 1 ELSE 0 END as cyclone,
    --CASE WHEN length(array_to_string(array_agg(FLOOD.ogc_fid),',')) > 0 THEN 1 ELSE 0 END as flood
    --CASE WHEN array_agg(LANDSLIDE.ogc_fid) IS NULL THEN 0 ELSE 1 END as landslide
FROM gaul_admin0_with_isoalpha3 as G
LEFT JOIN cyclone.events as CYCLONE ON st_intersects(CYCLONE.wkb_geometry, G.geom)
--LEFT JOIN flood.events as FLOOD ON st_intersects(FLOOD.wkb_geometry, G.geom)
--LEFT JOIN landslide.events as LANDSLIDE ON st_intersects(LANDSLIDE.wkb_geometry, G.geom)
GROUP BY G.iso_alpha3, G.admin0_code, G.admin0_name
ORDER BY G.iso_alpha3;
