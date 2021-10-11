# TODO: Proper implementation of kwargs in read_from_csv & read_from_excel

"""
Input/Output Methods
"""
# Built-in modules
import os
import pickle
from typing import Union, List, Dict, Callable
# Third-party modules
import pandas as pd
# RestDF modules
from . import exceptions


# Returns the extension of the file
def get_extension(path: Union[List[str], str]) -> str:
    if type(path) not in [list, str]:
        raise TypeError(f'Argument path cannot be of type {type(path)}\nAccepted types: [list | str]')
    elif isinstance(path, list):
        return os.path.splitext(path[-1])[-1][1:]
    else:
        return os.path.splitext(path)[-1][1:]


def read_from_csv(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


def read_from_excel(path: str, **kwargs) -> pd.DataFrame:
    return pd.read_excel(path, **kwargs)


def read_from_pickle(path: str) -> pd.DataFrame:
    with open(path, 'rb') as file:
        df = pickle.load(file)
    if isinstance(df, pd.DataFrame):
        return df
    else:
        raise exceptions.DataFrameError(
            path,
            f'Unpickled object is of type: {type(df)}'
        )


# Dictionary for reading dataframe
method_dictionary: Dict[str, Callable[..., pd.DataFrame]] = {
    'csv': read_from_csv,
    'xlsx': read_from_excel,
    'pkl': read_from_pickle,
    'pickle': read_from_pickle
}


def read_dataframe(path: Union[List[str], str]) -> pd.DataFrame:
    path = os.path.join(*path) if isinstance(path, list) else path
    if not os.path.exists(path):
        raise exceptions.PathError(
            path,
            f'Path: {path} does not exist!'
        )
    try:
        extension = get_extension(path)
    except TypeError as type_error:
        print(str(type_error))
    else:
        if hasattr(method_dictionary.get(extension), '__call__'):
            df = method_dictionary[extension](path)
            return df
        else:
            raise exceptions.UnknownFileTypeError(
                extension=extension,
                message=f'Currently supported formats!\n'
                        f'{set(list(method_dictionary.keys()))}'
            )
