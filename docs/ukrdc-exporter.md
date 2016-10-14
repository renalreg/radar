# UKRDC Exporter

The UKRDC exporter exports patients to the UKRDC.

## What is exported?

### Demographics

| Name          | RaDaR                                | SDA                                     |
|---------------|--------------------------------------|-----------------------------------------|
| First name    | `patient_demographics.first_name`    | `Patient.Name.GivenName`                |
| Last name     | `patient_demographics.last_name`     | `Patient.Name.FamilyName`               |
| Date of birth | `patient_demographics.date_of_birth` | `Patient.DateBirth`                     |
| Date of death | `patient_demographics.date_of_death` | `Patient.DateDeath`                     |
| Gender        | `patient_demographics.gender`        | `Patient.Gender.Code`                   |
| Ethnicity     | `patient_demographics.ethnicity`     | `Patient.EthnicGroup.Code`              |
| Home number   | `patient_demographics.home_number`   | `Patient.ContactInfo.HomePhoneNumber`   |
| Mobile number | `patient_demographics.mobile_number` | `Patient.ContactInfo.MobilePhoneNumber` |
| Work number   | `patient_demographics.work_number`   | `Patient.ContactInfo.WorkPhoneNumber`   |
| Email address | `patient_demographics.email_address` | `Patient.ContactInfo.EmailAddress`      |

### Aliases

| Name       | RaDaR                        | SDA                          |
|------------|------------------------------|------------------------------|
| First name | `patient_aliases.first_name` | `Patient.Aliases.GivenName`  |
| Last name  | `patient_aliases.last_name`  | `Patient.Aliases.FamilyName` |

### Addresses

| Name      | RaDaR                                                                                                                  | SDA                          |
|-----------|------------------------------------------------------------------------------------------------------------------------|------------------------------|
| From date | `patient_address.to_date`                                                                                              | `Patient.Addresses.FromTime` |
| To date   | `patient_address.from_date`                                                                                            | `Patient.Addresses.ToTime`   |
| Address   | `patient_addresses.address1`, `patient_addresses.address2`, `patient_addresses.address3`, `patient_addresses.address4` | `Patient.Addresses.Street`   |
| Postcode  | `patient_addresses.postcode`                                                                                           | `Patient.Addresses.Zip.Code` |

### Patient Numbers

| Name         | RaDaR                                            | SDA
|--------------|--------------------------------------------------|-----------------------------------------------
| Number       | `patient.id` and `patient_numbers.number`        | `Patient.PatientNumbers.Number`
| Number type  | `NI` for NHS, CHI, H&C numbers. Otherwise `MRN`. | `Patient.PatientNumbers.NumberType`
| Organisation | RaDAR or `patient_numbers.number_group_id`       | `Patient.PatientNumbers.Organization.Code`

### Medications

| Name         | RaDaR                                                                              | SDA                                                  |
|--------------|------------------------------------------------------------------------------------|------------------------------------------------------|
| ID           | `medications.id`                                                                   | `Medications.ExternalID`                             |
| From Date    | `medications.from_date`                                                            | `Medications.FromTime`                               |
| To Date      | `medications.to_date`                                                              | `Medications.ToTime`                                 |
| Drug         | `medications.drug_text` or `medications.drug_id`                                   | `Medications.DrugProduct.ProductName`                |
| Dose         | `medications.dose_text` or `medications.dose_quantity` and `medications.dose_unit` | `Medications.DoseQuantity` and `Medications.DoseUoM` |
| Route        | `medications.route`                                                                | `Medications.Route.Code`                             |
| Frequency    | `medications.frequency`                                                            | `Medications.Frequency.Code`                         |
| Source group | `medications.source_group_id`                                                      | `Medications.EnteringOrganization`                   |

### Results

Only observations with a PV code are exported. All observations can be exported once they are LOINC coded.

| Name         | RaDaR                     | SDA                                              |
|--------------|---------------------------|--------------------------------------------------|
| ID           | `results.id`              | `LabOrders.ExternalID`                           |
| Date         | `results.date`            | `LabOrders.Result.ResultItems.ObservationTime`   |
| Observation  | `results.observation_id`  | `LabOrders.Result.ResultItems.TestItemCode.Code` |
| Value        | `results.value`           | `LabOrders.Result.ResultItems.ResultValue`       |
| Source group | `results.source_group_id` | `LabOrders.EnteringOrganization`                 |

### Groups

Currently just the RaDaR group.

| Name      | RaDaR                      | SDA                                                                          |
|-----------|----------------------------|------------------------------------------------------------------------------|
| From date | `patient_groups.from_date` | `ProgramMemberships.FromTime`                                                |
| Group     | `patient_groups.group_id`  | `ProgramMemberships.ProgramName` and `ProgramMemberships.ProgramDescription` |

## Exporting Patients

The `radar-ukrdc-exporter` script checks the database for updated patients and add thems to a queue to be exported.
The script determines which patients have been updated by looking at `INSERT`, `UPDATE` and `DELETE` entries in the `logs` table.

The script can be run with the `--state-file FILENAME` to keep track of the log entries already processed.
The state file stores the `id` of the last log entry processed.
By default only log entries after this `id` are considered.
You can use the `--all` option to search all log entries (the state file will be updated as normal).
The script will lock the state file while it is running which prevent jobs overlapping (e.g. in cron) and patients being exported multiple times.

## Worker

Run the worker with:

```
RADAR_SETTINGS=/path/to/settings.py celery -A radar.ukrdc_exporter.worker worker -Q ukrdc_exporter
```

The number of worker processes/threads can be controlled with the `--concurrency` option. By default this is the number of CPUs on the machine.

The log level can be controlled using the `--loglevel` option, for example `INFO` level is set using `--loglevel=INFO`.

## Services

The `ukrdc_exporter` role in [radar-ansible](https://github.com/renalreg/radar-ansible) installs three systemd services:

* `radar-ukrdc-exporter-celery` - runs the celery workers.
* `radar-ukrdc-exporter-changed` - hourly job to add modified patients to the export queue.
* `radar-ukrdc-exporter-all` - daily job to add all patients to the export queue.

`radar-ukrdc-exporter-changed` and `radar-ukrdc-exporter-all` are run using systemd timers (see the corresponding `.timer` files).

You can view timers with `systemctl list-timers` and disable them with `systemctl disable $NAME.timer`.

You can run `radar-ukrdc-exporter-all` or `radar-ukrdc-exporter-changed` manually using `systemctl start`, e.g. `systemctl start radar-ukrdc-exporter-all`.
