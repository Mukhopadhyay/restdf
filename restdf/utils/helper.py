import sys
from typing import Optional

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
                'name': '/value_counts/<column>',
                'type': ['GET'],
                'description': ''
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
            include=kwargs.get('include')
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

def get_dataframe_head(df: pd.DataFrame, n: Optional[int] = 5) -> dict:
    response = []
    for index, row in df.head(n).astype(str).iterrows():
        d = row.to_dict()
        d.update({'_index': index})
        response.append(d)
    return response
