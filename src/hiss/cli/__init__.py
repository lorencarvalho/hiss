import os
import sys
import warnings as _warnings

from pathlib import Path

import IPython

from .config import build_config, load_rc
from .magic import *  # noqa
from .virtualenv import load_venv

_PYTHON_VERSION = "python{0}.{1}".format(*sys.version_info[0:2])
_HISS_CONFIG = Path(os.environ.get("HOME", "~"), ".hiss").expanduser()
_BANNER = """
hiss - {python_version}

"""


def main():
    # type: (str, bool) -> None
    """Console script for hiss"""
    banner = _BANNER.format(python_version=_PYTHON_VERSION)

    for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
        _warnings.filterwarnings("ignore", category=warning)

    # check for and (optionally) enter virtualenv
    load_venv(_PYTHON_VERSION)

    rc = {}
    config = Path("~/.hiss").expanduser()
    if config.exists():  # type: ignore
        rc.update(load_rc(config))

    # build configuration
    hc = build_config(rc, banner)

    # start customized ipython!
    IPython.start_ipython(argv=sys.argv, config=hc, quick=True, auto_create=False)


if __name__ == "__main__":
    main()
