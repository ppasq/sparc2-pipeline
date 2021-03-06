CREATE TABLE IF NOT EXISTS context.admin2_context (
    id serial NOT NULL,
    iso3 character(3),
    admin0_name text,  -- unknown codelist
    admin0_code text,  -- country name
    admin1_name text,
    admin1_code text,
    admin2_code text,
    admin2_name text,
    delta_negative double precision,
    delta_positive double precision,
    delta_mean double precision,
    delta_forest double precision,
    delta_crop double precision,
    erosion_propensity double precision,
    ldi integer,
    mask integer,
    CONSTRAINT admin2_context_pkey PRIMARY KEY (id)
);

INSERT INTO context.admin2_context (
    iso3,
    admin0_code, admin0_name, admin1_code, admin1_name, admin2_code, admin2_name,
    delta_negative, delta_positive, delta_mean, delta_forest, delta_crop,
    erosion_propensity, ldi,
    mask
)
SELECT
    iso3,
    A.ADM0_CODE, g.adm0_name, A.ADM1_CODE, G.adm1_name, A.ADM2_CODE, G.adm2_name,
    NCH1_12, PCH1_12, MEAN_12,
    FOR_2,
    CROP_2,
    EROSION1_2,
    LDI,
    NOCHNG_2
    FROM context.admin2_polygons as A
    LEFT JOIN gaul.admin2_polygons as G ON A.ADM2_CODE = G.adm2_code;
