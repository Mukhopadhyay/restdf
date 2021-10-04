"""Tests for restdf.utils.io module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Third-party modules
import pytest

# RestDF modules
from restdf.utils import io

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
