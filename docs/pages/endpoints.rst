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
These endpoints returns values from the dataset. Either by some condition or by
using some dataframe methods.

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

DataFrame equal values endpoint (``/equals/{column_name}``)
***********************************************************

This endpoint returns rows where all column values are exactly equal to the
given value. For the given column name, this endpoint returns the rows where
the values for that column is equal to the given ``values``.

``column_name`` is the name of the column on which we're performing the operation.

**Type:** ``POST``

``/equals`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": [],
    "index": true,
    "value": 0
  }

equals attributes
^^^^^^^^^^^^^^^^^
* ``as_string``: Converts the entire column as string first.
* ``columns``: Columns we're expecting in return.
* ``index``: Whether to include the index included in the returned objects.
* ``value``: Value to check the condition against (in this case equality).

``/equals`` Example Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": ["Age", "Name"],
    "index": true,
    "value": 18
  }

``/equals`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "values": [
      {
        "Age": 18,
        "Name": "Nilsson, Miss. Berta Olivia",
        "_index": 12
      },
      {
        "Age": 18,
        "Name": "Smith, Mrs. Lucien Philip (Mary Eloise Hughes)",
        "_index": 24
      },
      {
        "Age": 18,
        "Name": "Burns, Miss. Mary Delia",
        "_index": 25
      }
    ]
  }

Find String endpoint (``/find_string/{column_name}``)
*****************************************************

This endpoint returns rows where all string values contain given pattern. For the
given column name, this endpoint returns the rows where the values (string DataTypes) for
that column containing the given pattern. This uses the ``str.contains()`` method,
please refer to this `page <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html>`__
for more details.

**Type:** ``POST``

``/find_string`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "case": false,
    "columns": [],
    "flags": 0,
    "index": true,
    "na": true,
    "pattern": "string",
    "regex": false
  }

``find_string`` attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^
* ``case``: If ``True``, case sensitive.
* ``columns``: Columns we're expecting in return.
* ``flags``: Flags to pass through to the re module, e.g., ``re.IGNORECASE``.
* ``index``: Whether to include the index included in the returned objects.
* ``na``: Fill value for missing values. The default depends on dtype of the array. For object-dtype, ``numpy.nan`` is used.
* ``pattern``: Character sequence or regular expr.
* ``regex``: If ``True``, assumes the pattern is a regular expression, If ``False``, treats the pattern as a literal string.

``/find_string`` Example Request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "case": false,
    "columns": ["Name", "Pclass"],
    "flags": 0,
    "index": true,
    "na": true,
    "pattern": "miss.",
    "regex": false
  }

``/find_string`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "num": 9,
    "option_used": {
      "case": false,
      "flags": 0,
      "na": true,
      "pat": "miss.",
      "regex": false
    },
    "values": [
      {
        "Name": "Becker, Miss. Ruth Elizabeth",
        "Pclass": 2,
        "_index": 0
      },
      {
        "Name": "Abelseth, Miss. Karen Marie",
        "Pclass": 3,
        "_index": 2
      },
      {
        "Name": "Goodwin, Miss. Jessie Allis",
        "Pclass": 3,
        "_index": 5
      },
      {
        "Name": "Wilson, Miss. Helen Alice",
        "Pclass": 1,
        "_index": 8
      },
      {
        "Name": "Quick, Miss. Winifred Vera",
        "Pclass": 2,
        "_index": 9
      },
      {
        "Name": "Nilsson, Miss. Berta Olivia",
        "Pclass": 3,
        "_index": 12
      },
      {
        "Name": "Geiger, Miss. Amalie",
        "Pclass": 1,
        "_index": 23
      },
      {
        "Name": "Burns, Miss. Mary Delia",
        "Pclass": 3,
        "_index": 25
      },
      {
        "Name": "Lundin, Miss. Olga Elida",
        "Pclass": 3,
        "_index": 29
      }
    ]
  }

DataFrame ``head`` endpoint (``/head``)
***************************************

This endpoint returns the response from ``df.head()`` and returns the result.

**Type:** ``POST``

``/head`` Request Body
^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "columns": [],
    "index": true,
    "n": 5
  }

``head`` attributes
^^^^^^^^^^^^^^^^^^^

* ``columns``: Columns we're expecting in return.
* ``index``: Whether to include the index included in the returned objects.
* ``n``: Number of rows to return.

``/head`` Example Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "columns": [],
    "index": true,
    "n": 1
  }

``/head`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: javascript

  {
    "head": [
      {
        "Age": 12,
        "Cabin": "F4",
        "Embarked": "S",
        "Fare": 39,
        "Name": "Becker, Miss. Ruth Elizabeth",
        "Parch": 1,
        "PassengerId": 1218,
        "Pclass": 2,
        "Sex": "female",
        "SibSp": 2,
        "Ticket": "230136",
        "_index": 0
      }
    ]
  }

``isin`` Operation endpoint (``/isin/{column_name}``)
*****************************************************

For the given column name, this endpoint returns the rows where the values are
within the ``values`` array.

**Type:** ``POST``

``/isin`` Request Body
^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": [],
    "index": true,
    "values": []
  }

``isin`` attributes
^^^^^^^^^^^^^^^^^^^
* ``as_string``: Converts the entire column as string first.
* ``columns``: Columns we're expecting in return.
* ``index``: Whether to include the index included in the returned objects.
* ``values``: Values list to check the condition against (in this case isin).

``/isin`` Example Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": ["Pclass"],
    "index": true,
    "values": [1, 2]
  }

``/isin`` Example Response Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "values": [
      {
        "Pclass": 2,
        "_index": 0
      },
      {
        "Pclass": 1,
        "_index": 1
      },
      {
        "Pclass": 1,
        "_index": 3
      },
      {
        "Pclass": 1,
        "_index": 4
      }
    ]
  }


DataFrame equal values endpoint (``/not_equals/{column_name}``)
***************************************************************

This endpoint returns rows where all column values are not equals to the
given value. For the given column name, this endpoint returns the rows where
the values for that column is not equal to the given ``value``.

**Type:** ``POST``

``column_name`` is the name of the column on which we're performing the operation.

**Type:** ``POST``

``/not_equals`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": [],
    "index": true,
    "value": 0
  }

not_equals attributes
^^^^^^^^^^^^^^^^^^^^^
* ``as_string``: Converts the entire column as string first.
* ``columns``: Columns we're expecting in return.
* ``index``: Whether to include the index included in the returned objects.
* ``value``: Value to check the condition against (in this case not-equality).

``/not_equals`` Example Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": ["Age", "Name"],
    "index": true,
    "value": 18
  }

``/not_equals`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "values": [
      {
        "Age": 12.0,
        "Name": "Becker, Miss. Ruth Elizabeth",
        "_index": 0
      },
      {
        "Age": 64.0,
        "Name": "Warren, Mr. Frank Manley",
        "_index": 1
      },
      {
        "Age": 16.0,
        "Name": "Abelseth, Miss. Karen Marie",
        "_index": 2
      }
    ]
  }


``notin`` Operation endpoint (``/notin/{column_name}``)
*******************************************************

For the given column name, this endpoint returns the rows where the values are
not within the ``values`` array.

**Type:** ``POST``

``/notin`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": [],
    "index": true,
    "values": []
  }

``notin`` attributes
^^^^^^^^^^^^^^^^^^^^
* ``as_string``: Converts the entire column as string first.
* ``columns``: Columns we're expecting in return.
* ``index``: Whether to include the index included in the returned objects.
* ``values``: Values list to check the condition against (in this case notin).

``/notin`` Example Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "as_string": false,
    "columns": ["Pclass"],
    "index": true,
    "values": [1, 2]
  }

``/notin`` Example Response Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "values": [
      {
        "Pclass": 3,
        "_index": 2
      },
      {
        "Pclass": 3,
        "_index": 5
      },
      {
        "Pclass": 3,
        "_index": 10
      }
    ]
  }

DataFrame ``sample`` rows endpoint (``/sample``)
************************************************

This endpoint returns the response from ``df.sample(**kwargs)`` and returns the result.

**Type:** ``POST``

``/sample`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "columns": [],
    "frac": null,
    "index": true,
    "n": 1,
    "random_state": 0,
    "replace": false,
    "weights": null
  }

``sample`` attributes
^^^^^^^^^^^^^^^^^^^^^
* ``n``: Number of random rows to return (default: 1)
* ``frac``: Fraction of axis items to return. Cannot be used alongside **n**
* ``replace``: Allow or disallow sampling of the same row more than once. If n > (size of DataFrame) then replace must be True, else error will be thrown.
* ``weights``: [list containing probability distribution], Defaults to None, meaning equal probability weighting.
* ``random_state``: Seed for random number generator.

``/sample`` Example Request Body
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "columns": ["Age", "Name"],
    "frac": null,
    "index": false,
    "n": 1,
    "random_state": 0,
    "replace": false,
    "weights": null
  }

``/sample`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "sample": [
      {
        "Age": 16,
        "Name": "Abelseth, Miss. Karen Marie"
      }
    ]
  }


DataFrame values endpoint (``/values/{column_name}``)
*****************************************************

This method values from the passed ``column_name``, using ``pd[column_name]``. If **n**
exceeds the size of the dataframe, no warnings are given!

**Type:** ``POST``

``/values`` Request Body
^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: javascript

  {
    "add_index": true,
    "n": 5
  }

``/values`` Example Response
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: javascript

  {
    "values": {
      "0": "Becker, Miss. Ruth Elizabeth",
      "1": "Warren, Mr. Frank Manley",
      "2": "Abelseth, Miss. Karen Marie",
      "3": "Wick, Mr. George Dennick",
      "4": "Williams, Mr. Richard Norris II"
    }
  }

