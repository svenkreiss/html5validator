HTML5 Validator
===============

    This was written with static site generators like `Jekyll <http://jekyllrb.com/>`_
    and `Pelican <http://blog.getpelican.com/>`_ in mind that push to a static
    server. `html5validator` is a command line executable that integrates
    well with CircleCI and TravisCI and tests all static html files for
    HTML5 validity.

.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=master
    :target: https://travis-ci.org/svenkreiss/html5validator
.. image:: https://pypip.in/d/html5validator/badge.svg
    :target: https://pypi.python.org/pypi/html5validator/
.. image:: https://pypip.in/v/html5validator/badge.svg
    :target: https://pypi.python.org/pypi/html5validator/


Integration with CircleCI
-------------------------

Create a ``circle.yml`` file:

.. code-block:: yml

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

.. code-block:: yml

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

.. code-block:: yml

    branches:
      only:
        - gh-pages

from ``.travis.yml``. I am using this on
`my own user page <https://github.com/svenkreiss/svenkreiss.github.io/blob/master/.travis.yml>`_.


pip install
-----------

To facilitate the primary use case with ``TravisCI``, this repository also contains a
Python package called ``html5validator`` which can be installed using ``pip``:

.. code-block:: bash

    pip install html5validator

This package uses the `validator.nu backend <https://github.com/validator/validator.github.io>`_
which is written in Java. Therefore, a Java Runtime Environment must be
available on your system.


Technical
---------

The backend uses the same validator that powers the
`validator.nu backend <https://github.com/validator/validator.github.io>`_.

If you are using grunt already, maybe consider using the
`grunt-html <https://github.com/jzaefferer/grunt-html>`_ plugin for grunt instead.
