"""Tests for restdf.routes.flask_routes module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Built-in modules
import json
from typing import List, Dict, Any

# Third-party modules
import pytest
from flask import Blueprint, Flask

# RestDF modules
from restdf.routes import flask_routes

routes = [
    '/',
    '/stats',
    '/columns',
    '/describe',
    '/info',
    '/dtypes',
    '/value_counts/<column_name>',
    '/nulls',
    '/head',
    '/sample',
    '/values/<column_name>',
    '/isin/<column_name>',
    '/notin/<column_name>',
    '/equals/<column_name>',
    '/not_equals/<column_name>',
    '/find_string/<column_name>'
]

# Test dataframe columns
COLUMNS = ['Age', 'Cabin', 'Embarked', 
           'Fare', 'Name', 'Parch', 
           'PassengerId', 'Pclass', 
           'Sex', 'SibSp', 'Ticket']

def get_routes_from_blueprint(blueprint: Blueprint):
    temp_app = Flask(__name__)
    temp_app.register_blueprint(blueprint)
    return [str(p) for p in temp_app.url_map.iter_rules()]

@pytest.mark.routes
@pytest.mark.flask
def test_root(flask_client):
    response = flask_client.get('/')
    assert response.status_code == 200

    response_dict = json.loads(response.data)

    assert response_dict['filename'] == 'test.csv'
    assert 'endpoints' in response_dict

    resp_endp = [_['name'] for _ in response_dict['endpoints']]
    for route in routes:
        assert route in resp_endp

@pytest.mark.routes
@pytest.mark.flask
def test_get_stats(flask_client):
    response = flask_client.get('/stats')
    assert response.status_code == 200

    response_dict = json.loads(response.data)

    for attr in ['Server', 'Python', 'Runtime', 'Device']:
        assert attr in response_dict

@pytest.mark.routes
@pytest.mark.flask
def test_get_columns(flask_client):
    response = flask_client.get('/columns')
    assert response.status_code == 200

    response_dict = json.loads(response.data)

    columns = [
        "PassengerId",
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
        "Cabin",
        "Embarked"
    ]
    for column in columns:
        assert column in response_dict['columns']

@pytest.mark.routes
@pytest.mark.flask
@pytest.mark.parametrize('req_body,status_code', [
    ({}, 200),
    ({
        'datetime_is_numeric': True,
        'include': ["int"],
        'percentiles': [0.01, 0.25, 0.75, 0.99]
    }, 200),
    ({
        'include': 'all'
    }, 200),
    ({
        'percentiles': 'asd'
    }, 500),
    ({
        'include': 'wrong'
    }, 500),
    ({
        'wrong': 'option'
    }, 200)
])
def test_get_describe_codes(flask_client, req_body, status_code):
    r = flask_client.post('/describe', json=req_body)
    assert r.status_code == status_code

@pytest.mark.routes
@pytest.mark.flask
def test_get_describe_response(flask_client):
    # Checking percentiles
    r = flask_client.post('/describe', json={'percentiles': [0.01, 0.25, 0.75, 0.99]})
    resp = json.loads(r.data)
    assert 'description' in resp
    for key in ['1%', '25%', '50%', '75%', '99%']:
        assert key in resp['description']['Parch'].keys()

    # Checking includes 'all'
    r = flask_client.post('/describe', json={'include': 'all'})
    resp = json.loads(r.data)
    for col in COLUMNS:
        assert col in resp['description']

@pytest.mark.routes
@pytest.mark.flask
def test_get_dtypes(flask_client):
    # Checking the response
    r = flask_client.get('/dtypes')
    resp = json.loads(r.data)
    assert r.status_code == 200
    assert 'dtypes' in resp
    for col in COLUMNS:
        assert col in resp['dtypes']

    # Checking for wrong method
    assert flask_client.post('/dtypes').status_code == 405

@pytest.mark.routes
@pytest.mark.flask
def test_get_info(flask_client):
    # Checking the response
    r = flask_client.get('/info')
    resp = json.loads(r.data)
    assert r.status_code == 200
    assert 'info' in resp
    assert 'shape' in resp
    response_cols = [x['column'] for x in resp['info']]
    for column in COLUMNS:
        assert column in response_cols

    # Checking for wrong method
    assert flask_client.post('/info').status_code == 405

@pytest.mark.routes
@pytest.mark.flask
@pytest.mark.parametrize('column_name,status_code,attrs',[
    ('Age', 200, ['value_counts', 'column']),
    ('Pclass', 200, ['value_counts', 'column']),
    ('_', 500, ['error']),
    ('WRONG', 500, ['error'])
])
def test_get_value_counts(flask_client, column_name: str, status_code: int, attrs):
    # Checking the response
    r = flask_client.get(f'/value_counts/{column_name}')
    resp = json.loads(r.data)
    assert r.status_code == status_code
    for attr in attrs:
        assert attr in resp


@pytest.mark.routes
@pytest.mark.flask
def test_get_nulls(flask_client):
    # Checking the response
    r = flask_client.get('/nulls')
    resp = json.loads(r.data)
    assert r.status_code == 200
    assert 'nulls' in resp


@pytest.mark.routes
@pytest.mark.flask
@pytest.mark.parametrize('req_body,status_code,root_attr,column_names,size', [
    ({}, 200, 'head', COLUMNS, 5),
    ({'index': True}, 200, 'head', COLUMNS+['_index'], 5),
    ({'columns': ['Name'], 'index':False}, 200, 'head', ['Name'], 5),
    ({'n': 10}, 200, 'head', COLUMNS, 10),
    ({'n': 'all'}, 200, 'head', COLUMNS, 30),
    ({'n': '123'}, 500, 'error', [], -1),
    ({'columns': "wrong"}, 500, 'error', [], -1),
    ({'index': 'TRUE', 'n': 20}, 200, 'head', COLUMNS+['_index'], 20)
])
def test_get_head(flask_client,
                  req_body: Dict[str, Any], 
                  status_code: int,
                  root_attr: str,
                  column_names: List[str],
                  size: int):

    r = flask_client.post('/head', json=req_body)
    assert r.status_code == status_code                 # Check status code
    resp = json.loads(r.data)
    assert root_attr in resp                            # Check the root attribute
    if root_attr != 'error':
        response_attrs = list(resp[root_attr][0].keys())
        assert len(resp[root_attr]) == size             # Check the size of response
        for column in column_names:
            assert column in response_attrs             # Check the response attributes


@pytest.mark.routes
@pytest.mark.flask
@pytest.mark.parametrize('req_body,status_code,root_attr,column_names,size', [
    ({}, 200, 'sample', COLUMNS, 1),
    ({'n': 5}, 200, 'sample', COLUMNS, 5),
    ({'n': 31}, 500, 'error', COLUMNS, -1),
    ({'n': 31, 'replace': True}, 200, 'sample', COLUMNS, 31),
    ({'index': True}, 200, 'sample', COLUMNS+['_index'], 1),
    ({'frac': 0.5, 'n': 5}, 500, 'error', COLUMNS, -1),
    ({'frac': 0.5}, 200, 'sample', COLUMNS, 15)
])
def test_get_df_sample(flask_client,
                       req_body: Dict[str, Any],
                       status_code: int,
                       root_attr: str,
                       column_names: List[str],
                       size: int):

    r = flask_client.post('/sample', json=req_body)
    assert r.status_code == status_code
    resp = json.loads(r.data)
    assert root_attr in resp
    if root_attr != 'error':
        response_attrs = list(resp[root_attr][0].keys())
        assert len(resp[root_attr]) == size
        for column in column_names:
            assert column in response_attrs


@pytest.mark.routes
@pytest.mark.flask
@pytest.mark.parametrize('req_body,code,root_attr,column,dtype,size', [
    ({}, 200, 'values', 'Name', str, 30),
    ({'n': 5}, 200, 'values', 'Name', str, 5),
    ({'n': 31}, 200, 'values', 'Pclass', int, 30),
    ({'n': 'wrong'}, 500, 'error', 'Cabin', str, -1),
    ({}, 500, 'error', 'WRONG', None, -1),
    ({'n': 0}, 200, 'values', 'Name', None, 0)
])
def test_get_column_value(flask_client,
                          req_body: Dict[str, Any],
                          code: int,
                          root_attr: str,
                          column: List[str],
                          dtype: Any,
                          size: int):

    r = flask_client.post(f'/values/{column}', json=req_body)
    assert r.status_code == code
    resp = json.loads(r.data)
    assert root_attr in resp
    if root_attr != 'error':
        assert len(resp[root_attr]) == size
        if len(resp[root_attr]):
            assert isinstance(resp[root_attr][0], dtype)


@pytest.mark.routes
@pytest.mark.flask
@pytest.mark.parametrize('req,code,column,values,root_attr,return_cols', [
    ({"as_string": False, "columns": None, "index": False, "values": [1, 2]}, 200, 'Pclass', [1, 2], 'values', COLUMNS),

    ({"as_string": False, "columns": None, "index": True, "values": [1, 2]}, 200, 'Pclass', [1, 2], 'values', COLUMNS+['_index']),
    
    ({}, 200, 'Pclass', [1, 2], 'values', COLUMNS),

    ({"columns": ["Name", "Pclass"], "values": [1, 2]}, 200, 'Pclass', [1, 2], 'values', ['Name', 'Pclass']),
    
    ({"columns": ["Name"], "values": [
        'Malachard, Mr. Noel',
        'Geiger, Miss. Amalie'
    ]}, 200, 'Name', [
        'Malachard, Mr. Noel',
        'Geiger, Miss. Amalie'
    ], 'values', ['Name']),

    ({"columns": "wrong"}, 500, 'Pclass', [], 'error', None),
    ({'as_string': True, 'values': ['39.0']}, 200, 'Fare', [39.0,], 'values', COLUMNS)
])  
def test_get_isin_values(flask_client, req, code, column, values, root_attr, return_cols):
    r = flask_client.post(f'/isin/{column}', json=req)
    assert r.status_code == code

    # Checking the root attribute
    resp = json.loads(r.data)
    assert root_attr in resp

    if root_attr != 'error' and len(resp[root_attr]):
        # Checking if the rows returned satisfies 'isin'
        for val in set([_[column] for _ in resp['values']]):
            assert val in values
        # Checking if proper columns are there
        for col in return_cols:
            assert col in resp['values'][0]


@pytest.mark.routes
@pytest.mark.flask
def test_get_notin_values(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_equal_values(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_not_equal_values(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_find_string_values(flask_client):
    pass

