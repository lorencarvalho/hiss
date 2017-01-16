import os
import sys
import warnings as _warnings

import click
import IPython

from .config import HissConfig
from .magic import *  # noqa
from .virtualenv import load_venv

_PYTHON_VERSION = "python{0}.{1}".format(*sys.version_info[0:2])
_HISS_CONFIG = os.path.expanduser(os.path.join(os.environ.get('HOME', '~'), '.hiss'))
_BANNER = """
hiss - {python_version}

"""


@click.command()
@click.option('--config', '-c', type=click.Path(exists=False), default=_HISS_CONFIG)
@click.option('--warnings/--no-warnings', default=False)
def main(config, warnings):
    """Console script for hiss"""
    banner = _BANNER.format(python_version=_PYTHON_VERSION)

    if not warnings:
        for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
            _warnings.filterwarnings("ignore", category=warning)

    # load virtualenv & config and run ipython
    load_venv(_PYTHON_VERSION)
    hc = HissConfig(config, banner)
    IPython.start_ipython(
        argv=[],
        config=hc.config,
        quick=True,
        auto_create=False,
        )
