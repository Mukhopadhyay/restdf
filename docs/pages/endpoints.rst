===================
Available Endpoints
===================

The responses from ``RestDF`` can be categorized into three following types:
  - ``Docs``
  - ``Metadata``
  - ``Data``

Docs
~~~~
These endpoints provides some documentation on the API. Following are the available documentation related endpoints.

+--------------+----------------+--------------------------------------------------------+
| **Method**   | **Endpoint**   | **Description**                                        |
+==============+================+========================================================+
| ``GET``      | ``/``          | Index route, gives brief intro about the API           |
+--------------+----------------+--------------------------------------------------------+
| ``GET``      | ``/docs``      | ``SwaggerUI``                                          |
+--------------+----------------+--------------------------------------------------------+
| ``GET``      | ``/stats``     | Provides basic Stats about the currently running API   |
+--------------+----------------+--------------------------------------------------------+

Index route (``/``)
*******************

Index route, gives brief intro about the API.

**Type:** ``GET``

``/`` Example Response
^^^^^^^^^^^^^^^^^^^^^^
.. code:: javascript

    {
      "endpoints": [
        {
          "method": "get",
          "name": "/",
          "summary": "Index route, gives brief intro about the API"
        },
        {
          "method": "get",
          "name": "/stats",
          "summary": "Provides basic Stats about the currently running API"
        },
        {
          "method": "get",
          "name": "/columns",
          "summary": "Get the dataframe columns"
        }
      ],
      "filename": "dataset.csv"
    }

``SwaggerUI`` (``/docs``)
*******************************

SwaggerUI endpoint endpoint, which is generated using `flasgger <https://github.com/flasgger/flasgger>`__. The OpenAPI definitions are generated
in form of a dictionary in runtime, to make some attributes such as ``column_name`` dynamic Enums. 

**Type:** ``GET``

Device/Server Statistics endpoint (``/stats``)
**********************************************

Provides basic Stats about the currently running API. Returns details such as

**Type:** ``GET``

* Device stats (available, free, used, total memory of the device)
* Python version
* Runtime informations (# Requests, filename, running_since, runtime_duration)
* Server Framework info (Frameword being used & its version)

``/stats`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: javascript

    {
      "Device": {
        "Memory": {
          "available": 3022258176,
          "free": 3022258176
        },
        "cpu_percent": 23.5
      },
      "Python": {
        "version": "3.8.7 (tags/v3.8.7:6503f05, Dec 21 2020, 17:59:51) [MSC v.1928 64 bit (AMD64)]"
      },
      "Runtime": {
        "API": {
          "/values_requests": 0
        },
        "filename": "test.csv",
        "running_since": "2021-11-05 05:20:27.363299",
        "runtime_duration": 818.451938867569
      },
      "Server": {
        "name": "Flask",
        "version": "2.0.2"
      }
    }



Metadata
~~~~~~~~
As the name suggests, these provide some information about the dataset itself.

+--------------+-----------------------------------+---------------------------------------------------------------+
| **Method**   | **Endpoint**                      | **Description**                                               |
+==============+===================================+===============================================================+
| ``GET``      | ``/columns``                      | Get the dataframe columns                                     |
+--------------+-----------------------------------+---------------------------------------------------------------+
| ``POST``     | ``/describe``                     | Describes different properties of the dataframe               |
+--------------+-----------------------------------+---------------------------------------------------------------+
| ``GET``      | ``/dtypes``                       | Returns the datatype of all columns                           |
+--------------+-----------------------------------+---------------------------------------------------------------+
| ``GET``      | ``/info``                         | Returns some dataframe info (Datatype, Non-null counts etc)   |
+--------------+-----------------------------------+---------------------------------------------------------------+
| ``GET``      | ``/nulls``                        | Returns the count of nulls in the dataframe                   |
+--------------+-----------------------------------+---------------------------------------------------------------+
| ``GET``      | ``/value_counts/{column_name}``   | Returns the value\_count results of a column                  |
+--------------+-----------------------------------+---------------------------------------------------------------+

Columns endpoint (``/columns``)
*******************************

Returns the columns available in the dataframe.

**Type:** ``GET``

``/columns`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

    {
      "columns": [
        "column1",
        "column2",
        "column3"
      ]
    }

Dataset description endpoint (``/describe``)
********************************************

Returns some dataframe info (Datatype, Non-null counts etc). This endpoint 
returns the response from ``df.describe()`` and returns the result.

**Type:** ``POST``

``/describe`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^
The following request body is the usual arguments for ``df.describe()``. For more detailed info about the 
meaning of the arguments please refer to this documentation from `pandas <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.describe.html>`__
official documentation.

.. code:: javascript

  {
    "datetime_is_numeric": false,
    "exclude": [
      "O"
    ],
    "include": [
      "int"
    ],
    "percentiles": [
      0.01,
      0.25,
      0.75,
      0.99
    ]
  }

``/describe`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "description": {
      "Parch": {
        "1%": 0,
        "25%": 0,
        "50%": 0,
        "75%": 0,
        "99%": 2,
        "count": 30,
        "max": 2,
        "mean": 0.3,
        "min": 0,
        "std": 0.5959634332684375
      },
      "PassengerId": {
        "1%": 927.47,
        "25%": 1037.75,
        "50%": 1102,
        "75%": 1215,
        "99%": 1280.04,
        "count": 30,
        "max": 1287,
        "mean": 1112.4666666666667,
        "min": 915,
        "std": 107.31189905206654
      }
    }
  }

Datatypes endpoint (``/dtypes``)
**********************************

Returns the datatypes of the columns. This endpoint returns the response from ``df.dtypes``
and returns the result.

**Type:** ``GET``

``/dtypes`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "dtypes": {
      "column1": "float64",
      "column2": "object",
      "column3": "int64"
    }
  }

DataFrame info endpoint (``/info``)
***********************************

Returns some dataframe info (Datatypes, Non-null counts etc). This endpoint returns the
response from ``df.info()`` and returns the result.

**Type:** ``GET``

``/info`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "info": [
      {
        "column": "column1",
        "count": 30,
        "dtype": "int64",
        "index": 0
      },
      {
        "column": "column2",
        "count": 30,
        "dtype": "int64",
        "index": 1
      },
      {
        "column": "column3",
        "count": 30,
        "dtype": "object",
        "index": 2
      }
    ]
  }

DataFrame nulls endpoint (``/nulls``)
*************************************

Returns the counts of nulls in the dataframe. This endpoint returns the response
from ``pd.isna(df)`` aggregated by **sum**

**Type:** ``GET``

``/null`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

    {
      "nulls": {
        "column1": 7,
        "column2": 22,
        "column3": 0
      }
    }

Value Counts endpoint (``/value_counts/{column_name}``)
*******************************************************

Returns the value_count result of a column using the method
``pd.Series.value_counts()`` since, this method works on a ``pandas.Series``
we require the **column_name** on which we're performing the value_counts operation.

According to pandas `docs <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.value_counts.html>`__ on value_counts

*"The resulting object will be in descending order so that the first element is
the most frequently-occurring element. Excludes NA values by default."*

``/value_counts`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "column": "Sex",
    "value_counts": {
      "female": 16,
      "male": 14
    }
  }


Data
~~~~
These endpoints returns values from the dataset.

+--------------+----------------------------------+-----------------------------------------------------------------------------+
| **Method**   | **Endpoint**                     | **Description**                                                             |
+==============+==================================+=============================================================================+
| ``POST``     | ``/equals/{column_name}``        | Returns rows where all column values are exactly equal to the given value   |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/find_string/{column_name}``   | Returns rows where all string values contains given pattern                 |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/head``                        | Returns the head of the dataframe                                           |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/isin/{column_name}``          | Returns rows where all column values are within the array content           |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/not_equals/{column_name}``    | Returns rows where all column values are not equal to the given value       |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/notin/{column_name}``         | Returns rows where all column values are not within the array content       |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/sample/{column_name}``        | Returns random rows from the dataframe                                      |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
| ``POST``     | ``/values/{column_name}``        | Returns values for a selected column                                        |
+--------------+----------------------------------+-----------------------------------------------------------------------------+
