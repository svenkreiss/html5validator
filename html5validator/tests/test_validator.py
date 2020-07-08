# -*- coding: utf-8 -*-
"""Test cases for the Validator API."""

import glob
import os

import html5validator

HTML_TEST_FILES = os.path.abspath(os.path.dirname(__file__))


def all_files(directory):
    return glob.glob(os.path.join(directory, '**', '*.html'), recursive=True)


def test_valid():
    v = html5validator.Validator()
    root = os.path.join(HTML_TEST_FILES, 'valid')
    files = all_files(root)
    num_errors = v.validate(files)
    assert num_errors == 0
    messages = v.get_messages(files)
    assert messages == []


def test_invalid():
    v = html5validator.Validator()
    root = os.path.join(HTML_TEST_FILES, 'invalid')
    files = all_files(root)
    num_errors = v.validate(files)
    assert num_errors > 0
    messages = v.get_messages(files)
    assert len(messages) == num_errors

    assert messages[0]['type'] == 'error'
    assert messages[0]['lastLine'] == 1
    assert messages[0]['message'].startswith(
        u"Start tag seen without seeing a doctype first")


def test_warning():
    v = html5validator.Validator()
    root = os.path.join(HTML_TEST_FILES, 'warning')
    files = all_files(root)
    num_errors = v.validate(files)
    assert num_errors > 0
    messages = v.get_messages(files)
    assert len(messages) == num_errors

    assert messages[0]['type'] == 'info'
    assert messages[0]['firstLine'] == 1
    assert messages[0]['lastLine'] == 2
    assert messages[0]['message'].startswith(
        u"Consider adding a “lang” attribute to the “html” start tag")


if __name__ == '__main__':
    test_valid()
    test_invalid()
    test_warning()
