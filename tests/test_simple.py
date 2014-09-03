"""Do an integration test. Only use simple html files."""

import subprocess


def test_valid():
    subprocess.check_call(['html5validator', '--root=tests/valid/'])


def test_invalid():
    try:
        subprocess.check_call(['html5validator', '--root=tests/invalid/'])
    except subprocess.CalledProcessError, e:
        assert e.returncode == 1
