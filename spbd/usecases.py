"""
Collection of usecases
This module can/should be split into multiple modules
"""

from pathlib import Path
from typing import Annotated, BinaryIO

from fastapi import Depends
from pydub import AudioSegment

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
        """
        Get user by id
        """
        return self.user_repo.get(id)


class PhraseUseCase:

    def __init__(self, phrase_repo: Annotated[PhraseRepository, Depends(PhraseRepository)]):
        self.phrase_repo = phrase_repo

    def get(self, id: int) -> User:
        """
        Get phrase by id
        """
        return self.phrase_repo.get(id)


class AudioConverterUseCase:

    def convert_from_wav(self, file_path: Path, format="m4a") -> Path:
        """
        Convert from wav to another format.
        This function is using cached mechanism,
        which cache expiration should be handled by another system
        """
        ext = utils.format_to_ext(format)

        # Check if file is cached
        cached_path = utils.get_cached_path(file_path, ext=ext)

        if cached_path.is_file():
            return cached_path

        # ref: https://github.com/jiaaro/pydub/issues/755
        if format == "m4a":
            format = "ipod"

        audio: AudioSegment = AudioSegment.from_wav(file_path)
        audio.export(cached_path, format=format)

        return cached_path

    def convert_to_wav(self, content: BinaryIO, target_path: Path):
        """
        Convert binary content wav into persistent file
        """
        audio: AudioSegment = AudioSegment.from_file(content)
        audio.export(target_path, format="wav")
        return target_path


class AudioUseCase:

    def __init__(
        self,
        audio_repo: Annotated[AudioRepository, Depends(AudioRepository)],
        converter: Annotated[AudioConverterUseCase, Depends()],
    ):
        self.audio_repo = audio_repo
        self.converter = converter

    def find_by_user_phrase(self, user_id: int, phrase_id: int) -> Audio:
        """
        Get audio record based on user and phrase id
        """
        return self.audio_repo.find_by_user_phrase(user_id, phrase_id)

    def get_audio_download_info(self, audio: Audio, format: str = "m4a") -> AudioDownloadInfo:
        """
        Construct audio information into object
        this information will be use for file downloading.
        """
        audio_path = utils.get_file_fullpath(audio.path)
        out_file_name = f"audio_{audio.user_id}_{audio.phrase_id}.{format}"

        if format == "wav":
            # Return the original wav file just in case wav support in future
            out_path = audio_path
        else:
            # Otherwise convert file from wav to requested format
            out_path = self.converter.convert_from_wav(audio_path, format=format)

        return AudioDownloadInfo(file_path=out_path, download_name=out_file_name)

    def create(self, user_id: int, phrase_id: int) -> Audio:
        """
        Add audio object into db
        """
        return self.audio_repo.create(user_id, phrase_id)

    def store_file(self, audio: Audio, content: BinaryIO):
        """
        Convert and store audio to wav format
        """
        audio_path = settings.storage_path / audio.path
        self.converter.convert_to_wav(content, audio_path)

    def cleanup(self, id: int):
        """
        Remove audio record and file
        """
        audio = self.audio_repo.get(id)
        audio_path = settings.storage_path / audio.path

        if audio_path.is_file():
            audio_path.unlink(missing_ok=True)

        cached_file = utils.get_cached_path(audio_path, ".m4a")  # the only known extension

        if cached_file.is_file():
            cached_file.unlink(missing_ok=True)

        self.audio_repo.delete(id)
