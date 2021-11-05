# Built-ins
import sys
from typing import List, Union, Tuple, Dict, Any, Mapping
# Third-party modules
import psutil
import pandas as pd
# RestDF modules
from . import exceptions
from ..routes.flask_schemas import utils


def get_index(filename: str) -> Dict[str, Any]:
    """
    Generates & returns the response for the index ('/') route.

    Args:
        filename:       str:        Name of file using which on which we're running the server.

    Returns:
        Dict:                       Response for the index route containing endpoint details.
    """
    INDEX_RESPONSE = {
        'filename': filename,
        'endpoints': [
            {'name': ep,
             'method': method,
             'summary': data['summary']} for (ep, method, data) in utils.endpoints
        ]
    }
    return INDEX_RESPONSE


def get_stats(framework: str, framework_version: str, stats_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates & returns some of the information about the server. Current provides the following
    details:
        * Server    [Provides framework name and version]
        * Python    [Returns Python version]
        * Runtime   [Some of the Runtime details (# requests, running since and so on)]
        * Device    [Info for the running devices]

    Args:
        framework:          str:            Framework being used (Flask, FastAPI (later maybe))
        framework_version:  str:            Version of the framework
        stats_dict:         Dict:           Dictionary containing some runtime info.

    Returns:
        Dict:                               Response for the /stats endpoint.
    """
    vm = psutil.virtual_memory()
    stats = {
        'Server': {
            'name': framework,
            'version': framework_version,
        },
        'Python': {
            'version': sys.version,
        },
        'Runtime': {
            'filename': stats_dict.get('filename'),
            'runtime_duration': stats_dict.get('runtime_duration'),
            'running_since': stats_dict.get('running_since'),
            'API': {
                'total_requests': stats_dict.get('total_requests'),
                '/values_requests': stats_dict.get('values_requests'),
            }
        },
        'Device': {
            'cpu_percent': psutil.cpu_percent(),
            'Memory': {
                'total': vm.total,
                'available': vm.available,
                'percent': vm.percent,
                'used': vm.used,
                'free': vm.free
            }
        }
    }
    return stats


def get_dataframe_columns(df: pd.DataFrame) -> List[str]:
    """
    This method returns the columns available in the dataframe.

    Args:
        df:         pd.DataFrame:       DataFrame on which RestDF is running.

    Returns:
        List[str]:                      List containing the dataframe columns.
    """
    return list(df.columns.tolist())


def get_dataframe_descriptions(df: pd.DataFrame, **kwargs) -> Dict[str, object]:
    """
    This method takes in the dataframe and the unwrapped request body dictionary as input
    and produces the description object for the /describe endpoint. For more info on the optional arguments
    please refer to this pandas documentation:
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html

    Args:
        df:                     pd.DataFrame:       DataFrame on which RestDF is running.
        percentiles:            list:               [OPTIONAL] Percentiles to include in the describe objects, e.g., [0.01, 0.5, 0.99]
        include:                str | list:         [OPTIONAL] A white list of data types to include in the result, e.g., 'all' or, ['O']
        exclude:                list:               [OPTIONAL] A black list of data types to omit from the result.
        datetime_is_numeric:    bool:               [OPTIONAL] Whether to treat datetime dtypes as numeric.

    Returns:
        dict:                   Response object for the /describe endpoint.

    """
    try:
        describe_dict: Dict[str, Any] = df.describe(
            percentiles=kwargs.get('percentiles'),
            include=kwargs.get('include'),
            exclude=kwargs.get('exclude'),
            datetime_is_numeric=kwargs.get('datetime_is_numeric', False)
        ).to_dict()
    except Exception as err:
        raise exceptions.InvalidRequestBodyError(str(err))
    else:
        for column, column_desc in describe_dict.items():
            for stat, value in column_desc.items():
                if 'int' in str(type(value)):
                    describe_dict[column][stat] = int(value)
                elif 'float' in str(type(value)):
                    describe_dict[column][stat] = float(value)
        return describe_dict


def get_dataframe_info(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Returns the dataframe info similar to df.info().

    Args:
        df:                 pd.DataFrame:       DataFrame on which RestDF is running.


    Returns:
        list:               Returns the list containing column wise info (count, datatypes etc.)
    """
    shape = df.shape[0]
    info = [{
        'index': i,
        'column': col,
        'count': int(shape - df[col].isna().sum()),
        'dtype': str(df[col].dtype)
    } for i, col in enumerate(df.columns)]
    return info


def get_value_counts(df: pd.DataFrame, column: str) -> Dict[str, int]:
    """
    Performs and returns the value_counts() results for a given column.

    Args:
        df:                 pd.DataFrame:       DataFrame on which RestDF is running.
        column:             str:                Column on which we're performing value_counts.

    Returns:
        dict:               Returns the value_counts() results in form of a dictionary.
    """
    return dict(df[column].value_counts().to_dict())


def get_dataframe_head(df: pd.DataFrame, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Performs df.head() and returns the rows as elements of the returned list. Requires the
    request body to be passed in, from which we extract other optional arguments.

    Following attribtues are looked for in the request_body dictionary:
        * n:        Number of rows to return (default: 5)
                    n = 'all', will result in returning all the rows.
        * columns:  List of column names to return. e.g., ['column1', 'column3']
        * index:    True or False, indicating wheather to add the index alongside the row objects.

    Args:
        df:                 pd.DataFrame:       DataFrame on which RestDF is running.
        request_body:       dict:               Request Body received via the /head endpoint.

    Returns:
        list:               Returns the head() results for the /head response.
    """
    response = []

    n: Union[int, str] = request_body.get('n', 5)
    temp_df = df if n == "all" else df.head(n)

    return_cols = request_body.get('columns')
    temp_df = temp_df[return_cols] if return_cols else temp_df

    for index, row in temp_df.iterrows():
        d: Dict[str, Any] = dict(row.to_dict())
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)
    return response


def get_dataframe_sample(df: pd.DataFrame, request_body: Dict[str, Any]) -> List[Mapping[str, Any]]:
    """
    This method returns n random rows as using the df.sample() method. For more detailed
    documentation on sample please refer to following link from pandas:
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html

    Following attributes are looked for in the request_body dictionary:
        * n:                Number of random rows to return (default: 1)
        * frac:             Fraction of axis items to return. Cannot be used alongside 'n'
        * replace:          Allow or disallow sampling of the same row more than once.
                            If n > (size of DataFrame) then replace must be True, else error will be thrown
        * weights:          [list containing prob dist], Defaults to None, meaning equal probability weighting.
        * random_state:     Seed for random number generator.

    Args:
        df:             pd.DataFrame:       DataFrame on which RestDF is running.
        request_body:   dict:               Request body received via /sample endpoint.

    Returns:
        list:           Returns random dataframe rows in a list for /sample.

    """
    response = []

    options = {
        'n': request_body.get('n', None if request_body.get('frac') else 1),
        'frac': request_body.get('frac', None),
        'replace': request_body.get('replace', False),
        'weights': request_body.get('weights', None),
        'random_state': request_body.get('random_state', None)
    }

    temp_df = df.sample(**options)

    return_cols = request_body.get('columns')
    temp_df = temp_df[return_cols] if return_cols else temp_df

    for index, row in temp_df.iterrows():
        d = row.to_dict()
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)
    return response


def get_column_value(df: pd.DataFrame, column_name: str, request_body: Dict[str, Any]) -> Union[List[object], Dict[str, Any]]:
    """
    Given the 'column_name' this method returns the values for the rows. Accepts the request_body
    dictionary received.
    Following attributes are looked for in the request_body dictionary:
        * n:            Number of random rows to return

    Args:
        df:             pd.DataFrame:           DataFrame on which RestDF is running.
        column_name:    str:                    Name of the columne for which we want values.
        request_body:   dict:                   Request body received via /column endpoint.

    Returns:
        list | dict:    List or dictionary containing selected column's values.

    """
    if request_body.get('add_index', False):
        return dict(df[column_name].head(request_body.get('n')).to_dict())
    else:
        return list(df[column_name].head(request_body.get('n')).tolist())


def get_isin_values(df: pd.DataFrame, column_name: str, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Given the dataframe and the values, this method returns the rows where the column
    values are within the given values (array).
    Following attributes are looked for in the request_body dictionary:
        * values:           list | None:        List of values that are to be checked in the isin operation. if column_name is 'column1'
                                                and the 'values' in request_body is ['a', 'b'], then this method will only return rows
                                                where the values of column1 are either 'a' or 'b'.
        * as_string:        bool:               Converts the entire column into a string before performing the isin operation. (Default: False)
        * columns:          list                List of columns that're to be returned as response.
        * index:            bool:               Wheather to include the index with the row objects in response. If yes,
                                                then the index of the row will be returned as '_index'.

    Args:
        df:             pd.DataFrame:           DataFrame on which RestDF is running.
        column_name:    str:                    Name of the columne on which we're performing the isin operation.
        request_body:   dict:                   Request body received via /isin endpoint.

    Returns:
        list:    List containing the rows satisfying the isin condition.
    """
    values = request_body.get('values', [])
    if not isinstance(values, list):
        raise exceptions.InvalidRequestBodyError(f"'values' needs to be a list, got {type(values)}")

    temp_df = df[df[column_name].astype(str).isin(values)] if (
        request_body.get('as_string', False)
    ) else df[df[column_name].isin(values)]

    return_cols = request_body.get('columns', [])
    return_cols = [] if not return_cols else return_cols
    if not isinstance(return_cols, list):
        raise exceptions.InvalidRequestBodyError(f"'columns' needs to be a list, got {type(return_cols)}")

    temp_df = temp_df[return_cols] if return_cols else temp_df

    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)
    return response


def get_notin_values(df: pd.DataFrame, column_name: str, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Given the dataframe and the values, this method returns the rows where the column
    values are not within the given values (array).
    Following attributes are looked for in the request_body dictionary:
        * values:           list | None:        List of values that are to be checked in the notin operation. if column_name is 'column1'
                                                and the 'values' in request_body is ['a', 'b'], then this method will only return rows
                                                where the values of column1 are not either 'a' or 'b'.
        * as_string:        bool:               Converts the entire column into a string before performing the isin operation. (Default: False)
        * columns:          list                List of columns that're to be returned as response.
        * index:            bool:               Wheather to include the index with the row objects in response. If yes,
                                                then the index of the row will be returned as '_index'.

    Args:
        df:             pd.DataFrame:           DataFrame on which RestDF is running.
        column_name:    str:                    Name of the columne on which we're performing the isin operation.
        request_body:   dict:                   Request body received via /notin endpoint.

    Returns:
        list:    List containing the rows satisfying the notin condition.
    """
    values = request_body.get('values', [])

    temp_df = df[~(df[column_name].astype(str).isin(values))] if (
        request_body.get('as_string')
    ) else df[~(df[column_name].isin(values))]

    return_cols = request_body.get('columns', [])
    return_cols = [] if not return_cols else return_cols
    if not isinstance(return_cols, list):
        raise exceptions.InvalidRequestBodyError(f"'columns' needs to be a list, got {type(return_cols)}")

    temp_df = temp_df[return_cols] if return_cols else temp_df

    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)
    return response


def get_equal_values(df: pd.DataFrame, column_name: str, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Given the dataframe and the values, this method returns the rows where the column
    values are equal to the given value (from the request body).
    Following attributes are looked for in the request_body dictionary:
        * value:            object:             Value that is to be checked for equality in the pd.Series
                                                for example, if value is `1` and the column name is `column1`
                                                then for all rows where column1 == `1`, will be returned.
        * as_string:        bool:               Converts the entire column into a string before performing the equal operation. (Default: False)
        * columns:          list                List of columns that're to be returned as response.
        * index:            bool:               Wheather to include the index with the row objects in response. If yes,
                                                then the index of the row will be returned as '_index'.

    Args:
        df:             pd.DataFrame:           DataFrame on which RestDF is running.
        column_name:    str:                    Name of the columne on which we're performing the equal operation.
        request_body:   dict:                   Request body received via /equal endpoint.

    Returns:
        list:           List containing the rows satisfying the equality condition.
    """
    value = request_body.get('value')

    temp_df = df[df[column_name].astype(str) == value] if (
        request_body.get('as_string')
    ) else df[df[column_name] == value]

    return_cols = request_body.get('columns', [])
    if not isinstance(return_cols, list):
        raise exceptions.InvalidRequestBodyError(f"'columns' needs to be a list, got {type(return_cols)}")

    temp_df = temp_df[return_cols] if return_cols else temp_df

    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)
    return response


def get_not_equal_values(df: pd.DataFrame, column_name: str, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Given the dataframe and the values, this method returns the rows where the column
    values are not equal to the given value (from the request body).
    Following attributes are looked for in the request_body dictionary:
        * value:            object:             Value that is to be checked for not equals in the pd.Series
                                                for example, if value is `1` and the column name is `column1`
                                                then for all rows where column1 != `1`, will be returned.
        * as_string:        bool:               Converts the entire column into a string before performing the equal operation. (Default: False)
        * columns:          list                List of columns that're to be returned as response.
        * index:            bool:               Wheather to include the index with the row objects in response. If yes,
                                                then the index of the row will be returned as '_index'.

    Args:
        df:             pd.DataFrame:           DataFrame on which RestDF is running.
        column_name:    str:                    Name of the columne on which we're performing the not equal operation.
        request_body:   dict:                   Request body received via /not_equals endpoint.

    Returns:
        list:           List containing the rows satisfying the non-equality condition.
    """
    value = request_body.get('value')

    temp_df = df[~(df[column_name].astype(str) == value)] if (
        request_body.get('as_string')
    ) else df[~(df[column_name] == value)]

    return_cols = request_body.get('columns', [])
    if not isinstance(return_cols, list):
        raise exceptions.InvalidRequestBodyError(f"'columns' needs to be a list, got {type(return_cols)}")

    temp_df = temp_df[return_cols] if return_cols else temp_df

    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)
    return response


def get_find_string_values(df: pd.DataFrame,
                           column_name: str,
                           request_body: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], int]:
    """
    Given the dataframe and the search pattern, this method uses the pd.Series.str.contains
    method and search for rows where the pattern matches the given column.
    For more info on the actual pandas method please refer to this page:
    https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html

    Following attributes are looked for in the request_body dictionary:
        * pat:              str:                Character sequence or regular expr.
        * case:             bool:               If True, case sensitive (default: False)
        * flags:            int:                Flags to pass through to the re module, e.g. re.IGNORECASE
                                                default: 0 (no flags)
        * na:               scalar:             Fill value for missing values. The default depends on dtype of the array
        * regex:            bool:               If True, assumes the pat is a regular expression.
                                                If False, treats the pat as a literal string.
                                                default: True
        * columns:          list:               List of columns that're to be returned as response.
        * index:            bool:               Wheather to include the index with the row objects in response. If yes,
                                                then the index of the row will be returned as '_index'.

    Args:
        df:             pd.DataFrame:           DataFrame on which RestDF is running.
        column_name:    str:                    Name of the columne on which we're performing the find string operation.
        request_body:   dict:                   Request body received via /find_string endpoint.

    Returns:
        list:           List containing the rows satisfying the string search operation.
    """

    options = {
        'pat': request_body.get('pattern', ''),
        'case': request_body.get('case', False),
        'flags': request_body.get('flags', 0),
        'na': request_body.get('na', False),
        'regex': request_body.get('regex', True)
    }
    temp_df = df[df[column_name].str.contains(**options)]

    return_cols = request_body.get('columns', [])
    if not isinstance(return_cols, list):
        raise exceptions.InvalidRequestBodyError(f"'columns' needs to be a list, got {type(return_cols)}")

    temp_df = temp_df[return_cols] if return_cols else temp_df

    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        if request_body.get('index'):
            d.update({'_index': index})
        response.append(d)

    return options, response, temp_df.shape[0]


def get_error_response(exception: object) -> Dict[str, str]:
    """
    This method expects the exception object and returns the returns
    the dictionary containing the error messages.

    Args:
        exception:      object:     Caught exception object.

    Returns:
        dict:           Dictionary containing the exception message, type and the module of the exception.
    """
    return {'err': repr(exception), 'type': type(exception).__name__, 'module': type(exception).__module__}
