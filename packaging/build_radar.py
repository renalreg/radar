from utils import info


def install_radar(v, src_path):
    info('Installing radar ...')
    v.run(['setup.py', 'install'], cwd=src_path)
