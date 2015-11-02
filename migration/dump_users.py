#!/usr/bin/env python

import click

from dump_tools import rows_to_csv, get_db


@click.command()
@click.argument('output')
@click.option('--host', default='localhost')
@click.option('--port', default=3306)
@click.option('--username', default='dbaccess')
@click.option('--password', required=True)
@click.option('--database', default='patientview')
def main(output, host, port, username, password, database):
    db = get_db('mysql', host, port, username, password, database)
    users = get_users(db)
    output_file = open(output, 'wb')
    rows_to_csv(users, output_file)


def get_users(db):
    return db.execute("""
        select
            user.id as 'id',
            user.username as 'username',
            user.email as 'email',
            rdr_user_mapping.role as 'radar_role',
            usermapping.unitcode as 'unit',
            user.created as 'date_registered_pv',
            tbl_users.udatejoin as 'date_registered_radar',
            user.lastlogon as 'last_login',
            tbl_users.utitle as 'title',
            tbl_users.uforename as 'first_name',
            tbl_users.usurname as 'last_name',
            tbl_users.urole as 'job_title',
            tbl_users.ugmc as 'gmc',
            user.isclinician as 'is_clinician',
            tbl_users.uphone as 'phone',
            case when x.patients_recruited is null then 0 else x.patients_recruited end as 'patients_recruited'
        from user
        inner join rdr_user_mapping on user.id = rdr_user_mapping.userid
        left join usermapping on usermapping.username = user.username
        left join tbl_users on rdr_user_mapping.radaruserid = tbl_users.uid
        left join (
            select
                radarconsentconfirmedbyuserid as id,
                count(*) as patients_recruited
            from patient
            group by radarconsentconfirmedbyuserid
        ) as x on x.id = user.id
        where
            rdr_user_mapping.role != 'ROLE_PATIENT' and
            usermapping.unitcode != 'PATIENT'
        order by lower(user.username)
    """)


if __name__ == '__main__':
    main()
