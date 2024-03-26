import uvicorn
from fastapi import FastAPI, APIRouter

from src.api_router import api_router

app = FastAPI(
    title="ECG app",
    summary="Register and check insights on electrocardiograms (ECGs)",
    version="0.0.1",
    contact={
        "name": "Robert Carausu",
        "url": "https://www.linkedin.com/in/robertcarausu/",
    },
)

health_router = APIRouter()


@health_router.get("/ping")
def ping():
    return "pong"


app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
