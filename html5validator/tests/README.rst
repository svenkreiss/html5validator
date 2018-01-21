Tests
=====

Run the tests from the main directory with::

  python setup.py test

or::

  nosetests tests

For the integration with TravisCI, this repository contains two test branches: one that is valid HTML5 (``gh-pages``) and one that is not (``gh-pages-failing``). These buttons show the HTML5 validity of the two branches:

.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=gh-pages
    :target: https://travis-ci.org/svenkreiss/html5validator)
.. image:: https://travis-ci.org/svenkreiss/html5validator.svg?branch=gh-pages-failing
    :target: https://travis-ci.org/svenkreiss/html5validator)
