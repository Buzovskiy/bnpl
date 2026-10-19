from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="BNPL Notification Service",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["health"],
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="notification",
        version="0.1.0",
    )