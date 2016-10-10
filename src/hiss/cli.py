import configparser
import os
import site
import sys
import warnings

import click
import pkg_resources
import pygments

from IPython import embed
from IPython.terminal.prompts import ClassicPrompts
from traitlets.config.loader import Config
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

PYTHON_VERSION = "python{0}.{1}".format(*sys.version_info[0:2])
HISS_CONFIG = os.path.expanduser(os.path.join(os.environ.get('HOME', '~'), '.hiss'))
BANNER = """
hiss - {python_version}

"""


def casted(value):
    if value.lower() in ('true', '1'):
        return True
    elif value.lower() in ('false', '0'):
        return False
    return value


def load_venv():
    if 'VIRTUAL_ENV' in os.environ:
        virtual_env = os.path.join(
            os.environ.get('VIRTUAL_ENV'),
            'lib',
            PYTHON_VERSION,
            'site-packages',
        )
        if os.path.exists(virtual_env):
            site.addsitedir(virtual_env)
            print("virtualenv detected -> {}".format(virtual_env))


def load_configs(ipython_config, hiss_config, path):
    config = configparser.RawConfigParser()
    config.optionxform = str  # preserve case, cast ints to str
    config.read(path)

    if config.has_section('IPython'):
        for item, value in config.items('IPython'):
            option, name = item.split('.')
            config_obj = ipython_config.get(option, option)
            config_obj[name] = casted(value)
            ipython_config[option] = config_obj

    if config.has_section('hiss.themes'):
        hiss_config.update(dict(config.items('hiss.themes')))

    return ipython_config, hiss_config


def embed_ipython(c):
    for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
        warnings.filterwarnings("ignore", category=warning)

    embed(config=c)


def import_theme(theme=None, path='~/.hiss_themes'):
    # TODO: fix this None-checking nonsense:
    if theme is not None:
        theme = theme.strip("'")
        if not theme in pygments.styles.get_all_styles():
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
@click.option('--config', '-c', default=HISS_CONFIG)
def main(config):
    """Console script for hiss"""

    i = Config()
    h = dict()

    # hiss defaults
    i.TerminalInteractiveShell.prompts_class = ClassicPrompts
    i.TerminalInteractiveShell.separate_in = ''
    i.TerminalInteractiveShell.true_color = True
    i.TerminalInteractiveShell.banner1 = BANNER.format(python_version=PYTHON_VERSION)
    i.TerminalInteractiveShell.autoindent = True
    i.TerminalInteractiveShell.colors = 'Linux'
    i.TerminalInteractiveShell.confirm_exit = False
    i.PrefilterManager.multi_line_specials = True

    # override defaults and add add'l options
    i, h = load_configs(i, h, config)

    # set up any themes
    theme = import_theme(**h) or 'legacy'
    i.TerminalInteractiveShell.highlighting_style = theme

    # if any extra overrides were set, add them (such as prompt colors)
    try:
        i.TerminalInteractiveShell.highlighting_style_overrides = get_style_by_name(theme).styles
    except ClassNotFound:
        pass

    # load virtual
    load_venv()

    embed_ipython(i)
