from utils import info


def install_radar(v, src_directory='.'):
    info('Installing radar ...')
    v.run(['setup.py', 'install'], cwd=src_directory)
