from sqlalchemy import Boolean, Column, Integer, String, TypeDecorator
from sqlalchemy.dialects.postgresql import ARRAY
from server.database import Base

class ArrayType(TypeDecorator):
    """Fallback mechanism to support postgres ARRAY in sqlite tests"""
    impl = String
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(ARRAY(String))
        return dialect.type_descriptor(String)

    def process_bind_param(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return ','.join(value) if isinstance(value, list) else value
        return ''

    def process_result_value(self, value, dialect):
        if dialect.name == 'postgresql':
            return value
        if value is not None:
            return [x for x in value.split(',') if x]
        return []
from server.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    skills = Column(ArrayType, server_default='{}')
