DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS demographics;
DROP TABLE IF EXISTS sda_medications;
DROP TABLE IF EXISTS sda_patients;
DROP TABLE IF EXISTS sda_containers;
DROP TABLE IF EXISTS unit_patients;
DROP TABLE IF EXISTS unit_users;
DROP TABLE IF EXISTS disease_group_patients;
DROP TABLE IF EXISTS disease_group_users;
DROP TABLE IF EXISTS disease_group_features;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS facilities;
DROP TABLE IF EXISTS disease_groups;

CREATE TABLE patients (
    id serial PRIMARY KEY
);

CREATE TABLE users (
    id serial PRIMARY KEY,
    username character varying NOT NULL,
    password_hash character varying NOT NULL,
    email character varying NOT NULL
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
    UNIQUE (disease_group_id, user_id)
);

CREATE TABLE disease_group_features (
    id serial PRIMARY KEY,
    disease_group_id integer not null references disease_groups (id) ON DELETE CASCADE ON UPDATE CASCADE,
    feature_name character varying
);

CREATE TABLE sda_containers (
    id serial PRIMARY KEY,
    patient_id integer not null REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    facility_id integer NOT NULL REFERENCES facilities (id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE sda_patients (
    id serial PRIMARY KEY,
    sda_container_id integer NOT NULL REFERENCES sda_containers (id) ON DELETE CASCADE ON UPDATE CASCADE,
    name_name_prefix character varying,
    name_given_name character varying,
    name_middle_name character varying,
    name_family_name character varying,
    name_preferred_name character varying,
    gender_coding_standard character varying,
    gender_code character varying,
    gender_description character varying,
    birth_time timestamp,
    death_time timestamp
);

CREATE TABLE sda_medications (
    id serial PRIMARY KEY,
    sda_container_id integer NOT NULL REFERENCES sda_containers (id) ON DELETE CASCADE ON UPDATE CASCADE,
    from_time timestamp,
    to_time timestamp
);

CREATE TABLE medications (
    id serial PRIMARY KEY,
    patient_id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    from_date date NOT NULL,
    to_date date,
    name character varying NOT NULL,
    sda_container_id integer REFERENCES sda_containers (id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE demographics (
    id serial PRIMARY KEY,
    patient_id integer NOT NULL REFERENCES patients (id) ON DELETE CASCADE ON UPDATE CASCADE,
    sda_container_id integer REFERENCES sda_containers (id) ON DELETE SET NULL ON UPDATE CASCADE,
    first_name character varying,
    last_name character varying
);

INSERT INTO units VALUES (DEFAULT, 'Springfield General Hospital');
INSERT INTO units VALUES (DEFAULT, 'East Hampton Hospital');

INSERT INTO disease_groups VALUES (DEFAULT, 'SRNS');
INSERT INTO disease_groups VALUES (DEFAULT, 'MPGN');
INSERT INTO disease_groups VALUES (DEFAULT, 'Salt Wasting');

INSERT INTO disease_group_features VALUES (DEFAULT, 1, 'DIAGNOSIS');
INSERT INTO disease_group_features VALUES (DEFAULT, 2, 'DIAGNOSIS');
INSERT INTO disease_group_features VALUES (DEFAULT, 3, 'DIAGNOSIS');
INSERT INTO disease_group_features VALUES (DEFAULT, 3, 'RENAL_IMAGING');

-- INSERT INTO patients VALUES (DEFAULT, 'Homer', 'Simpson');
-- INSERT INTO patients VALUES (DEFAULT, 'Marge', 'Simpson');
-- INSERT INTO patients VALUES (DEFAULT, 'Bart', 'Simpson');
-- INSERT INTO patients VALUES (DEFAULT, 'Caroline', 'Todd');
-- INSERT INTO patients VALUES (DEFAULT, 'John', 'Smith');

INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);

INSERT INTO unit_patients VALUES (DEFAULT, 1, 1);
INSERT INTO unit_patients VALUES (DEFAULT, 1, 2);
INSERT INTO unit_patients VALUES (DEFAULT, 1, 3);
INSERT INTO unit_patients VALUES (DEFAULT, 2, 4);
INSERT INTO unit_patients VALUES (DEFAULT, 1, 5);
INSERT INTO unit_patients VALUES (DEFAULT, 2, 5);

INSERT INTO disease_group_patients VALUES (DEFAULT, 1, 1);
INSERT INTO disease_group_patients VALUES (DEFAULT, 2, 1);
INSERT INTO disease_group_patients VALUES (DEFAULT, 3, 1);

INSERT INTO disease_group_patients VALUES (DEFAULT, 2, 2);
INSERT INTO disease_group_patients VALUES (DEFAULT, 2, 3);

-- Note: username: username, password: password
-- Note: plaintext password used here but application will hash passwords
-- Note: generated with werkzeug.security.generate_password_hash('password', method='plain')
INSERT INTO users VALUES (DEFAULT, 'username', 'plain$$password', 'username@example.org');
INSERT INTO users VALUES (DEFAULT, 'srns', 'plain$$password', 'srns@example.org');

INSERT INTO unit_users VALUES (DEFAULT, 1, 1);

INSERT INTO disease_group_users VALUES (DEFAULT, 1, 1);
INSERT INTO disease_group_users VALUES (DEFAULT, 2, 1);
INSERT INTO disease_group_users VALUES (DEFAULT, 1, 2);

-- Homer's medications
INSERT INTO medications VALUES (DEFAULT, 1, '2015-01-01', '2015-02-01', 'Paracetamol');
INSERT INTO medications VALUES (DEFAULT, 1, '2015-01-02', '2015-02-02', 'Ibuprofen');
INSERT INTO medications VALUES (DEFAULT, 1, '2015-01-03', '2015-02-03', 'Aspirin');

INSERT INTO facilities VALUES (DEFAULT, 'TEST', 'Test Facility');

INSERT INTO sda_containers VALUES (DEFAULT, 1, 1);
INSERT INTO sda_patients VALUES (DEFAULT, 1, 'Mr', 'Homer', 'Jay', 'Simpson', 'Homer', 'RENAL', '1', 'Male', '1955-05-12');