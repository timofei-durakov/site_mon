CREATE SEQUENCE public.sitestate_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;

CREATE TABLE public.sitestate
(
    id integer NOT NULL DEFAULT nextval('sitestate_id_seq'::regclass),
    url character varying COLLATE pg_catalog."default" NOT NULL,
    regexp character varying COLLATE pg_catalog."default",
    code integer NOT NULL,
    ts timestamp without time zone NOT NULL,
    has_text boolean,
    CONSTRAINT sitestate_pkey PRIMARY KEY (id),
    CONSTRAINT sitestate_url_key UNIQUE (url)
)