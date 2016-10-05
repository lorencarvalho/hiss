import configparser
import os
import site
import sys

import click
import warnings

from IPython import embed
from IPython.terminal.prompts import ClassicPrompts
from IPython.utils.coloransi import TermColors
from traitlets.config.loader import Config

HISS_CONFIG = os.path.expanduser(os.path.join(os.environ.get('HOME', '~'), '.hiss'))
BANNER = """
hiss - python{0}.{1}

"""


def casted(value):
    if value.lower() in ('true', '1'):
        return True
    elif value.lower() in ('false', '0'):
        return False
    return value


def load_config(defaults, path):
    config = configparser.RawConfigParser()
    config.optionxform = str  # preserve case, cast ints to str
    config.read(path)

    if config.has_section('IPython'):
        for item, value in config.items('IPython'):
            option, name = item.split('.')
            config_obj = defaults.get(option, option)
            config_obj[name] = casted(value)
            defaults[option] = config_obj

    return defaults


def embed_ipython(c):
    for warning in (UserWarning, DeprecationWarning, RuntimeWarning):
        warnings.filterwarnings("ignore", category=warning)

    embed(config=c)


@click.command()
@click.option('--config', '-c', default=HISS_CONFIG)
def main(config):
    """Console script for hiss"""

    c = Config()

    # hiss defaults
    c.TerminalInteractiveShell.prompts_class = ClassicPrompts
    c.TerminalInteractiveShell.separate_in = ''
    c.InteractiveShell.banner1 = BANNER.format(*sys.version_info[0:2])
    c.PrefilterManager.multi_line_specials = True
    c.InteractiveShell.autoindent = True
    c.InteractiveShell.colors = 'linux'
    c.InteractiveShell.confirm_exit = False

    # override defaults and add add'l options
    c = load_config(c, config)

    embed_ipython(c)
