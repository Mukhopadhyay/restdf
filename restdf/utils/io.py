"""
Input/Output Methods
"""
# Built-ins
import os
from typing import Union
# RestDF imports
from . import exceptions

def get_extension(path: Union[list, str]) -> str:
    if type(path) not in [list, str]:
        raise exceptions.PathError(path, 'Path needs to be of type list or str!')
    elif isinstance(path, list):
        return os.path.splitext(path[-1])[-1][1:]
    else:
        return os.path.splitext(path)[-1][1:]

