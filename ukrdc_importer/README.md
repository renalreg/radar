# UKRDC Importer

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
