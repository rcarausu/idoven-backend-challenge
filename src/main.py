from fastapi import FastAPI

from src.ecg.adapter.in_adapters.web.main import api_router

app = FastAPI(
    title="ECG app",
    summary="Register and check insights on electrocardiograms (ECGs)",
    version="0.0.1",
    contact={
        "name": "Robert Carausu",
        "url": "https://www.linkedin.com/in/robertcarausu/",
    },
)

app.include_router(api_router)
