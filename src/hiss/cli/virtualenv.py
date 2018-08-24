import os
import site

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # type: ignore

from .magic import HissMagics


def load_venv(python_version):
    # type: (str) -> None
    if "VIRTUAL_ENV" in os.environ:
        virtual_env = Path(
            os.environ.get("VIRTUAL_ENV"), "lib", python_version, "site-packages"
        )
        if virtual_env.exists():
            site.addsitedir(str(virtual_env))
            HissMagics().reload_pkg_resources("")
            print("\x1B[3mvirtualenv detected -> {}\x1B[23m".format(virtual_env))
