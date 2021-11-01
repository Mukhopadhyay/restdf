from typing import Dict, Any

COLUMNS_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'string',
        'example': 'column1'
    },
    'default': None,
    'example': []
}

# Error Response
error_response = {
    'type': 'object',
    'properties': {
        'error': {
            'type': 'object',
            'properties': {
                'err': {
                    'type': 'string',
                    'example': "'columns' needs to be a list, got str"
                },
                'type': {
                    'type': 'string',
                    'example': 'InvalidRequestBodyError'
                },
                'module': {
                    'type': 'string',
                    'example': 'restdf.utils.exceptions'
                }
            }
        }
    }
}

# Response for / endpoint
index_response = {
    'type': 'object',
    'properties': {
        'endpoints': {
            'type': 'object',
            'example': [{'name': '/stats', 'type': ['GET']}]
        },
        'filename': {
            'type': 'string',
            'example': 'filename.csv'
        }
    }
}
# Response for /stats endpoint
stats_response = {
    'type': 'object',
    'properties': {
        'Device': {
            'type': 'object'
        },
        'Python': {
            'type': 'object'
        },
        'Runtime': {
            'type': 'object'
        },
        'Server': {
            'type': 'object'
        }
    }
}
# Response for /columns endpoint
columns_response = {
    'type': 'object',
    'properties': {
        'columns': {
            'type': 'object',
            'example': ['column1', 'column2', 'column3']
        }
    }
}
# Request Body for /describe endpoint
describe_request_body = {
    'type': 'object',
    'properties': {
        'datetime_is_numeric': {
            'type': 'boolean',
            'default': False
        },
        'exclude': {
            'type': 'object',
            'example': ['O']
        },
        'include': {
            'type': 'object',
            'example': ['int']
        },
        'percentiles': {
            'type': 'object',
            'example': [0.01, 0.25, 0.75, 0.99]
        }
    }
}
# Response for /describe endpoint
describe_response = {
    'type': 'object',
    'properties': {
        'description': {
            'type': 'object'
        }
    }
}
# Response for /dtypes endpoint
dtypes_response = {
    'type': 'object',
    'properties': {
        'dtypes': {
            'type': 'object',
            'example': {'Age': 'float64'}
        }
    }
}
# Response for /info endpoint
info_response = {
    'type': 'object',
    'properties': {
        'info': {
            'type': 'object'
        }
    }
}
# Response for /nulls endpoint
nulls_response = {
    'type': 'object',
    'properties': {
        'nulls': {
            'type': 'object'
        }
    }
}
# Response for /value_counts/{column_name} endpoint
value_counts_response = {
    'type': 'object',
    'properties': {
        'column': {
            'type': 'string',
            'example': 'column1'
        },
        'value_counts': {
            'type': 'object'
        }
    }
}
# Request Body for /equals/{column_name} endpoint
equals_request_body = {
    'type': 'object',
    'properties': {
        'as_string': {
            'type': 'boolean',
            'default': False
        },
        'columns': COLUMNS_SCHEMA,
        'index': {
            'type': 'boolean',
            'default': True
        },
        'value': {
            'type': 'object',
            'default': "",
            'example': 0
        }
    }
}
# Request body for /find_string/column_name endpoints
find_string_request_body = {
    'type': 'object',
    'properties': {
        'case': {
            'type': 'boolean',
            'default': False
        },
        'columns': COLUMNS_SCHEMA,
        'flags': {
            'type': 'integer',
            'default': 0
        },
        'index': {
            'type': 'boolean',
            'default': True
        },
        'na': {
            'type': 'boolean',
            'default': 'False'
        },
        'pattern': {
            'type': 'string',
            'default': 'miss.'
        },
        'regex': {
            'type': 'boolean',
            'default': False
        }
    }
}
# Common Response for all values endpoints
values_response = {
    'type': 'object',
    'properties': {
        'values': {
            'type': 'object',
            'example': [{'column1': 'value1', 'column2': 'value2'}]
        }
    }
}
# Response body for /find_string/{column_name} endpoints
find_string_response_body = {
    'type': 'object',
    'properties': {
        'values': {
            'type': 'object'
        },
        'num': {
            'type': 'integer'
        },
        'option_used': {
            'type': 'object'
        }
    }
}
# Request body for /head endpoints
head_request_body = {
    'type': 'object',
    'properties': {
        'columns': COLUMNS_SCHEMA,
        'index': {
            'type': 'boolean',
            'default': True,
            'example': True
        },
        'n': {
            'type': 'integer',
            'default': 5,
            'example': 5
        }
    }
}
# Response for /head endpoint
head_response = {
    'type': 'object',
    'properties': {
        'head': {
            'type': 'object',
            'example': [{'column1': 'value1', 'column2': 'value2'}]
        }
    }
}
# Request Body for /isin/{column_name} endpoint
isin_request_body = {
    'type': 'object',
    'properties': {
        'as_string': {
            'type': 'boolean',
            'default': False
        },
        'columns': COLUMNS_SCHEMA,
        'index': {
            'type': 'boolean',
            'default': True
        },
        'values': {
            'type': 'object',
            'default': [],
            'example': []
        }
    }
}
# Request Body for /not_equals/{column_name} endpoint
not_equals_request_body = {
    'type': 'object',
    'properties': {
        'as_string': {
            'type': 'boolean',
            'default': False
        },
        'columns': COLUMNS_SCHEMA,
        'index': {
            'type': 'boolean',
            'default': True
        },
        'value': {
            'type': 'object',
            'default': 0,
            'example': 0
        }
    }
}
# Request Body for /notin/{column_name} endpoint
notin_request_body = {
    'type': 'object',
    'properties': {
        'as_string': {
            'type': 'boolean',
            'default': False
        },
        'columns': COLUMNS_SCHEMA,
        'index': {
            'type': 'boolean',
            'default': True
        },
        'values': {
            'type': 'object',
            'default': [],
            'example': []
        }
    }
}

# Request Body for /sample endpoint
sample_request_body = {
    'type': 'object',
    'properties': {
        'columns': COLUMNS_SCHEMA,
        'frac': {
            'type': 'number',
            'format': 'float',
            'default': None,
            'example': None
        },
        'index': {
            'type': 'boolean',
            'default': True
        },
        'n': {
            'type': 'integer',
            'default': 1,
            'example': 1
        },
        'random_state': {
            'type': 'integer',
            'default': 1
        },
        'replace': {
            'type': 'boolean',
            'default': False
        },
        'weights': {
            'type': 'object',
            'default': None,
            'example': None
        }
    }
}
# Response for /sample endpoint
sample_response = {
    'type': 'object',
    'properties': {
        'sample': {
            'type': 'object',
            'example': [{'column1': 'value1', 'column2': 'value2'}]
        }
    }
}
# Request body for /values/{column_name} endpoint
values_request_body = {
    'type': 'object',
    'properties': {
        'add_index': {
            'type': 'boolean',
            'default': True
        },
        'n': {
            'type': 'integer',
            'default': 5,
            'example': 5
        }
    }
}

index_path_kwargs: Dict[str, Any] = {
    'summary': 'Index route, gives brief intro about the API',
    'description': "Returns each endpoint's type & description",
    'parameters': [],
    'tags': ['Docs'],
    'produces': ['application/json'],
    'responses': {'200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/IndexResponse'}}}
}
stats_path_kwargs: Dict[str, Any] = {
    'summary': 'Provides basic Stats about the currently running API',
    'description': 'Return current sys info, API hit counts etc',
    'parameters': [],
    'tags': ['Docs'],
    'produces': ['application/json'],
    'responses': {'200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/StatsResponse'}}}
}
columns_path_kwargs: Dict[str, Any] = {
    'summary': 'Get the dataframe columns',
    'description': 'Performs <code>df.columns</code> & returns the available columns in the dataframe.',
    'parameters': [],
    'tags': ['Metadata'],
    'produces': ['application/json'],
    'responses': {'200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ColumnsResponse'}}}
}
describe_path_kwargs: Dict[str, Any] = {
    'summary': 'Describes different properties of the dataframe.',
    'description': 'This endpoint returns the response from <code>df.describe()</code> & returns the result.',
    'parameters': [
        {
            'name': 'describe() kwargs',
            'in': 'body',
            'description': 'Kwargs for <code>pd.describe()</code>',
            'required': True,
            'schema': {
                '$ref': '#/definitions/DescribeRequest'
            }
        }
    ],
    'tags': ['Metadata'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/DescribeResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
dtypes_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns the datatypes of all columns',
    'description': 'This endpoint returns the response from <code>df.dtypes</code> & returns the result.',
    'parameters': [],
    'tags': ['Metadata'],
    'produces': ['application/json'],
    'responses': {'200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/DtypesResponse'}}}
}

info_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns some dataframe info (Datatypes, Non-null counts etc)',
    'description': 'This endpoint returns the response from <code>df.info()</code> & returns the result.',
    'parameters': [],
    'tags': ['Metadata'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/InfoResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
nulls_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns the count of nulls in the dataframe',
    'description': 'This endpoint returns the response from <code>pd.isna(df)</code> & returns the result aggregated by sum',
    'parameters': [],
    'tags': ['Metadata'],
    'produces': ['application/json'],
    'responses': {'200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/NullsResponse'}}}
}
value_counts_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns the value_count result of a column',
    'description': 'This endpoint returns the response from <code>pd.Series.value_counts()</code> & returns the result.',
    'parameters': [],
    'tags': ['Metadata'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ValueCountsResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
equals_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns rows where all column values are exactly equal to the given value',
    'description': 'For the given column name, this endpoint returns the rows where the values for that column is equal to <code>value</code>.',
    'parameters': [
        {
            'name': 'Equals options',
            'in': 'body',
            'description': 'Options required for getting the values.',
            'required': True,
            'schema': {
                '$ref': '#/definitions/EqualsRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ValuesResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
find_string_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns rows where all string values contains given pattern',
    'description': "For the given column name, this endpoint returns the rows where the values (string DataTypes) for that column containg the given p\
                    attern. This uses the <code>str.contains()</code> method, please refer to \
                    <a href='https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.contains.html' \
                    target='_blank'>this</a> page for more details.",
    'parameters': [
        {
            'name': 'str.contains kwargs',
            'in': 'body',
            'description': 'Keyword arguments for the method <code>str.contains()</code>',
            'required': True,
            'schema': {
                '$ref': '#/definitions/FindStringRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/FindStringResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
head_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns the head of the dataframe.',
    'description': 'This endpoint returns the response from <code>df.head()</code> & returns the result.',
    'parameters': [
        {
            'name': '# rows',
            'in': 'body',
            'description': 'Number of rows to return from the <code>DataFrame</code>',
            'required': True,
            'schema': {
                '$ref': '#/definitions/HeadRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/HeadResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
isin_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns rows where all column values are within the array content',
    'description': 'For the given column name, this endpoint returns the rows where the values are within the <code>values</code> array',
    'parameters': [
        {
            'name': 'isin options',
            'in': 'body',
            'description': 'Options required for getting the values.',
            'required': True,
            'schema': {
                '$ref': '#/definitions/IsinRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ValuesResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
not_equals_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns rows where all column values are not equal to the given value',
    'description': 'For the given column name, this endpoint returns the rows where the values for that column is not equal to <code>value</code>.',
    'parameters': [
        {
            'name': 'not equals options',
            'in': 'body',
            'description': 'Options required for checking non equality',
            'required': True,
            'schema': {
                '$ref': '#/definitions/NotEqualsRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ValuesResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
notin_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns rows where all column values are not within the array content',
    'description': 'For the given column name, this endpoint returns the rows where the values are not within the <code>values</code> array. Basically,\
                    the inverse of <code>/isin</code> endpoint.',
    'parameters': [
        {
            'name': 'not in options',
            'in': 'body',
            'description': 'Options required for checking not in values in dataframe',
            'required': True,
            'schema': {
                '$ref': '#/definitions/NotInRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ValuesResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
sample_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns random rows from the dataframe.',
    'description': 'This endpoint returns the response from <code>df.sample(**kwargs)</code> & returns the result.',
    'parameters': [
        {
            'name': 'sample kwargs',
            'in': 'body',
            'description': 'Keyword arguments for the pandas method df.sample()',
            'required': True,
            'schema': {
                '$ref': '#/definitions/SampleRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/SampleResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}
values_path_kwargs: Dict[str, Any] = {
    'summary': 'Returns values for a selected column',
    'description': 'This method returns values from the passed <code>column_name</code>, using <code>pd[column_name]</code>, \
                    If <b>n</b> exceeds the size of the dataframe, no warnings are given!',
    'parameters': [
        {
            'name': 'request_body',
            'in': 'body',
            'description': 'Request Body',
            'required': True,
            'schema': {
                '$ref': '#/definitions/ValuesRequest'
            }
        }
    ],
    'tags': ['Data'],
    'produces': ['application/json'],
    'responses': {
        '200': {'description': 'Successful response', 'schema': {'$ref': '#/definitions/ValuesResponse'}},
        '500': {'description': 'Error response', 'schema': {'$ref': '#/definitions/ErrorResponse'}}
    }
}

definitions = {
    'IndexResponse': index_response,
    'StatsResponse': stats_response,
    'ColumnsResponse': columns_response,
    'DescribeRequest': describe_request_body,
    'DescribeResponse': describe_response,
    'DtypesResponse': dtypes_response,
    'InfoResponse': info_response,
    'NullsResponse': nulls_response,
    'ValueCountsResponse': value_counts_response,
    'EqualsRequest': equals_request_body,
    'FindStringRequest': find_string_request_body,
    'FindStringResponse': find_string_response_body,
    'HeadRequest': head_request_body,
    'HeadResponse': head_response,
    'IsinRequest': isin_request_body,
    'NotEqualsRequest': not_equals_request_body,
    'NotInRequest': notin_request_body,
    'SampleRequest': sample_request_body,
    'SampleResponse': sample_response,
    'ValuesRequest': values_request_body,
    'ValuesResponse': values_response,
    'ErrorResponse': error_response
}

tags = [
    ('Docs', 'API Documentations'),
    ('Metadata', 'Dataset information'),
    ('Data', 'Data from the dataframe')
]
