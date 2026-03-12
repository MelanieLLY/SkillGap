from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from server.auth import models
from server.auth.router import router as auth_router
from server.database import engine
from server.extraction.router import router as extraction_router
from server.history import models as history_models
from server.history.router import router as history_router
from server.profile.router import router as profile_router
from server.roadmap.router import router as roadmap_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI application startup and shutdown events.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    models.Base.metadata.create_all(bind=engine)
    history_models.Base.metadata.create_all(bind=engine)
    # Fallback to add skills column explicitly since we don't use alembic for existing DBs
    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS skills VARCHAR[] DEFAULT '{}'"))
        conn.commit()
    yield

app = FastAPI(title="SkillGap API", lifespan=lifespan)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(extraction_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(history_router, prefix="/api/history", tags=["history"])
app.include_router(roadmap_router, prefix="/api/roadmap", tags=["roadmap"])

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    Global exception handler for SQLAlchemyError.

    Catches database-related exceptions globally, preventing app crashes,
    and returns a clean JSON response.

    Args:
        request (Request): The incoming FastAPI request.
        exc (SQLAlchemyError): The caught exception instance.

    Returns:
        JSONResponse: An HTTP 500 JSON response containing an error summary.
    """
    # Log the error here to console so we can debug it
    print(f"Global DB Error -> URL: {request.url} | Error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred while processing your request."},
    )


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint for the API.

    Returns:
        Dict[str, str]: A simple welcome message.
    """
    return {"message": "Welcome to SkillGap API"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Dict[str, str]: The health status of the application.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
