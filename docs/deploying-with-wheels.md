# Deploying with Wheels

[Python Wheels](http://pythonwheels.com/) are useful for deployment as they can be installed without compiling or downloading any extra files.
The package and it's dependencies are built as wheels and bundled with a install script.

## Build

The process is based on [platter](http://platter.pocoo.org/).

1. The package and it's dependencies are packaged as wheels using `pip wheel --wheel-dir data ...`.
1. `pip` is used to download the `virtualenv` package from PyPi. `virtualenv.py` and the wheels in `virtualenv_support` are copied from the download to the `data` folder in the output.
1. The install script is copied to the output folder.
1. A `.tar.gz` file is created from the output folder.

The output file contains:

* `install.sh` - shell script installer.
* `data/*.whl` - the module/package and it's dependencies built as wheels.
* `data/virtualenv.py` - virtualenv script.

## Install

1. Extract the `.tar.gz`.
2. Run the `install.sh` script. This will create a virtual env and install the wheels into it.

For example:

```bash
tar xf radar-api-1.2.3-1.tar.gz
radar-api-1.2.3-1/install.sh /path/to/install/to
```
