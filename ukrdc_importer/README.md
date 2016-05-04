# UKRDC Importer

The UKRDC importer imports patient records from the UKRDC into RaDaR.

## What is imported?

### Patient

| Name          | SDA                                     | RaDaR                                |
|---------------|-----------------------------------------|--------------------------------------|
| First name    | `Patient.Name.GivenName`                | `patient_demographics.first_name`    |
| Last name     | `Patient.Name.FamilyName`               | `patient_demographics.last_name`     |
| Date of birth | `Patient.BirthTime`                     | `patient_demographics.date_of_birth` |
| Date of death | `Patient.DeathTime`                     | `patient_demographics.date_of_death` |
| Gender        | `Patient.Gender.Code`                   | `patient_demographics.gender`        |
| Ethnicity     | `Patient.EthnicGroup.Code`              | `patient_demographics.ethnicity`     |
| Home number   | `Patient.ContactInfo.HomePhoneNumber`   | `patient_demographics.home_number`   |
| Work number   | `Patient.ContactInfo.WorkPhoneNumber`   | `patient_demographics.work_number`   |
| Mobile number | `Patient.ContactInfo.MobilePhoneNumber` | `patient_demographics.mobile_number` |
| Email address | `Patient.ContactInfo.EmailAddress`      | `patient_demographics.email_address` |

### Aliases

| Name       | SDA                          | RaDaR                        |
|------------|------------------------------|------------------------------|
| First name | `Patient.Aliases.GivenName`  | `patient_aliases.first_name` |
| Last name  | `Patient.Aliases.FamilyName` | `patient_aliases.last_name`  |

### Addresses

| Name           | SDA                              | RaDaR                         |
|----------------|----------------------------------|-------------------------------|
| From date      | `Patient.Addresses.FromTime`     | `patient_addresses.from_date` |
| To date        | `Patient.Addresses.ToTime`       | `patient_addresses.to_date`   |
| Address Line 1 | `Patient.Addresses.Street`       | `patient_addresses.address_1` |
| Address Line 2 | `Patient.Addresses.City.Code`    | `patient_addresses.address_2` |
| Address Line 3 | `Patient.Addresses.State.Code`   | `patient_addresses.address_3` |
| Address Line 4 | `Patient.Addresses.Country.Code` | `patient_addresses.address_4` |
| Postcode       | `Patient.Addresses.Zip.Code`     | `patient_addresses.postcode`  |

### Patient Numbers

| Name         | SDA                                        | RaDaR                          |
|--------------|--------------------------------------------|--------------------------------|
| Number       | `Patient.PatientNumbers.Number`            | `patient_numbers.number`       |
| Number group | `Patient.PatientNumbers.Organization.Code` | `patient_numbers.number_group` |

### Medications

| Name         | SDA                                                                  | RaDaR                      |
|--------------|----------------------------------------------------------------------|----------------------------|
| ID           | `Medications.EnteringOrganization.Code` and `Medications.ExternalId` | `medications.id`           |
| From date    | `Medications.FromTime`                                               | `medications.from_date`    |
| To date      | `Medications.ToTime`                                                 | `medications.to_date`      |
| Drug         | `Medications.DrugProduct.ProductName`                                | `medications.drug_text`    |
| Dose         | `Medications.DoseUoM.Code`                                           | `medications.dose_text`    |
| Source group | `Medications.EnteringOrganization.Code`                              | `medications.source_group` |

### Lab Orders

| Name         | SDA                                                                                                                | RaDaR                    |
|--------------|--------------------------------------------------------------------------------------------------------------------|--------------------------|
| ID           | `LabOrders.EnteringOrganization.Code`, `LabOrders.ExternalId` and `LabOrders.Result.ResultItems.TestItemCode.Code` | `results.id`             |
| Date         | `LabOrders.Result.ResultItems.ObservationTime` or `LabOrders.FromTime`                                             | `results.date`           |
| Observation  | `LabOrders.Result.ResultItems.TestItemCode.Code`                                                                   | `results.observation_id` |
| Value        | `LabOrders.Result.ResultItems.ResultValue`                                                                         | `results.value`          |
| Source group | `LabOrders.EnteringOrganization.Code`                                                                              | `results.source_group`   |

## Example Settings

```
# settings.py
SQLALCHEMY_DATABASE_URI = 'postgres://radar:password@localhost/radar'
SQLALCHEMY_TRACK_MODIFICATIONS = False
CELERY_BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = False
```

## API

Run the API with:

```
RADAR_SETTINGS=$(pwd)/settings.py python radar_ukrdc/api.py
```

| URL            | HTTP Method | Input                                          | Output                                    |
|----------------|-------------|------------------------------------------------|-------------------------------------------|
| `/import`      | `POST`      | Patient record as SDA JSON in the HTTP body.   | Task ID for checking with `/status/<id>`. |
| `/status/<id>` | `GET`       | Task ID in the URL.                            | `1` if task complete, otherwise `0`.      |

## Worker

Run the worker with:

```
RADAR_SETTINGS=$(pwd)/settings.py celery -A radar_ukrdc_importer.worker worker
```

The number of worker processes/threads can be controlled with the `--concurrency` option. By default this is the number of CPUs on the machine.

The log level can be controlled using the `--loglevel` option, for example `INFO` level is set using `--loglevel=INFO`.

## Sequence Numbers

A sequence number is generated when the patient record is received by the API.
Currently the sequence number is the number of seconds since `1970-01-01` (UTC).
Ideally we'd use the time the patient record was generated (patient records might not be received in the order they were generated by the UKRDC).
In practice this should be quite unlikely and will eventually correct itself.

The lastest sequence number imported for each patient is stored in the `patient_locks.sequence_number` column.
When a patient record is imported this value is checked so an older patient record (older sequence number) doesn't overwrite a newer one.
This is possible if some workers are faster than others or a task is retryed.

Two different patients may have the same sequence number if their patient records were received at the same time (second precision).

If two patient records for a patient are received at the same time (second precision) then they will have the same sequence number.
Both files will be processed but it is undefined in which order.
After both files are processed the system will reflect either the first or second file (i.e. not a mix of the two).

## Locking

Before importing a patient record the worker locks the patient.
This is so the database always reflects a single patient record and not a mix of several patient records received at similar times.

The `patient_locks` table has a row for each patient.
On the first import for a patient a row in the `patient_locks` table is created.
The worker locks the relevant row with `SELECT * FROM patient_locks WHERE patient_id = ? FOR UPDATE`.
If another worker has the lock the worker will block until it is released.

Once the worker has the lock, it imports the patient record and commits the transaction which releases the lock.

## Logs

When the log level is set to `INFO` the worker will output details of the records being created, updated and deleted.
Regardless of the log level changes are logged to the `logs` table.
