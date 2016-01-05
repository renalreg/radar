from radar_migration import tables


COHORT_MAP = {
    'SRNS': 'INS',
}


def create_cohort(conn, data):
    result = conn.execute(
        tables.cohorts.insert(),
        code=data['code'],
        name=data['name'],
        short_name=data['short_name'],
    )

    cohort_id = result.inserted_primary_key[0]

    for i, name in enumerate(data['features']):
        # Leave gaps between features
        weight = i * 100

        conn.execute(
            tables.cohort_features.insert(),
            cohort_id=cohort_id,
            name=name,
            weight=weight,
        )


def convert_cohort_code(old_value):
    return COHORT_MAP.get(old_value, old_value)
