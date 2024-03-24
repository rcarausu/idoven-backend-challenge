from fastapi import FastAPI

from src.ecg.adapter.in_adapters.web.ecg_controller import router as ecg_router
from src.ecg.adapter.in_adapters.web.health_controller import router as health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(ecg_router)
