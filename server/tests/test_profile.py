import pytest
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)

# Helper function to get mock token
def get_auth_headers():
    # In a real setup, we should create a test user and generate a token
    # For now, we will mock the get_current_active_user dependency if needed, 
    # but let's assume we can hit the endpoint by overriding dependency
    pass

def test_get_skills():
    # Mocking the dependency
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    
    mock_user = User(id=1, email="test@test.com", skills=["python", "fastapi"])
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    
    response = client.get("/api/profile/skills")
    assert response.status_code == 200
    assert response.json() == ["python", "fastapi"]

def test_add_skill():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    
    class MockDB:
        def commit(self):
            pass
            
    mock_db = MockDB()
    mock_user = User(id=1, email="test@test.com", skills=["python"])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/api/profile/skills", json={"skill": "react"})
    assert response.status_code == 200
    assert "react" in response.json()
    assert mock_user.skills == ["python", "react"]

def test_remove_skill():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    
    class MockDB:
        def commit(self):
            pass
            
    mock_db = MockDB()
    mock_user = User(id=1, email="test@test.com", skills=["python", "fastapi"])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.delete("/api/profile/skills/fastapi")
    assert response.status_code == 200
    assert response.json() == ["python"]

def test_extract_resume():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    
    class MockDB:
        def commit(self):
            pass
            
    mock_db = MockDB()
    mock_user = User(id=1, email="test@test.com", skills=["python"])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    resume_text = "I have experience with React, fastAPI, and AWS."
    response = client.post("/api/profile/extract-resume", json={"resume_text": resume_text})
    
    assert response.status_code == 200
    skills = response.json()
    # "python" from original, plus extracted
    # "react", "fastapi", "aws" should be extracted based on CURATED_SKILLS
    assert "python" in skills
    assert "react" in skills
    assert "fastapi" in skills
    assert "aws" in skills
