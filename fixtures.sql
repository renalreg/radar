INSERT INTO units VALUES (DEFAULT, 'Springfield General Hospital');
INSERT INTO units VALUES (DEFAULT, 'East Hampton Hospital');

INSERT INTO disease_groups VALUES (DEFAULT, 'SRNS');
INSERT INTO disease_groups VALUES (DEFAULT, 'MPGN');
INSERT INTO disease_groups VALUES (DEFAULT, 'Salt Wasting');

INSERT INTO disease_group_features VALUES (DEFAULT, 1, 'DIAGNOSIS');
INSERT INTO disease_group_features VALUES (DEFAULT, 2, 'DIAGNOSIS');
INSERT INTO disease_group_features VALUES (DEFAULT, 3, 'DIAGNOSIS');

INSERT INTO disease_group_features VALUES (DEFAULT, 3, 'RENAL_IMAGING');
INSERT INTO disease_group_features VALUES (DEFAULT, 3, 'SALT_WASTING_CLINICAL_FEATURES');

INSERT INTO disease_group_features VALUES (DEFAULT, 1, 'GENETICS');

INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);
INSERT INTO patients VALUES (DEFAULT);

-- Springfield patients
INSERT INTO unit_patients VALUES (DEFAULT, 1, 1);
INSERT INTO unit_patients VALUES (DEFAULT, 1, 2);
INSERT INTO unit_patients VALUES (DEFAULT, 1, 3);

-- East Hampton patients
INSERT INTO unit_patients VALUES (DEFAULT, 2, 4);
INSERT INTO unit_patients VALUES (DEFAULT, 2, 5);

-- SRNS patients
INSERT INTO disease_group_patients VALUES (DEFAULT, 1, 1);

-- MPGN patients
INSERT INTO disease_group_patients VALUES (DEFAULT, 2, 2);

-- Salt Wasting patients
INSERT INTO disease_group_patients VALUES (DEFAULT, 3, 3);

INSERT INTO facilities VALUES (DEFAULT, 'RADAR', 'RADAR');

-- Note: username: username, password: password
-- Note: plaintext password used here but application will hash passwords
-- Note: generated with werkzeug.security.generate_password_hash('password', method='plain')
INSERT INTO users VALUES (DEFAULT, 'admin', 'plain$$password', 'admin@example.org', 'Foo', 'Bar', true);

INSERT INTO dialysis_types (id, name) VALUES (DEFAULT, 'HD');