import imp
from fastapi import APIRouter
from .routes.statistics import router as statistics_router
router = APIRouter(prefix='/api/v1')
router.include_router(statistics_router)