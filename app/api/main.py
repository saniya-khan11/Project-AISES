from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.models.response_models import HealthResponse
from app.api.routes.analysis import router as analysis_router

app = FastAPI(
    title="AISES API",
    description="AI Software Implementation Evaluation System",
    version="1.0",
)

register_exception_handlers(app)

app.include_router(analysis_router)


@app.get("/")
def root():

    return {
        "application": "AISES",
        "version": "1.0",
        "status": "Running",
    }


@app.get(
    "/health",
    response_model=HealthResponse,
)
def health():

    return HealthResponse(
        status="healthy",
    )