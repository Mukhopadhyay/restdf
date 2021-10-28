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

    Attributes:
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

    Attributes:
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

    Attributes:
        df:         pd.DataFrame:

    Returns:
        List[str]:                      List containing the dataframe columns.
    """
    return list(df.columns.tolist())


def get_dataframe_descriptions(df: pd.DataFrame, **kwargs) -> Dict[str, object]:
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
    shape = df.shape[0]
    info = [{
        'index': i,
        'column': col,
        'count': int(shape - df[col].isna().sum()),
        'dtype': str(df[col].dtype)
    } for i, col in enumerate(df.columns)]
    return info


def get_value_counts(df: pd.DataFrame, column: str) -> Dict[str, int]:
    return dict(df[column].value_counts().to_dict())


def get_dataframe_head(df: pd.DataFrame, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
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
    if request_body.get('add_index', False):
        return dict(df[column_name].head(request_body.get('n')).to_dict())
    else:
        return list(df[column_name].head(request_body.get('n')).tolist())


def get_isin_values(df: pd.DataFrame, column_name: str, request_body: Dict[str, Any]) -> List[Dict[str, Any]]:
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
    return {'err': repr(exception), 'type': type(exception).__name__, 'module': type(exception).__module__}
