from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from app.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String, nullable=False)
    username: str = Column(String, nullable=False)
    registered_at: datetime = Column(TIMESTAMP, default=datetime.utcnow)
    role: str = Column(String, nullable=False, default="user")
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
