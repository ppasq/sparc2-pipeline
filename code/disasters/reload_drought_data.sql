INSERT INTO drought.admin2_popatrisk (
    iso3,
    admin0_code, admin0_name, admin1_code, admin1_name, admin2_code, admin2_name,
    month,
    prob,
    popatrisk
)
SELECT
    iso3,
    A.ADM0_CODE, g.adm0_name, A.ADM1_CODE, G.adm1_name, A.ADM2_CODE, G.adm2_name,
    month,
    freq / 100.0 as prob,
    popatrisk
FROM drought.admin2_raw as A
LEFT JOIN gaul.admin2_polygons as G ON A.ADM2_CODE = G.adm2_code;
