"""Validate HTML5 files."""

__version__ = "0.1.2"

import os
import sys
import fnmatch
import subprocess


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
        try:
            subprocess.check_output(['java', '-jar', self.vnu_jar_location] +
                                    opts + files)
        except subprocess.CalledProcessError:
            print '===> Not HTML5 compatible.'
            return 1
        return 0
