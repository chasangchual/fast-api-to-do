from typing import List
from uuid import UUID

from app.config.database import db_session
from app.models.todo import ToDo
from app.setvices.service_base import ServiceBase


class TodoService(ServiceBase):
    def __init__(self, db=None):
        super().__init__(db)

    def find_all(self, session: db_session = None) -> List[ToDo]:
        return self._get_session(session).query(ToDo).all()

    def find_by_id(self, public_id: UUID, session: db_session = None) -> None | ToDo:
        return self._get_session(session).query(ToDo).filter(ToDo.public_id == public_id).first()

    def find_all_by_title(self, title: str, session: db_session = None) -> List[ToDo]:
        return self._get_session(session).query(ToDo).filter(ToDo.title.contains(title))

    def add(self, todo: ToDo, session: db_session = None) -> None | ToDo:
        _session = self._get_session(session)
        _session.add(todo)
        _session.commit()
        _session.refresh(todo)
        return todo

    def update(self, todo: ToDo, session: db_session = None) -> None | ToDo:
        _session = self._get_session(session)
        _session.add(todo)
        _session.commit()
        _session.refresh(todo)
        return todo

    def delete(self, todo: ToDo, session: db_session = None):
        _session = self._get_session(session)
        _session.delete(todo)
        _session.commit()
