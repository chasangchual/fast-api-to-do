import uuid
from typing import Any
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    todos = relationship('ToDo', back_populates='category')

    def __init__(self, name, public_id: UUID = None, **kw: Any):
        super().__init__(**kw)
        self.public_id = uuid.uuid4() if public_id is None else public_id
        self.name = name

    def __repr__(self):
        return f"<Category(id={self.public_id}, name={self.name})>"


class ToDo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    public_id = Column(UUID(as_uuid=True), unique=True, index=True, default=uuid.uuid4, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(Integer, CheckConstraint('priority >= 1 AND priority <= 5'), server_default='3', nullable=False)
    is_completed = Column(Boolean, server_default='false', nullable=False)
    category = relationship("Category", back_populates="todos")
    owner = relationship("User", back_populates="todos")

    def __init__(self, category: Category, title, description, priority=3, is_completed=False, **kw: Any):
        super().__init__(**kw)
        self.category_id = category.id
        self.title = title
        self.description = description
        self.priority = priority
        self.is_completed = is_completed
