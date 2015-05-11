from radar.disease_groups.models import DiseaseGroup
from radar.units.models import Unit


def get_managed_units(user):
    # TODO
    return Unit.query.order_by(Unit.name).all()


def get_managed_disease_groups(user):
    # TODO
    return DiseaseGroup.query.order_by(DiseaseGroup.name).all()