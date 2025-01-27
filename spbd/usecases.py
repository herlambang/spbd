from typing import Annotated

from fastapi import Depends

from spbd.domain.entities import Audio, User
from spbd.repositories.audio import AudioRepository
from spbd.repositories.user import UserRepository


class UserUseCase:

    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repo = user_repo

    def get(self, id: int) -> User:
        return self.user_repo.get(id)


class AudioUseCase:

    def __init__(self, audio_repo: Annotated[AudioRepository, Depends(AudioRepository)]):
        self.audio_repo = audio_repo

    def find_by_user_phrase(self, user_id: int, phrase_id: int) -> Audio:
        return self.audio_repo.find_by_user_phrase(user_id, phrase_id)
