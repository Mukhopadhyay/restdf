from fastapi import APIRouter
from schemas.response import IndexResponse


router = APIRouter()


@router.get("/")
async def index():
    return IndexResponse()
