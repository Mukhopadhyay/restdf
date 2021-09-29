"""Tests for restdf.routes.flask_routes module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Built-in modules
from typing import List

# Third-party modules
from flask import Blueprint, Flask
import pandas as pd
import pytest

# RestDF modules
from restdf.routes import flask_routes

routes = [
    '/',
    '/stats'
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
