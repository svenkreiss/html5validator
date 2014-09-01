# HTML5 Validator Integration for TravisCI

> This was written with static site generators in mind.

Create a `.travis.yml` file

    language: python
    branches:
      only:
        - gh-pages
    python:
     - "2.7"
    install:
     - "pip install git+https://github.com/svenkreiss/html5validator.git"
    script: "html5validator"

in your repository with static html files and get HTML5 validation on every `git push`. Enable the repository on [TravisCI](https://travis-ci.org).

You probably don't want TravisCI to run on the `master` branch but only on the `gh-pages` branch. TravisCI has an option (off by default) to run tests only on branches that have a `.travis.yml`.

This button shows the HTML5 validity of this `gh-pages` branch:
![travisci build status](https://travis-ci.org/svenkreiss/html5validator.svg?branch=gh-pages)<br />
And this one shows the validity of the `gh-pages-failing` branch:
![travisci build status](https://travis-ci.org/svenkreiss/html5validator.svg?branch=gh-pages-failing)


### User Pages

You can also use this for user pages (repositories of the form `<username>.github.io`) where the html files are in the master branch. You only have to remove

    branches:
      only:
        - gh-pages

from `.travis.yml`. I am using this on [my own user page](https://github.com/svenkreiss/svenkreiss.github.io/blob/master/.travis.yml).


### Technical

The backend uses the same validator that powers the [validator.nu backend](https://github.com/validator/validator.github.io).

If you are using grunt already, maybe consider using the [grunt-html](https://github.com/jzaefferer/grunt-html) plugin for grunt instead or in addition.
