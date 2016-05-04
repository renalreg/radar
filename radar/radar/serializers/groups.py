from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields

from radar.serializers.common import MetaMixin
from radar.models.groups import Group, GROUP_TYPE


class GroupSerializer(MetaMixin, ModelSerializer):
    type = fields.EnumField(GROUP_TYPE)
    pages = fields.ListField(fields.StringField())

    class Meta(object):
        model_class = Group
