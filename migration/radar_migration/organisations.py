from radar_migration import tables


def create_organisation(conn, data):
    result = conn.execute(
        tables.organisations.insert(),
        code=data['code'],
        type=data['type'],
        name=data['name'],
        recruitment=data['recruitment'],
    )

    organisation_id = result.inserted_primary_key[0]

    return organisation_id
