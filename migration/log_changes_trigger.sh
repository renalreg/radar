#!/bin/sh

set -e

table_name="$1"

echo "CREATE TRIGGER ${table_name}_log_changes
AFTER INSERT OR UPDATE OR DELETE ON ${table_name}
FOR EACH ROW EXECUTE PROCEDURE log_changes();"
