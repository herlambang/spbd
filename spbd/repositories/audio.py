from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, delete, select

from spbd.domain.entities import Audio
from spbd.infra.db import get_session
from spbd.repositories.common import CRUDRepository


class AudioRepository(CRUDRepository):

    def __init__(self, session: Annotated[Session, Depends(get_session)]):
        self.session: Session = session

    def get(self, id: int) -> Audio | None:
        """
        Get audio record by id
        """
        stm = select(Audio).where(Audio.id == id)
        result = self.session.exec(stm)
        return result.one_or_none()

    def find_by_user_phrase(self, user_id: int, phrase_id: int) -> Audio | None:
        """
        Get audio record based on user and phrase id
        """
        stm = select(Audio).where(Audio.user_id == user_id, Audio.phrase_id == phrase_id)
        result = self.session.exec(stm)
        return result.one_or_none()

    def create(self, user_id: int, phrase_id: int) -> Audio:
        """
        Add audio to database
        """
        new_audio_path = Path("wav") / f"audio_{user_id}_{phrase_id}.wav"
        audio = Audio(user_id=user_id, phrase_id=phrase_id, path=str(new_audio_path))
        self.session.add(audio)
        self.session.commit()
        self.session.refresh(audio)
        return audio

    def delete(self, id: int):
        """
        Remove audio from database
        """
        stm = delete(Audio).where(id=id)
        self.session.exec(stm)
        self.session.commit()
