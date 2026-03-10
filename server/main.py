from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from contextlib import asynccontextmanager
from server.extraction.router import router as extraction_router
from server.auth.router import router as auth_router
from server.database import engine
from server.auth import models

from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    try:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS skills VARCHAR[] SERVER DEFAULT '{}';"))
    except Exception as e:
        print(f"Auto-migration skipped: {e}")
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

from server.profile.router import router as profile_router

# Register routers
app.include_router(extraction_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(profile_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Welcome to SkillGap API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)
