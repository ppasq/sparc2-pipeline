CREATE TABLE IF NOT EXISTS drought.admin2_popatrisk (
    id serial NOT NULL,
    iso3 character(3),
    admin0_name text,  -- unknown codelist
    admin0_code text,  -- country name
    admin1_name text,
    admin1_code text,
    admin2_code text,
    admin2_name text,
    month character(3),
    prob double precision, -- probability
    popatrisk integer,
    CONSTRAINT admin2_popatrisk_pkey PRIMARY KEY (id)
);
