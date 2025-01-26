from spbd.repositories import UserRepository
from fastapi import Depends
from typing import Annotated


class UserUseCase:

    def __init__(self, user_repo: Annotated[UserRepository, Depends(UserRepository)]):
        self.user_repo = user_repo

    def get(self, id: int):
        return self.user_repo.get(id)
