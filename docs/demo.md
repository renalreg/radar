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
      --table drugs \
      --table group_consultants \
      --table group_diagnoses \
      --table groups \
      --table observations \
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
    cat radar.sql | sudo -u postgres radar
    ```

    Note: we need to import the data as a super-user so triggers can be
    disabled while the data is imported (for foreign keys).

1. Create users:

   ```bash
   python fixtures.py users --password password123
   ```

1. Create patients:

   ```bash
   python fixtures.py patients --patients 500
   ```
