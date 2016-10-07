#!/bin/sh

set -e

cd "$(dirname "$0")"

git add radar/__init__.py
git commit -m "Bump version"

version=$(python setup.py --version)
git tag -a "v$version" -m "v$version"

git push --tags
