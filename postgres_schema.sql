-- DROP TABLE IF EXISTS public.players;

CREATE TABLE IF NOT EXISTS public.players
(
    player_id integer NOT NULL,
    first_name varchar NOT NULL,
    last_name varchar NOT NULL,
    "position" "char",
    shoots_catches "char",
    height_inches numeric,
    weight_pounds numeric,
    birth_date date,
    birth_country varchar,
    CONSTRAINT players_pkey PRIMARY KEY (player_id)
);


-- DROP TABLE IF EXISTS public.teams;

CREATE TABLE IF NOT EXISTS public.teams
(
    team_id integer NOT NULL,
    franchise_id integer,
    full_name varchar,
    tri_code varchar,
    CONSTRAINT teams_pkey PRIMARY KEY (team_id)
);