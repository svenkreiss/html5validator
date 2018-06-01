# -*- coding: utf-8 -*-
"""Do an integration test. Only use simple html files."""

import os
import subprocess

HTML_TEST_FILES = os.path.abspath(os.path.dirname(__file__))


def test_valid():
    assert subprocess.call(['html5validator',
                            '--root={}/valid/'.format(HTML_TEST_FILES)]) == 0


def test_invalid():
    assert subprocess.call(['html5validator',
                            '--root={}/invalid/'.format(HTML_TEST_FILES)]) == 1


def test_invalid_with_css():
    assert subprocess.call([
        'html5validator',
        '--root={}/invalid/'.format(HTML_TEST_FILES),
        '--also-check-css',
    ]) == 2


def test_invalid_css_only():
    assert subprocess.call([
        'html5validator',
        '--root', '{}/invalid/'.format(HTML_TEST_FILES),
        '--skip-non-css',
    ]) == 1


def test_invalid_single_file():
    assert subprocess.call([
        'html5validator',
        '{}/invalid/index.html'.format(HTML_TEST_FILES),
    ]) == 1


def test_warning():
    assert subprocess.call(['html5validator',
                            '--root={}/warning/'.format(HTML_TEST_FILES),
                            '--show-warnings']) == 1


def test_warning_but_pass():
    assert subprocess.call(['html5validator',
                            '--root={}/warning/'.format(HTML_TEST_FILES)]) == 0


def test_return_value():
    assert subprocess.call(['html5validator',
                            '--root={}/return_value/'.format(HTML_TEST_FILES),
                            '--match=254.html']) == 254
    assert subprocess.call(['html5validator',
                            '--root={}/return_value/'.format(HTML_TEST_FILES),
                            '--match=255.html']) == 255
    assert subprocess.call(['html5validator',
                            '--root={}/return_value/'.format(HTML_TEST_FILES),
                            '--match=256.html']) == 255


def test_angularjs():
    assert subprocess.call([
        'html5validator',
        '--root={}/angularjs/'.format(HTML_TEST_FILES),
        '--ignore-re=Attribute “ng-[a-z-]+” not allowed',
    ]) == 0


def test_angularjs_normal_quotes():
    assert subprocess.call([
        'html5validator',
        '--root={}/angularjs/'.format(HTML_TEST_FILES),
        '--ignore-re=Attribute "ng-[a-z-]+" not allowed',
    ]) == 0


def test_multiple_ignoreres():
    o = subprocess.call([
        'html5validator',
        '--root={}/multiple_ignores/'.format(HTML_TEST_FILES),
        '--ignore-re', 'Attribute “ng-[a-z-]+” not allowed',
        'Start tag seen without seeing a doctype first',
    ])
    assert o == 0


def test_ignore_and_ignorere():
    o = subprocess.call([
        'html5validator',
        '--root={}/multiple_ignores/'.format(HTML_TEST_FILES),
        '--ignore-re', 'Attribute “ng-[a-z-]+” not allowed',
        '--ignore', 'Start tag seen without seeing a doctype first',
    ])
    assert o == 0


def test_stack_size():
    assert subprocess.call(['html5validator',
                            '--root={}/valid/'.format(HTML_TEST_FILES),
                            '-lll']) == 0


if __name__ == '__main__':
    test_valid()
    test_invalid()
    test_return_value()
    test_angularjs()
    test_multiple_ignoreres()
    test_ignore_and_ignorere()
