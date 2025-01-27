from spbd.repositories.user import UserRepository
from sqlmodel import Session


def test_get(session_fixture: Session, users_fixture):
    repo = UserRepository(session_fixture)
    result = repo.get(1)

    assert result.email == "abc@gmail.com"


def test_get_not_found(session_fixture: Session, users_fixture):
    repo = UserRepository(session_fixture)
    result = repo.get(3)

    assert result is None
