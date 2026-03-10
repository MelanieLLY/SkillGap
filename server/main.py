from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from contextlib import asynccontextmanager
from sqlalchemy import text
from server.extraction.router import router as extraction_router
from server.auth.router import router as auth_router
from server.profile.router import router as profile_router
from server.history.router import router as history_router
from server.database import engine
from server.auth import models
from server.history import models as history_models

@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.get("/")
async def root():
    return {"message": "Welcome to SkillGap API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
