"""
Input/Output methods required for RestDF
"""
# Built-in modules
import os
import pickle
from typing import Union, List, Dict, Callable
# Third-party modules
import pandas as pd
# RestDF modules
from . import exceptions


def get_extension(path: Union[List[str], str]) -> str:
    """
    Given the path (in form of a list or as a string) this method tries to
    return the extension. If the path leads to no file then returns
    an empty string ``

    Args:
        path:       list | str:         Expects the path in as a list e.g., ['.', 'dataset', 'data.csv']
                                        or as string e.g., './dataset/data.csv'
    Returns:
        str:        Extension from the path, e.g., './dataset/data.csv' => '.csv', or './dataset/' => ''
    """
    if type(path) not in [list, str]:
        raise TypeError(f'Argument path cannot be of type {type(path)}\nAccepted types: [list | str]')
    elif isinstance(path, list):
        return os.path.splitext(path[-1])[-1][1:]
    else:
        return os.path.splitext(path)[-1][1:]


def read_from_csv(path: str, **kwargs) -> pd.DataFrame:
    """
    Read from csv file, where the path is given and the rest of the
    keyword arguments for the pd.read_csv method.

    Args:
        path:       str:        Path to the csv file as string literal.

    Returns:
        pd.DataFrame:           Read dataframe from the path.
    """
    return pd.read_csv(path, **kwargs)


def read_from_excel(path: str, **kwargs) -> pd.DataFrame:
    """
    Read from excel file, where the path is given and the rest of the
    keyword arguments for the pd.read_excel method.

    Args:
        path:       str:        Path to the csv file as string literal.

    Returns:
        pd.DataFrame:           Read dataframe from the path.
    """
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
    """
    This method receives the path to the dataset, tries to perform the method
    resolution to read the dataframe and returns the DataFrame object if successful.

    Raises:
        TypeError:                  If any other type but list or string is provided to get_extension()
        UnknownFileTypeError:       If the extension of the file is unknown to us.

    Args:
        path:           list | str:     Path to the dataset, either as a string or a list.

    Returns:
        pd.DataFrame:   Returns the read dataframe.
    """
    path = os.path.join(*path) if isinstance(path, list) else path
    if not path.startswith('https://') and not os.path.exists(path):
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
