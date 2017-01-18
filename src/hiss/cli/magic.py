import os
import sys

from IPython.core.magic import Magics, magics_class, line_magic


@magics_class
class HissMagics(Magics):
    @line_magic
    def pex(self, entry_point):
        if entry_point:
            sys.path[0] = os.path.abspath(sys.path[0])
            sys.path.insert(0, entry_point)
            sys.path.insert(0, os.path.abspath(os.path.join(entry_point, '.bootstrap')))
            from _pex import pex_bootstrapper
            pex_bootstrapper.bootstrap_pex_env(entry_point)
            self.reload_pkg_resources('')
            print("Bootstrapped into pex {0}.".format(entry_point))
        else:
            print("No pex provided! Doing nothing.")

    @line_magic
    def reload_pkg_resources(self, line):
        import pkg_resources
        import six
        six.moves.reload_module(pkg_resources)
