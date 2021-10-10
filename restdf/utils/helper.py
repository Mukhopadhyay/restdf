import sys
from typing import Optional, List, Union, Tuple

# Third-party modules
import psutil
import pandas as pd

# RestDF modules
from . import exceptions

def get_index(filename: str) -> dict:
    INDEX_RESPONSE = {
        'filename': filename,
        'endpoints': [
            {
                'name': '/',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/stats',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/columns',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/describe',
                'type': ['POST'],
                'description': ''
            },
            {
                'name': '/info',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/dtypes',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/value_counts/<column>',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/nulls',
                'type': ['GET'],
                'description': ''
            },
            {
                'name': '/head',
                'type': ['POST'],
                'description': ''
            },
            {
                'name': '/sample',
                'type': ['POST'],
                'description': ''
            },
            {
                'name': '/values/<column_name>',
                'type': ['POST'],
                'description': ''
            },
            {
                'name': '/values/<column_name>',
                'type': ['POST'],
                'decription': ''
            },
            {
                'name': '/isin/<column_name>',
                'type': ['POST'],
                'decription': ''
            },
            {
                'name': '/notin/<column_name>',
                'type': ['POST'],
                'decription': ''
            },
            {
                'name': '/equals/<column_name>',
                'type': ['POST'],
                'decription': ''
            },
            {
                'name': '/not_equals/<column_name>',
                'type': ['POST'],
                'decription': ''
            },
            {
                'name': '/find_string/<column_name>',
                'type': ['POST'],
                'decription': ''
            }
        ]
    }
    return INDEX_RESPONSE

def get_stats(framework:str, framework_version:str, stats_dict: dict) -> dict:
    vm = psutil.virtual_memory()
    stats = {
        'Server': {
            'name'   : framework,
            'version': framework_version,
        },
        'Python': {
            'version': sys.version,
        },
        'Runtime': {
            'filename'        : stats_dict.get('filename'),
            'runtime_duration': stats_dict.get('runtime_duration'),
            'running_since'   : stats_dict.get('running_since'),
            'API': {
                'total_requests'  : stats_dict.get('total_requests'),
                '/values_requests': stats_dict.get('values_requests'),
            }
        },
        'Device': {
            'cpu_percent': psutil.cpu_percent(),
            'Memory': {
                'total'    : vm.total,
                'available': vm.available,
                'percent'  : vm.percent,
                'used'     : vm.used,
                'free'     : vm.free
            }
        }
    }
    return stats

def get_dataframe_columns(df: pd.DataFrame) -> list:
    return df.columns.tolist()

def get_dataframe_descriptions(df: pd.DataFrame, **kwargs) -> dict:
    try:
        describe_dict: dict = df.describe(
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

def get_dataframe_info(df: pd.DataFrame) -> list:
    shape = df.shape[0]
    info =[{
        'index' : i,
        'column': col,
        'count' : int(shape - df[col].isna().sum()),
        'dtype' : str(df[col].dtype)
    } for i, col in enumerate(df.columns)]
    return info

def get_value_counts(df: pd.DataFrame, column: str) -> dict:
    return df[column].value_counts().to_dict()

def get_dataframe_head(df: pd.DataFrame, n: Optional[int] = 5) -> List[dict]:
    response = []
    for index, row in df.head(n).iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response

def get_dataframe_sample(df: pd.DataFrame, request_body: dict) -> List[dict]:
    response = []
    for index, row in df.sample(**request_body).iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response


def get_column_value(df: pd.DataFrame, column_name: str, request_body: dict) -> Union[List[object], dict]:
    if request_body.get('add_index', False):
        return df[column_name].head(request_body.get('n')).to_dict()
    else: 
        return df[column_name].head(request_body.get('n')).tolist()


def get_isin_values(df: pd.DataFrame, column_name: str, request_body: dict) -> List[dict]:
    values = request_body.get('values', [])
    
    temp_df = df[df[column_name].astype(str).isin(values)] if (
        request_body.get('as_string')
    ) else df[df[column_name].isin(values)]
    
    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response

def get_notin_values(df: pd.DataFrame, column_name: str, request_body: dict) -> List[dict]:
    values = request_body.get('values', [])
    
    temp_df = df[~(df[column_name].astype(str).isin(values))] if (
        request_body.get('as_string')
    ) else df[~(df[column_name].isin(values))]
    
    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response

def get_equal_values(df: pd.DataFrame, column_name: str, request_body: dict) -> List[dict]:
    value = request_body.get('value')
    
    temp_df = df[df[column_name].astype(str) == value] if (
        request_body.get('as_string')
    ) else df[df[column_name] == value]
    
    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response

def get_not_equal_values(df: pd.DataFrame, column_name: str, request_body: dict) -> List[dict]:
    value = request_body.get('value')
    
    temp_df = df[~(df[column_name].astype(str) == value)] if (
        request_body.get('as_string')
    ) else df[~(df[column_name] == value)]
    
    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response

def get_find_string_values(df: pd.DataFrame, column_name: str, request_body: dict) -> Tuple[dict, List[dict], int]:

    options = {
        'pat': request_body.get('pattern', ''),
        'case': request_body.get('case', False),
        'flags': request_body.get('flags', 0),
        'na': request_body.get('na', False),
        'regex': request_body.get('regex', True)
    }
    
    temp_df = df[df[column_name].str.contains(**options)]
    
    response = []
    for index, row in temp_df.iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    
    
    return options, response, temp_df.shape[0]

