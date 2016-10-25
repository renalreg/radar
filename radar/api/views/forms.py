from cornflake import serializers, fields
from cornflake.validators import in_
from sqlalchemy import func, or_

from radar.api.serializers.common import QueryPatientField, GroupField
from radar.api.serializers.forms import (
    FormSerializer,
    EntrySerializer,
    FormCountSerializer
)
from radar.api.views.common import (
    PatientObjectDetailView,
    PatientObjectListView
)
from radar.api.views.generics import (
    ListView,
    ListModelView,
    RetrieveModelView,
    parse_args
)
from radar.database import db
from radar.models.forms import Entry, Form, GroupForm, GroupQuestionnaire


class FormListRequestSerializer(serializers.Serializer):
    group = GroupField(required=False)
    type = fields.StringField(required=False, validators=[in_(['form', 'questionnaire'])])
    slug = fields.StringField(required=False)


class FormCountListRequestSerializer(serializers.Serializer):
    group = GroupField(required=False)
    patient = QueryPatientField(required=False)
    type = fields.StringField(required=False, validators=[in_(['form', 'questionnaire'])])


class EntryRequestSerializer(serializers.Serializer):
    form = fields.IntegerField(required=False)


def filter_by_group_form(group):
    return GroupForm.query\
        .filter(GroupForm.form_id == Form.id)\
        .filter(GroupForm.group_id == group.id)\
        .exists()


def order_by_group_form_weight(group):
    return db.session.query(GroupForm.weight)\
        .filter(GroupForm.form_id == Form.id)\
        .filter(GroupForm.group_id == group.id)


def query_by_group_form(query, group):
    query = query.filter(filter_by_group_form(group))
    query = query.order_by(order_by_group_form_weight(group), Form.id)
    return query


def filter_by_group_questionnaire(group):
    return GroupQuestionnaire.query\
        .filter(GroupQuestionnaire.form_id == Form.id)\
        .filter(GroupQuestionnaire.group_id == group.id)\
        .exists()


def order_by_group_questionnaire_weight(group):
    return db.session.query(GroupQuestionnaire.weight)\
        .filter(GroupQuestionnaire.form_id == Form.id)\
        .filter(GroupQuestionnaire.group_id == group.id)


def query_by_group_questionnaire(query, group):
    query = query.filter(filter_by_group_questionnaire(group))
    query = query.order_by(order_by_group_questionnaire_weight(group), Form.id)
    return query


def query_by_group(query, group, type=None):
    if type == 'form':
        query = query_by_group_form(query, group)
    elif type == 'questionnaire':
        query = query_by_group_questionnaire(query, group)
    else:
        # Forms and questionnaires for this group
        query = query.filter(or_(
            filter_by_group_form(group),
            filter_by_group_questionnaire(group),
        ))
        query = query.order_by(Form.id)

    return query


def query_by_type(query, type):
    if type == 'form':
        # Just forms
        f = GroupForm.query.filter(GroupForm.form_id == Form.id).exists()
    else:
        # Just questionnaires
        f = GroupQuestionnaire.query.filter(GroupQuestionnaire.form_id == Form.id).exists()

    return query.filter(f)


class FormListView(ListModelView):
    serializer_class = FormSerializer
    model_class = Form

    def filter_query(self, query):
        query = super(FormListView, self).filter_query(query)

        args = parse_args(FormListRequestSerializer)

        group = args['group']
        type = args['type']
        slug = args['slug']

        if slug is not None:
            # Filter by form slug
            query = query.filter(Form.slug == slug)
        elif group is not None:
            # Filter by forms for group
            query = query_by_group(query, group, type)
        elif type is not None:
            # Filter by form type
            query = query_by_type(query, type)
        else:
            query = query.order_by(Form.id)

        return query


class FormCountListView(ListView):
    serializer_class = FormCountSerializer

    def get_object_list(self):
        args = parse_args(FormCountListRequestSerializer)

        group = args['group']
        patient = args['patient']
        type = args['type']

        q1 = db.session.query(
            Entry.form_id.label('form_id'),
            func.count().label('entry_count')
        )
        q1 = q1.select_from(Entry)

        if patient is not None:
            # Only include entries that belong to this patient
            q1 = q1.filter(Entry.patient == patient)

        q1 = q1.group_by(Entry.form_id)
        q1 = q1.subquery()

        # Get forms with their entry counts (set entry count to zero if their
        # form hasn't been filled in yet).
        q2 = db.session.query(Form, func.coalesce(q1.c.entry_count, 0))
        q2 = q2.outerjoin(q1, Form.id == q1.c.form_id)

        if group is not None:
            # Filter by forms for group
            q2 = query_by_group(q2, group, type)
        elif type is not None:
            # Filter by form type
            q2 = query_by_type(q2, type)
        else:
            q2 = q2.order_by(Form.id)

        results = [dict(form=form, count=count) for form, count in q2]

        return results


class FormDetailView(RetrieveModelView):
    serializer_class = FormSerializer
    model_class = Form


class EntryListView(PatientObjectListView):
    serializer_class = EntrySerializer
    model_class = Entry

    def filter_query(self, query):
        query = super(EntryListView, self).filter_query(query)

        args = parse_args(EntryRequestSerializer)

        form_id = args['form']

        # Filter entries by form
        if form_id is not None:
            query = query.filter(Entry.form_id == form_id)

        return query


class EntryDetailView(PatientObjectDetailView):
    serializer_class = EntrySerializer
    model_class = Entry


def register_views(app):
    app.add_url_rule('/forms', view_func=FormListView.as_view('form_list'))
    app.add_url_rule('/forms/<id>', view_func=FormDetailView.as_view('form_detail'))
    app.add_url_rule('/entries', view_func=EntryListView.as_view('entry_list'))
    app.add_url_rule('/entries/<id>', view_func=EntryDetailView.as_view('entry_detail'))
    app.add_url_rule('/form-counts', view_func=FormCountListView.as_view('form_count_list'))
