.. image:: https://api.travis-ci.org/tzengerink/groceries-api.svg
  :target: https://travis-ci.org/tzengerink/groceries-api

.. image:: https://coveralls.io/repos/github/tzengerink/groceries-api/badge.svg?branch=master
  :target: https://coveralls.io/github/tzengerink/groceries-api?branch=master

=============
GROCERIES API
=============

A simple RESTful API to manage your grocery list.

Installation
------------

To install the dependencies run::

  pip install -e .

Make sure that the `Heroku Toolbelt`_ is properly installed. Furthermore the
code needs two environment variables to be set.

- ``DATABASE_URL`` should point to the development database.
- ``JWT_SECRET`` should contain a secret string to be used as signing key.

Development
-----------

To install all development dependencies run::

  pip install -e ".[dev]"

Other commands that could be useful during development, can be found in the
``Makefile``.

  .. _`Heroku Toolbelt`: https://toolbelt.heroku.com/
