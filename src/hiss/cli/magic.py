import json
import os
import site
import sys
import zipfile

from imp import reload

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # type: ignore

from IPython.core.magic import Magics, magics_class, line_magic  # type: ignore
from IPython import start_ipython  # type: ignore


@magics_class
class HissMagics(Magics):

    @line_magic
    def shiv(self, shiv_path):
        if shiv_path:
            sys.path.insert(0, shiv_path)
            from _bootstrap import cache_path  # type: ignore

            zf = zipfile.ZipFile(shiv_path)
            env = json.loads(zf.read("environment.json"))
            site.addsitedir(
                cache_path(zf, Path.home() / ".shiv", env["build_id"]) / "site-packages"
            )
            print("Bootstrapped into shiv {shiv_path}".format(shiv_path=shiv_path))
        else:
            print("No pyz provided! Doing nothing.")

    @line_magic
    def pex(self, entry_point):
        if entry_point:
            sys.path[0] = os.path.abspath(sys.path[0])
            sys.path.insert(0, entry_point)
            sys.path.insert(0, os.path.abspath(os.path.join(entry_point, ".bootstrap")))
            from _pex import pex_bootstrapper  # type: ignore

            pex_bootstrapper.bootstrap_pex_env(entry_point)
            self.reload_pkg_resources("")
            print("Bootstrapped into pex {0}.".format(entry_point))
        else:
            print("No pex provided! Doing nothing.")

    @line_magic
    def reload_pkg_resources(self, line):
        if "pkg_resources" in sys.modules:
            import pkg_resources

            reload(pkg_resources)

    @line_magic
    def debug(self, line):
        import logging

        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger(__name__)  # noqa: F841
        print("Debug logging enabled.")

    @line_magic
    def flask(self, app):
        """This is hella sketchy"""
        try:
            # we assume we have access to flask/werkzeug,
            # if not, go ahead and raise the importerror
            from flask import _request_ctx_stack  # type: ignore
            from werkzeug import import_string  # type: ignore
        except ImportError as e:
            raise ImportError("You don't have flask/werkzeug! {err}".format(err=e))
        else:
            app = import_string(app)
            with app.test_request_context():
                banner = (
                    "\nNow using flask context from: {app_repr}\n"
                    "There is no escape! Exit the session when you are done.\n".format(
                        app_repr=repr(app)
                    )
                )

                # add our custom message
                get_ipython().banner1 = banner  # noqa: F821

                # starting a new session dorks up history, so end our sesh
                get_ipython().history_manager.end_session()  # noqa: F821
                get_ipython().history_manager.reset()  # noqa: F821

                # respawn ipython with the flask context
                start_ipython(user_ns=dict(app=_request_ctx_stack.top.app))
