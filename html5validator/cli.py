#!/usr/bin/env python
"""Command line tool for HTML5 validation. Return code is 0 for valid HTML5."""

import sys
import argparse

from .validator import Validator
from . import __version__ as VERSION


def main():
    parser = argparse.ArgumentParser(description='[v'+VERSION+'] '+__doc__,
                                     prog='html5validator')
    parser.add_argument('--root', default='.')
    parser.add_argument('--match', default='*.html',
                        help='file matching pattern')
    parser.add_argument('--blacklist', type=str, nargs='*',
                        help='specify a space-separated list of blacklisted ' +
                        'directory names', default=[])
    parser.add_argument('--show-warnings', dest='error_only',
                        action='store_false', default=True)
    parser.add_argument('--ignore', nargs='*', default=None,
                        help='Regex of message to be ignored.')
    parser.add_argument('--version', action='version',
                        version='%(prog)s '+VERSION)
    args = parser.parse_args()

    v = Validator(directory=args.root, match=args.match,
                  blacklist=args.blacklist, ignore=args.ignore)
    files = v.all_files()
    print('Found files to validate: {0}'.format(len(files)))
    sys.exit(v.validate(files, errors_only=args.error_only))


if __name__ == "__main__":
    main()
