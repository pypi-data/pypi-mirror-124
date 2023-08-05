Documentation
=============

|Documentation Status| |PyPI Status| |CI Test| |Coverage|

Introduction
------------

Simple package/script to setup ``JSON`` logging for a Python app or script.
Uses `python-json-logger <https://github.com/madzak/python-json-logger>`__ and
is mostly just a wrapper around it. Instead of adding this script to every
Python module that I/you create you can just add this as a dependency and call:

.. code:: python

   from nialog.logger import setup_module_logging

   # Default logging level is WARNING
   setup_module_logging()

Running tests
-------------

To run pytest in currently installed environment:

.. code:: bash

   poetry run pytest

To run test suite best suited for before pushing to e.g. GitHub.

.. code:: bash

   poetry run invoke prepush

To run full extensive test suite:

.. code:: bash

   poetry run invoke test

Formatting and linting
----------------------

Formatting and linting is done with a single command. First formats,
then lints.

.. code:: bash

   poetry run invoke format-and-lint

Building docs
-------------

Docs can be built locally to test that ``ReadTheDocs`` can also build them:

.. code:: bash

   poetry run invoke docs

Invoke usage
------------

To list all available commands from ``tasks.py``:

.. code:: bash

   poetry run invoke --list

Development
~~~~~~~~~~~

Development dependencies include:

   -  invoke
   -  nox
   -  copier
   -  pytest
   -  coverage
   -  sphinx

Big thanks to all maintainers of the above packages!

License
~~~~~~~

Copyright © 2021, Nikolas Ovaskainen.


.. |Documentation Status| image:: https://readthedocs.org/projects/nialog/badge/?version=latest
   :target: https://nialog.readthedocs.io/en/latest/?badge=latest
.. |PyPI Status| image:: https://img.shields.io/pypi/v/nialog.svg
   :target: https://pypi.python.org/pypi/nialog
.. |CI Test| image:: https://github.com/nialov/nialog/workflows/test-and-publish/badge.svg
   :target: https://github.com/nialov/nialog/actions/workflows/test-and-publish.yaml?query=branch%3Amaster
.. |Coverage| image:: https://raw.githubusercontent.com/nialov/nialog/master/docs_src/imgs/coverage.svg
   :target: https://github.com/nialov/nialog/blob/master/docs_src/imgs/coverage.svg
