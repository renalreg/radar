from cornflake.sqlalchemy_orm import ModelSerializer
from cornflake import fields

from radar.models.groups import Group, GROUP_TYPE


class GroupSerializer(ModelSerializer):
    type = fields.EnumField(GROUP_TYPE)
    pages = fields.ListField(child=fields.StringField())

    class Meta(object):
        model_class = Group
