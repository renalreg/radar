#!/bin/bash

set -e

cd "$(dirname "$0")"

echo "Building package with Poetry..."

poetry install --no-interaction --no-ansi
poetry build
