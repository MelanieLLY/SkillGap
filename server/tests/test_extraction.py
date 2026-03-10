import pytest
from server.extraction.engine import extract_skills

def test_extract_skills_empty():
    assert extract_skills("", []) == {"have": [], "missing": [], "bonus": []}

def test_extract_skills_languages():
    jd = "Looking for a Python developer with TypeScript experience. Good to have Go."
    user = ["Python", "JavaScript", "Go"]
    
    result = extract_skills(jd, user)
    assert "python" in result["have"]
    assert "go" in result["have"]
    assert "typescript" in result["missing"]
    assert "javascript" in result["bonus"]

def test_extract_skills_frameworks():
    jd = "Experience with React, FastAPI, Django, and Uiautomator."
    user = ["react", "fastapi", "vue"]
    
    result = extract_skills(jd, user)
    assert set(result["have"]) == {"react", "fastapi"}
    assert set(result["missing"]) == {"django", "uiautomator"}
    assert set(result["bonus"]) == {"vue"}

def test_extract_skills_databases():
    jd = "Knowledge of PostgreSQL and Redis."
    user = ["PostgreSQL", "MongoDB"]
    
    result = extract_skills(jd, user)
    assert "postgresql" in result["have"]
    assert "redis" in result["missing"]
    assert "mongodb" in result["bonus"]

def test_extract_skills_tools_cloud_ml():
    jd = "Deploy with Docker, Kubernetes on AWS. ML experience with PyTorch, scikit-learn, LangChain."
    user = ["Docker", "Git", "AWS", "TensorFlow", "scikit-learn"]
    
    result = extract_skills(jd, user)
    assert {"docker", "aws", "scikit-learn"}.issubset(set(result["have"]))
    assert {"kubernetes", "pytorch", "langchain"}.issubset(set(result["missing"]))
    assert "git" in result["bonus"]
    assert "tensorflow" in result["bonus"]

def test_extract_skills_case_and_boundaries():
    jd = "Must know C++, Node.js, and Java. Also JavaScript."
    user = ["c++", "Node.js"]
    
    result = extract_skills(jd, user)
    assert "c++" in result["have"]
    assert "node.js" in result["have"]
    assert "java" in result["missing"]
    assert "javascript" in result["missing"]
