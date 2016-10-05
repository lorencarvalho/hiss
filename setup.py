import sys
import setuptools
import subprocess

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Click>=6.0',
    'setuptools>25',
]

python_version = sys.version_info[0:2]

if python_version == (2, 6):
    requirements.append("IPython<=0.13")

if python_version <= (3, 3):
    requirements.extend(["enum34", "backports.shutil-get-terminal-size"])

if python_version >= (2, 7):
    requirements.extend(["IPython>=5", "traitlets"])


class Venv(setuptools.Command):
    user_options = []

    def initialize_options(self):
        """Abstract method that is required to be overwritten"""

    def finalize_options(self):
        """Abstract method that is required to be overwritten"""

    def run(self):
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv', 'hiss')
        venv_cmd = [
            'virtualenv',
            venv_path
        ]
        print('Creating virtual environment in ', venv_path)
        subprocess.check_call(venv_cmd)
        print('Linking `activate` to top level of project.\n')
        print('To activate, simply run `source activate`.')
        try:
            os.symlink(
                os.path.join(venv_path, 'bin', 'activate'),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'activate')
            )
        except OSError:
            print('Unable to create symlink, you may have a stale symlink from a previous invocation.')


setuptools.setup(
    name='hiss-repl',
    version='0.1.12',
    description="A simple and easily configured iPython-based python repl",
    long_description=readme,
    author="Loren Carvalho",
    author_email='me@loren.pizza',
    url='https://github.com/sixninetynine/hiss',
    packages=[
        'hiss',
    ],
    package_dir={'hiss': 'hiss'},
    entry_points={
        'console_scripts': [
            'hiss=hiss.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    keywords='hiss',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    cmdclass={'venv': Venv},
)
