# HTML5 Validator integration for TravisCI

> This was written with static site generators in mind.

Copy the files of this repo to your repository with static HTML5 files and get continuous integrations validation for HTML5.

You probably don't want TravisCI to run on the master branch but only on the gh-pages branch. TravisCI has an option (off by default) to only run tests on branches that have a `.travis.yml`.

This button shows the HTML5 validity of the `gh-pages` branch:
![travisci build status](https://travis-ci.org/svenkreiss/travisci_html5.svg?branch=gh-pages)
