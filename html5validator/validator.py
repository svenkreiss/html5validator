# -*- coding: utf-8 -*-
"""The main validator class."""

from __future__ import unicode_literals

import contextlib
import fnmatch
import logging
import os
import pystache
import re
import shutil
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
                 ignore=None, ignore_re=None, mustache_remover_copy_ext='~'):
        self.directory = directory
        self.match = match
        self.blacklist = blacklist if blacklist else []
        self.ignore = ignore if ignore else []
        self.ignore_re = ignore_re if ignore_re else []
        self.mustache_remover_copy_ext = mustache_remover_copy_ext

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
            self.vnu_jar_location = subprocess.check_output(['cygpath', '-w', self.vnu_jar_location]).strip().decode('utf8')

    def _normalize_string(self, s):
        s = s.replace('“', '"')
        s = s.replace('”', '"')
        return s

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

    def validate(self, files=None, remove_mustaches=False, **kwargs):
        if not files:
            files = self.all_files()
        if remove_mustaches:
            with generate_mustachefree_tmpfiles(files, copy_ext=self.mustache_remover_copy_ext) as files:
                return self._validate(files, **kwargs)
        else:
            return self._validate(files, **kwargs)

    def _validate(self, files, errors_only=True, stack_size=None):
        opts = []
        if errors_only:
            opts.append('--errors-only')
        if stack_size:
            opts.append('-Xss{}k'.format(stack_size))

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

@contextlib.contextmanager
def generate_mustachefree_tmpfiles(filepaths, copy_ext):
    mustachefree_tmpfiles = []

    for filepath in filepaths:
        tmpfile = filepath + copy_ext
        shutil.copyfile(filepath, tmpfile)
        with open(filepath, 'r') as src_file:
            with open(tmpfile, 'w+') as new_tmpfile:
                new_tmpfile.write(pystache.render(src_file.read()))
        mustachefree_tmpfiles.append(tmpfile)

    try:
        yield mustachefree_tmpfiles
    finally:
        for tmpfile in mustachefree_tmpfiles:
            os.remove(tmpfile)
