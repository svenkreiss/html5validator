# -*- coding: utf-8 -*-
"""Do an integration test for config file usage."""

import os
import subprocess

HTML_TEST_FILES = os.path.abspath(os.path.dirname(__file__))


def test_config_valid():
    """Config test for valid HTML"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/valid.yaml'.format(HTML_TEST_FILES)]) == 0


def test_config_invalid():
    """Config test for invalid HTML"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/invalid.yaml'.format(HTML_TEST_FILES)]) == 1


def test_config_skip():
    """Config test for skipping files"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/skip.yaml'.format(HTML_TEST_FILES)]) == 2


def test_config_invalid_with_css():
    """Config test for CSS and HTML"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/invalid_css.yaml'.format(HTML_TEST_FILES)
    ]) == 3


def test_config_invalid_css_only():
    """Config test for CSSS only"""
    assert subprocess.call([
        'html5validator',
        "--config={}/config_files/invalid_css_only.yaml".format(
            HTML_TEST_FILES
        )]) == 2


def test_config_invalid_single_file():
    """Config test for invalid single file"""
    assert subprocess.call([
        'html5validator',
        "--config={}/config_files/invalid_single_file.yaml".format(
            HTML_TEST_FILES
        )]) == 1


def test_config_warning():
    """Config test for warnings"""
    assert subprocess.call([
        'html5validator',
        "--config={}/config_files/warning.yaml".format(
            HTML_TEST_FILES)]) == 1


def test_config_warning_but_pass():
    """Config test for allowed warnings"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/warning_pass.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_return_value():
    """Config test for error code return value"""
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
    """Config test for angularjs"""
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
    """Config test for normal angularjs"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/angularjs_normal.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_multiple_ignoreres():
    """Config test for multiple regex ignores"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/multiple_ignores.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_ignore_and_ignorere():
    """Config test for ignore and regex ignore"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/ignore_and_ignorere.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_stack_size():
    """Config test for stack size"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/stack_size.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_valid_format_flags():
    """Config test for output format for valid files"""
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
    """Config test for output format with invalid files"""
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
    """Config test for log file"""
    assert subprocess.call([
        'html5validator',
        '--config={}/config_files/log_file.yaml'.format(
            HTML_TEST_FILES)]) == 0


def test_config_extra():
    """Config test for vnu extra arguments"""
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
