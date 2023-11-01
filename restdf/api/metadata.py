"""
Metadata
~~~~~~~~
Metadata endpoints
"""
import pandas as pd
from fastapi import APIRouter, status


router = APIRouter(prefix="/metadata", tags=["Metadata"])

df: pd.DataFrame = None


def get_router(dataframe: pd.DataFrame) -> APIRouter:
    global df
    df = dataframe
    return router


@router.get("/columns")
async def get_columns():
    return {}


@router.post("/describe")
async def describe(body):
    return {}


@router.get("/dtypes")
async def get_columns():
    return {}


@router.get("/info")
async def info():
    return {}


@router.get("/nulls")
async def nulls():
    return {}


@router.get("/value_counts/{column}")
async def value_counts(column: str):
    return {}
