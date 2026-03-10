import pytest
from server.extraction.engine import extract_skills, calculate_match_score, extract_company_and_position

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
    assert "javascript" in result["missing"]

def test_calculate_match_score_empty():
    assert calculate_match_score([], []) == 0.0

def test_calculate_match_score_full_match():
    assert calculate_match_score(["python", "react"], []) == 100.0

def test_calculate_match_score_no_match():
    assert calculate_match_score([], ["python", "react"]) == 0.0

def test_calculate_match_score_partial_match():
    have = ["python", "react"]
    missing = ["django", "postgres"]
    # 2 / 4 = 50%
    assert calculate_match_score(have, missing) == 50.0

def test_calculate_match_score_rounding():
    have = ["python", "react"]
    missing = ["django"]
    # 2 / 3 = 66.666...
    assert calculate_match_score(have, missing) == 66.67

def test_extract_company_and_position():
    jd1 = "Welcome to TechLogix. Company: TechLogix Inc.\nRole: Senior Developer"
    res1 = extract_company_and_position(jd1)
    assert res1["company_name"] == "TechLogix Inc."
    assert res1["position_name"] == "Senior Developer"
    
    jd2 = "We are hiring! Position: Software Engineer"
    res2 = extract_company_and_position(jd2)
    assert res2["company_name"] is None
    assert res2["position_name"] == "Software Engineer"
    
    jd3 = "No obvious fields here."
    res3 = extract_company_and_position(jd3)
    assert res3["company_name"] is None
    assert res3["position_name"] is None
