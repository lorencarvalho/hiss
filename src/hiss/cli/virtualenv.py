import os
import site

from pathlib import Path

from .magic import HissMagics


def load_venv(python_version: str) -> None:
    if 'VIRTUAL_ENV' in os.environ:
        virtual_env = Path(
            os.environ.get('VIRTUAL_ENV'),
            'lib',
            python_version,
            'site-packages',
        )
        if virtual_env.exists():
            site.addsitedir(str(virtual_env))
            HissMagics().reload_pkg_resources('')
            print("\x1B[3mvirtualenv detected -> {}\x1B[23m".format(virtual_env))
