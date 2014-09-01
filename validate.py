"""Validates HTML5 pages.

     Authors: Sven Kreiss and contributors
     License: MIT
Project page: http://github.com/svenkreiss/travisci_html5/

"""

__version__ = "0.0.2"

import sys
import requests


# Change to your username and project of the form
# http://<username>.github.io/<project>/
URL = 'http://svenkreiss.github.io/travisci_html5/'


def main():
    r = requests.get('http://html5.validator.nu/', params={'doc': URL})
    if 'The document is valid HTML5' in r.text:
        # success. all good.
        return

    # there were problems. here is the output:
    print r.text
    sys.exit(1)


if __name__ == "__main__":
    main()
