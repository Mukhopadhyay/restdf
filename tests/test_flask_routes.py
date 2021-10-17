"""Tests for restdf.routes.flask_routes module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Built-in modules
import json
from typing import List

# Third-party modules
import pytest
import pandas as pd
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

def get_routes_from_blueprint(blueprint: Blueprint):
    temp_app = Flask(__name__)
    temp_app.register_blueprint(blueprint)
    return [str(p) for p in temp_app.url_map.iter_rules()]

@pytest.mark.routes
@pytest.mark.flask
def test_root(flask_client):
    response = flask_client.get('/')
    response.status_code == 200

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
    response.status_code == 200

    response_dict = json.loads(response.data)

    for attr in ['Server', 'Python', 'Runtime', 'Device']:
        assert attr in response_dict

@pytest.mark.routes
@pytest.mark.flask
def test_get_columns(flask_client):
    response = flask_client.get('/columns')
    response.status_code == 200

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
    }, 500)
])
def test_get_describe(flask_client, req_body, status_code):
    r = flask_client.post('/describe', json=req_body)
    assert r.status_code == status_code

@pytest.mark.routes
@pytest.mark.flask
def test_get_info(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_dtypes(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_value_counts(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_nulls(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_head(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_df_sample(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_column_value(flask_client):
    pass

@pytest.mark.routes
@pytest.mark.flask
def test_get_isin_values(flask_client):
    pass

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

