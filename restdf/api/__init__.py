from .data import router as data_router
from .metadata import router as metadata_router

from fastapi import APIRouter

router = APIRouter()

# Adding the Routers
router.include_router(data_router)
router.include_router(metadata_router)
