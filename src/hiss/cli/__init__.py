import os
import sys
import warnings as _warnings

from pathlib import Path

import click  # type: ignore
import IPython  # type: ignore

from .config import build_config, load_rc
from .magic import *  # noqa
from .virtualenv import load_venv

_PYTHON_VERSION = "python{0}.{1}".format(*sys.version_info[0:2])
_HISS_CONFIG = Path(os.environ.get('HOME', '~'), '.hiss').expanduser()
_BANNER = """
hiss - {python_version}

"""


@click.command()
@click.option('--config', '-c', type=click.Path(exists=False), default=_HISS_CONFIG)
@click.option('--warnings/--no-warnings', default=False)
def main(config: Path, warnings: bool) -> None:
    """Console script for hiss"""
    banner = _BANNER.format(python_version=_PYTHON_VERSION)

    if not warnings:
        for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
            _warnings.filterwarnings("ignore", category=warning)

    # check for and (optionally) enter virtualenv
    load_venv(_PYTHON_VERSION)

    if isinstance(config, str):
        config = Path(config)

    rc = {}

    if config.exists():
        rc.update(load_rc(config))

    # build configuration
    hc = build_config(rc, banner)

    # start customized ipython!
    IPython.start_ipython(
        argv=[],
        config=hc,
        quick=True,
        auto_create=False,
        )
