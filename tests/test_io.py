"""Tests for restdf.utils.io module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Third-party imports
import pytest

# RestDF imports
from restdf.utils import io
from restdf.utils import exceptions

@pytest.fixture
def paths():
    return [
        ('~/Downloads/data.zip', 'zip'),
        ('~/data.rar', 'rar'),
        (r'C:\Users\Name\Desktop\something.txt', 'txt'),
        ('~/Downloads/', ''),
        ('./../', '')
    ]

@pytest.mark.io
def test_get_extension(paths):
    for path in paths:
        assert io.get_extension(path[0]) == path[1]

@pytest.mark.io
def test_get_extension_exception():
    with pytest.raises(exceptions.PathError) as path_err:
        io.get_extension(1)
    assert isinstance(io.get_extension('file.ext'), str)