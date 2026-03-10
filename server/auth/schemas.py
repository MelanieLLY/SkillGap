from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    skills: List[str] = []

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str
