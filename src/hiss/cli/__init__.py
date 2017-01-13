import os
import sys
import warnings

import click

from .config import HissConfig
from .magic import *  # noqa
from .virtualenv import load_venv

_PYTHON_VERSION = "python{0}.{1}".format(*sys.version_info[0:2])
_HISS_CONFIG = os.path.expanduser(os.path.join(os.environ.get('HOME', '~'), '.hiss'))
_BANNER = """
hiss - {python_version}

"""


def embed_ipython(c):
    for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
        warnings.filterwarnings("ignore", category=warning)

    configured_shell = c.configured_shell()
    configured_shell()


@click.command()
@click.option('--config', '-c', default=_HISS_CONFIG)
def main(config):
    """Console script for hiss"""
    # load virtual
    load_venv(_PYTHON_VERSION)
    embed_ipython(HissConfig(config, _BANNER, _PYTHON_VERSION))


if __name__ == '__main__':
    main()
