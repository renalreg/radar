from radar_packaging import run_command


class PackageBuilder(object):
    def __init__(self, name, version, release, architecture, url):
        self.name = name
        self.version = version
        self.architecture = architecture
        self.after_install = None
        self.before_install = None
        self.after_remove = None
        self.before_remove = None
        self.after_upgrade = None
        self.before_upgrade = None
        self.url = url
        self.release = release
        self.dependencies = []
        self.paths = []
        self.config_files = []

    def add_dependency(self, package_name):
        self.dependencies.append(package_name)

    def add_path(self, src, dst):
        self.paths.append('%s=%s' % (src, dst))

    def add_config_file(self, path):
        self.config_files.append(path)

    def build(self):
        rpm_path = '%s-%s-%s.%s.rpm' % (self.name, self.version, self.release, self.architecture)

        args = [
            'fpm',
            '-s', 'dir',
            '-t', 'rpm',
            '--package', rpm_path,
            '--name', self.name,
            '--version', str(self.version),
            '--iteration', str(self.release),
            '--url', self.url,
            '--architecture', self.architecture,
            '--force',
        ]

        for package_name in self.dependencies:
            args.extend(['--depends', package_name])

        for path in self.config_files:
            args.extend(['--config-files', path])

        if self.after_install is not None:
            args.extend(['--after-install', self.after_install])

        if self.before_install is not None:
            args.extend(['--before-install', self.before_install])

        if self.after_remove is not None:
            args.extend(['--after-remove', self.after_remove])

        if self.before_remove is not None:
            args.extend(['--before-remove', self.before_remove])

        if self.after_upgrade is not None:
            args.extend(['--after-upgrade', self.after_upgrade])

        if self.before_upgrade is not None:
            args.extend(['--before-upgrade', self.before_upgrade])

        for path in self.paths:
            args.append(path)

        run_command(args, env={'PATH': '/usr/local/bin:/usr/bin:/bin'})

        return rpm_path
