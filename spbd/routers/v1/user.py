from typing import Annotated

from fastapi import APIRouter, Depends

from spbd.core.exceptions import HTTPNotFound
from spbd.usecases import UserUseCase

user_router = APIRouter(prefix="/v1/users")


@user_router.get("/{id}")
def get(id: int, usecase: Annotated[UserUseCase, Depends(UserUseCase)]):

    if user := usecase.get(id):
        return user
    else:
        raise HTTPNotFound("user not found")
