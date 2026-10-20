import json

from radar.marmoset.registry import Registry
from radar.marmoset.schema import Schema

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("schema")
    parser.add_argument("data")
    args = parser.parse_args()

    with open(args.schema) as f:
        schema = json.load(f)

    with open(args.data) as f:
        raw_data = json.load(f)

    registry = Registry()
    schema = Schema(registry, schema)
    data = schema.validate(raw_data)

    print(data)
