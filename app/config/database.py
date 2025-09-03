from typing import Any, Generator, Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://cwealth:@localhost:54320/todo'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = Base.metadata

def get_session() -> Generator[Session, Any, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

db_session = Annotated[Session, Depends(get_session)]