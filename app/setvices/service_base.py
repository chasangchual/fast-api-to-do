from sqlalchemy.orm import Session
from app.config.database import db_session

class ServiceBase:
    def __init__(self, session=None):
        self.session = session

    def set_session(self, session: db_session):
        self.session = session

    def _get_session(self, session: db_session = None) -> Session:
        if session is not None:
            return session
        if self.session is not None:
            return self.session
        raise Exception("Session is not set")