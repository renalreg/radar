from datetime import datetime

from sqlalchemy import event, DDL, Column, Integer, DateTime, String, text
from sqlalchemy.dialects import postgresql

from radar.database import db


class Log(db.Model):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, server_default=text('now()'))
    type = Column(String, nullable=False)
    user_id = Column(Integer)

    table_name = Column(String)
    original_data = Column(postgresql.JSONB)
    new_data = Column(postgresql.JSONB)
    statement = Column(String)

    data = Column(postgresql.JSONB)


def log_changes(cls):
    event.listen(cls.__table__, 'after_create', DDL("""
        CREATE TRIGGER {0}_log_changes
        AFTER INSERT OR UPDATE OR DELETE ON {0}
        FOR EACH ROW EXECUTE PROCEDURE log_changes()
    """.format(cls.__tablename__)))

    return cls


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
                table_name,
                original_data,
                new_data,
                statement
            ) VALUES (
                'UPDATE',
                user_id,
                TG_TABLE_NAME,
                row_to_json(OLD)::jsonb,
                row_to_json(NEW)::jsonb,
                current_query()
            );
            RETURN NEW;
        ELSIF (TG_OP = 'DELETE') THEN
            INSERT INTO logs (
                type,
                user_id,
                table_name,
                original_data,
                statement
            ) VALUES (
                'DELETE',
                user_id,
                TG_TABLE_NAME,
                row_to_json(OLD)::jsonb,
                current_query()
            );
            RETURN OLD;
        ELSIF (TG_OP = 'INSERT') THEN
            INSERT INTO logs (
                type,
                user_id,
                table_name,
                new_data,
                statement
            ) VALUES (
                'INSERT',
                user_id,
                TG_TABLE_NAME,
                row_to_json(NEW)::jsonb,
                current_query()
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
