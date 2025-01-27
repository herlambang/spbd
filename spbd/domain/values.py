from pathlib import Path

from pydantic import BaseModel


class AudioDownloadInfo(BaseModel):
    file_path: Path
    download_name: str
