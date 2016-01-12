from radar_api.serializers.groups import GroupReferenceField
from radar_api.serializers.meta import MetaSerializerMixin
from radar.serializers.fields import ListField, IntegerField
from radar.serializers.models import ModelSerializer
from radar.serializers.core import Serializer
from radar.models.consultants import Consultant
from radar.models.groups import GroupConsultant
from radar.database import db


class GroupConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    group = GroupReferenceField()

    class Meta(object):
        model_class = GroupConsultant
        exclude = ['id', 'consultant_id', 'group_id']


class ConsultantSerializer(MetaSerializerMixin, ModelSerializer):
    groups = ListField(field=GroupConsultantSerializer(), source='group_consultants')

    class Meta(object):
        model_class = Consultant

    def create_group_consultant(self, deserialized_data):
        group_consultant = GroupConsultant()
        self.groups.field.update(group_consultant, deserialized_data)
        return group_consultant

    def update(self, obj, deserialized_data):
        print deserialized_data

        for attr, value in deserialized_data.items():
            if attr == 'group_consultants':
                obj.group_consultants = []

                # Unique constraint fails unless we flush the deletes before the inserts
                db.session.flush()

                for x in value:
                    group_consultant = self.create_group_consultant(x)
                    obj.group_consultants.append(group_consultant)
            elif hasattr(obj, attr):
                setattr(obj, attr, value)

        return obj


class ConsultantRequestSerializer(Serializer):
    patient = IntegerField()
