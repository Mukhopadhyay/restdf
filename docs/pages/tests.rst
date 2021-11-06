================
Testing RestDF
================


Testing using pytest
~~~~~~~~~~~~~~~~~~~~
**RestDF** tests are written using ``pytest``.

.. code:: bash

    pytest -v --cov

The available pytest ``markers`` are:

+--------------+---------------------------------------------------------------------+
| **Name**     | **Description**                                                     |
+==============+=====================================================================+
| ``io``       | File input-output related tests, mainly the ``utils/io.py`` script  |
+--------------+---------------------------------------------------------------------+
| ``flask``    | All Flask related tests (``routes/flask_routes.py`` script.)        |
+--------------+---------------------------------------------------------------------+
| ``routes``   | All endpoint related tests (``routes/flask_routes.py`` script.)     |
+--------------+---------------------------------------------------------------------+
| ``utils``    | Testing all utility scripts (``routes/utils.py`` script.)           |
+--------------+---------------------------------------------------------------------+

mypy
~~~~
For static typing we're using ``mypy``.

.. code:: bash

    mypy restdf

The configs for **mypy** can be found at ``pyproject.toml``.

flake8
~~~~~~
Code style checking is handled via ``flake8``

.. code:: bash

    flake8 restdf

The config for **flake8** are kept at ``setup.cfg``.

tox
~~~
For testing ``RestDF`` on different python versions we're using ``tox``. The
configuration for it is available in ``tox.ini``

.. code:: bash

    tox

Apart from the unittests, tox tests for code style and static typing using
flake8 & mypy respectively.