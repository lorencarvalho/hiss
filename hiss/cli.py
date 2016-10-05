import sys

import click
import warnings

from IPython import embed

try:
    from IPython import version_info as ipython_version
except ImportError:
    # probably 0.11 or thereabout
    import IPython
    ipython_version = tuple(map(int, IPython.__version__.split('.')))

from traitlets.config.loader import Config


def embed_ipython():
    warnings.filterwarnings("ignore", category=UserWarning)

    c = Config()

    if ipython_version[0] == 5 :
        from IPython.terminal.prompts import ClassicPrompts
        c.TerminalInteractiveShell.prompts_class = ClassicPrompts
    else:
        c.PromptManager.in_template  = '>>> '
        c.PromptManager.in2_template = '... '
        c.PromptManager.out_template = ''

    c.InteractiveShell.banner1 = "\nhiss - python{0}.{1}\n".format(*sys.version_info[0:2])
    c.PrefilterManager.multi_line_specials = True
    c.InteractiveShell.autoindent = True
    c.InteractiveShell.colors = 'linux'
    c.InteractiveShell.confirm_exit = False

    embed(config=c)


@click.command()
def main(args=None):
    """Console script for hiss"""
    embed_ipython()
