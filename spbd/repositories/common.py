from abc import ABC, abstractmethod

from spbd.domain.entities import User


class CRUDRepository(ABC):
    """Base class for CRUD based repository."""

    @abstractmethod
    def get(self, id: int) -> User:
        pass
