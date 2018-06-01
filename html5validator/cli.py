#!/usr/bin/env python
"""Command line tool for HTML5 validation. Return code is 0 for valid HTML5.

Arguments that are unknown to html5validator are passed as arguments
to `vnu.jar`.
"""

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
    parser.add_argument('files', nargs='*', default=None,
                        help='specify files to check')

    parser.add_argument('--root', default='.',
                        help='start directory to search for files to validate')
    parser.add_argument('--match', nargs='+',
                        help=('match file pattern in search '
                              '(default: "*.html" or '
                              '"*.html *.css" if --also-check-css is used)'))
    parser.add_argument('--blacklist', type=str, nargs='*',
                        help='directory names to skip in search', default=[])

    parser.add_argument('--show-warnings', dest='errors_only',
                        action='store_false', default=True,
                        help='show warnings and count them as errors')
    parser.add_argument('--no-langdetect', dest='detect_language',
                        action='store_false', default=True,
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
    args, extra_args = parser.parse_known_args()

    if args.match is None:
        args.match = ['*.html']

        # append to match
        if '--also-check-css' in extra_args or '--css' in extra_args:
            args.match.append('*.css')
        if '--also-check-svg' in extra_args or '--svg' in extra_args:
            args.match.append('*.svg')

        # overwrite match
        if '--skip-non-css' in extra_args:
            args.match = ['*.css']
        if '--skip-non-svg' in extra_args:
            args.match = ['*.svg']

    logging.basicConfig(level=getattr(logging, args.log))

    validator = Validator(ignore=args.ignore,
                          ignore_re=args.ignore_re,
                          errors_only=args.errors_only,
                          detect_language=args.detect_language,
                          format=args.format,
                          stack_size=args.stack_size,
                          vnu_args=extra_args)

    if args.files:
        files = args.files
    else:
        files = validator.all_files(directory=args.root,
                                    match=args.match,
                                    blacklist=args.blacklist)
    LOGGER.info('Files to validate: \n  {0}'.format('\n  '.join(files)))
    LOGGER.info('Number of files: {0}'.format(len(files)))

    error_count = validator.validate(files)
    sys.exit(min(error_count, 255))


if __name__ == "__main__":
    main()
