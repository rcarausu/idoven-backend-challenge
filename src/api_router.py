from fastapi import APIRouter

from src.ecg.adapter.in_adapters.web.routers.ecgs_router import router as ecgs_router
from src.ecg.adapter.in_adapters.web.routers.health_router import router as health_router
from src.user.adapter.in_adapters.web.routers.users_router import router as users_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/health", tags=["health"])
api_router.include_router(ecgs_router, prefix="/ecgs", tags=["ecg"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
