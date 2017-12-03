import configparser
import io
import os

from pathlib import Path
from typing import Dict, Union, Tuple, Optional

from IPython.terminal.prompts import ClassicPrompts  # type: ignore

from traitlets.config import Config as Config  # type: ignore
from pygments.styles import get_style_by_name  # type: ignore
from pygments.util import ClassNotFound  # type: ignore

_BOOLMAP = {
    'true': True,
    't': True,
    '1': True,
    'false': False,
    'f': False,
    '0': False,
}


def _bool(value: Union[str, bool]) -> bool:
    return value if isinstance(value, bool) else _BOOLMAP[str(value).lower()]


def load_rc(path: Path) -> Dict[str, str]:
    """This function loads the .hiss file represented as a dict"""
    config = io.StringIO()
    config.write('[hiss]\n')

    # attempt load of rc file
    try:
        with open(path) as f:
            config.write(f.read().replace('%', '%%'))
    except IOError:
        # no rc file found
        pass

    config.seek(0, os.SEEK_SET)
    parser = configparser.SafeConfigParser()
    parser.read_file(config)

    return {key: str(value) for key, value in parser.items('hiss')}


def get_theme(rc: Dict[str, str]) -> Tuple[str, Optional[str]]:
    pygments_style = None
    theme = rc.get('theme', 'legacy')

    if theme != 'legacy':
        try:
            pygments_style = get_style_by_name(theme)
        except ClassNotFound:
            theme = 'legacy'

    return theme, pygments_style


def build_config(rc: Dict[str, str], banner: str) -> Config:
    rc = rc

    # initialize traitlets config obj
    config = Config()

    # hardcoded configs
    config.TerminalInteractiveShell.prompts_class = ClassicPrompts
    config.TerminalInteractiveShell.separate_in = ''
    config.TerminalInteractiveShell.true_color = True
    config.TerminalInteractiveShell.banner1 = banner
    config.PrefilterManager.multi_line_specials = True

    # overrideable configs
    config.TerminalInteractiveShell.confirm_exit = _bool(rc.get('confirm_exit', False))
    config.TerminalInteractiveShell.autoindent = _bool(rc.get('autoindent', True))
    config.TerminalInteractiveShell.colors = rc.get('colors', 'Linux')

    # auto reload
    if _bool(rc.get('autoreload', False)):
        config.InteractiveShellApp.extensions = ['autoreload']
        config.InteractiveShellApp.exec_lines = ['%autoreload 2']

    # themes
    theme, pygments_style = get_theme(rc)
    config.TerminalInteractiveShell.highlighting_style = theme
    if pygments_style is not None:
        config.TerminalInteractiveShell.highlighting_style_overrides = pygments_style.styles

    # ensure magics will be loaded
    config.InteractiveShellApp.exec_lines.extend([
        'from hiss.cli.magic import HissMagics',
        'get_ipython().register_magics(HissMagics)',
    ])

    return config
