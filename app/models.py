from pydantic import BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

# SQLAlchemy Model

def get_lib_version():
    return "0.0.1"

def set_deafult_group():
    return "gac_users"

def set_default_status():
    return "submitted"

def set_default_description():
    return "default"

def set_default_title():
    return "default"

def set_default_email_id():
    return "admin@mmm.ab-inbev.com"

def set_default_country():
    return "global"


class Model(Base):
    __tablename__ = "models"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(50),nullable=False)
    description = Column(String(50),nullable=False)
    status = Column(String(50))
    country = Column(String(50),nullable=False)
    email = Column(String(50),nullable=False)
    user_group = Column(String(50),nullable=False)
    version = Column(String(16),onupdate = get_lib_version(), default=get_lib_version(),nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, title, description, status, country, email, user_group):
        self.title = title
        self.description = description
        self.status = status
        self.user_group = country
        self.country = email
        self.email = user_group

# Pydantic Model

class ModelSchema(BaseModel):
    title: str = None
    description: str = None
    status: str
    country:str = None
    email:str = None
    user_group:str = None

class ModelDB(ModelSchema):
    id: uuid.UUID

    class Config:
        orm_mode = True
