.. image:: https://api.travis-ci.org/Mytho/groceries-api.svg
  :target: https://travis-ci.org/Mytho/groceries-api

=============
GROCERIES API
=============

A simple RESTful API to manage your grocery list.

Development
-----------

Make sure that the `Heroku Toolbelt`_ is properly installed. Furthermore the
code needs two environment variables to be set.

- ``DATABASE_URL`` should point to the development database.
- ``JWT_SECRET`` should contain a secret string to be used as signing key.

All commands that could be used during development, can be found in the
``Makefile``.

  .. _`Heroku Toolbelt`: https://toolbelt.heroku.com/
