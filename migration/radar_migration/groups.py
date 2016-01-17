from radar_migration import tables


COHORT_MAP = {
    'SRNS': 'INS',
    'HYPERRDG': 'HYPOXAL',
    'MEMRDG': 'MEMNEPHRO',
    'VASRDG': 'VAS',
}


def create_group(conn, data):
    conn.execute(
        tables.groups.insert(),
        code=data['code'],
        type=data['type'],
        name=data['name'],
        short_name=data.get('short_name', data['name']),
        recruitment=data.get('recruitment', False),
        pages=data.get('pages'),
    )


def convert_cohort_code(old_value):
    return COHORT_MAP.get(old_value, old_value)
