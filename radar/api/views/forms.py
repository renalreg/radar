from cornflake import serializers

from radar.api.serializers.common import QueryPatientField
from radar.api.serializers.forms import FormSerializer, EntrySerializer
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.api.views.generics import (
    ListModelView,
    RetrieveModelView,
    ListCreateModelView,
    RetrieveUpdateDestroyModelView,
    parse_args
)
from radar.models.forms import Entry, Form, GroupForm


class FormRequestSerializer(serializers.Serializer):
    patient = QueryPatientField(required=False)


class FormListView(ListModelView):
    serializer_class = FormSerializer
    model_class = Form

    def filter_query(self, query):
        query = super(FormListView, self).filter_query(query)

        args = parse_args(FormRequestSerializer)

        patient = args['patient']

        # Filter by forms relevant to patient
        if patient:
            group_ids = [x.id for x in patient.groups]

            q = GroupForm.query\
                .filter(GroupForm.group_id.in_(group_ids))\
                .filter(GroupForm.form_id == Form.id)\
                .exists()

            query = query.filter(q)

        return query


class FormDetailView(RetrieveModelView):
    serializer_class = FormSerializer
    model_class = Form


class EntryListView(PatientObjectListView):
    serializer_class = EntrySerializer
    model_class = Entry


# TODO filter by form
class EntryDetailView(PatientObjectDetailView):
    serializer_class = EntrySerializer
    model_class = Entry


def register_views(app):
    app.add_url_rule('/forms', view_func=FormListView.as_view('form_list'))
    app.add_url_rule('/forms/<id>', view_func=FormDetailView.as_view('form_detail'))
    app.add_url_rule('/entries', view_func=EntryListView.as_view('entry_list'))
    app.add_url_rule('/entries/<id>', view_func=EntryDetailView.as_view('entry_detail'))
