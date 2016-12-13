import os

import click
from click.testing import CliRunner

from hiss.cli import main


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
