DROP TABLE IF EXISTS demographics;
DROP TABLE IF EXISTS medications;

DROP TABLE IF EXISTS remote_sda_resources;
DROP TABLE IF EXISTS form_sda_resources;

DROP TABLE IF EXISTS sda_medications;
DROP TABLE IF EXISTS sda_patient_aliases;
DROP TABLE IF EXISTS sda_patient_numbers;
DROP TABLE IF EXISTS sda_patient_addresses;
DROP TABLE IF EXISTS sda_patients;
DROP TABLE IF EXISTS sda_resources;

DROP TABLE IF EXISTS unit_patients;
DROP TABLE IF EXISTS unit_users;
DROP TABLE IF EXISTS units;

DROP TABLE IF EXISTS facilities;

DROP TABLE IF EXISTS disease_group_patients;
DROP TABLE IF EXISTS disease_group_users;
DROP TABLE IF EXISTS disease_group_features;
DROP TABLE IF EXISTS disease_groups;

DROP TABLE IF EXISTS users;

DROP TABLE IF EXISTS patients;

CREATE TABLE patients (
    id serial PRIMARY KEY
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    username character varying NOT NULL,
    password_hash character varying NOT NULL,
    email character varying NOT NULL,
    is_admin boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE facilities (
    id serial PRIMARY KEY,
    code character varying NOT NULL UNIQUE,
    name character varying NOT NULL
);

CREATE TABLE units (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    facility_id integer REFERENCES facilities (id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE unit_patients (
    id serial PRIMARY KEY,
    unit_id integer NOT NULL REFERENCES units (id) ON DELETE CASCADE ON UPDATE CASCADE,
    patient_id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (unit_id, patient_id)
);

CREATE TABLE unit_users (
    id serial PRIMARY KEY,
    unit_id integer NOT NULL REFERENCES units (id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id integer NOT NULL REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    role character varying NOT NULL,
    UNIQUE (unit_id, user_id)
);

CREATE TABLE disease_groups (
    id serial PRIMARY KEY,
    name character varying NOT NULL
);

CREATE TABLE disease_group_patients (
    id serial PRIMARY KEY,
    disease_group_id integer NOT NULL REFERENCES disease_groups (id) ON DELETE CASCADE ON UPDATE CASCADE,
    patient_id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (disease_group_id, patient_id)
);

CREATE TABLE disease_group_users (
    id serial PRIMARY KEY,
    disease_group_id integer REFERENCES disease_groups (id) ON DELETE CASCADE ON UPDATE CASCADE,
    user_id integer REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE,
    role character varying NOT NULL,
    UNIQUE (disease_group_id, user_id)
);

CREATE TABLE disease_group_features (
    id serial PRIMARY KEY,
    disease_group_id integer not null references disease_groups (id) ON DELETE CASCADE ON UPDATE CASCADE,
    feature_name character varying
);

CREATE TABLE sda_resources (
    id serial primary key,
    patient_id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    facility_id integer NOT NULL REFERENCES facilities (id) ON DELETE CASCADE ON UPDATE CASCADE,
    mpiid integer
);

CREATE TABLE sda_patients (
    id serial PRIMARY KEY,
    sda_resource_id integer NOT NULL REFERENCES sda_resources (id) ON DELETE CASCADE ON UPDATE CASCADE,
    data jsonb
);

CREATE TABLE sda_patient_aliases (
    id serial PRIMARY KEY,
    sda_patient_id integer NOT NULL references sda_patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    data jsonb
);

CREATE TABLE sda_patient_numbers (
    id serial PRIMARY KEY,
    sda_patient_id integer NOT NULL references sda_patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    data jsonb
);

CREATE TABLE sda_patient_addresses (
    id serial PRIMARY KEY,
    sda_patient_id integer NOT NULL references sda_patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    data jsonb
);

CREATE TABLE sda_medications (
    id serial PRIMARY KEY,
    sda_resource_id integer NOT NULL REFERENCES sda_resources (id) ON DELETE CASCADE ON UPDATE CASCADE,
    data jsonb
);

CREATE TABLE form_sda_resources (
    form_id integer,
    form_type character varying,
    sda_resource_id integer REFERENCES sda_resources (id),
    PRIMARY KEY (form_id, form_type)
);

CREATE TABLE remote_sda_resources (
	patient_id integer REFERENCES patients (id),
	facility_id integer REFERENCES facilities (id),
	sda_resource_id integer REFERENCES sda_resources (id),
	PRIMARY KEY (patient_id, facility_id)
);

CREATE TABLE demographics (
    id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    first_name character varying,
    last_name character varying
);

CREATE TABLE medications (
    id serial PRIMARY KEY,
    patient_id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    from_date date NOT NULL,
    to_date date,
    name character varying NOT NULL
);