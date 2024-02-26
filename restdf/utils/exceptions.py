"""
Exceptions for the module
"""
from typing import Union, List


class Error(Exception):
    """
    Base class for exceptions in this module
    """

    pass


class PathError(Error):
    """
    Exception raised when there's an error in the given path.

    Attributes:
        path:       Union[str, list]:   Path which caused the exception
        message:    str:                Explanation of the error.
    """

    def __init__(self, path: Union[List[str], str], message: str) -> None:
        super().__init__(f"[{self.__class__.__name__}] {message}\nPath: {path}")
        self.path = path
        self.message = message

    def __repr__(self) -> str:
        return f"[{self.__class__.__name__}] {self.message}\nPath: {self.path}"


class UnknownFileTypeError(Error):
    """
    Exception raised when the File extension is not known, or no such io
    method exists to deal with given extension.

    Attributes:
        extension:  str:                Extension of the file.
        message:    str:                Explanation of the error.
    """

    def __init__(self, extension: str, message: str) -> None:
        super().__init__(
            f"[{self.__class__.__name__}] {message}\nExtension: {extension}"
        )
        self.extension = extension
        self.message = message

    def __repr__(self) -> str:
        return (
            f"[{self.__class__.__name__}] {self.message}\nExtension: {self.extension}"
        )
