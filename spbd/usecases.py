from typing import Annotated, BinaryIO

from fastapi import Depends

from spbd import utils
from spbd.core.config import settings
from spbd.domain.entities import Audio, User
from spbd.domain.values import AudioDownloadInfo
from spbd.repositories.audio import AudioRepository
from spbd.repositories.phrase import PhraseRepository
from spbd.repositories.user import UserRepository


class UserUseCase:

    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repo = user_repo

    def get(self, id: int) -> User:
        return self.user_repo.get(id)


class PhraseUseCase:

    def __init__(self, phrase_repo: Annotated[PhraseRepository, Depends(PhraseRepository)]):
        self.phrase_repo = phrase_repo

    def get(self, id: int) -> User:
        return self.phrase_repo.get(id)


class AudioUseCase:

    def __init__(self, audio_repo: Annotated[AudioRepository, Depends(AudioRepository)]):
        self.audio_repo = audio_repo

    def find_by_user_phrase(self, user_id: int, phrase_id: int) -> Audio:
        return self.audio_repo.find_by_user_phrase(user_id, phrase_id)

    def get_audio_download_info(self, audio: Audio, format: str = "m4a") -> AudioDownloadInfo:
        audio_path = utils.get_file_fullpath(audio.path)
        out_file_name = f"audio_{audio.user_id}_{audio.phrase_id}.{format}"

        if format == "wav":
            out_path = audio_path
        else:
            out_path = utils.convert_from_wav(audio_path, format=format)

        return AudioDownloadInfo(file_path=out_path, download_name=out_file_name)

    def create(self, user_id: int, phrase_id: int) -> Audio:
        return self.audio_repo.create(user_id, phrase_id)

    def store_file(self, audio: Audio, content: BinaryIO, format="wav"):
        audio_path = settings.storage_path / audio.path
        utils.convert_to_wav(content, audio_path)
