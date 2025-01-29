from pathlib import Path

from spbd.core.config import settings


def format_to_ext(format: str) -> str:
    """
    convert format to extension
    """
    if not format.startswith("."):
        format = "." + format

    return format


def ext_to_format(ext: str) -> str:
    """
    convert extension to format
    """
    return ext.removeprefix(".")


def get_cached_dir():
    """
    Get cache directory
    """
    cached_dir = settings.cached_dir

    if not cached_dir.is_dir():
        cached_dir.mkdir()

    return cached_dir


def get_audio_dir():
    """
    Get wav directory
    """
    audio_dir = settings.audio_dir

    if not audio_dir.is_dir():
        audio_dir.mkdir()

    return audio_dir


def get_cached_path(file_path: Path, ext: str) -> Path:
    """
    Convert file path to cached file path
    wav/my_file.wav ->  cached/my_file.m4a
    """
    file_stem = file_path.stem
    cached_file_name = f"{file_stem}{ext}"
    cached_dir = get_cached_dir()
    return cached_dir / cached_file_name


def ensure_file(file_path: Path):
    """
    Validate file
    - existance
    - todo: other validation
    """
    if not file_path.is_file():
        raise FileNotFoundError(f"File {str(file_path)} does not exist")


def get_file_fullpath(file_path: Path | str):
    """
    Return file full path relative to storage settings
    """
    return settings.storage_dir / file_path


def is_valid_audio_format(format: str) -> bool:
    """
    Check if format defined on settings
    """
    return format in settings.audio_formats
