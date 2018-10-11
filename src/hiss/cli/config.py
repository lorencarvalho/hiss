import configparser
import io
import os

from typing import Any, Dict, Union, Tuple, Optional  # noqa

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # type: ignore

from IPython.terminal.prompts import ClassicPrompts  # type: ignore

from traitlets.config import Config as Config  # type: ignore
from pygments.styles import get_style_by_name  # type: ignore
from pygments.util import ClassNotFound  # type: ignore

assert Path  # to shush flake8


def _bool(value):
    if not isinstance(value, bool):
        return str(value).lower() in ("true", "t", "1")
    return value


def load_rc(path):
    # type: (Path) -> Dict[str, str]
    """This function loads the .hiss file represented as a dict"""
    config = io.BytesIO()
    config.write(b"[hiss]\n")

    # attempt load of rc file
    try:
        with open(str(path)) as f:
            config.write(f.read().replace("%", "%%").encode("utf8"))
    except IOError:
        # no rc file found
        pass

    config.seek(0, os.SEEK_SET)
    parser = configparser.SafeConfigParser()
    parser.read_string(config.read().decode())

    return {key: str(value) for key, value in parser.items("hiss")}


def get_theme(rc):
    # type: (Dict[str, str]) -> Tuple[str, Optional[Any]]
    pygments_style = None
    theme = rc.get("theme", "legacy")

    if theme != "legacy":
        try:
            pygments_style = get_style_by_name(theme)
        except ClassNotFound:
            theme = "legacy"

    return theme, pygments_style


def build_config(rc, banner):
    # type: (Dict[str, str], str) -> Config

    rc = rc

    # initialize traitlets config obj
    config = Config()

    # hardcoded configs
    config.TerminalInteractiveShell.prompts_class = ClassicPrompts
    config.TerminalInteractiveShell.separate_in = ""
    config.TerminalInteractiveShell.true_color = True
    config.TerminalInteractiveShell.banner1 = banner
    config.PrefilterManager.multi_line_specials = True

    # overrideable configs
    config.TerminalInteractiveShell.confirm_exit = _bool(rc.get("confirm_exit", False))
    config.TerminalInteractiveShell.autoindent = _bool(rc.get("autoindent", True))
    config.TerminalInteractiveShell.colors = rc.get("colors", "Linux")
    config.TerminalInteractiveShell.editing_mode = rc.get("editing_mode", "emacs")

    # auto reload
    if _bool(rc.get("autoreload", False)):
        config.InteractiveShellApp.extensions = ["autoreload"]
        config.InteractiveShellApp.exec_lines = ["%autoreload 2"]

    # themes
    theme, pygments_style = get_theme(rc)
    config.TerminalInteractiveShell.highlighting_style = theme
    if pygments_style is not None:
        config.TerminalInteractiveShell.highlighting_style_overrides = (
            pygments_style.styles
        )

    # ensure magics will be loaded
    config.InteractiveShellApp.exec_lines.extend(
        [
            "from hiss.cli.magic import HissMagics",
            "get_ipython().register_magics(HissMagics)",
        ]
    )

    return config
