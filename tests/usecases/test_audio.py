from pathlib import Path
from unittest import mock

import pytest
from sqlmodel import Session

from spbd.core.config import settings
from spbd.core.exceptions import EntityNotFound
from spbd.domain.entities import Audio
from spbd.repositories.audio import AudioRepository
from spbd.repositories.phrase import PhraseRepository
from spbd.repositories.user import UserRepository
from spbd.usecases import AudioConverterUseCase, AudioUseCase
from spbd.utils import get_audio_dir, get_cached_dir


class FakeConverterError:

    def convert_file_path(self, file_path: Path, to_format="m4a") -> Path:
        raise Exception()


def get_usecase_deps(session_fixture):
    audio_repo = AudioRepository(session_fixture)
    phrase_repo = PhraseRepository(session_fixture)
    user_repo = UserRepository(session_fixture)
    converter = AudioConverterUseCase()
    return audio_repo, phrase_repo, user_repo, converter


def test_find_by_user_phrase(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    assert audio_usecase.find_by_user_phrase(1, 1) is not None


def test_find_by_user_phrase_not_found(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    assert audio_usecase.find_by_user_phrase(1, 100) is None


def test_get_audio_download_info(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    converter.convert_file_path = lambda file_path, to_format: Path()
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    audio = audio_repo.get(1)
    info = audio_usecase.get_audio_download_info(audio, "mp3")
    assert info.download_name.endswith(".mp3")
    assert info.file_path == Path()


def test_get_audio_download_info_wav(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    audio_usecase.get_full_path = lambda audio_obj: Path("fake.wav")
    audio = audio_repo.get(1)
    info = audio_usecase.get_audio_download_info(audio, "wav")
    assert info.download_name.endswith(".wav")
    assert info.file_path.stem == "fake"


def test_create(session_fixture: Session, users_fixture, phrases_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    audio = audio_usecase.create(1, 1)
    assert audio.path.endswith(settings.audio_target_ext)


def test_create_error(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)

    with pytest.raises(EntityNotFound):
        audio_usecase.create(1, 10)


def test_store_file(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    with mock.patch.object(converter, "store_content") as mocked:
        audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
        audio = Audio(path="fake.mp3")
        content = b"123"
        audio_usecase.store_file(audio, content, "mp3")
        mocked.assert_called_once()


def test_store_file_wav(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)

    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    audio = Audio(path="fake.wav")
    content = b"123"

    opener = mock.mock_open()

    def mocked_open(self, *args, **kwargs):
        return opener(self, *args, **kwargs)

    with mock.patch("spbd.usecases.Path.open", mocked_open):
        with mock.patch("spbd.usecases.shutil.copyfileobj") as mock_cp:
            audio_usecase.store_file(audio, content, "wav")
            mock_cp.assert_called_once()


def test_cleanup(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)

    # setup
    audio_dir = get_audio_dir()
    cached_dir = get_cached_dir()
    audio = audio_repo.get(1)
    test_file = audio_dir / audio.path
    test_file_cached = cached_dir / audio.path

    with test_file.open("wb") as fp:
        fp.write(b"123")

    with test_file_cached.open("wb") as fp:
        fp.write(b"123")

    # test
    audio_usecase.cleanup(1)
    assert test_file.is_file() is False
    assert test_file_cached.is_file() is False
    assert audio_repo.get(1) is None


def test_get_full_path(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)
    audio = audio_repo.get(1)
    full_path = audio_usecase.get_full_path(audio)

    assert str(full_path).endswith(audio.path)


def test_validate_user_phrase(session_fixture: Session, audios_fixture):
    audio_repo, user_repo, phrase_repo, converter = get_usecase_deps(session_fixture)
    audio_usecase = AudioUseCase(audio_repo, user_repo, phrase_repo, converter)

    with pytest.raises(EntityNotFound):
        audio_usecase.validate_user_phrase(10, 10)
