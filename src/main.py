from fastapi import FastAPI

from src.ecg.adapter.in_adapters.web.main import api_router

app = FastAPI()

app.include_router(api_router)



