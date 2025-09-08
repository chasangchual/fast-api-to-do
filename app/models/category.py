import uuid
from typing import Any
from sqlalchemy import Column, Integer, String
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


