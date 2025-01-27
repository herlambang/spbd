from typing import Annotated

from fastapi import APIRouter, Depends

from spbd.core.exceptions import NotFound
from spbd.usecases import AudioUseCase

audio_router = APIRouter(prefix="/v1/audio")


@audio_router.get("/user/{user_id}/phrase/{phrase_id}")
def get(user_id: int, phrase_id: int, usecase: Annotated[AudioUseCase, Depends(AudioUseCase)]):

    if audio := usecase.find_by_user_phrase(user_id, phrase_id):
        return audio
    else:
        raise NotFound("audio not found")
