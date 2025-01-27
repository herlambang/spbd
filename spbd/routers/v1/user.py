from typing import Annotated

from fastapi import APIRouter, Depends

from spbd.core.exceptions import NotFound
from spbd.usecases import UserUseCase

user_router = APIRouter(prefix="/v1/users")


@user_router.get("/{id}")
def get(id: int, usecase: Annotated[UserUseCase, Depends(UserUseCase)]):

    if user := usecase.get(id):
        return user
    else:
        raise NotFound("user not found")
