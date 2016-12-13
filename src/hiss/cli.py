import ast
import configparser
import os
import site
import sys
import warnings

import click
import pygments
import six

from IPython import embed
from IPython.terminal.prompts import ClassicPrompts
from traitlets.config.loader import Config
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

import pkg_resources
six.moves.reload_module(pkg_resources)  # for entry_points to load

from .magic import *  # noqa

_PYTHON_VERSION = "python{0}.{1}".format(*sys.version_info[0:2])
_HISS_CONFIG = os.path.expanduser(os.path.join(os.environ.get('HOME', '~'), '.hiss'))
_BANNER = """
hiss - {python_version}

"""

def _load_venv():
    if 'VIRTUAL_ENV' in os.environ:
        virtual_env = os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'lib',
            _PYTHON_VERSION,
            'site-packages',
        )
        if os.path.exists(virtual_env):
            site.addsitedir(virtual_env)
            print("virtualenv detected -> {}".format(virtual_env))


def _load_config(path):
    def casted(value):
        if isinstance(value, (str, int)) and value.lower() in ('true', '1', 1):
            value = True
        elif isinstance(value, (str, int)) and  value.lower() in ('false', '0', 0):
            value = False
        else:
            value = ast.literal_eval(value)

        return value

    ip_overrides = {}
    themes = {}

    config = configparser.RawConfigParser()
    config.optionxform = str  # preserve case, cast ints to str
    config.read(path)

    if config.has_section('IPython'):
        for option, value in config.items('IPython'):
            ip_overrides[option] = casted(value)

    if config.has_section('hiss.themes'):
        themes.update(dict(config.items('hiss.themes')))

    return ip_overrides, themes


def _embed_ipython(c):
    for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
        warnings.filterwarnings("ignore", category=warning)

    embed(config=c)


def _import_theme(theme=None, path='~/.hiss_themes'):
    # TODO: fix this None-checking nonsense:
    if theme is not None:
        theme = theme.strip("'")
        if theme not in pygments.styles.get_all_styles():
            path = os.path.expanduser(path)
            sys.path.append(path)

            # build entry point
            dist = pkg_resources.get_distribution('pygments')
            ep = pkg_resources.EntryPoint.parse('hiss={}'.format(theme))
            ep.dist = dist
            dist._ep_map['pygments.styles'] = {'hiss': ep}
            theme = 'hiss'
    return theme


@click.command()
@click.option('--config', '-c', default=_HISS_CONFIG)
def main(config):
    """Console script for hiss"""

    i = Config()

    # hiss defaults
    i.TerminalInteractiveShell.prompts_class = ClassicPrompts
    i.TerminalInteractiveShell.separate_in = ''
    i.TerminalInteractiveShell.true_color = True
    i.TerminalInteractiveShell.banner1 = _BANNER.format(python_version=_PYTHON_VERSION)
    i.TerminalInteractiveShell.autoindent = True
    i.TerminalInteractiveShell.colors = 'Linux'
    i.TerminalInteractiveShell.confirm_exit = False
    i.PrefilterManager.multi_line_specials = True

    # collect config & theme overrides from config file
    ip_overrides, themes = _load_config(config)

    # override defaults and add add'l options
    ip_overrides['highlighting_style'] = _import_theme(**themes) or 'legacy'
    i.TerminalInteractiveShell.update(ip_overrides)

    # if any extra implicit overrides were set, add them (such as prompt colors)
    try:
        i.TerminalInteractiveShell.highlighting_style_overrides = get_style_by_name(ip_overrides['highlighting_style']).styles
    except ClassNotFound:
        pass

    # load virtual
    _load_venv()

    _embed_ipython(i)
