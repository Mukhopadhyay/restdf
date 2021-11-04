================
Testing RestDF
================


Testing using Pytest
~~~~~~~~~~~~~~~~~~~~
**RestDF** tests are written using ``pytest``.

.. code:: bash

    pytest -v --cov

The available pytest ``markers`` are:

+--------------+-----------------------------------+
| **Name**     | **Description**                   |
+==============+===================================+
| ``io``       | File input-output related tests   |
+--------------+-----------------------------------+
| ``flask``    | All Flask related tests           |
+--------------+-----------------------------------+
| ``routes``   | All endpoint related tests        |
+--------------+-----------------------------------+
| ``utils``    | Testing all utility scripts       |
+--------------+-----------------------------------+