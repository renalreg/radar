#!/usr/bin/env python

from ansible.module_utils.basic import *
import os.path
import re

CONFIG_REGEX = re.compile('^\s*([^=]+)\s*=\s*(.*)\s*$')


def get_value(module, key):
    cmd = ['npm', 'config', '--global', 'get', 'globalconfig']
    config_filename = module.run_command(cmd)[1].strip()

    try:
        config_f = open(config_filename, 'rb')
    except IOError:
        return None

    for line in config_f:
        m = CONFIG_REGEX.match(line)

        if m and m.group(1) == key:
            return m.group(2)

    return None


def set_value(module, key, value):
    if value is None:
        cmd = ['npm', 'config', '--global', 'delete', key]
    else:
        cmd = ['npm', 'config', '--global', 'set', key, value]

    module.run_command(cmd)


def main():
    module = AnsibleModule(
        argument_spec={
            'key': {'required': True, 'type': 'str'},
            'value': {'type': 'str'},
        },
        supports_check_mode=True
    )

    key = module.params['key']
    value = module.params['value']

    old_value = get_value(module, key)

    changed = old_value != value

    if changed and not module.check_mode:
        set_value(module, key, value)

    return module.exit_json(
        changed=changed,
        key=key,
        value=value,
        old_value=old_value,
    )


if __name__ == '__main__':
    main()
