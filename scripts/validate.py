"""Command line tool for HTML5 validation."""

import sys
import argparse
import html5validator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default='.')
    parser.add_argument('--match', default='*.html',
                        help='file matching pattern')
    parser.add_argument('--blacklist', type=str, nargs='*',
                        help='specify a space-separated list of blacklisted ' +
                        'directory names', default=[])
    parser.add_argument('--show-warnings', dest='error_only',
                        action='store_false', default=True)
    args = parser.parse_args()

    v = html5validator.Validator(directory=args.root,
                                 match=args.match,
                                 blacklist=args.blacklist)
    sys.exit(v.validate(args.error_only))


if __name__ == "__main__":
    main()
