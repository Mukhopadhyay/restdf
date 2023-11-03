"""
Input/Output methods required for RestDF
"""
import os
import pandas as pd


def optimize_df(df: pd.DataFrame) -> None:
    pass


def read_df(path: str) -> pd.DataFrame:
    _ext = os.path.splitext(path)
    if len(_ext) != 2:
        # TODO: Patherror to be raised here
        raise ValueError("Invalid path received")

    df: pd.DataFrame = None

    if _ext[-1].casefold() == ".csv":
        # CSV
        pass
    elif _ext[-1].casefold() == ".xlsx":
        # EXCEL
        pass
    elif _ext[-1].casefold() in (".pkl", ".pickle"):
        # Pickle
        pass

    return df
