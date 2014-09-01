"""Validates HTML5 files."""

import sys
import requests


URL = "http://www.svenkreiss.com/travisci_html5/"


def main():
    r = requests.get('http://html5.validator.nu/', params={'doc': URL})
    if 'The document is valid HTML5' in r.text:
        # success. all good.
        return

    # there were problems. here is the output:
    print r.text
    sys.exit(-1)


if __name__ == "__main__":
    main()
