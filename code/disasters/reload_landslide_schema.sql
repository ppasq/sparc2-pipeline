CREATE TABLE IF NOT EXISTS landslide.admin2_popatrisk (
    id serial NOT NULL,
    iso3 character(3),
    admin0_name text,  -- unknown codelist
    admin0_code text,  -- country name
    admin1_name text,
    admin1_code text,
    admin2_code text,
    admin2_name text,
    jan integer,
    feb integer,
    mar integer,
    apr integer,
    may integer,
    jun integer,
    jul integer,
    aug integer,
    sep integer,
    oct integer,
    nov integer,
    "dec" integer,
    CONSTRAINT admin2_popatrisk_pkey PRIMARY KEY (id)
);
