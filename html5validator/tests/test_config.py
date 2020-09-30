# -*- coding: utf-8 -*-
"""Do an integration test for config file usage."""

import os
import subprocess

HTML_TEST_FILES = os.path.abspath(os.path.dirname(__file__))


def test_config_valid():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/valid.yaml'.format(HTML_TEST_FILES)]) == 0


def test_config_invalid():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/invalid.yaml'.format(HTML_TEST_FILES)]) == 1


def test_config_invalid_with_css():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/invalid_css.yaml'.format(HTML_TEST_FILES)
    ]) == 3


def test_config_invalid_css_only():
    assert subprocess.call([
        'html5validator',
        "--config={}/config_files/invalid_css_only.yaml".format(
            HTML_TEST_FILES
        )]) == 2


def test_config_invalid_single_file():
    assert subprocess.call([
        'html5validator',
        "--config={}/config_files/invalid_single_file.yaml".format(
            HTML_TEST_FILES
        )]) == 1


def test_config_warning():
    assert subprocess.call([
        'html5validator',
        "--config={}/config_files/warning.yaml".format(
            HTML_TEST_FILES)]) == 1


def test_config_warning_but_pass():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/warning_pass.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_return_value():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/return_254.yaml'.format(
            HTML_TEST_FILES)]) == 254
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/return_255.yaml'.format(
            HTML_TEST_FILES)]) == 255
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/return_255_256.yaml'.format(
            HTML_TEST_FILES)]) == 255


def test_config_angularjs():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/angularjs.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_angularjs_no_output_with_ignore():
    """Make sure there is no spurious output when messages are ignored."""

    assert subprocess.check_output([
        'html5validator',
        '--config={}/config_files/angularjs.yaml'.format(
            HTML_TEST_FILES)]) == b''


def test_config_angularjs_normal_quotes():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/angularjs_normal.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_multiple_ignoreres():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/multiple_ignores.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_ignore_and_ignorere():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/ignore_and_ignorere.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_stack_size():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/stack_size.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_valid_format_flags():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/text_valid.yaml'.format(
            HTML_TEST_FILES)]) == 0
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/gnu_valid.yaml'.format(
            HTML_TEST_FILES)]) == 0
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/json_valid.yaml'.format(
            HTML_TEST_FILES)]) == 0
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/xml_valid.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_invalid_format_flags():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/text_invalid.yaml'.format(
            HTML_TEST_FILES)]) == 3
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/gnu_invalid.yaml'.format(
            HTML_TEST_FILES)]) == 1
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/json_invalid.yaml'.format(
            HTML_TEST_FILES)]) == 1
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/format_flags/xml_invalid.yaml'.format(
            HTML_TEST_FILES)]) == 8


def test_config_log_file():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/log_file.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_extra():
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/extra.yaml'.format(HTML_TEST_FILES)]) == 0


if __name__ == '__main__':
    test_config_valid()
    test_config_invalid()
    test_config_return_value()
    test_config_angularjs()
    test_config_multiple_ignoreres()
    test_config_ignore_and_ignorere()
    test_config_stack_size()
    test_config_valid_format_flags()
    test_config_invalid_format_flags()
    test_config_log_file()
    test_config_extra()
