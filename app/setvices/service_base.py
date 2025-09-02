from sqlalchemy.orm import Session
from app.config.database import db_dependency

class ServiceBase:
    def __init__(self, db=None):
        self.db = db
        self.session = None

    def set_session(self, session: db_dependency):
        self.session = session

    def _get_session(self, session: db_dependency = None) -> Session:
        if session is not None:
            return session
        if self.session is not None:
            return self.session
        raise Exception("Session is not set")