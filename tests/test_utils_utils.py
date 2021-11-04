"""Tests for restdf.utils.utils module"""

try:
    import context
except ModuleNotFoundError:
    import tests.context

# Third-party modules
import pytest

# RestDF modules
from restdf.utils import utils

@pytest.mark.parametrize('parameters,path,host,port,debug,email', [
    (['/tests/test_data/test.csv', '-H', '127.0.0.1', '-p', '1333', '-d', '-t', 'test', '-e', 'abc@email.com'],
     '/tests/test_data/test.csv',
     '127.0.0.1',
     1333,
     True,
     'abc@email.com'),
     (['/tests/test_data/test.csv'],
      '/tests/test_data/test.csv',
      None,
      None,
      False,
      None),
      (['test.csv', '--host', 'localhost', '--port', '1234'],
       'test.csv',
       'localhost',
       1234,
       False,
       None),
       (['test.csv',  '--port', '1234', '--email', 'test@email.com'],
       'test.csv',
       None,
       1234,
       False,
       'test@email.com'),
])
@pytest.mark.utils
def test_get_parser(parameters, path, host, port, debug, email) -> None:
    arg = utils.get_parser()
    namespace = arg.parse_args(parameters)
    # Checking the args
    assert namespace.path == path
    assert isinstance(namespace.path, str)
    assert namespace.host == host
    assert isinstance(namespace.host, type(host))
    assert namespace.port == port
    assert isinstance(namespace.port, type(port))
    assert namespace.debug == debug
    assert isinstance(namespace.debug, type(debug))
    assert namespace.email == email
    assert isinstance(namespace.email, type(email))


@pytest.mark.parametrize('params', [
    ['-d'],
    [123, '-e', 'abc@email.com']
])
@pytest.mark.utils
def test_get_parser_exceptions(params) -> None:
    with pytest.raises(SystemExit):
        arg = utils.get_parser().parse_args()
