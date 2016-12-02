CREATE TABLE IF NOT EXISTS landslide.admin2_popatrisk (
    id serial NOT NULL,
    iso3 character(3),
    admin0_name text,  -- unknown codelist
    admin0_code text,  -- country name
    admin1_name text,
    admin1_code text,
    admin2_code text,
    admin2_name text,
    month character(3),
    prob_class_text text, -- low, medium, high, or very_high
    prob_class_int integer, -- 1, 2, 3, 4
    popatrisk integer,
    CONSTRAINT admin2_popatrisk_pkey PRIMARY KEY (id)
);
