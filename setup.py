import os
import sys
import setuptools
import subprocess
import venv
import re

from setuptools.command import easy_install

requirements = [
    'Click==6.6',
    'IPython==6.2.1',
    'cached_property==1.2.0',
    'traitlets',
    'configparser',
    'pygments',
    'six',
]

if sys.version_info[0] < 3:
    raise SystemExit("hiss does not support python2 !!")


# fast entry points, Copyright (c) 2016, Aaron Christianson
# https://github.com/ninjaaron/fast-entry_point
TEMPLATE = '''\
# -*- coding: utf-8 -*-
# EASY-INSTALL-ENTRY-SCRIPT: '{3}','{4}','{5}'
__requires__ = '{3}'
import re
import sys
from {0} import {1}
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit({2}())'''


@classmethod
def get_args(cls, dist, header=None):
    """
    Yield write_script() argument tuples for a distribution's
    console_scripts and gui_scripts entry points.
    """
    if header is None:
        header = cls.get_header()
    spec = str(dist.as_requirement())
    for type_ in 'console', 'gui':
        group = type_ + '_scripts'
        for name, ep in dist.get_entry_map(group).items():
            # ensure_safe_name
            if re.search(r'[\\/]', name):
                raise ValueError("Path separators not allowed in script names")
            script_text = TEMPLATE.format(
                ep.module_name,
                ep.attrs[0],
                '.'.join(ep.attrs),
                spec,
                group,
                name,
            )
            args = cls._get_script_args(type_, name, header, script_text)
            for res in args:
                yield res


easy_install.ScriptWriter.get_args = get_args


class Venv(setuptools.Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'hiss')
        print('Creating virtual environment in {}'.format(venv_path))
        venv.main(args=[venv_path])
        print(
            'Linking `activate` to top level of project.\n'
            'To activate, simply run `source activate`.'
        )
        try:
            os.symlink(
                os.path.join(venv_path, 'bin', 'activate'),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'activate')
            )
        except OSError:
            # symlink already exists
            pass


setuptools.setup(
    name='hiss-repl',
    version='3.0.1',
    description="A simple and easily configured iPython-based python repl",
    author="Loren Carvalho",
    author_email='me@loren.pizza',
    url='https://github.com/sixninetynine/hiss',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'hiss=hiss.cli:main'
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    keywords='hiss',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    cmdclass={'venv': Venv},
)
