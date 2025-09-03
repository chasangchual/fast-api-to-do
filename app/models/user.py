import uuid
from typing import Any
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base
from app.models.types import Email

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    first_name = Column(String(64), index=True, nullable=False)
    last_name = Column(String(64), index=True, nullable=False)
    hashed_password = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, server_default='true', nullable=False)
    role = Column(String(16), server_default='USER', nullable=False)
    todos = relationship('Todo', back_populates='owner')
    salts = relationship('Salt', back_populates='user', cascade='all, delete-orphan')


class Salt(Base):
    __tablename__ = "salts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    salt = Column(String, nullable=False)
    user = relationship("User", back_populates="salts")
