import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.main import app
from server.database import Base, get_db
from server.auth import models
from server.auth.deps import get_current_active_user

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_profile.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

from fastapi import Depends
from sqlalchemy.orm import Session

def override_get_current_active_user(db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id=1).first()
    if not user:
        user = models.User(id=1, email="test@example.com", hashed_password="hashed_password", is_active=True, skills=[])
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

app.dependency_overrides[get_current_active_user] = override_get_current_active_user

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown():
    # Reset test user skills before each test
    db = TestingSessionLocal()
    user = db.query(models.User).filter_by(id=1).first()
    if user:
        user.skills = []
        db.commit()
    db.close()
    yield

def test_get_skills():
    response = client.get("/api/profile/skills")
    assert response.status_code == 200
    assert response.json() == []

def test_add_skill():
    response = client.post("/api/profile/skills", json={"skill": "python"})
    assert response.status_code == 200
    assert response.json() == ["python"]
    
    db = TestingSessionLocal()
    user = db.query(models.User).filter_by(id=1).first()
    assert "python" in user.skills
    db.close()

def test_add_empty_skill():
    response = client.post("/api/profile/skills", json={"skill": "  "})
    assert response.status_code == 400

def test_remove_skill():
    db = TestingSessionLocal()
    user = db.query(models.User).filter_by(id=1).first()
    user.skills = ["python", "react"]
    db.commit()
    db.close()
    
    response = client.delete("/api/profile/skills/python")
    assert response.status_code == 200
    assert response.json() == ["react"]

def test_extract_resume_skills():
    resume_text = "I am a software engineer with experience in Python, React, and AWS."
    response = client.post("/api/profile/extract-resume", json={"resume_text": resume_text})
    assert response.status_code == 200
    skills = response.json()
    assert "python" in skills
    assert "react" in skills
    assert "aws" in skills
