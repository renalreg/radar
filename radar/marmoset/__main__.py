import json

from radar.marmoset.registry import Registry
from radar.marmoset.schema import Schema

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('schema')
    parser.add_argument('data')
    args = parser.parse_args()

    schema = json.load(open(args.schema, 'r'))
    raw_data = json.load(open(args.data, 'r'))

    registry = Registry()
    schema = Schema(registry, schema)
    data = schema.validate(raw_data)

    print data
