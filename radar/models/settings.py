from radar.database import db

from sqlalchemy import Column, String


class Setting(db.Model):
    __tablename__ = 'settings'

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)


def get_setting(key):
    setting = Setting.query.get(key)

    if setting:
        return setting.value
    else:
        return None
