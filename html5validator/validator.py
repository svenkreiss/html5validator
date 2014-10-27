"""The main validator class."""

import os
import vnujar
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
        self.blacklist = blacklist

        # Determine jar location.
        self.vnu_jar_location = vnujar.__file__.replace(
            '__init__.pyc', 'vnu.jar'
        ).replace(
            '__init__.py', 'vnu.jar'
        )

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

    def validate(self, files=None, errors_only=True):
        opts = []
        if errors_only:
            opts.append('--errors-only')
        if not files:
            files = self.all_files()

        with open(os.devnull, 'w') as f_null:
            if subprocess.call(['java', '-version'],
                               stdout=f_null, stderr=f_null) != 0:
                raise JavaNotFoundException()

        return subprocess.call(['java', '-Xss512k', '-jar',
                                self.vnu_jar_location] + opts + files)
