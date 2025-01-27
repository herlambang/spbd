from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, select

from spbd.domain.entities import Phrase
from spbd.infra.db import get_session
from spbd.repositories.common import CRUDRepository


class PhraseRepository(CRUDRepository):

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session: Session = session

    def get(self, id: int) -> Phrase | None:
        stm = select(Phrase).where(Phrase.id == id)
        result = self.session.exec(stm)
        return result.one_or_none()
