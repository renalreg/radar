import logging


def install_radar(v, src_directory='.'):
    logging.info('Installing radar ...')
    v.run(['setup.py', 'install'], cwd=src_directory)
