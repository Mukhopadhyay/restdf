try:
    import context
except ModuleNotFoundError:
    import tests.context

import pytest
from flask import Flask

from restdf.utils import io
from restdf.utils import exceptions
from restdf.routes.flask_routes import get_flask_app

@pytest.fixture
def extension_paths():
    return [
        ('~/Downloads/data.zip', 'zip'),
        ('~/data.rar', 'rar'),
        (r'C:\Users\Name\Desktop\something.txt', 'txt'),
        ('~/Downloads/', ''),
        ('./../', '')
    ]

@pytest.fixture
def df_read_paths():
    return [
        ('tests/test_data/test.csv',  1218),
        ('tests/test_data/test.xlsx', 1149),
        ('tests/test_data/test.pkl',   936)
    ]

@pytest.fixture
def df_read_exceptions():
    return [
        ('tests/test_data/test',    exceptions.PathError),
        ('tests/context.py',        exceptions.UnknownFileTypeError),
        ('tests/test_data/int.pkl', exceptions.DataFrameError)
    ]

@pytest.fixture
def flask_client():
    df = io.read_from_csv('tests/test_data/test.csv')

    app = get_flask_app(df, 'test.csv')
    
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client

