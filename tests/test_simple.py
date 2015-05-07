# -*- coding: utf-8 -*-
"""Do an integration test. Only use simple html files."""

import subprocess


def test_valid():
    assert subprocess.call(['html5validator', '--root=tests/valid/']) == 0


def test_invalid():
    assert subprocess.call(['html5validator', '--root=tests/invalid/']) == 1


def test_angularjs():
    assert subprocess.call([
        'html5validator',
        '--root=tests/angularjs/',
        '--ignore=Attribute “ng-[a-z-]+” not allowed',
    ]) == 0


if __name__ == '__main__':
    # test_valid()
    # test_invalid()
    test_angularjs()
