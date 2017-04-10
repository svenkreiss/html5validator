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


class JavaNotFoundException(Exception):
    def __str__(self):
        return 'Missing Java Runtime Environment on this system. ' +\
               'The command "java" must be available.'


class Validator(object):

    def __init__(self, directory='.', match='*.html', blacklist=None,
                 ignore=None, ignore_re=None):
        self.directory = directory
        self.match = match
        self.blacklist = blacklist if blacklist else []
        self.ignore = ignore if ignore else []
        self.ignore_re = ignore_re if ignore_re else []

        # process fancy quotes in ignore
        self.ignore = [self._normalize_string(s) for s in self.ignore]
        self.ignore_re = [self._normalize_string(s) for s in self.ignore_re]

        # Determine jar location.
        self.vnu_jar_location = vnujar.__file__.replace(
            '__init__.pyc', 'vnu.jar'
        ).replace(
            '__init__.py', 'vnu.jar'
        )
        if sys.platform == 'cygwin':
            self.vnu_jar_location = self._cygwin_path_convert(
                self.vnu_jar_location)

    def _normalize_string(self, s):
        s = s.replace('“', '"')
        s = s.replace('”', '"')
        return s

    def _cygwin_path_convert(self, filepath):
        return subprocess.check_output(
            ['cygpath', '-w', filepath]).strip().decode('utf8')

    def all_files(self, skip_invisible=True):
        files = []
        for root, dirnames, filenames in os.walk(self.directory):
            # filter out blacklisted directory names
            for b in self.blacklist:
                if b in dirnames:
                    dirnames.remove(b)

            if skip_invisible:
                # filter out directory names starting with '.'
                invisible_dirs = [d for d in dirnames if d[0] == '.']
                for d in invisible_dirs:
                    dirnames.remove(d)

            for filename in fnmatch.filter(filenames, self.match):
                if skip_invisible and filename[0] == '.':
                    # filter out invisible files
                    continue
                files.append(os.path.join(root, filename))
        return files

    def validate(self, files=None, errors_only=True, stack_size=None):
        opts = []
        if errors_only:
            opts.append('--errors-only')
        if stack_size:
            opts.append('-Xss{}k'.format(stack_size))
        if not files:
            files = self.all_files()

        if sys.platform == 'cygwin':
            files = [self._cygwin_path_convert(f) for f in files]

        with open(os.devnull, 'w') as f_null:
            if subprocess.call(['java', '-version'],
                               stdout=f_null, stderr=f_null) != 0:
                raise JavaNotFoundException()

        try:
            o = subprocess.check_output(['java', '-jar',
                                         self.vnu_jar_location] + opts + files,
                                        stderr=subprocess.STDOUT,
                                        ).decode('utf-8')
        except subprocess.CalledProcessError as e:
            o = e.output.decode('utf-8')

        # process fancy quotes into standard quotes
        o = self._normalize_string(o)

        o = o.splitlines()
        for i in self.ignore:
            o = [l for l in o if i not in l]
        for i in self.ignore_re:
            regex = re.compile(i)
            o = [l for l in o if not regex.search(l)]

        if o:
            LOGGER.warn('\n'.join(o))
        else:
            LOGGER.info('All good.')

        return len(o)
