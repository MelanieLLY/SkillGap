import pytest
from fastapi.testclient import TestClient
from server.main import app
from datetime import datetime

client = TestClient(app)

def test_create_history():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    
    class MockDB:
        def __init__(self):
            self.adds = []
        def add(self, item):
            self.adds.append(item)
            item.id = 1
            item.date_analyzed = datetime.now()
        def commit(self):
            pass
        def refresh(self, item):
            pass
            
    mock_db = MockDB()
    mock_user = User(id=1, email="test@test.com", skills=[])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.post("/api/history/", json={
        "company_name": "ACME",
        "position_name": "Engineer",
        "match_score": 85.5,
        "have_skills": ["python"],
        "missing_skills": ["aws"],
        "bonus_skills": []
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "ACME"
    assert data["match_score"] == 85.5
    assert len(mock_db.adds) == 1

def test_get_history():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    from server.history.models import AnalysisHistory
    
    class MockQuery:
        def filter(self, *args):
            return self
        def order_by(self, *args):
            return self
        def all(self):
            return [
                AnalysisHistory(
                    id=1, user_id=1, company_name="ACME", position_name="Engineer", 
                    date_analyzed=datetime.now(), match_score=85.5, 
                    have_skills=["python"], missing_skills=["aws"], bonus_skills=[]
                )
            ]
            
    class MockDB:
        def query(self, model):
            return MockQuery()
            
    mock_db = MockDB()
    mock_user = User(id=1, email="test@test.com", skills=[])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/api/history/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["company_name"] == "ACME"

def test_update_history():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    from server.history.models import AnalysisHistory
    
    mock_history = AnalysisHistory(
        id=1, user_id=1, company_name="ACME", position_name="Engineer", 
        date_analyzed=datetime.now(), match_score=85.5, 
        have_skills=["python"], missing_skills=["aws"], bonus_skills=[]
    )
    
    class MockQuery:
        def filter(self, *args):
            return self
        def first(self):
            return mock_history
            
    class MockDB:
        def query(self, model):
            return MockQuery()
        def commit(self):
            pass
        def refresh(self, item):
            pass
            
    mock_db = MockDB()
    mock_user = User(id=1, email="test@test.com", skills=[])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.put("/api/history/1", json={"company_name": "Globex", "position_name": "Senior Engineer"})
    assert response.status_code == 200
    data = response.json()
    assert data["company_name"] == "Globex"
    assert data["position_name"] == "Senior Engineer"

def test_update_history_unauthorized():
    from server.auth.models import User
    from server.auth.deps import get_current_active_user
    from server.database import get_db
    from server.history.models import AnalysisHistory
    
    # History belongs to user 2
    mock_history = AnalysisHistory(
        id=1, user_id=2, company_name="ACME", position_name="Engineer", 
        date_analyzed=datetime.now(), match_score=85.5, 
        have_skills=["python"], missing_skills=["aws"], bonus_skills=[]
    )
    
    class MockQuery:
        def filter(self, *args):
            return self
        def first(self):
            return mock_history
            
    class MockDB:
        def query(self, model):
            return MockQuery()
            
    mock_db = MockDB()
    # Current user is user 1
    mock_user = User(id=1, email="test@test.com", skills=[])
    
    app.dependency_overrides[get_current_active_user] = lambda: mock_user
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.put("/api/history/1", json={"company_name": "Globex"})
    assert response.status_code == 403
