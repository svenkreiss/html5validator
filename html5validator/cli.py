#!/usr/bin/env python
"""Command line tool for HTML5 validation. Return code is 0 for valid HTML5."""

from __future__ import unicode_literals

import sys
import logging
import argparse

from .validator import Validator
from . import __version__ as VERSION

LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='[v'+VERSION+'] '+__doc__,
                                     prog='html5validator')
    parser.add_argument('--root', default='.',
                        help='start directory to search for files to validate')
    parser.add_argument('--match', default='*.html',
                        help='match file pattern (default: *.html)')
    parser.add_argument('--blacklist', type=str, nargs='*',
                        help='directory names to skip', default=[])
    parser.add_argument('--show-warnings', dest='error_only',
                        action='store_false', default=True)
    parser.add_argument('--ignore', nargs='*', default=None,
                        type=lambda s: (s.decode('utf-8')
                                        if isinstance(s, bytes) else s),
                        help='ignore messages containing the given strings')
    parser.add_argument('--ignore-re', nargs='*', default=None,
                        type=lambda s: (s.decode('utf-8')
                                        if isinstance(s, bytes) else s),
                        dest='ignore_re',
                        help='regular expression of messages to ignore')
    parser.add_argument('-l', action='store_const', const=2048,
                        dest='stack_size',
                        help=('run on larger files: sets Java '
                              'stack size to 2048k')
                        )
    parser.add_argument('-ll', action='store_const', const=8192,
                        dest='stack_size',
                        help=('run on larger files: sets Java '
                              'stack size to 8192k')
                        )
    parser.add_argument('-lll', action='store_const', const=32768,
                        dest='stack_size',
                        help=('run on larger files: sets Java '
                              'stack size to 32768k')
                        )
    parser.add_argument('--log', default='WARNING',
                        help=('log level: DEBUG, INFO or WARNING '
                              '(default: WARNING)'))
    parser.add_argument('--version', action='version',
                        version='%(prog)s '+VERSION)
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log))

    v = Validator(directory=args.root, match=args.match,
                  blacklist=args.blacklist,
                  ignore=args.ignore, ignore_re=args.ignore_re)
    files = v.all_files()
    LOGGER.info('Files to validate: \n  {0}'.format('\n  '.join(files)))
    LOGGER.info('Number of files: {0}'.format(len(files)))
    sys.exit(v.validate(
        files,
        errors_only=args.error_only,
        stack_size=args.stack_size,
    ))


if __name__ == "__main__":
    main()
