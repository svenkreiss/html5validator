"""Validate HTML5 files."""

__version__ = "0.1.3"

import os
import sys
import fnmatch
import subprocess


class JavaNotFoundException(Exception):
    def __str__(self):
        return 'Missing Java Runtime Environment on this system. ' +\
               'The command "java" must be available.'


class Validator(object):

    def __init__(self, directory='.', match='*.html', blacklist=[]):
        self.directory = directory
        self.match = match
        self.blacklist = ['.git', '.svn'] + blacklist
        self.vnu_jar_location = sys.prefix+'/vnu.jar'

    def all_files(self):
        files = []
        for root, dirnames, filenames in os.walk(self.directory):
            for b in self.blacklist:
                if b in dirnames:
                    dirnames.remove(b)
            for filename in fnmatch.filter(filenames, self.match):
                files.append(os.path.join(root, filename))
        return files

    def validate(self, errors_only=True):
        opts = []
        if errors_only:
            opts.append('--errors-only')
        files = self.all_files()

        with open(os.devnull, 'w') as f_null:
            if subprocess.call(['java', '-version'],
                               stdout=f_null, stderr=f_null) != 0:
                raise JavaNotFoundException()

        return subprocess.call(['java', '-jar', self.vnu_jar_location] +
                               opts + files)
