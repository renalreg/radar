#!/usr/bin/env python

from ansible.module_utils.basic import *
import re

CONFIG_REGEX = re.compile('^\s*([^=]+)\s*=\s*(.*)\s*$')


def get_value(module, key, global_flag=False):
    if global_flag:
        cmd = ['npm', 'config', 'get', 'globalconfig']
    else:
        cmd = ['npm', 'config', 'get', 'userconfig']

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


def set_value(module, key, value, global_flag=False):
    cmd = ['npm', 'config']

    if global_flag:
        cmd.append('--global')

    if value:
        cmd.extend(['set', key, value])
    else:
        cmd.extend(['delete', key])

    module.run_command(cmd)


def main():
    module = AnsibleModule(
        argument_spec={
            'key': {'required': True, 'type': 'str'},
            'value': {'type': 'str'},
            'global': dict(default='no', type='bool'),
        },
        supports_check_mode=True
    )

    key = module.params['key']
    value = module.params['value']
    global_flag = module.params['global']

    old_value = get_value(module, key, global_flag=global_flag)

    changed = old_value != value

    if changed and not module.check_mode:
        set_value(module, key, value, global_flag=global_flag)

    return module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
