from sqlalchemy import create_engine
import click


# TODO
def migrate_ins(old_conn, new_conn):
    pass


@click.command()
@click.argument('src')
@click.argument('dest')
def cli(src, dest):
    src_engine = create_engine(src)
    dest_engine = create_engine(dest)

    src_conn = src_engine.connect()
    dest_conn = dest_engine.connect()

    with dest_conn.begin():
        migrate_ins(src_conn, dest_conn)


if __name__ == '__main__':
    cli()
