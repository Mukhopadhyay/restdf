"""
Exceptions for RestDf
"""

from typing import Union


class Error(Exception):
    """
    Base class for exceptions in this module.
    """
    pass


class PathError(Error):
    """
    Exception raised when there's an error in the given path.

    Attributes:
        path:       Union[str, list]:   Path which caused the exception
        message:    str:                Explanation of the error.
    """
    def __init__(self, path: Union[list, str], message: str) -> None:
        super().__init__(f'[{self.__class__.__name__}] {message}\nPath: {path}')
        self.path = path
        self.message = message

    def __repr__(self) -> str:
        return f'[{self.__class__.__name__}] {self.message}\nPath: {self.path}'


class DataFrameError(Error):
    """
    Exception raised when the read file is not a dataframe.

    Attributes:
        path:       Union[str, list]:   Path which lead to non df object.
        message:    str:                Explanation of the error.
    """
    def __init__(self, path: Union[list, str], message: str) -> None:
        super().__init__(f'[{self.__class__.__name__}] {message}\nPath: {path}')
        self.path = path
        self.message = message

    def __repr__(self) -> str:
        return f'[{self.__class__.__name__}] {self.message}\nPath: {self.path}'


class UnknownFileTypeError(Error):
    """
    Exception raised when the File extension is not known, or no such io
    method exists to deal with given extension.
    
    Attributes:
        extension:  str:                Extension of the file.
        message:    str:                Explanation of the error.
    """
    def __init__(self, extension: str, message: str) -> None:
        super().__init__(f'[{self.__class__.__name__}] {message}\nExtension: {extension}')
        self.extension = extension
        self.message = message
        
    def __repr__(self) -> str:
        return f'[{self.__class__.__name__}] {self.message}\nExtension: {self.extension}'


class InvalidRequestBodyError(Error):
    """
    Exception raised when passed request body has invalid values in them.

    Attributes:

    """
    def __init__(self, message: str) -> None:
        super().__init__(f'[{self.__class__.__name__}] {message}\n')
        self.message = message

    def __repr__(self) -> str:
        return f'[{self.__class__.__name__}] {self.message}\n'
