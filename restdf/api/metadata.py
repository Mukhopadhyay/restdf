"""
Metadata
~~~~~~~~
Metadata endpoints
"""
import pandas as pd
from fastapi import APIRouter, status
from schemas import response, request


router = APIRouter(prefix="/metadata", tags=["Metadata"])

df: pd.DataFrame = None


def get_router(dataframe: pd.DataFrame) -> APIRouter:
    global df
    df = dataframe
    return router


@router.get("/columns", response_model=response.ColumnResponse)
async def get_columns():
    return response.Response(data=list(df.columns))


@router.post("/describe")
async def describe(body: request.DescribeRequest):
    """
    This endpoint returns the response from `df.describe()` & returns the result
    """
    describe_dict = df.describe(**body.model_dump(exclude_unset=True)).to_dict()
    for column, column_desc in describe_dict.items():
        for stat, value in column_desc.items():
            if "int" in str(type(value)):
                describe_dict[column][stat] = int(value)
            elif "float" in str(type(value)):
                describe_dict[column][stat] = float(value)
    return describe_dict

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
