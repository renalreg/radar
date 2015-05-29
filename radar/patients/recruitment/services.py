from sqlalchemy import and_, or_

from radar.models.patients import Patient
from radar.patients.search import filter_by_date_of_birth, filter_by_first_name, filter_by_last_name, filter_by_nhs_no, \
    filter_by_chi_no


def find_existing_radar_patients(date_of_birth, first_name, last_name, nhs_no, chi_no):
    query = Patient.query

    or_filters = []

    if first_name and last_name:
        or_filters.append(and_(
            filter_by_date_of_birth(date_of_birth),
            filter_by_first_name(first_name),
            filter_by_last_name(last_name),
        ))

    if nhs_no:
        or_filters.append(and_(
            filter_by_date_of_birth(date_of_birth),
            filter_by_nhs_no(nhs_no),
        ))

    if chi_no:
        or_filters.append(and_(
            filter_by_date_of_birth(date_of_birth),
            filter_by_chi_no(chi_no),
        ))

    query = query.filter(or_(*or_filters))
    query = query.order_by(Patient.id)

    return query.all()


# TODO
def find_existing_rdc_patients(date_of_birth, first_name, last_name, nhs_no, chi_no):
    return []