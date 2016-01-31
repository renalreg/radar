#!/bin/sh

set -e

table_names="
foo
bar
baz
"

for table_name in $table_names; do
  ./log_changes_trigger.sh $table_name
done
