from typing import List
from uuid import UUID

from app.config.database import db_session
from app.models.todo import Category
from app.setvices.service_base import ServiceBase


class CategoryService(ServiceBase):
    def __init__(self, session=None):
        super().__init__(session)

    def find_all(self, session: db_session = None) -> List[Category]:
        return self._get_session(session).query(Category).all()

    def find_by_id(self, public_id: UUID, session: db_session = None) -> None | Category:
        return self._get_session(session).query(Category).filter(Category.public_id == public_id).first()

    def find_by_name(self, name: str, session: db_session = None) -> None | Category:
        return self._get_session(session).query(Category).filter(Category.name == name).first()

    def add(self, category: Category, session: db_session = None) -> None | Category:
        _session = self._get_session(session)
        _session.add(category)
        _session.commit()
        _session.refresh(category)
        return category

    def update(self, category: Category, session: db_session = None) -> None | Category:
        _session = self._get_session(session)
        _session.add(category)
        _session.commit()
        _session.refresh(category)
        return category

    def delete(self, category: Category, session: db_session = None):
        _session = self._get_session(session)
        _session.delete(category)
        _session.commit()
