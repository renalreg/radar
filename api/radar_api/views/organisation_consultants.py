from radar_api.serializers.organisation_consultants import OrganisationConsultantSerializer
from radar.models import OrganisationConsultant
from radar.views.core import RetrieveUpdateDestroyModelView, ListCreateModelView


class OrganisationConsultantListView(ListCreateModelView):
    serializer_class = OrganisationConsultantSerializer
    model_class = OrganisationConsultant


class OrganisationConsultantDetailView(RetrieveUpdateDestroyModelView):
    serializer_class = OrganisationConsultantSerializer
    model_class = OrganisationConsultant
