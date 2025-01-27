from typing import Annotated

from fastapi import APIRouter, Depends

from spbd.core.exceptions import NotFound
from spbd.usecases import UserUseCase

audio_router = APIRouter(prefix="/v1/audio")


@audio_router.get("/user/{user_id}/phrase/{phrase_id}")
def get(user_id: int, phrase_id: int, usecase: Annotated[UserUseCase, Depends(UserUseCase)]):

    raise NotFound("audio not found")
