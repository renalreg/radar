import tempfile
import os
import zipfile
import tarfile
import shutil

from radar_packaging import run_command

INSTALLER = '''\
#!/bin/bash

HERE="$(cd "$(dirname "$0")"; pwd)"
DATA_DIR="$HERE/data"

python "$DATA_DIR/virtualenv.py" "$1"
VIRTUAL_ENV="$(cd "$1"; pwd)"

INSTALL_ARGS=$(cd "$DATA_DIR"; ls -1 *.whl | awk -F - '{ gsub("_", "-", $1); print $1 }' | uniq)

"$VIRTUAL_ENV/bin/pip" install --pre --no-index --find-links "$DATA_DIR" $INSTALL_ARGS
'''


class WheelBuilder(object):
    def __init__(self):
        self.tmp_dirs = []

        self.build_dir = self.make_tmp_dir()
        self.data_dir = os.path.join(self.build_dir, 'data')
        os.makedirs(self.data_dir)

    def make_tmp_dir(self):
        tmp_dir = tempfile.mkdtemp()
        self.tmp_dirs.append(tmp_dir)
        return tmp_dir

    def cleanup(self):
        for tmp_dir in self.tmp_dirs:
            try:
                shutil.rmtree(tmp_dir)
            except (OSError, IOError):
                pass

    def extract_virtualenv(self):
        tmp_dir = self.make_tmp_dir()
        run_command(['pip', 'install', '--download', tmp_dir, 'virtualenv'])
        archive = os.path.join(tmp_dir, os.listdir(tmp_dir)[0])

        if archive.endswith(('.whl', '.zip')):
            f = zipfile.ZipFile(archive)
        else:
            f = tarfile.open(archive)

        extracted = os.path.join(tmp_dir, 'extracted')

        f.extractall(extracted)
        f.close()

        contents = os.listdir(extracted)

        # Check if archive extracted to a folder
        if len(contents) == 1:
            return contents[0]
        else:
            return extracted

    def add_virtualenv(self):
        """Add the virtualenv script and wheels."""

        venv_src = self.extract_virtualenv()

        venv_support = os.path.join(venv_src, 'virtualenv_support')

        # Add the wheels
        for filename in os.listdir(venv_support):
            if filename.endswith('.whl'):
                shutil.copy(os.path.join(venv_support, filename), self.data_dir)

        # Add virtualenv.py
        virtualenv_py = os.path.join(venv_src, 'virtualenv.py')

        shutil.copy(virtualenv_py, self.data_dir)

    def add_installer(self):
        """Add the install script."""

        filename = os.path.join(self.build_dir, 'install.sh')

        with open(filename, 'w') as f:
            f.write(INSTALLER.encode('utf-8'))

        # Make the script executable
        os.chmod(filename, 0100755)

    def add(self, args, env=None, cwd=None):
        """Build and add  wheels using pip wheel."""

        cmd = ['pip', 'wheel', '--wheel-dir', self.data_dir]
        cmd.extend(args)
        run_command(cmd, env=env, cwd=cwd)

    def create_archive(self, filename):
        """Create an archive from the build directory."""

        base_filename = filename.rstrip('.tar.gz')

        def reset(tarinfo):
            tarinfo.uid = tarinfo.gid = 0
            tarinfo.uname = tarinfo.gname = 'root'
            return tarinfo

        # Compress with gzip
        f = tarfile.open(filename, 'w:gz')
        f.add(self.build_dir, base_filename, filter=reset)
        f.close()

    def build(self, filename):
        """Build an archive."""

        self.add_virtualenv()
        self.add_installer()
        self.create_archive(filename)
