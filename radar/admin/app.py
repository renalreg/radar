from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from radar.app import Radar
from radar.database import db
from radar.models.diagnoses import Diagnosis
from radar.models.groups import Group
from radar.models.medications import Drug, DrugGroup
from radar.models.results import Observation
from radar.models.consultants import Consultant, Specialty


class ConsultantView(ModelView):
    pass


class DiagnosisView(ModelView):
    column_default_sort = 'name'
    column_searchable_list = ['name', 'edta']


class DrugView(ModelView):
    pass


class DrugGroupView(ModelView):
    pass


class GroupView(ModelView):
    pass


class ObservationView(ModelView):
    pass


class SpecialtyView(ModelView):
    pass


def create_app():
    app = Radar()
    admin = Admin(app, template_mode='bootstrap3', url='')
    admin.add_view(ConsultantView(Consultant, db.session))
    admin.add_view(DiagnosisView(Diagnosis, db.session))
    admin.add_view(DrugView(Drug, db.session))
    admin.add_view(DrugGroupView(DrugGroup, db.session))
    admin.add_view(GroupView(Group, db.session))
    admin.add_view(ObservationView(Observation, db.session))
    admin.add_view(SpecialtyView(Specialty, db.session))
    return app
