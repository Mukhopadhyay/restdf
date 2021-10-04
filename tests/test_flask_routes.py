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
    '/value_counts/<column>'
]

def get_routes_from_blueprint(blueprint: Blueprint):
    temp_app = Flask(__name__)
    temp_app.register_blueprint(blueprint)
    return [str(p) for p in temp_app.url_map.iter_rules()]

@pytest.mark.routes
@pytest.mark.flask
def test_get_flask_blueprint():
    path = 'tests/test_data/test.xlsx'
    df = pd.read_excel(path)
    blueprint = flask_routes.get_flask_blueprint(df, path)

    # Test if the return type is correct
    assert isinstance(blueprint, Blueprint)

    # Test if blueprint contains all the endpoints
    blueprint_routes: List[str] = get_routes_from_blueprint(blueprint)
    for route in routes:
        assert route in blueprint_routes

@pytest.mark.routes
@pytest.mark.flask
def test_root(flask_client):
    response = flask_client.get('/')
    response.status_code == 200

    response_dict = json.loads(response.data)

    assert response_dict['filename'] == 'test.pkl'
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
def get_columns(flask_client):
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

