"""
Data
~~~~

Endpoints to fetch the rows
"""
import pandas as pd
from fastapi import APIRouter

router = APIRouter(prefix="/data", tags=["Data"])


df: pd.DataFrame = None


def get_router(dataframe: pd.DataFrame) -> APIRouter:
    global df
    df = dataframe
    return router


# @staticmethod
@router.post("/equals/{column}")
async def equals(column: str):
    return {}


# @staticmethod
@router.post("/find_string/{column}")
async def find_string(column: str):
    return {}


# @staticmethod
@router.post("/head")
async def head():
    return {}


# @staticmethod
@router.post("/isin/{column}")
async def isin(column: str):
    return {}


# @staticmethod
@router.post("/not_equals/{column}")
async def not_equals(column: str):
    return {}


# @staticmethod
@router.post("/notin/{column}")
async def notin(column: str):
    return {}


# @staticmethod
@router.post("/sample")
async def sample():
    return {}
