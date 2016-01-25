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
        '--ignore-re=Attribute “ng-[a-z-]+” not allowed',
    ]) == 0


def test_angularjs_normal_quotes():
    assert subprocess.call([
        'html5validator',
        '--root=tests/angularjs/',
        '--ignore-re=Attribute "ng-[a-z-]+" not allowed',
    ]) == 0


def test_multiple_ignoreres():
    o = subprocess.call([
        'html5validator',
        '--root=tests/multiple_ignores/',
        '--ignore-re', 'Attribute “ng-[a-z-]+” not allowed', 'Start tag seen without seeing a doctype first',
    ])
    assert o == 0


def test_ignore_and_ignorere():
    o = subprocess.call([
        'html5validator',
        '--root=tests/multiple_ignores/',
        '--ignore-re', 'Attribute “ng-[a-z-]+” not allowed',
        '--ignore', 'Start tag seen without seeing a doctype first',
    ])
    assert o == 0


def test_stack_size():
    assert subprocess.call(['html5validator',
                            '--root=tests/valid/',
                            '-lll']) == 0


if __name__ == '__main__':
    test_valid()
    test_invalid()
    test_angularjs()
    test_multiple_ignoreres()
    test_ignore_and_ignorere()
