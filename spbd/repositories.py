from abc import ABC, abstractmethod
from sqlmodel import Session, select
from fastapi import Depends

from spbd.domain.entities import User
from spbd.infra.db import get_session
from typing import Annotated


class CRUDRepository(ABC):

    @abstractmethod
    def get(self, id: int) -> User:
        pass


class UserRepository(CRUDRepository):
    session: Session

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session = session

    def get(self, id: int) -> User | None:
        stm = select(User).where(User.id == id)
        result = self.session.exec(stm)
        return result.one_or_none()
