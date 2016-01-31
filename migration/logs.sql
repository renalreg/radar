CREATE TABLE logs (
    id integer NOT NULL,
    date timestamp with time zone DEFAULT now() NOT NULL,
    type character varying NOT NULL,
    user_id integer,
    table_name character varying,
    original_data jsonb,
    new_data jsonb,
    statement character varying,
    data jsonb
);

CREATE SEQUENCE logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE logs_id_seq OWNED BY logs.id;

ALTER TABLE ONLY logs ALTER COLUMN id SET DEFAULT nextval('logs_id_seq'::regclass);

ALTER TABLE ONLY logs ADD CONSTRAINT logs_pkey PRIMARY KEY (id);

CREATE INDEX logs_date_idx ON logs USING btree (date);
