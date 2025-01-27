import io
from pathlib import Path
from typing import BinaryIO

from fastapi import status
from fastapi.testclient import TestClient

from spbd.infra.db import get_session
from spbd.main import app
from spbd.usecases import AudioConverterUseCase


class FakeConverter:

    def convert_from_wav(self, file_path: Path, format="m4a") -> Path:
        return Path(__file__)

    def convert_to_wav(self, content: BinaryIO, target_path: Path) -> Path:
        return Path(__file__)


def test_upload_audio(session_callable_fixture, users_fixture, phrases_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture
    app.dependency_overrides[AudioConverterUseCase] = FakeConverter

    client = TestClient(app)

    fh = io.BytesIO()

    file_payload = {
        "audio_file": ("sample.m4a", fh),
    }

    response = client.post("/v1/audio/user/1/phrase/1", files=file_payload)

    assert response.status_code == status.HTTP_201_CREATED


def test_get_audio(session_callable_fixture, audios_fixture):
    app.dependency_overrides[get_session] = session_callable_fixture
    app.dependency_overrides[AudioConverterUseCase] = FakeConverter

    client = TestClient(app)

    response = client.get("/v1/audio/user/1/phrase/1/m4a")

    assert response.status_code == status.HTTP_200_OK
