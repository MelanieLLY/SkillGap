from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from services.skill_extractor import match_skills

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "SkillGap API is running"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
    job_description: str
    user_skills: List[str]

@app.post("/api/match")
def match_skills_endpoint(req: MatchRequest):
    result = match_skills(req.job_description, req.user_skills)
    return {"matchResult": result}
