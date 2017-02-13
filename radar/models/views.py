from sqlalchemy import Column, event, MetaData, Table
from sqlalchemy.ext import compiler
from sqlalchemy.schema import DDLElement

from radar.database import db


class CreateView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable


class DropView(DDLElement):
    def __init__(self, name):
        self.name = name


@compiler.compiles(CreateView)
def compile_create_view(element, compiler, **kwargs):
    return 'CREATE OR REPLACE VIEW {name} AS {query}'.format(
        name=element.name,
        query=compiler.sql_compiler.process(element.selectable, literal_binds=True)
    )


@compiler.compiles(DropView)
def compile_drop_view(element, compiler, **kwargs):
    return 'DROP VIEW IF EXISTS {name}'.format(name=element.name)


def create_view(name, selectable, *args):
    # Add the table to a new MetaData object so CREATE TABLE isn't run
    tmp_metadata = MetaData()
    table_args = [Column(c.name, c.type) for c in selectable.c]
    table_args.extend(args)
    t = Table(name, tmp_metadata, *table_args)

    metadata = db.Model.metadata
    event.listen(metadata, 'after_create', CreateView(name, selectable))
    event.listen(metadata, 'before_drop', DropView(name))

    return t
