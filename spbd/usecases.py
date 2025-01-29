"""
Collection of usecases
This module can/should be split into multiple modules
"""

import logging
import shutil
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

log = logging.getLogger(__name__)


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

    def convert_file_path(self, file_path: Path, to_format="m4a") -> Path:
        """
        Convert from wav to another format.
        This function is using cached mechanism,
        which cache expiration should be handled by another system
        """
        ext = utils.format_to_ext(to_format)

        # Check if file is cached
        cached_path = utils.get_cached_path(file_path, ext=ext)

        if cached_path.is_file():
            log.debug(f"Cached found {str(cached_path)}")
            return cached_path

        # ref: https://github.com/jiaaro/pydub/issues/755
        if to_format == "m4a":
            to_format = "ipod"

        log.debug(f"Converting file path {str(file_path)} to {settings.audio_target_format}")
        audio: AudioSegment = AudioSegment.from_file(file_path, format=settings.audio_target_format)
        audio.export(cached_path, format=to_format)

        return cached_path

    def store_content(self, content: BinaryIO, target_path: Path):
        """
        Convert binary content wav into persistent file
        """
        audio: AudioSegment = AudioSegment.from_file(content)
        audio.export(target_path, format=settings.audio_target_format)
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
        audio_path = self.get_full_path(audio)
        out_file_name = f"{audio_path.stem}.{format}"

        if format == "wav":
            # Return the original wav file just in case wav support in future
            out_path = audio_path
        else:
            # Otherwise convert file from wav to requested format
            out_path = self.converter.convert_file_path(audio_path, format)

        return AudioDownloadInfo(file_path=out_path, download_name=out_file_name)

    def create(self, user_id: int, phrase_id: int) -> Audio:
        """
        Add audio object into db
        """
        return self.audio_repo.create(user_id, phrase_id)

    def store_file(self, audio: Audio, content: BinaryIO, format: str):
        """
        Convert and store audio to wav format
        """
        audio_path = settings.audio_dir / audio.path

        if format == "wav":
            # dont convert if it's wav
            with audio_path.open("wb") as f:
                shutil.copyfileobj(content, f)
        else:
            self.converter.store_content(content, audio_path)

    def cleanup(self, id: int):
        """
        Remove audio record and files
        """
        audio = self.audio_repo.get(id)
        audio_path = settings.storage_dir / audio.path
        audio_path.unlink(missing_ok=True)

        # Clean up all cached file if any
        for fmt in settings.audio_formats:
            ext = utils.format_to_ext(fmt)
            utils.get_cached_path(audio_path, ext).unlink(missing_ok=True)

        # Remove audio data
        self.audio_repo.delete(id)

    def is_valid_format(self, content: BinaryIO, format: str) -> bool:
        if not utils.is_valid_audio_format(format):
            return False

        # todo: inspect and validate file mime type
        return True

    def get_full_path(self, audio: Audio) -> Path:
        return settings.audio_dir / audio.path
