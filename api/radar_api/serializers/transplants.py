from radar_api.serializers.data_sources import DataSourceSerializerMixin
from radar_api.serializers.meta import MetaSerializerMixin
from radar_api.serializers.patient_mixins import PatientSerializerMixin
from radar.models.transplants import TYPES_OF_TRANSPLANT, Transplant, TransplantRejection, TransplantBiopsy
from radar.serializers.models import ModelSerializer
from radar.serializers.codes import CodedIntegerSerializer
from radar.serializers.fields import ListField


class TransplantRejectionSerializer(ModelSerializer):
    class Meta(object):
        model_class = TransplantRejection
        exclude = ['id']


class TransplantBiopsySerializer(ModelSerializer):
    class Meta(object):
        model_class = TransplantBiopsy
        exclude = ['id']


class TransplantSerializer(PatientSerializerMixin, DataSourceSerializerMixin, MetaSerializerMixin, ModelSerializer):
    type_of_transplant = CodedIntegerSerializer(TYPES_OF_TRANSPLANT)
    rejections = ListField(TransplantRejectionSerializer())
    biopsies = ListField(TransplantBiopsySerializer())

    class Meta(object):
        model_class = Transplant

    def create_rejection(self, deserialized_data):
        rejection = TransplantRejection()
        self.rejections.field.update(rejection, deserialized_data)
        return rejection

    def create_biopsy(self, deserialized_data):
        biopsy = TransplantBiopsy()
        self.biopsies.field.update(biopsy, deserialized_data)
        return biopsy

    def update(self, obj, deserialized_data):
        for attr, value in deserialized_data.items():
            if attr == 'rejections':
                obj.rejections = []

                for x in value:
                    rejection = self.create_rejection(x)
                    obj.rejections.append(rejection)
            elif attr == 'biopsies':
                obj.biopsies = []

                for x in value:
                    biopsy = self.create_biopsy(x)
                    obj.biopsies.append(biopsy)
            elif hasattr(obj, attr):
                setattr(obj, attr, value)

        return obj
