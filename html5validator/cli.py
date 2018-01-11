#!/usr/bin/env python
"""Command line tool for HTML5 validation. Return code is 0 for valid HTML5."""

from __future__ import unicode_literals

from .validator import Validator
import argparse
import logging
import sys

from . import __version__ as VERSION

LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='[v' + VERSION + '] ' + __doc__,
        prog='html5validator'
    )
    parser.add_argument('--root', default='.',
                        help='start directory to search for files to validate')
    parser.add_argument('--match', default='*.html',
                        help='match file pattern (default: *.html)')
    parser.add_argument('--blacklist', type=str, nargs='*',
                        help='directory names to skip', default=[])

    parser.add_argument('--show-warnings', dest='errors_only',
                        action='store_false', default=True,
                        help='show warnings')
    parser.add_argument('--no-langdetect',
                        action='store_true', default=False,
                        help='disable language detection')
    parser.add_argument('--format', choices=['gnu', 'xml', 'json', 'text'],
                        help='output format', default=None)

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
                              'stack size to 2048k'))
    parser.add_argument('-ll', action='store_const', const=8192,
                        dest='stack_size',
                        help=('run on larger files: sets Java '
                              'stack size to 8192k'))
    parser.add_argument('-lll', action='store_const', const=32768,
                        dest='stack_size',
                        help=('run on larger files: sets Java '
                              'stack size to 32768k'))

    parser.add_argument('--log', default='WARNING',
                        help=('log level: DEBUG, INFO or WARNING '
                              '(default: WARNING)'))
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + VERSION)
    args = parser.parse_args()

    vnu_options = []
    if args.errors_only:
        vnu_options.append('--errors_only')
    if args.no_langdetect:
        vnu_options.append('--no-langdetect')
    if args.format:
        vnu_options.append('--format')
        vnu_options.append(args.format)

    java_options = []
    if args.stack_size:
        java_options.append('-Xss{}k'.format(args.stack_size))

    logging.basicConfig(level=getattr(logging, args.log))

    validator = Validator(directory=args.root,
                          match=args.match,
                          blacklist=args.blacklist,
                          ignore=args.ignore,
                          ignore_re=args.ignore_re,
                          java_options=java_options,
                          vnu_options=vnu_options)
    files = validator.all_files()
    LOGGER.info('Files to validate: \n  {0}'.format('\n  '.join(files)))
    LOGGER.info('Number of files: {0}'.format(len(files)))

    error_count = validator.validate(files)
    sys.exit(min(error_count, 255))


if __name__ == "__main__":
    main()
