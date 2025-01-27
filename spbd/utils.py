from pathlib import Path

from pydub import AudioSegment

from spbd.core.config import settings


def format_to_ext(format: str) -> str:
    if not format.startswith("."):
        format = "." + format

    return format


def get_cached_dir():
    cached_dir = settings.storage_path / "cached"

    if not cached_dir.is_dir():
        cached_dir.mkdir()

    return cached_dir


def get_cached_path(file_path: Path, ext: str) -> Path:
    file_stem = file_path.stem
    cached_file_name = f"{file_stem}{ext}"
    cached_dir = get_cached_dir()
    return cached_dir / cached_file_name


def convert_wav(file_path: Path, format="m4a") -> Path:
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
