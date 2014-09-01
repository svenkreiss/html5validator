# HTML5 Validator Integration for TravisCI

> This was written with static site generators in mind. Currently only checks the front page.

Copy the files of this repo's `gh-pages` branch to your repository with static html files and get continuous validation for HTML5. Adjust the `URL` parameter inside the `validate.py` file to your website.

You probably don't want TravisCI to run on the `master` branch but only on the `gh-pages` branch. TravisCI has an option (off by default) to only run tests on branches that have a `.travis.yml`.

This button shows the HTML5 validity of this `gh-pages` branch:
![travisci build status](https://travis-ci.org/svenkreiss/travisci_html5.svg?branch=gh-pages)


### User Pages

You can also use this for user pages (repositories of the form `<username>.github.io`) where the html files are in the master branch. You only have to remove

    branches:
      only:
        - gh-pages

from `.travis.yml`. I am using this on [my own user page](https://github.com/svenkreiss/svenkreiss.github.io/blob/master/.travis.yml).


### Technical

On the backend, this does a request to [http://html5.validator.nu/](http://html5.validator.nu/).
