from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from app.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False, unique=True)
    firstname: str = Column(String, nullable=False)
    lastname: str = Column(String, nullable=False)
    city: str = Column(String, nullable=False)
    phone: str = Column(String, nullable=False)
    avatar: str = Column(String, default="DefaultAvatar.png")
    hashed_password: str = Column(String(length=1024), nullable=False)
    created_at: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at: datetime = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
