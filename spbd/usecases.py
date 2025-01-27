from typing import Annotated

from fastapi import Depends

from spbd import utils
from spbd.domain.entities import Audio, User
from spbd.domain.values import AudioDownloadInfo
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

    def get_audio_info(self, audio: Audio, format: str = "m4a") -> AudioDownloadInfo:
        audio_path = utils.get_file_fullpath(audio.path)
        out_path = utils.convert_wav(audio_path, format=format)
        out_file_name = f"audio_{audio.user_id}_{audio.phrase_id}.{format}"

        return AudioDownloadInfo(file_path=out_path, download_name=out_file_name)
