import logging

from radar.models.medications import Medication, MEDICATION_DOSE_UNITS, MEDICATION_ROUTES


logger = logging.getLogger(__name__)


def export_medications(sda_container, patient):
    q = Medication.query
    q = q.filter(Medication.patient == patient)
    q = q.filter(Medication.source_type == 'RADAR')
    medications = q.all()

    if not medications:
        return

    sda_medications = sda_container.setdefault('medications', list())

    for medication in medications:
        sda_medication = dict()
        sda_medication['external_id'] = str(medication.id)
        sda_medication['from_time'] = medication.from_date

        if medication.to_date:
            sda_medication['to_time'] = medication.to_date

        if medication.drug_text:
            sda_medication['drug_product'] = {
                'product_name': medication.drug_text
            }
        elif medication.drug:
            sda_medication['drug_product'] = {
                'product_name': medication.drug.name
            }
        else:
            continue

        if medication.dose_text:
            sda_medication['dose_u_o_m'] = {
                'code': medication.dose_text,
                'description': medication.dose_text
            }
        else:
            if medication.dose_quantity is not None:
                sda_medication['dose_quantity'] = medication.dose_quantity

            if medication.dose_unit:
                code = medication.dose_unit
                description = MEDICATION_DOSE_UNITS.get(code)

                if description:
                    sda_medication['dose_u_o_m'] = {
                        'sda_coding_standard': 'RADAR',
                        'code': code,
                        'description': description,
                    }
                else:
                    logger.error('Unknown dose unit code={}'.format(code))

            if medication.route:
                code = medication.route
                description = MEDICATION_ROUTES.get(code)

                if description:
                    sda_medication['route'] = {
                        'sda_coding_standard': 'RADAR',
                        'code': code,
                        'description': description,
                    }
                else:
                    logger.error('Unknown route code={}'.format(code))

            if medication.frequency:
                sda_medication['frequency'] = {
                    'code': medication.frequency,
                    'description': medication.frequency,
                }

        sda_medication['entering_organization'] = {
            'code': medication.source_group.code,
            'description': medication.source_group.name
        }

        sda_medications.append(sda_medication)
