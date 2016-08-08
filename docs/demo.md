# Demo

The instructions show how to setup a demo server with data from another
server.

Note: you'll probably need to specify the `--connection-string` argument to
`fixtures.py`.

1. Export groups, types of observation etc. from another server (e.g. production):

    ```bash
    sudo -u postgres pg_dump radar \
      --data-only \
      --disable-triggers \
      --table consultants \
      --table diagnoses \
      --table drug_groups \
      --table drugs \
      --table group_consultants \
      --table group_diagnoses \
      --table group_observations \
      --table groups \
      --table observations \
      --table posts \
      --table settings \
      --table specialties \
      > radar.sql
    ```

1. Create the RaDaR schema:

    Drop tables:

    ```bash
    python fixtures.py drop
    ```

    Create tables:
    ```bash
    python fixtures.py create
    ```

1. Import the data we exported earlier:

    ```bash
    cat radar.sql | sudo -u postgres psql radar
    ```

    Note: we need to import the data as a super-user so triggers can be
    disabled while the data is imported (for foreign keys).

1. Create users:

   ```bash
   python fixtures.py users --password password123
   ```

1. Update user IDs:

   ```sql
   select id from users where username = 'admin' \gset
   update consultants set created_user_id = :id, modified_user_id = :id;
   update group_consultants set created_user_id = :id, modified_user_id = :id;
   update posts set created_user_id = :id, modified_user_id = :id;
   ```

1. Create patients:

   ```bash
   python fixtures.py patients --patients 450 --no-data
   python fixtures.py patients --patients 50 --data
   ```
