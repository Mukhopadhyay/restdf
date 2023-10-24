"""
Data
~~~~

Endpoints to fetch the rows
"""
from fastapi import APIRouter

router = APIRouter(prefix="/data", tags=["Data"])


@router.get("/")
def get_data():
    return {}
