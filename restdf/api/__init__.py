from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def index():
    return {"name": "RestDF", "version": "2.0.0"}
