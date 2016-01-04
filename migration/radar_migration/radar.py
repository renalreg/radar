from radar_migration import tables


def create_radar(conn):
    result = conn.execute(
        tables.organisations.insert(),
        code='RADAR',
        type='RADAR',
        name='RaDaR',
        recruitment=True,
    )

    organisation_id = result.inserted_primary_key[0]

    conn.execute(
        tables.data_sources.insert(),
        organisation_id=organisation_id,
        type='RADAR',
    )
