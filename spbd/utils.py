from pathlib import Path
from typing import BinaryIO

from pydub import AudioSegment

from spbd.core.config import settings


def format_to_ext(format: str) -> str:
    if not format.startswith("."):
        format = "." + format

    return format


def ext_to_format(ext: str) -> str:
    return ext.removeprefix(".")


def get_cached_dir():
    cached_dir = settings.storage_path / "cached"

    if not cached_dir.is_dir():
        cached_dir.mkdir()

    return cached_dir


def get_wav_dir():
    wav_dir = settings.storage_path / "wav"

    if not wav_dir.is_dir():
        wav_dir.mkdir()

    return wav_dir


def get_cached_path(file_path: Path, ext: str) -> Path:
    file_stem = file_path.stem
    cached_file_name = f"{file_stem}{ext}"
    cached_dir = get_cached_dir()
    return cached_dir / cached_file_name


def convert_from_wav(file_path: Path, format="m4a") -> Path:
    ext = format_to_ext(format)
    cached_path = get_cached_path(file_path, ext=ext)

    if cached_path.is_file():
        return cached_path

    if format == "m4a":
        format = "ipod"

    audio: AudioSegment = AudioSegment.from_wav(file_path)
    audio.export(cached_path, format=format)

    return cached_path


def ensure_file(file_path: Path):
    if not file_path.is_file():
        raise FileNotFoundError(f"File {str(file_path)} does not exist")


def get_file_fullpath(file_path: Path | str):
    return settings.storage_path / file_path


def is_valid_audio_format(format: str) -> bool:
    return format in settings.audio_formats


def wav_storage_dir() -> Path:
    return settings.storage_path / "wav"


def convert_to_wav(content: BinaryIO, target_path: Path) -> Path:
    audio: AudioSegment = AudioSegment.from_file(content)
    audio.export(target_path, format="wav")

    return target_path
