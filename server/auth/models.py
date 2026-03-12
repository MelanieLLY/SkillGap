from database import Base
from sqlalchemy import JSON, Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    skills = Column(ARRAY(String), server_default="{}")
    roadmap = Column(JSON, nullable=True)
