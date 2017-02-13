from datetime import datetime

from sqlalchemy import Column, DateTime, DDL, event, Index, Integer, String, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

from radar.database import db


class Log(db.Model):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, server_default=text('now()'))
    type = Column(String, nullable=False)

    user_id = Column(Integer)
    user = relationship('User', primaryjoin='User.id == Log.user_id', foreign_keys=[user_id])

    data = Column(postgresql.JSONB)

Index('logs_date_idx', Log.date)
Index('logs_type_idx', Log.type)
Index('logs_user_idx', Log.user_id)

Index('logs_user_date_idx', Log.user_id, Log.date)
Index('logs_user_type_idx', Log.user_id, Log.type)

Index('logs_patient1_idx', Log.data['patient_id'].astext.cast(Integer), postgresql_where=Log.type == 'VIEW_PATIENT')
Index('logs_patient2_idx',
      Log.data[('new_data', 'patient_id')].astext.cast(Integer),
      postgresql_where=Log.type == 'INSERT')
Index('logs_patient3_idx',
      Log.data[('original_data', 'patient_id')].astext.cast(Integer),
      postgresql_where=Log.type == 'UPDATE')
Index('logs_patient4_idx',
      Log.data[('new_data', 'patient_id')].astext.cast(Integer),
      postgresql_where=Log.type == 'UPDATE')
Index('logs_patient5_idx',
      Log.data[('original_data', 'patient_id')].astext.cast(Integer),
      postgresql_where=Log.type == 'DELETE')

Index('logs_table_name_idx',
      Log.data['table_name'].astext,
      postgresql_where=Log.type.in_(['INSERT', 'UPDATE', 'DELETE']))


def log_changes(cls):
    event.listen(cls.__table__, 'after_create', DDL("""
        CREATE TRIGGER {0}_log_changes
        AFTER INSERT OR UPDATE OR DELETE ON {0}
        FOR EACH ROW EXECUTE PROCEDURE log_changes()
    """.format(cls.__tablename__)))

    return cls


# Trigger to log changes (INSERTs, UPDATEs, DELETEs)
event.listen(db.Model.metadata, 'before_create', DDL("""
    CREATE OR REPLACE FUNCTION log_changes() RETURNS TRIGGER AS $body$
    DECLARE
        user_id INTEGER;
    BEGIN
        BEGIN
            user_id = current_setting('radar.user_id');
        EXCEPTION WHEN OTHERS THEN
            user_id = NULL;
        END;

        IF (TG_OP = 'UPDATE') THEN
            INSERT INTO logs (
                type,
                user_id,
                data
            ) VALUES (
                'UPDATE',
                user_id,
                json_build_object(
                    'table_name', TG_TABLE_NAME,
                    'original_data', row_to_json(OLD)::jsonb,
                    'new_data', row_to_json(NEW)::jsonb,
                    'query', current_query()
                )::jsonb
            );
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO logs (
                type,
                user_id,
                data
            ) VALUES (
                'DELETE',
                user_id,
                json_build_object(
                    'table_name', TG_TABLE_NAME,
                    'original_data', row_to_json(OLD)::jsonb,
                    'query', current_query()
                )::jsonb
            );
            RETURN OLD;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO logs (
                type,
                user_id,
                data
            ) VALUES (
                'INSERT',
                user_id,
                json_build_object(
                    'table_name', TG_TABLE_NAME,
                    'new_data', row_to_json(NEW)::jsonb,
                    'query', current_query()
                )::jsonb
            );
            RETURN NEW;
        ELSE
            RAISE WARNING '[log_action] Unknown action: %% at %%', TG_OP, now();
            RETURN NULL;
        END IF;
    END;
    $body$
    LANGUAGE plpgsql
"""))


event.listen(db.Model.metadata, 'after_drop', DDL("""
    DROP FUNCTION IF EXISTS log_changes()
"""))
