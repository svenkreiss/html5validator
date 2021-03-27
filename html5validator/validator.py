# -*- coding: utf-8 -*-
"""The main validator class."""

from __future__ import unicode_literals

import fnmatch
import logging
import os
import re
import subprocess
import sys
import vnujar

LOGGER = logging.getLogger(__name__)

DEFAULT_IGNORE_RE = [
    r'\APicked up _JAVA_OPTIONS:.*',
    r'\ADocument checking completed. No errors found.*',
]

DEFAULT_IGNORE = [
    '{"messages":[]}'
]

DEFAULT_IGNORE_XML = [
    '</messages>',
    '<?xml version=\'1.0\' encoding=\'utf-8\'?>',
    '<messages xmlns="http://n.validator.nu/messages/">'
]


class JavaNotFoundException(Exception):
    def __str__(self):
        return ('Missing Java Runtime Environment on this system. '
                'The command "java" must be available.')


def all_files(directory='.', match='*.html', blacklist=None,
              skip_invisible=True):
    if blacklist is None:
        blacklist = []
    if not isinstance(match, list):
        match = [match]

    files = []
    for root, dirnames, filenames in os.walk(directory):
        # filter out blacklisted directory names
        for b in blacklist:
            if b in dirnames:
                dirnames.remove(b)
            if b in filenames:
                filenames.remove(b)

        if skip_invisible:
            # filter out directory names starting with '.'
            invisible_dirs = [d for d in dirnames if d[0] == '.']
            for d in invisible_dirs:
                dirnames.remove(d)

        for pattern in match:
            for filename in fnmatch.filter(filenames, pattern):
                if skip_invisible and filename[0] == '.':
                    # filter out invisible files
                    continue
                files.append(os.path.join(root, filename))

    return files


def _cygwin_path_convert(filepath):
    return subprocess.check_output(
        ['cygpath', '-w', filepath], shell=False).strip().decode('utf8')


def _normalize_string(s):
    s = s.replace('“', '"')
    s = s.replace('”', '"')
    return s


class Validator(object):

    def __init__(self,
                 ignore=None, ignore_re=None,
                 errors_only=False, detect_language=True, format=None,
                 stack_size=None, vnu_args=None):
        self.ignore = ignore if ignore else []
        self.ignore_re = ignore_re if ignore_re else []

        # java options
        self.stack_size = stack_size

        # vnu options
        self.errors_only = errors_only
        self.detect_language = detect_language
        self.format = format
        self.vnu_args = vnu_args

        # add default ignore_re
        self.ignore_re += DEFAULT_IGNORE_RE

        # add default ignore
        self.ignore += DEFAULT_IGNORE

        # process fancy quotes in ignore
        self.ignore = [_normalize_string(s) for s in self.ignore]
        self.ignore_re = [_normalize_string(s) for s in self.ignore_re]

        # Determine jar location.
        self.vnu_jar_location = (vnujar.__file__
                                 .replace('__init__.pyc', 'vnu.jar')
                                 .replace('__init__.py', 'vnu.jar'))
        if sys.platform == 'cygwin':
            self.vnu_jar_location = _cygwin_path_convert(
                self.vnu_jar_location)

    def _java_options(self):
        java_options = []

        if self.stack_size is not None:
            java_options.append('-Xss{}k'.format(self.stack_size))

        return java_options

    def _vnu_options(self):
        vnu_options = []

        if self.errors_only:
            vnu_options.append('--errors-only')
        if not self.detect_language:
            vnu_options.append('--no-langdetect')
        if self.format is not None:
            vnu_options.append('--format')
            vnu_options.append(self.format)
        if self.vnu_args is not None:
            vnu_options += self.vnu_args

        return vnu_options

    def validate(self, files):
        if sys.platform == 'cygwin':
            files = [_cygwin_path_convert(f) for f in files]

        try:
            cmd = (['java'] + self._java_options()
                   + ['-jar', self.vnu_jar_location]
                   + self._vnu_options()
                   + files)
            LOGGER.debug(cmd)
            p = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            _, stderr = p.communicate()
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                raise JavaNotFoundException()
            else:
                raise
        except subprocess.CalledProcessError as error:
            raise (error.output.decode('utf-8'))

        # process fancy quotes into standard quotes
        stderr = _normalize_string(stderr.decode('utf-8'))

        err = stderr.splitlines()

        # Removes any empty items in the list
        err = list(filter(None, err))

        # Prevents removal of xml tags if there are errors
        if self.format == "xml" and len(err) < 4:
            self.ignore = DEFAULT_IGNORE_XML

        LOGGER.debug(err)

        for ignored in self.ignore:
            err = [line for line in err if ignored not in line]
        for ignored in self.ignore_re:
            regex = re.compile(ignored)
            err = [line for line in err if not regex.search(line)]

        if err:
            for line in err:
                LOGGER.error(line)
        else:
            LOGGER.info('All good.')
        return len(err)
