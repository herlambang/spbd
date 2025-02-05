import io
from pathlib import Path
from typing import BinaryIO

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from spbd.core.config import settings
from spbd.domain.entities import Audio
from spbd.infra.db import get_session
from spbd.main import app
from spbd.usecases import AudioConverterUseCase


class FakeConverterError:

    def convert_file_path(self, file_path: Path, to_format="m4a") -> Path:
        raise Exception()

    def store_content(self, content: BinaryIO, target_path: Path) -> Path:
        raise Exception()


def test_upload_audio(session_callable_fixture, users_fixture, phrases_fixture, sample_file_fixture: Path):
    app.dependency_overrides[get_session] = session_callable_fixture

    with TestClient(app) as client:
        with sample_file_fixture.open("rb") as fh:
            file_payload = {
                "audio_file": ("sample.mp3", fh),
            }

            response = client.post("/v1/audio/user/1/phrase/1", files=file_payload)

        session: Session = next(session_callable_fixture())
        stm = select(Audio).where(Audio.user_id == 1, Audio.phrase_id == 1).limit(1)
        audio = session.exec(stm).one_or_none()

        # assert object exist in db
        assert audio is not None
        # assert file exist
        assert (settings.audio_dir / audio.path).is_file()
        # assert status code created
        assert response.status_code == status.HTTP_201_CREATED

        session.close()


def test_get_audio(session_callable_fixture, audios_fixture, sample_file_fixture: Path):
    app.dependency_overrides[get_session] = session_callable_fixture

    with TestClient(app) as client:

        # Trigger audio creation
        with sample_file_fixture.open("rb") as fh:
            file_payload = {
                "audio_file": ("sample.mp3", fh),
            }

            client.post("/v1/audio/user/1/phrase/2", files=file_payload)

        response = client.get("/v1/audio/user/1/phrase/2/m4a")
        assert response.status_code == status.HTTP_200_OK
        # assert response is attachment
        assert ".m4a" in response.headers["content-disposition"]
        assert "attachment" in response.headers["content-disposition"]


def test_upload_audio_error(session_callable_fixture, users_fixture, phrases_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture
    app.dependency_overrides[AudioConverterUseCase] = FakeConverterError

    with TestClient(app, raise_server_exceptions=False) as client:
        fh = io.BytesIO()

        file_payload = {
            "audio_file": ("sample.m4a", fh),
        }

        response = client.post("/v1/audio/user/1/phrase/1", files=file_payload)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    session: Session = next(session_callable_fixture())
    stm = select(Audio).where(Audio.user_id == 1, Audio.phrase_id == 1).limit(1)
    audio = session.exec(stm).one_or_none()

    # make sure audio is cleaned up when error occurs
    assert audio is None


def test_upload_audio_not_found(session_callable_fixture, users_fixture, phrases_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture

    with TestClient(app, raise_server_exceptions=False) as client:
        fh = io.BytesIO()

        file_payload = {
            "audio_file": ("sample.m4a", fh),
        }

        response = client.post("/v1/audio/user/10/phrase/10", files=file_payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    session: Session = next(session_callable_fixture())
    stm = select(Audio).where(Audio.user_id == 10, Audio.phrase_id == 10).limit(1)
    audio = session.exec(stm).one_or_none()

    # make sure audio is cleaned up when error occurs
    assert audio is None


def test_get_audio_error(session_callable_fixture, audios_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture
    app.dependency_overrides[AudioConverterUseCase] = FakeConverterError

    with TestClient(app, raise_server_exceptions=False) as client:
        # assert error
        response = client.get("/v1/audio/user/1/phrase/1/m4a")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

        # assert bad param
        response = client.get("/v1/audio/user/1/phrase/1/xxx")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        # assert user not exist
        response = client.get("/v1/audio/user/100/phrase/1/mp3")
        assert response.status_code == status.HTTP_404_NOT_FOUND
