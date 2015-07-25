HTML5 Validator
===============

    This was written with static site generators like `Jekyll <http://jekyllrb.com/>`_
    and `Pelican <http://blog.getpelican.com/>`_ in mind that push to a static
    server. ``html5validator`` is a command line executable that integrates
    well with CircleCI and TravisCI and tests all static html files for
    HTML5 validity.

.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=master
    :target: https://travis-ci.org/svenkreiss/html5validator
.. image:: https://img.shields.io/pypi/dm/html5validator.svg
    :target: https://pypi.python.org/pypi/html5validator/
.. image:: https://badge.fury.io/py/html5validator.svg
    :target: https://pypi.python.org/pypi/html5validator/


Install
-------

Install with ``pip install html5validator`` and run with

.. code-block:: bash

    html5validator --root _build/ --ignore "Attribute “ng-[a-z-]+” not allowed"

to validate all html files in the ``_build`` directory and to ignore all messages
that match the regular expression ``Attribute “ng-[a-z-]+” not allowed``.

This package uses the `validator.nu backend <https://github.com/validator/validator.github.io>`_
which is written in Java. Therefore, a Java Runtime Environment must be
available on your system.


Integration with CircleCI
-------------------------

Create a ``circle.yml`` file:

.. code-block:: yaml

    dependencies:
      pre:
        - sudo pip install html5validator
    test:
      override:
        - html5validator

in your repository with static html files and get HTML5 validation on every
``git push``.


Integration with TravisCI
-------------------------

Create a ``.travis.yml`` file:

.. code-block:: yaml

    language: python
    branches:
      only:
        - gh-pages
    python:
     - "2.7"
    install:
     - "pip install html5validator"
    script: "html5validator"

Enable the repository on `TravisCI <https://travis-ci.org>`_.

You probably don't want TravisCI to run on the ``master`` branch but only on
the ``gh-pages`` branch. TravisCI has an option (off by default) to run tests
only on branches that have a ``.travis.yml``.

You can also use this for user pages (repositories of the form ``<username>.github.io``)
where the html files are in the master branch. You only have to remove:

.. code-block:: yaml

    branches:
      only:
        - gh-pages

from ``.travis.yml``. I am using this on
`my own user page <https://github.com/svenkreiss/svenkreiss.github.io/blob/master/.travis.yml>`_.


Technical Notes
---------------

* If you are using grunt already, maybe consider using the
  `grunt-html <https://github.com/jzaefferer/grunt-html>`_ plugin for grunt instead.
* Use ``--ignore "Attribute “ng-[a-z-]+” not allowed"`` with angular.js apps.
* Example with multiple ignores: ``html5validator --root tests/multiple_ignores/ --ignore "Attribute “ng-[a-z-]+” not allowed" "Start tag seen without seeing a doctype first"``
* Be careful with the non-standard quotes in the error messages when constructing the expressions to ignore.


Changelog
---------

* `master <https://github.com/svenkreiss/html5validator/compare/v0.1.11...master>`_
* `0.1.12 <https://github.com/svenkreiss/html5validator/compare/v0.1.9...v0.1.12>`_ (2015-05-07)
    * document how to specify multiple regular expressions to be ignored
    * add ``--ignore`` as command line argument. Takes a regular expression
      for warnings and errors that should be ignored.
* `0.1.9 <https://github.com/svenkreiss/html5validator/compare/v0.1.8...v0.1.9>`_ (2015-03-02)
