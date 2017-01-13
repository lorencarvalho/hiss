import configparser
import os
import pkg_resources
import six

from IPython.terminal.embed import InteractiveShellEmbed
from IPython.terminal.prompts import ClassicPrompts

from cached_property import cached_property
from traitlets.config import Config as Config
from pygments.styles import get_style_by_name
from pygments.util import ClassNotFound

THEMES = "hiss.themes"
DEFAULTS = dict(
    autoreload=False,
    confirm_exit=False,
    theme='legacy',
)


def extra_themes():
    return {
        ep.name: ep.load() for ep in pkg_resources.iter_entry_points(THEMES)
    }


class HissConfig(object):
    def __init__(self, path, banner, python_version):
        self.path = path
        self.config = Config()

        # hiss non-overridable defaults
        self.config.TerminalInteractiveShell.prompts_class = ClassicPrompts
        self.config.TerminalInteractiveShell.separate_in = ''
        self.config.TerminalInteractiveShell.true_color = True
        self.config.TerminalInteractiveShell.banner1 = banner.format(python_version=python_version)
        self.config.TerminalInteractiveShell.autoindent = True
        self.config.TerminalInteractiveShell.colors = 'Linux'
        self.config.TerminalInteractiveShell.confirm_exit = False
        self.config.PrefilterManager.multi_line_specials = True

    @cached_property
    def rc(self):
        try:
            with open(self.path) as f:
                config = six.StringIO()
                config.write('[hiss]\n')
                config.write(f.read().replace('%', '%%'))
                config.seek(0, os.SEEK_SET)

                cp = configparser.SafeConfigParser()
                cp.readfp(config)

                return dict(cp.items('hiss'))
        except IOError:
            return {}

    def bool(self, value):
        if type(value) == bool:
            return value

        value = value.lower()
        valid = {
            'true': True,
            't': True,
            '1': True,
            'false': False,
            'f': False,
            '0': False,
        }

        return valid[value]

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
        return self.bool(self.rc.get('autoreload', False))

    def confirm_exit(self):
        ce = self.bool(self.rc.get('confirm_exit', False))
        self.config.TerminalInteractiveShell.confirm_exit = ce

    def configured_shell(self):
        self.theme()
        self.confirm_exit()

        shell = InteractiveShellEmbed(config=self.config)

        if self.autoreload():
            shell.extension_manager.load_extension('autoreload')
            shell.run_cell('%autoreload 2')

        return shell
