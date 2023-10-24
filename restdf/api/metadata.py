"""
Metadata
~~~~~~~~
Metadata endpoints
"""
from fastapi import APIRouter

router = APIRouter(prefix="/metadata", tags=["Metadata"])


@router.get("/columns")
async def get_columns():
    return {}


@router.post("/describe")
async def describe():
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
