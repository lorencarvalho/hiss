import os

import click
from click.testing import CliRunner

from hiss.cli import main, casted

def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0


def test_casted():
    assert casted('True') is True
    assert casted('some value') == 'some value'
