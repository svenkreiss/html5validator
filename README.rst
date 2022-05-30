HTML5 Validator
===============

    ``html5validator`` is a command line tool that tests files for
    HTML5 validity. This was written with static site generators like
    `Jekyll <http://jekyllrb.com/>`_ and
    `Pelican <http://blog.getpelican.com/>`_ in mind. Dynamic html content
    (for example from JS template engines) can be crawled
    (e.g. with `localcrawl <https://github.com/svenkreiss/localcrawl>`_)
    and then validated.

.. image:: https://github.com/svenkreiss/html5validator/actions/workflows/tests.yml/badge.svg?branch=main
    :target: https://github.com/svenkreiss/html5validator/actions/workflows/tests.yml
.. image:: https://badge.fury.io/py/html5validator.svg
    :target: https://pypi.python.org/pypi/html5validator/


Install
-------

This module requires Python 3.6, 3.7, 3.8, 3.9 or 3.10 and Java 8 (``openjdk8`` or ``oraclejdk8``).
Install with ``pip install html5validator`` and run with

.. code-block:: bash

    html5validator --root _build/

to validate all html files in the ``_build`` directory.
Run ``html5validator --help`` to see the list of command line options::

    usage: html5validator [-h] [--root ROOT] [--match MATCH [MATCH ...]]
                          [--blacklist [BLACKLIST ...]] [--show-warnings]
                          [--no-langdetect] [--no-vnu-stdout] [--no-asciiquotes]
                          [--format {gnu,xml,json,text}]
                          [--ignore [IGNORE ...]] [--ignore-re [IGNORE_RE ...]]
                          [--config CONFIG] [-l] [-ll] [-lll] [--log LOG]
                          [--log-file LOG_FILE] [--version]
                          [files ...]

    [v0.4.2] Command line tool for HTML5 validation. Return code is 0 for valid
    HTML5. Arguments that are unknown to html5validator
    are passed as arguments to `vnu.jar`.

    positional arguments:
      files                 specify files to check

    optional arguments:
      -h, --help            show this help message and exit
      --root ROOT           start directory to search for files to validate
      --match MATCH [MATCH ...]
                            match file pattern in search (default: "*.html" or
                            "*.html *.css" if --also-check-css is used)
      --blacklist [BLACKLIST ...]
                            directory names to skip in search
      --show-warnings       show warnings and count them as errors
      --no-langdetect       disable language detection
      --no-vnu-stdout       do not use --stdout with vnu.jar
      --no-asciiquotes      do not use --asciiquotes with vnu.jar
      --format {gnu,xml,json,text}
                            output format
      --ignore [IGNORE ...]
                            ignore messages containing the given strings
      --ignore-re [IGNORE_RE ...]
                            regular expression of messages to ignore
      --config CONFIG       Path to a config file for options
      -l                    run on larger files: sets Java stack size to 2048k
      -ll                   run on larger files: sets Java stack size to 8192k
      -lll                  run on larger files: sets Java stack size to 32768k
      --log LOG             log level: DEBUG, INFO or WARNING (default: WARNING)
      --log-file LOG_FILE   Name for log file. If no name supplied then no log
                            file will be created
      --version             show program's version number and exit

This module uses the `validator.nu backend <https://github.com/validator/validator.github.io>`_
which is written in Java. Therefore, a Java Runtime Environment must be
available on your system. Since version 0.2, Java 8 is required.


Checking CSS/SVG
----------------

.. code-block:: bash

    html5validator --root _build/ --also-check-css

    # checking only CSS
    html5validator --root _build/ --skip-non-css

Replace ``css`` with ``svg`` for similar behavior with SVG files.


Integration with CircleCI 1.0
-----------------------------

Create a ``circle.yml`` file:

.. code-block:: yaml

    machine:
      java:
        version: openjdk8
    dependencies:
      pre:
        - sudo pip install html5validator
    test:
      override:
        - html5validator --root _build/

in your repository with static html files and get HTML5 validation on every
``git push``.


Integration with CircleCI 2.0
-----------------------------

Simplified example ``circle.yml`` file from
`pelican-jsmath <https://github.com/svenkreiss/pelican-jsmath>`_:

.. code-block:: yaml

    version: 2
    jobs:
      test-3.6:
        docker:
          - image: python:3.6-stretch
        steps:
          - run:
              name: install Java
              command: apt-get update && apt-get install -y openjdk-8-jre
          - checkout
          - run:
              name: install
              command: pip install '.[test]'
          - run:
              name: generate html
              working_directory: test/example_site
              command: pelican content -s pelicanconf.py
          - run:
              name: validate html
              command: html5validator --root test/example_site/output
    workflows:
      version: 2
      build_and_test:
        jobs:
          - test-3.6


Integration with TravisCI
-------------------------

Create a ``.travis.yml`` file. This is an example for a Python project:

.. code-block:: yaml

    language: python
    python:
     - "2.7"
    addons:
      apt:
        packages:
          - openjdk-8-jre  # install Java8 as required by vnu.jar

    branches:
      only:
        - gh-pages

    install:
     - pip install html5validator

    script: html5validator --root _build/

This is an example for Java project:

.. code-block:: yaml

    language: java
    jdk:
     - oraclejdk8  # vnu.jar requires Java 8

    branches:
      only:
        - gh-pages

    install:
     - pip install --user html5validator

    script: html5validator --root _build/


Fix the ``html5validator`` version by using
``pip install --user html5validator==<version number>``.

You can also use this for user pages (repositories of the form ``<username>.github.io``)
where the html files are in the master branch. You only have to remove:

.. code-block:: yaml

    branches:
      only:
        - gh-pages

from ``.travis.yml``. I am using this on
`my own user page <https://github.com/svenkreiss/svenkreiss.github.io/blob/master/.travis.yml>`_.


Integration with CodeShip
-------------------------

Add this lines to the ``Setup Commands``:

.. code-block:: yaml

    jdk_switcher use oraclejdk8
    pip install html5validator


This is an example for Ruby project:

.. code-block:: yaml

    rvm use 2.2.0 --install
    bundle install
    bundle update
    export RAILS_ENV=test
    jdk_switcher use oraclejdk8
    pip install html5validator

Integration with GitLab CI
--------------------------------

There is a docker image available to be used with GitLab CI or stand alone.
`Docker image <https://hub.docker.com/r/cyb3rjak3/html5validator>`_,
`Docker image repo <https://github.com/Cyb3r-Jak3/html5validator-docker>`_.

Example for html test `(Full) <https://gitlab.com/Cyb3r-Jak3/Portfolio-Website/blob/master/.gitlab-ci.yml>`_:

.. code-block:: yaml

    html_test:
      stage: html_test
      image: cyb3rjak3/html5validator:latest
      script:
        - html5validator --root public/ --also-check-css --format text

Integration with GitHub Actions
---------------------------------

There is a Github Action that can be used to check repositories. `Marketplace Link <https://github.com/marketplace/actions/html5-validator>`_.

Example action:

.. code-block:: yaml

    - name: HTML5 Validator
      uses: Cyb3r-Jak3/html5validator-action@master
      with:
        root: html/

Technical Notes
---------------

* If you are using grunt already, maybe consider using the
  `grunt-html <https://github.com/jzaefferer/grunt-html>`_ plugin for grunt instead.
* Use ``--ignore-re 'Attribute "ng-[a-z-]+" not allowed'`` with angular.js apps.
* Example with multiple ignores: ``html5validator --root tests/multiple_ignores/ --ignore-re 'Attribute "ng-[a-z-]+" not allowed' 'Start tag seen without seeing a doctype first'``


Changelog
---------

Install a particular version, for example ``0.1.14``, with ``pip install html5validator==0.1.14``.

* `main <https://github.com/svenkreiss/html5validator/compare/v0.4.2...main>`_
* `0.4.2 <https://github.com/svenkreiss/html5validator/compare/v0.4.0...v0.4.2>`_ (2022-05-29)
    * test with Python 3.10
    * vnu.jar updated to 20.6.30
    * compatibility restored with certain versions of Python (`os.errno` issue)
* `0.4.0 <https://github.com/svenkreiss/html5validator/compare/v0.3.3...v0.4.0>`_ (2021-05-03)
    * update vnu jar to 21.4.9
    * use `--stdout` and `--asciiquotes` by default for vnu.jar
    * make `--format=json` parsable
    * better log file and config file tests
    * move tests to GitHub Actions and setup auto-deploy to PyPI from GitHub releases
* `0.3.3 <https://github.com/svenkreiss/html5validator/compare/v0.3.2...v0.3.3>`_ (2019-12-07)
    * `PR#59 <https://github.com/svenkreiss/html5validator/pull/59>`_
* `0.3.2 <https://github.com/svenkreiss/html5validator/compare/v0.3.1...v0.3.2>`_ (2019-11-22)
    * update vnu jar to 18.11.5
    * better output check `PR#57 <https://github.com/svenkreiss/html5validator/pull/57>`_ by `@Cyb3r-Jak3 <https://github.com/Cyb3r-Jak3>`_
* `0.3.1 <https://github.com/svenkreiss/html5validator/compare/v0.3.0...v0.3.1>`_ (2018-06-01)
    * update vnu jar to 18.3.0
    * pass remaining command line options to ``vnu.jar``
    * allow to match multiple file patterns, e.g. ``--match *.html *.css``
* `0.3.0 <https://github.com/svenkreiss/html5validator/compare/v0.2.8...v0.3.0>`_ (2018-01-21)
    * update vnu jar to 17.11.1
    * support explicit list of files: ``html5validator file1.html file2.html``
    * new command line options: ``--no-langdetect``, ``--format``
    * new tests for ``--show-warnings`` flag
    * refactored internal API
    * bugfix: check existence of Java
    * bugfix: split Java and vnu.jar command line options
* `0.2.8 <https://github.com/svenkreiss/html5validator/compare/v0.2.7...v0.2.8>`_ (2017-09-08)
    * update vnu jar to 17.9.0
    * suppress a warning from the JDK about picked up environment variables
* `0.2.7 <https://github.com/svenkreiss/html5validator/compare/v0.2.5...v0.2.7>`_ (2017-04-09)
    * update vnu jar to 17.3.0
    * lint Python code
* `0.2.5 <https://github.com/svenkreiss/html5validator/compare/v0.2.4...v0.2.5>`_ (2016-07-30)
    * clamp CLI return value at 255: `PR26 <https://github.com/svenkreiss/html5validator/pull/26>`_
* `0.2.4 <https://github.com/svenkreiss/html5validator/compare/v0.2.3...v0.2.4>`_ (2016-07-14)
    * a fix for Cygwin thanks to this `PR20 <https://github.com/svenkreiss/html5validator/pull/20>`_
* `0.2.3 <https://github.com/svenkreiss/html5validator/compare/v0.2.2...v0.2.3>`_ (2016-07-05)
    * ``vnu.jar`` updated to 16.6.29 thanks to this `PR <https://github.com/svenkreiss/html5validator/pull/19>`_
* `0.2.2 <https://github.com/svenkreiss/html5validator/compare/v0.2.1...v0.2.2>`_ (2016-04-30)
    * ``vnu.jar`` updated to 16.3.3
* `0.2.1 <https://github.com/svenkreiss/html5validator/compare/v0.1.14...v0.2.1>`_ (2016-01-25)
    * ``--ignore``, ``--ignore-re``: ignore messages containing an exact pattern or
      matching a regular expression (migration from version 0.1.14: replace ``--ignore`` with ``--ignore-re``)
    * curly quotes and straight quotes can now be used interchangeably
    * change Java stack size handling (introduced the new command line options ``-l``, ``-ll`` and ``-lll``)
    * update vnu.jar to 16.1.1 (which now requires Java 8)
* `0.1.14 <https://github.com/svenkreiss/html5validator/compare/v0.1.12...v0.1.14>`_ (2015-10-09)
    * change text encoding handling
    * adding command line arguments ``--log`` and ``--version``
* `0.1.12 <https://github.com/svenkreiss/html5validator/compare/v0.1.9...v0.1.12>`_ (2015-05-07)
    * document how to specify multiple regular expressions to be ignored
    * add ``--ignore`` as command line argument. Takes a regular expression
      for warnings and errors that should be ignored.
* `0.1.9 <https://github.com/svenkreiss/html5validator/compare/v0.1.8...v0.1.9>`_ (2015-03-02)
