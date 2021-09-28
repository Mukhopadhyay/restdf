"""Tests for restdf.utils.io module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Built-in modules
import os

# Third-party modules
import pytest

# RestDF modules
from restdf.utils import io
from restdf.utils import exceptions

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

@pytest.mark.io
def test_get_extension(extension_paths):
    for path in extension_paths:
        assert io.get_extension(path[0]) == path[1]

@pytest.mark.io
def test_get_extension_exception():
    with pytest.raises(TypeError) as _:
        io.get_extension(1)
    assert isinstance(io.get_extension('file.ext'), str)

@pytest.mark.io
def test_read_dataframe_success(df_read_paths):
    for path, first_val in df_read_paths:
        df = io.read_dataframe(path)
        assert df.shape[0] == 30
        assert df.PassengerId.iloc[0] == first_val

@pytest.mark.io
def test_read_dataframe_exceptions(df_read_exceptions):
    for path, exception_obj in df_read_exceptions:
        with pytest.raises(exception_obj) as _:
            x = io.read_dataframe(path)
            print('received:', x)
