from fastapi import FastAPI

from .ecg.adapter.in_adapters.web.health_controller import router as health_router

app = FastAPI()

app.include_router(health_router)
