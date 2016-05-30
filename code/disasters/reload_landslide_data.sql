INSERT INTO landslide.admin2_popatrisk (
    iso3,
    admin0_code, admin0_name, admin1_code, admin1_name, admin2_code, admin2_name,
    jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, "dec"
)
SELECT
    iso3,
    adm0_code, adm0_name, adm1_code, adm1_name, adm2_code, adm2_name,
    january, february, march, april, may, june, july, august, september, october, november, december
FROM landslide.admin2_polygons;
