"""Do an integration test. Only use simple html files."""

import subprocess


def test_valid():
    assert subprocess.call(['html5validator', '--root=tests/valid/']) == 0


def test_invalid():
    assert subprocess.call(['html5validator', '--root=tests/invalid/']) == 1
