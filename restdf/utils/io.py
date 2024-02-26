"""
Input/Output methods required for RestDF
"""
import os
import pandas as pd
from typing import Optional
from utils.exceptions import PathError, UnknownFileTypeError


# TODO: Finish this
def optimize_df(df: pd.DataFrame) -> None:
    pass


def read_df(path: str) -> Optional[pd.DataFrame]:
    _ext = os.path.splitext(path)

    if _ext not in (".csv", ".xlsx", ".pkl", ".pickle"):
        raise UnknownFileTypeError(
            f"Extension '{_ext}' is not supported.\nTry one of ('.csv', '.xlsx', '.pkl', '.pickle') files"
        )

    if len(_ext) != 1:
        raise PathError(path, f'No file found found at "{path}"')

    df: pd.DataFrame = None

    if _ext[-1].casefold() == ".csv":
        # CSV
        df = pd.read_csv(path)
    elif _ext[-1].casefold() == ".xlsx":
        # EXCEL
        df = pd.read_excel(path)
    elif _ext[-1].casefold() in (".pkl", ".pickle"):
        # Pickle
        df = pd.read_pickle(path)

    return df
