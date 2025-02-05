from pathlib import Path

import pytest

from spbd import utils
from spbd.core.config import settings


@pytest.mark.parametrize(
    "test_input,expected",
    [("pdf", ".pdf"), (".pdf", ".pdf")],
)
def test_format_to_ext(test_input: str, expected: str):
    assert utils.format_to_ext(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [(".pdf", "pdf"), ("pdf", "pdf")],
)
def test_ext_to_format(test_input: str, expected: str):
    assert utils.ext_to_format(test_input) == expected


def test_get_cached_dir():
    assert utils.get_cached_dir().is_dir()


def test_get_audio_dir():
    assert utils.get_audio_dir().is_dir()


def test_get_cached_path():
    assert utils.get_cached_path(Path("fake_path/fake_file.mp3"), ".m4a") == settings.cached_dir / "fake_file.m4a"


def test_ensure_file(sample_file_fixture: Path):
    assert utils.ensure_file(sample_file_fixture) is None


def test_ensure_file_error():
    with pytest.raises(Exception):
        utils.ensure_file(Path("fake_file.mp3"))


def test_get_file_fullpath():
    assert utils.get_file_fullpath(Path("fake_file.mp3")) == settings.storage_dir / Path("fake_file.mp3")
