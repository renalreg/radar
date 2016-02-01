CREATE TABLE renal_diagnoses (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    patient_id integer NOT NULL,
    onset_date date,
    esrf_date date,
    created_user_id integer NOT NULL,
    created_date timestamp with time zone DEFAULT now() NOT NULL,
    modified_user_id integer NOT NULL,
    modified_date timestamp with time zone DEFAULT now() NOT NULL
);

ALTER TABLE ONLY renal_diagnoses
    ADD CONSTRAINT renal_diagnoses_patient_id_key UNIQUE (patient_id);

ALTER TABLE ONLY renal_diagnoses
    ADD CONSTRAINT renal_diagnoses_pkey PRIMARY KEY (id);

CREATE INDEX renal_diagnoses_patient_idx ON renal_diagnoses USING btree (patient_id);

ALTER TABLE ONLY renal_diagnoses
    ADD CONSTRAINT renal_diagnoses_created_user_id_fkey FOREIGN KEY (created_user_id) REFERENCES users(id);

ALTER TABLE ONLY renal_diagnoses
    ADD CONSTRAINT renal_diagnoses_modified_user_id_fkey FOREIGN KEY (modified_user_id) REFERENCES users(id);

ALTER TABLE ONLY renal_diagnoses
    ADD CONSTRAINT renal_diagnoses_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES patients(id) ON UPDATE CASCADE ON DELETE CASCADE;
