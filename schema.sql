DROP TABLE IF EXISTS medications;
DROP TABLE IF EXISTS sda_medications;
DROP TABLE IF EXISTS sda_containers;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS users;

CREATE TABLE patients (
    id serial NOT NULL,
    first_name character varying,
    last_name character varying,
    CONSTRAINT patients_pkey PRIMARY KEY (id)
);

CREATE TABLE users (
    id serial NOT NULL,
    username character varying,
    password_hash character varying,
    email character varying,
    CONSTRAINT users_pkey PRIMARY KEY (id)
);

CREATE TABLE sda_containers (
    id serial NOT NULL,
    CONSTRAINT sda_containers_pkey PRIMARY KEY (id)
);

CREATE TABLE sda_medications (
    id serial NOT NULL,
    sda_container_id integer,
    from_time timestamp,
    to_time timestamp,
    CONSTRAINT sda_medications_pkey PRIMARY KEY (id),
    CONSTRAINT sda_medications_sda_container_id_fkey FOREIGN KEY (sda_container_id)
        REFERENCES sda_containers (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE medications (
    id serial NOT NULL,
    patient_id integer,
    from_date date,
    to_date date,
    name character varying,
    sda_container_id integer,
    CONSTRAINT medications_pkey PRIMARY KEY (id),
    CONSTRAINT medications_patient_id_fkey FOREIGN KEY (patient_id)
        REFERENCES patients (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT medications_sda_container_id_fkey FOREIGN KEY (sda_container_id)
        REFERENCES sda_containers (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

INSERT INTO patients VALUES (DEFAULT, 'Homer', 'Simpson');
INSERT INTO patients VALUES (DEFAULT, 'Marge', 'Simpson');
INSERT INTO patients VALUES (DEFAULT, 'Bart', 'Simpson');

-- Note: username: username, password: password
-- Note: plaintext password used here but application will hash passwords
-- Note: generated with werkzeug.security.generate_password_hash('password', method='plain')
INSERT INTO users VALUES (DEFAULT, 'username', 'plain$$password', 'username@example.org');

-- Homer's medications
INSERT INTO medications VALUES (DEFAULT, 1, '2015-01-01', '2015-02-01', 'Paracetamol');
INSERT INTO medications VALUES (DEFAULT, 1, '2015-01-02', '2015-02-02', 'Ibuprofen');
INSERT INTO medications VALUES (DEFAULT, 1, '2015-01-03', '2015-02-03', 'Aspirin');