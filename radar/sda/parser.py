from radar.sda.models import SDAMedication, SDABundle, SDAPatientAddress, SDAPatientAlias, SDAPatient, \
    SDAPatientNumber, SDALabOrder, SDALabResult

import dateutil.parser


def set_float(data, key, node):
    if node is not None:
        data[key] = parse_float(node)


def parse_float(node):
    return float(node.text)


def set_text(data, key, node):
    if node is not None:
        data[key] = parse_text(node)


def parse_text(node):
    return node.text


def set_datetime(data, key, node):
    if node is not None:
        data[key] = parse_datetime(node)


def parse_datetime(node):
    return dateutil.parser.parse(node.text)


def set_boolean(data, key, node):
    if node is not None:
        data[key] = parse_boolean(node)


def parse_boolean(node):
    text = node.text
    return text.lower() == 'true' or text == '1'


def set_code_description(data, key, node):
    if node is not None:
        data[key] = parse_code_description(node)


def parse_code_description(node):
    data = dict()
    set_text(data, 'coding_standard', node.find('./CodingStandard'))
    set_text(data, 'code', node.find('./Code'))
    set_text(data, 'description', node.find('./Description'))
    return data


def set_organization(data, key, node):
    if node is not None:
        data[key] = parse_organization(node)


def parse_container(node):
    sda_bundle = SDABundle()

    patient_node = node.find('./Patient')

    sda_patient = parse_patient(patient_node)
    sda_bundle.sda_patient = sda_patient

    for medication_node in node.findall('./Medications/Medication'):
        sda_medication = parse_medication(medication_node)
        sda_bundle.sda_medications.append(sda_medication)

    for lab_order_node in node.findall('./LabOrders/LabOrder'):
        sda_lab_order = parse_lab_order(lab_order_node)
        sda_bundle.sda_lab_orders.append(sda_lab_order)

    return sda_bundle


def parse_base(node):
    data = dict()
    set_datetime(data, 'entered_on', node.find('./EnteredOn'))
    set_datetime(data, 'updated_on', node.find('./UpdatedOn'))
    set_text(data, 'encounter_number', node.find('./EncounterNumber'))
    set_text(data, 'external_id', node.find('./ExternalId'))
    set_datetime(data, 'from_time', node.find('./FromTime'))
    set_datetime(data, 'to_time', node.find('./ToTime'))
    return data


def parse_order(node):
    data = parse_base(node)
    set_text(data, 'placer_id', node.find('./PlacerId'))
    set_text(data, 'filler_id', node.find('./FillerId'))
    set_code_description(data, 'order_item', node.find('./OrderItem'))
    set_code_description(data, 'order_category', node.find('./OrderCategory'))
    set_text(data, 'order_quantity', node.find('./OrderQuantity'))
    set_text(data, 'specimen', node.find('./Specimen'))
    set_datetime(data, 'specimen_collection_time', node.find('./Specimen'))
    set_datetime(data, 'specimen_received_time', node.find('./SpecimenReceivedTime'))
    set_datetime(data, 'reassessmentTime', node.find('./ReassessmentTime'))
    set_code_description(data, 'frequency', node.find('./Frequency'))
    set_code_description(data, 'duration', node.find('./Duration'))
    set_text(data, 'status', node.find('./Status'))
    set_code_description(data, 'priority', node.find('./Priority'))
    set_code_description(data, 'confidentiality_code', node.find('./ConfidentialityCode'))
    set_text(data, 'condition', node.find('./Condition'))
    set_text(data, 'text_instruction', node.find('./TextInstruction'))
    set_text(data, 'order_group', node.find('./OrderGroup'))
    set_text(data, 'comments', node.find('./Comments'))
    set_datetime(data, 'authorization_time', node.find('./AuthorizationTime'))
    set_text(data, 'verified_comments', node.find('./VerifiedComments'))
    set_text(data, 'group_id', node.find('./GroupId'))
    return data


def parse_medication(node):
    sda_medication = SDAMedication()

    data = parse_order(node)

    set_float(data, 'strength_volume', node.find('./StrengthVolume'))
    set_text(data, 'strength_volume_units', node.find('./StrengthVolumeUnits'))
    set_float(data, 'rate_amount', node.find('./RateAmount'))
    set_code_description(data, 'rate_units', node.find('./RateUnits'))
    set_text(data, 'rate_time_unit', node.find('./RateTimeUnit'))
    set_float(data, 'dose_quantity', node.find('./DoseQuantity'))
    set_float(data, 'max_dose_quantity', node.find('./MaxDoseQuantity'))
    set_text(data, 'number_of_refills', node.find('./NumberOfRefills'))
    set_code_description(data, 'dose_uom', node.find('./DoseUoM'))
    set_code_description(data, 'dosage_form', node.find('./DosageForm'))
    set_text(data, 'indication', node.find('./Indication'))
    set_text(data, 'pharmacy_status', node.find('./PharmacyStatus'))
    set_text(data, 'prescription_number', node.find('./PrescriptionNumber'))

    sda_medication.data = data

    return sda_medication


def parse_name(node):
    data = dict()
    set_text(data, 'name_prefix', node.find('./NamePrefix'))
    set_text(data, 'given_name', node.find('./GivenName'))
    set_text(data, 'middle_name', node.find('./MiddleName'))
    set_text(data, 'family_name', node.find('./FamilyName'))
    set_text(data, 'preferred_name', node.find('./PreferredName'))
    return data


def parse_patient_alias(node):
    sda_patient_alias = SDAPatientAlias()
    sda_patient_alias.data = parse_name(node)
    return sda_patient_alias


def parse_patient_address(node):
    sda_patient_address = SDAPatientAddress()

    data = dict()
    set_datetime(data, 'from_time', node.find('./FromTime'))
    set_datetime(data, 'to_time', node.find('./ToTime'))
    set_text(data, 'street', node.find('./Street'))
    set_code_description(data, 'city', node.find('./City'))
    set_code_description(data, 'state', node.find('./State'))
    set_code_description(data, 'zip', node.find('./Zip'))
    set_code_description(data, 'country', node.find('./Country'))
    sda_patient_address.data = data

    return sda_patient_address


def parse_patient(node):
    sda_patient = SDAPatient()
    sda_patient.data = dict()

    name_node = node.find('./Name')

    if name_node is not None:
        sda_patient.data['name'] = parse_name(name_node)

    set_code_description(sda_patient.data, 'gender', node.find('./Gender'))
    set_code_description(sda_patient.data, 'ethnic_group', node.find('./EthnicGroup'))

    set_datetime(sda_patient.data, 'birth_time', node.find('./BirthTime'))
    set_datetime(sda_patient.data, 'death_time', node.find('./DeathTime'))

    for patient_name_node in node.findall('./Aliases/Name'):
        sda_patient_alias = parse_patient_alias(patient_name_node)
        sda_patient.aliases.append(sda_patient_alias)

    for patient_number_node in node.findall('./PatientNumbers/PatientNumber'):
        sda_patient_number = parse_patient_number(patient_number_node)
        sda_patient.numbers.append(sda_patient_number)

    for patient_address_node in node.findall('./Addresses/Address'):
        sda_patient_address = parse_patient_address(patient_address_node)
        sda_patient.addresses.append(sda_patient_address)

    return sda_patient


def parse_patient_number(node):
    sda_patient_number = SDAPatientNumber()

    sda_patient_number.data = dict()
    set_text(sda_patient_number.data, 'number', node.find('./Number'))
    set_text(sda_patient_number.data, 'number_type', node.find('./NumberType'))
    set_organization(sda_patient_number.data, 'organization', node.find('./Organization'))

    return sda_patient_number


def parse_organization(node):
    data = dict()
    set_text(data, 'code', node.find('./Code'))
    set_text(data, 'description', node.find('./Description'))
    return data


def parse_result(node):
    data = dict()
    set_datetime(data, 'from_time', node.find('./FromTime'))
    set_datetime(data, 'to_time', node.find('./ToTime'))
    set_text(data, 'result_type', node.find('./ResultType'))
    set_datetime(data, 'result_time', node.find('./ResultTime'))
    set_text(data, 'result_text', node.find('./ResultText'))
    set_text(data, 'comments', node.find('./Comments'))
    set_datetime(data, 'authorization_time', node.find('./AuthorizationTime'))
    set_organization(data, 'performed_at', node.find('./PerformedAt'))
    set_text(data, 'result_interpretation', node.find('./ResultInterpretation'))
    set_text(data, 'external_id', node.find('./ExternalId'))
    return data


def parse_lab_result(node):
    sda_lab_result = SDALabResult()

    data = dict()

    set_code_description(data, 'test_item_code', node.find('./TestItemCode'))

    if 'test_item_code' in data:
        set_boolean(data['test_item_code'], 'is_numeric', node.find('./TestItemCode/IsNumeric'))

    set_text(data, 'result_value', node.find('./ResultValue'))
    set_text(data, 'result_value_units', node.find('./ResultValueUnits'))
    set_text(data, 'result_normal_range', node.find('./ResultNormalRange'))
    set_text(data, 'result_interpretation', node.find('./ResultInterpretation'))
    set_text(data, 'comments', node.find('./Comments'))
    set_organization(data, 'performed_at', node.find('./PerformedAt'))
    set_text(data, 'external_id', node.find('./ExternalId'))

    sda_lab_result.data = data

    return sda_lab_result


def parse_lab_order(node):
    sda_lab_order = SDALabOrder()

    data = parse_order(node)

    result_node = node.find('./Result')

    if result_node is not None:
        data['result'] = parse_result(result_node)

    sda_lab_order.data = data

    for lab_result_node in node.findall('./Result/ResultItems/LabResultItem'):
        sda_lab_result = parse_lab_result(lab_result_node)
        sda_lab_order.results.append(sda_lab_result)

    return sda_lab_order