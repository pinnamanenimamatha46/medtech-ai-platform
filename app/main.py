"""Main FastAPI application."""

from fastapi import FastAPI

from app.api.patients import router as patients_router

app = FastAPI(
    title="MedTech AI Platform",
    version="0.1.0",
)


@app.get("/")
def root() -> dict[str, str]:
    """Return application status."""
    return {
        "name": "MedTech AI Platform",
        "status": "running",
    }


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Return service health."""
    return {"status": "healthy"}


app.include_router(
    patients_router,
    prefix="/api/v1",
)
