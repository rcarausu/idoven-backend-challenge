from fastapi import APIRouter

from src.ecg.adapter.in_adapters.web.routers.ecg_router import router as ecg_router
from src.ecg.adapter.in_adapters.web.routers.health_router import router as health_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(ecg_router, prefix="/ecg", tags=["ecg"])
