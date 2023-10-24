"""
Metadata
~~~~~~~~
Metadata endpoints
"""
from fastapi import APIRouter

router = APIRouter(prefix="/metadata", tags=["Metadata"])


@router.get("/")
def get_metadata():
    return {}
