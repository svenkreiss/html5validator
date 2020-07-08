# -*- coding: utf-8 -*-
"""The main validator class."""

from __future__ import unicode_literals

import fnmatch
import json
import logging
import os
import re
import subprocess
import sys
import vnujar

LOGGER = logging.getLogger(__name__)

DEFAULT_IGNORE_RE = [
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

STDERR_IGNORE_RE = '^Picked up (?:_JAVA_OPTIONS|JAVA_TOOL_OPTIONS):.*\n'


class JavaNotFoundException(Exception):
    def __str__(self):
        return ('Missing Java Runtime Environment on this system. '
                'The command "java" must be available.')


class Validator(object):
    """An object that can be used to validate HTML and other files.

    The constructor accepts the following optional arguments:
     - ignore: A list of strings to ignore in error messages.
     - ignore_re: A list of regular expressions to ignore.
     - errors_only: If true, ignore non-fatal warning messages.
     - format: Format for output messages, which must be one of
       'gnu', 'xml', 'json', or 'text'.
     - stack_size: Maximum stack size for the Java virtual machine.
     - vnu_args: List of additional arguments to pass to 'vnu.jar'.
    """

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
        self.ignore = [self._normalize_string(s) for s in self.ignore]
        self.ignore_re = [self._normalize_string(s) for s in self.ignore_re]

        # Determine jar location.
        self.vnu_jar_location = (vnujar.__file__
                                 .replace('__init__.pyc', 'vnu.jar')
                                 .replace('__init__.py', 'vnu.jar'))
        if sys.platform == 'cygwin':
            self.vnu_jar_location = self._cygwin_path_convert(
                self.vnu_jar_location)

    def _java_options(self):
        java_options = []

        if self.stack_size is not None:
            java_options.append('-Xss{}k'.format(self.stack_size))

        return java_options

    def _vnu_options(self, format=None):
        if format is None:
            format = self.format

        vnu_options = []

        if self.errors_only:
            vnu_options.append('--errors-only')
        if not self.detect_language:
            vnu_options.append('--no-langdetect')
        if format is not None:
            vnu_options.append('--format')
            vnu_options.append(format)
        if self.vnu_args is not None:
            vnu_options += self.vnu_args

        return vnu_options

    def _normalize_string(self, s):
        s = s.replace('“', '"')
        s = s.replace('”', '"')
        return s

    def _cygwin_path_convert(self, filepath):
        return subprocess.check_output(
            ['cygpath', '-w', filepath]).strip().decode('utf8')

    def all_files(self, directory='.', match='*.html', blacklist=None,
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

    def _run_validator(self, files, format=None):
        if sys.platform == 'cygwin':
            files = [self._cygwin_path_convert(f) for f in files]

        try:
            cmd = (['java'] + self._java_options()
                   + ['-jar', self.vnu_jar_location]
                   + self._vnu_options(format)
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

        stderr = stderr.decode('utf-8')

        # filter out Java cruft
        stderr = re.sub(STDERR_IGNORE_RE, '', stderr, flags=re.MULTILINE)

        if format != 'json':
            # process fancy quotes into standard quotes
            stderr = self._normalize_string(stderr)

        return stderr

    def validate(self, files):
        """Validate one or more files and report the number of errors."""
        stderr = self._run_validator(files)

        e = stderr.splitlines()

        # Removes any empty items in the list
        e = list(filter(None, e))

        # Prevents removal of xml tags if there are errors
        if self.format == "xml" and len(e) < 4:
            self.ignore = DEFAULT_IGNORE_XML

        LOGGER.debug(e)

        for i in self.ignore:
            e = [l for l in e if i not in l]
        for i in self.ignore_re:
            regex = re.compile(i)
            e = [l for l in e if not regex.search(l)]

        if e:
            for line in e:
                LOGGER.error(line)
        else:
            LOGGER.info('All good.')
        return len(e)

    def get_messages(self, files):
        """Validate one or more files and return a list of messages.

        Each message is returned as a dictionary containing some or
        all of the following keys:
         - "type"
         - "subtype"
         - "message"
         - "extract"
         - "offset"
         - "url"
         - "firstLine"
         - "firstColumn"
         - "lastLine"
         - "lastColumn"

        Details of this format are documented at:
        https://github.com/validator/validator/wiki/Output-%C2%BB-JSON
        """
        stderr = self._run_validator(files, format='json')
        json_data = json.loads(stderr)
        return json_data['messages']
