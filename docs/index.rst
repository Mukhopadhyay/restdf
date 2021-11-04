.. RestDF documentation master file, created by
   sphinx-quickstart on Thu Nov  4 23:30:22 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

RestDF
======

|made-with-python| |Flask|

|GitHub license| |PRs Welcome| |RTD Badge|

**RestDF** is a command line utility for running any
``pandas.DataFrame`` compatible datasets as a Rest API, with built-in
``SwaggerUI`` support.

-  Source code: https://github.com/Mukhopadhyay/restdf
-  License:
   `MIT <https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE>`__

.. toctree::
   :maxdepth: 2
   :caption: Navigation:

   pages/endpoints
   pages/tests
   pages/command-line-arguments

Running ``RestDF``
~~~~~~~~~~~~~~~~~~

``RestDF`` can be run like any other python module using the ``-m``
flag, additional flags can be used to configure the server. Following
will start a server with
`this <https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv>`__
dataset on `localhost:5000/docs <http://localhost:5000/docs>`__

.. code:: bash

    python -m restdf https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv



.. |made-with-python| image:: https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=appveyor
   :target: https://www.python.org/
.. |Flask| image:: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
   :target: https://flask.palletsprojects.com/en/2.0.x/
.. |GitHub license| image:: https://img.shields.io/badge/license-MIT-brightgreen?style=flat-square
   :target: https://github.com/Mukhopadhyay/restdf/blob/master/LICENSE
.. |PRs Welcome| image:: https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square
   :target: http://makeapullrequest.com
.. |RTD Badge| image:: https://readthedocs.org/projects/restdf/badge/?version=latest
   :target: https://restdf.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Indices and tables
==================

* :ref:`search`
