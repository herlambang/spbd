import logging
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import FileResponse

from spbd import utils
from spbd.core.exceptions import EntityNotFound, HTTPBadRequest, HTTPError, HTTPNotFound
from spbd.usecases import AudioUseCase

audio_router = APIRouter(prefix="/v1/audio")
log = logging.getLogger(__name__)


@audio_router.get("/user/{user_id}/phrase/{phrase_id}/{format}")
def download_audio(
    user_id: int,
    phrase_id: int,
    audio_usecase: Annotated[AudioUseCase, Depends(AudioUseCase)],
    format: str = "m4a",
):
    format = format.lower()

    if not utils.is_valid_audio_format(format):
        raise HTTPBadRequest(f"{format} is not acceptable format")

    if audio := audio_usecase.find_by_user_phrase(user_id, phrase_id):
        try:
            utils.ensure_file(audio_usecase.get_full_path(audio))
        except FileNotFoundError as e:
            # If somehow data object exist but file is not there
            log.error(e)
            raise HTTPError()

        audio_info = audio_usecase.get_audio_download_info(audio, format=format)

        return FileResponse(audio_info.file_path, filename=audio_info.download_name)
    else:
        # No audio data
        raise HTTPNotFound("audio not found")


@audio_router.post("/user/{user_id}/phrase/{phrase_id}", status_code=status.HTTP_201_CREATED)
def upload_audio(
    audio_file: UploadFile,
    user_id: int,
    phrase_id: int,
    audio_usecase: Annotated[AudioUseCase, Depends(AudioUseCase)],
):
    format = utils.ext_to_format(Path(audio_file.filename).suffix).lower()

    if not audio_usecase.is_valid_format(audio_file.file, format):
        raise HTTPBadRequest("Not acceptable file format")

    try:
        audio_usecase.validate_user_phrase(user_id, phrase_id)
    except EntityNotFound as e:
        log.error(e)
        raise HTTPNotFound(str(e))

    audio = audio_usecase.find_by_user_phrase(user_id, phrase_id)

    if audio:
        raise HTTPBadRequest("Audio already exists")
    else:
        log.debug(f"audio object not found, create new u:{user_id} p:{phrase_id}")
        audio = audio_usecase.create(user_id, phrase_id)

    try:
        audio_usecase.store_file(audio, audio_file.file, format)
    except Exception as e:
        log.error("Unable to store/convert file")
        log.exception(e)
        audio_usecase.cleanup(audio.id)
        raise HTTPError()
    else:
        audio_file.file.close()

    return audio
