from radar.api.serializers.forms import FormSerializer, EntrySerializer
from radar.api.views.generics import ListCreateModelView, RetrieveUpdateDestroyModelView
from radar.models.forms import Entry, Form


class FormListView(ListCreateModelView):
    serializer_class = FormSerializer
    model_class = Form


class FormDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = FormSerializer
    model_class = Form


class EntryListView(ListCreateModelView):
    serializer_class = EntrySerializer
    model_class = Entry


class EntryDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = EntrySerializer
    model_class = Entry


def register_views(app):
    app.add_url_rule('/forms', view_func=FormListView.as_view('form_list'))
    app.add_url_rule('/forms/<id>', view_func=FormDetailView.as_view('form_detail'))
    app.add_url_rule('/entries', view_func=EntryListView.as_view('entry_list'))
    app.add_url_rule('/entries/<id>', view_func=EntryDetailView.as_view('entry_detail'))