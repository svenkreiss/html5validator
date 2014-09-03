HTML5 Validator Integration for TravisCI
========================================

    This was written with static site generators like `Jekyll <http://jekyllrb.com/>`_
    and `Pelican <http://blog.getpelican.com/>`_ in mind.

Create a ``.travis.yml`` file::

    language: python
    branches:
      only:
        - gh-pages
    python:
     - "2.7"
    install:
     - "pip install git+https://github.com/svenkreiss/html5validator.git"
    script: "html5validator"

in your repository with static html files and get HTML5 validation on every 
``git push``. Enable the repository on `TravisCI <https://travis-ci.org>`_.

You probably don't want TravisCI to run on the ``master`` branch but only on 
the ``gh-pages`` branch. TravisCI has an option (off by default) to run tests 
only on branches that have a ``.travis.yml``.

These buttons show the HTML5 validity of the `gh-pages` and `gh-pages-failing` branches:

.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=gh-pages
    :target: https://travis-ci.org/svenkreiss/html5validator)
.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=gh-pages-failing
    :target: https://travis-ci.org/svenkreiss/html5validator)


User Pages
----------

You can also use this for user pages (repositories of the form ``<username>.github.io``)
where the html files are in the master branch. You only have to remove::

    branches:
      only:
        - gh-pages

from ``.travis.yml``. I am using this on
`my own user page <https://github.com/svenkreiss/svenkreiss.github.io/blob/master/.travis.yml>`_.


pip install
-----------

To facilitate the primary use case with ``TravisCI``, this repository also contains a
Python package called ``html5validator`` which can be installed using ``pip``::

    pip install git+http://github.com/svenkreiss/html5validator.git


Technical
---------

The backend uses the same validator that powers the
`validator.nu backend <https://github.com/validator/validator.github.io>`_.

If you are using grunt already, maybe consider using the
`grunt-html <https://github.com/jzaefferer/grunt-html>`_ plugin for grunt instead or in addition.
