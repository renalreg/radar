# RaDaR 1 to RaDaR 2 Migration

This is a brief overview of the tables in RaDaR 1 and how they will be migrated into RaDaR 2.

# Users

* `rdr_user_mapping` - one-to-one table mapping RaDaR users (`tbl_users` table) to PatientView users (`user` table) with a role (e.g. `ROLE_SUPER_USER`)
* `tbl_adminusers` - old table of admin users (`tbl_users.uId`)
* `tbl_users` - RaDaR users
* `user` - PatientView users
* `usermappings` - many-to-many table mapping PatientView users to their units (joining `usermappings.unitcode` on `unit.unitcode`)
* `unit` - groups (units and cohorts)

User details (e.g. first name and last name) are duplicated in the `tbl_users` and `user` table. The `user` table will be used for migration.

All existing RaDaR users will be migrated (all users in `tbl_users`). Once RaDaR has gone live inactive accounts will be disabled and new accounts added based on Mel's list.

# Patients

* `patient` - RaDaR and PV patients (RaDaR users have a `radarNo`). One row per patient and unitcode combination (e.g. patient who is attending / has attended multiple units)
* `tbl_patient_users` - probably from when patients could log into RaDaR
* `tbl_demographics` - the SRNS and MPGN groups have their own demographics form which is stored here
* `usermapping` - many-to-many table mapping patients to their groups (joining `patient.nhsno` to `usermapping.nhsno`)

All but one patient in `tbl_demographics` is in the `patient` table. The `patient` table is updated by the PatientView feed so this should be used over the `tbl_demographics` table which is only updated by hand.

Patients in the `patients` table whose `dateofbirth` is `null` have been entered manually (i.e. data not sent electronically). Some of these may be paediatric patients with incomplete demographics. Where possible these should be corrected by hand using data from the `tbl_demographics` table.

There is one record in the `patients` table for each of the units that has sent in data for that patient. We will only be migrating the last updated record (determined using the `log` table). Data from other units will arrive via the UKRDC.

# Consultants

* `tbl_consultants` - consultants on RaDaR
* `tbl_demographics` - the `cons_neph` column stores the ID (referencing either the `tbl_consultants` or `tbl_users` table) of the SRNS or MPGN patient's nephrologist
* `patient` - the `consNeph` column stores the ID of the patient's nephrologist (refers to either `user.id` or `tbl_consultants.cId`)
* `user` - RaDaR and PatientView users

We should use the `consNeph` column from the `patient` table. Some of these IDs refer to a row in the `tbl_consultants` table while others refer to a row in the `user` table. Some IDs are in both tables so we need to be careful not to assign a patient a consultant who is actually another patient. We should check the `tbl_consultants` table first, then check the `user` table for a user with the `isclinician` flag set. It's likely that some patients will have had the ID of their nephrologist corrupted as they weren't migrated properly (updating `tbl_consultants.cId` references to `users.id`). The drop-down is populated from the `user` table but some records are using an ID from the `tbl_consultants` table. When the demographics page is saved the consultant defaults to the first one in the drop-down.

# Patient Data

* `diagnosis` - unstructured diagnoses
* `medicine` - medications currently held on the renal system (may be historic)
* `testresult` - test results (e.g. creatinine)

The `medicine` table contains both medications received in the PatientView feed and medications entered by hand in RaDaR. Only the RaDaR medications will be migrated (where the `unitcode` is a RaDaR cohort). The PatientView medications will be received via the UKRDC (HealthShare) so don't need to be migrated.

The `testresult` table contains test results from the PatientView feed (no hand entered results) - again these will be received from the UKRDC so don't need to migrated.

Diagnoses aren't coded (just free text) so we don't bother with those for now.
