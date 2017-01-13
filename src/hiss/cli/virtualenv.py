import os
import site


def load_venv(python_version):
    if 'VIRTUAL_ENV' in os.environ:
        virtual_env = os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'lib',
            python_version,
            'site-packages',
        )
        if os.path.exists(virtual_env):
            site.addsitedir(virtual_env)
            print("\x1B[3mvirtualenv detected -> {}\x1B[23m".format(virtual_env))
