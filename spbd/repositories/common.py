from abc import ABC, abstractmethod

from spbd.domain.entities import User


class CRUDRepository(ABC):

    @abstractmethod
    def get(self, id: int) -> User:
        pass
