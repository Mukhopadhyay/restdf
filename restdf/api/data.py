"""
Data
~~~~

Endpoints to fetch the rows
"""
from fastapi import APIRouter

router = APIRouter(prefix="/data", tags=["Data"])


@router.post("/equals/{column}")
async def get_data(column: str):
    return {}


@router.post("/find_string/{column}")
async def find_string(column: str):
    return {}


@router.post("/head")
async def head():
    return {}


@router.post("/isin/{column}")
async def isin(column: str):
    return {}


@router.post("/not_equals/{column}")
async def not_equals(column: str):
    return {}


@router.post("/notin/{column}")
async def notin(column: str):
    return {}


@router.post("/sample")
async def sample():
    return {}
