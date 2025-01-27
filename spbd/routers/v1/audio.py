import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from spbd import utils
from spbd.core.exceptions import HTTPBadRequest, HTTPError, HTTPNotFound
from spbd.usecases import AudioUseCase

audio_router = APIRouter(prefix="/v1/audio")
log = logging.getLogger(__name__)


@audio_router.get("/user/{user_id}/phrase/{phrase_id}/{format}")
def download_audio(
    user_id: int,
    phrase_id: int,
    usecase: Annotated[AudioUseCase, Depends(AudioUseCase)],
    format: str = "m4a",
):
    format = format.lower()

    if not utils.is_valid_audio_format(format):
        raise HTTPBadRequest(f"{format} is not acceptable format")

    if audio := usecase.find_by_user_phrase(user_id, phrase_id):
        try:
            utils.ensure_file(utils.get_file_fullpath(audio.path))
        except FileNotFoundError as e:
            log.error(e)
            raise HTTPError()

        audio_info = usecase.get_audio_info(audio, format=format)

        return FileResponse(audio_info.file_path, filename=audio_info.download_name)
    else:
        raise HTTPNotFound("audio not found")
