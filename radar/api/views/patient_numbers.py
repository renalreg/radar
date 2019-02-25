from cornflake.exceptions import ValidationError

from radar.api.serializers.patient_numbers import PatientNumberSerializer
from radar.api.views.common import (
    DemographicsViewMixin,
    PatientObjectDetailView,
    PatientObjectListView,
    SystemObjectViewMixin,
)
from radar.models.groups import GROUP_CODE_CHI, GROUP_CODE_HSC, GROUP_CODE_NHS
from radar.models.patient_numbers import PatientNumber
from radar.models.source_types import SOURCE_TYPE_MANUAL


class PatientNumberListView(SystemObjectViewMixin, DemographicsViewMixin, PatientObjectListView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber


class PatientNumberDetailView(SystemObjectViewMixin, DemographicsViewMixin, PatientObjectDetailView):
    serializer_class = PatientNumberSerializer
    model_class = PatientNumber

    def delete(self, *args, **kwargs):
        """Prevent deletion of the last manually entered NHS/CHI/HSC patient number."""
        patient_number = self.get_object()
        interested = (GROUP_CODE_CHI, GROUP_CODE_HSC, GROUP_CODE_NHS)
        if patient_number.number_group.code not in interested:
            return self.destroy(*args, **kwargs)

        numbers = patient_number.patient.patient_numbers
        for number in numbers:
            if number.source_type == SOURCE_TYPE_MANUAL and patient_number != number:
                if number.number_group.code in interested:
                    return self.destroy(*args, **kwargs)

        raise ValidationError({'number': 'Can\'t delete the last NHS/CHI/HSC patient number.'})


def register_views(app):
    app.add_url_rule('/patient-numbers', view_func=PatientNumberListView.as_view('patient_number_list'))
    app.add_url_rule('/patient-numbers/<id>', view_func=PatientNumberDetailView.as_view('patient_number_detail'))
