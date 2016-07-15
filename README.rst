HTML5 Validator
===============

    This was written with static site generators like `Jekyll <http://jekyllrb.com/>`_
    and `Pelican <http://blog.getpelican.com/>`_ in mind that push to a static
    server. ``html5validator`` is a command line executable that integrates
    well with CircleCI and TravisCI and tests all static html files for
    HTML5 validity.

.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=master
    :target: https://travis-ci.org/svenkreiss/html5validator
.. image:: https://badge.fury.io/py/html5validator.svg
    :target: https://pypi.python.org/pypi/html5validator/


Install
-------

This module requires Python 2.7, 3.4 or 3.5 and Java 8.
Install with ``pip install html5validator`` and run with

.. code-block:: bash

    html5validator --root _build/ --ignore-re 'Attribute "ng-[a-z-]+" not allowed'

to validate all html files in the ``_build`` directory and to ignore all messages
that match the regular expression ``Attribute "ng-[a-z-]+" not allowed``.
Run ``html5validator --help`` to see the list of command line options.

.. image:: https://raw.githubusercontent.com/svenkreiss/html5validator/master/cmdlinehelp.png

This module uses the `validator.nu backend <https://github.com/validator/validator.github.io>`_
which is written in Java. Therefore, a Java Runtime Environment must be
available on your system. Since version 0.2, Java 8 is required.


Integration with CircleCI
-------------------------

Create a ``circle.yml`` file:

.. code-block:: yaml

    machine:
      java:
        version: oraclejdk8
    dependencies:
      pre:
        - sudo pip install html5validator
    test:
      override:
        - html5validator --root _build/

in your repository with static html files and get HTML5 validation on every
``git push``.


Integration with TravisCI
-------------------------

Create a ``.travis.yml`` file. This is an example for a Python project:

.. code-block:: yaml

    language: python
    python:
     - "2.7"

    branches:
      only:
        - gh-pages

    # install Java 8 as required by vnu.jar
    before_install:
     - sudo apt-get update
     - sudo apt-get install oracle-java8-installer
     - sudo update-java-alternatives -s java-8-oracle

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


Technical Notes
---------------

* If you are using grunt already, maybe consider using the
  `grunt-html <https://github.com/jzaefferer/grunt-html>`_ plugin for grunt instead.
* Use ``--ignore-re 'Attribute "ng-[a-z-]+" not allowed'`` with angular.js apps.
* Example with multiple ignores: ``html5validator --root tests/multiple_ignores/ --ignore-re 'Attribute "ng-[a-z-]+" not allowed' 'Start tag seen without seeing a doctype first'``


Changelog
---------

Install a particular version, for example ``0.1.14``, with ``pip install html5validator==0.1.14``.

* `master <https://github.com/svenkreiss/html5validator/compare/v0.2.4...master>`_
* `0.2.4 <https://github.com/svenkreiss/html5validator/compare/v0.2.3...v0.2.4>`_ (2016-07-14)
    * a fix for Cygwin thanks to this `PR <https://github.com/svenkreiss/html5validator/pull/20>`_
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
