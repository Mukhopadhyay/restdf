======================
Command line arguments
======================

Starting a API server from an existing dataset using ``RestDF`` is as simple as

.. code:: bash

    python restdf -m path/to/file.csv

However we have following additional flags that can be used to somewhat configure the API server.
Additional configuration options will be added to the project shortly!

+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+
| **Flag**              | **Expected Dtype**   | **Description**                                                                                       | **example**                              |
+=======================+======================+=======================================================================================================+==========================================+
|                       | ``str``              | Path to the dataset                                                                                   | ``restdf ./path/to/dataset.csv``         |
+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+
| ``-H``, ``--host``    | ``str``              | **Host** for the Flask server                                                                         | ``restdf data.csv -H 0.0.0.0``           |
+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+
| ``-p``, ``--port``    | ``int``              | **Port** on which to run the server                                                                   | ``restdf data.csv -p 8080``              |
+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+
| ``-d``, ``-debug``    | ``bool``             | Whether to run the server on `debug <https://flask.palletsprojects.com/en/2.0.x/debugging/>`__ mode   | ``restdf data.csv -d``                   |
+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+
| ``-t``, ``--title``   | ``str``              | Name of the API on ``SwaggerUI``                                                                      | ``restdf data.csv -t "Test API"``        |
+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+
| ``-e``, ``--email``   | ``str``              | Developer email on ``SwaggerUI``                                                                      | ``restdf data.csv -e email@email.com``   |
+-----------------------+----------------------+-------------------------------------------------------------------------------------------------------+------------------------------------------+

Using all of these options our command to start the server would look something like this

.. code:: bash

    python -m restdf https://raw.githubusercontent.com/cs109/2014_data/master/diamonds.csv --host 0.0.0.0 --port 5555 -d -t "Diamonds Dataset" -e "username@email.com"

this would run start the server on the port number ``5555``.