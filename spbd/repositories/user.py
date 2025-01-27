from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from spbd.domain.entities import User
from spbd.infra.db import get_session
from spbd.repositories.common import CRUDRepository


class UserRepository(CRUDRepository):

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session: Session = session

    def get(self, id: int) -> User | None:
        stm = select(User).where(User.id == id)
        result = self.session.exec(stm)
        return result.one_or_none()
