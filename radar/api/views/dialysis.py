from collections import defaultdict

from radar.api.serializers.dialysis import DialysisSerializer, DialysisTypeSerializer
from radar.lib.foo import PatientMixin, Validation, Field, required, FacilityMixin, optional
from radar.lib.serializers import ValidationError
from radar.lib.views import FacilityDataMixin, PatientDataList, PatientDataDetail, ListView
from radar.models import Dialysis, DialysisType


class DialysisValidation(PatientMixin, FacilityMixin, Validation):
    from_date = Field(chain=[required])
    to_date = Field(chain=[optional])
    dialysis_type = Field(chain=[required])

    def validate(self, ctx, obj):
        super(DialysisValidation, self).validate(ctx, obj)

        errors = defaultdict(list)

        if obj.to_date and obj.to_date < obj.from_date:
            errors['to_date'].append('Must be on or after from date.')

        if errors:
            raise ValidationError(errors)

        return obj


class DialysisList(FacilityDataMixin, PatientDataList):
    serializer_class = DialysisSerializer
    validator_class = DialysisValidation
    model_class = Dialysis


class DialysisDetail(FacilityDataMixin, PatientDataDetail):
    serializer_class = DialysisSerializer
    validator_class = DialysisValidation
    model_class = Dialysis


class DialysisTypeList(ListView):
    serializer_class = DialysisTypeSerializer
    model_class = DialysisType
