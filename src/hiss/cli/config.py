import configparser
import os
import six

from IPython.terminal.prompts import ClassicPrompts

from cached_property import cached_property
from traitlets.config import Config as Config
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

_BOOLMAP = {
    'true': True,
    't': True,
    '1': True,
    'false': False,
    'f': False,
    '0': False,
}


def _bool(value):
    return value if type(value) == bool else _BOOLMAP[value.lower()]


class HissConfig(object):

    _OVERRIDES = (
        'theme',
        'autoreload',
        'confirm_exit',
        'colors',
        'deep_reload',
        'editor',
        'xmode',
    )

    def __init__(self, path, banner):
        self.path = os.path.expanduser(path)

        # initialize traitlets config obj
        self.config = Config()

        # hardcoded configs
        self.config.TerminalInteractiveShell.prompts_class = ClassicPrompts
        self.config.TerminalInteractiveShell.separate_in = ''
        self.config.TerminalInteractiveShell.true_color = True
        self.config.TerminalInteractiveShell.banner1 = banner
        self.config.PrefilterManager.multi_line_specials = True

        # overrideable configs
        self.theme()
        self.autoreload()
        self.config.TerminalInteractiveShell.confirm_exit = _bool(self.rc.get('confirm_exit', False))
        self.config.TerminalInteractiveShell.autoindent = _bool(self.rc.get('autoindent', True))
        self.config.TerminalInteractiveShell.colors = self.rc.get('colors', 'Linux')

        # ensure magics will be loaded
        self.config.InteractiveShellApp.exec_lines.extend([
            'from hiss.cli.magic import HissMagics',
            'get_ipython().register_magics(HissMagics)',
        ])

    @cached_property
    def rc(self):
        config = six.StringIO()
        config.write('[hiss]\n')

        # attempt load of rc file
        try:
            with open(self.path) as f:
                config.write(f.read().replace('%', '%%'))
        except IOError:
            # no rc file found
            pass

        config.seek(0, os.SEEK_SET)
        cp = configparser.SafeConfigParser()
        cp.readfp(config)

        return dict(cp.items('hiss'))

    def theme(self):
        theme = self.rc.get('theme', 'legacy')

        if theme != 'legacy':
            try:
                pygments_style = get_style_by_name(theme)
            except ClassNotFound:
                pygments_style = False
                theme = 'legacy'
        else:
            pygments_style = None

        self.config.TerminalInteractiveShell.highlighting_style = theme

        if pygments_style:
            self.config.TerminalInteractiveShell.highlighting_style_overrides = pygments_style.styles

    def autoreload(self):
        ar = _bool(self.rc.get('autoreload', False))
        if ar:
            self.config.InteractiveShellApp.extensions = ['autoreload']
            self.config.InteractiveShellApp.exec_lines = ['%autoreload 2']
