from sqlmodel import Session

from spbd.repositories.phrase import PhraseRepository


def test_get(session_fixture: Session, phrases_fixture):
    repo = PhraseRepository(session_fixture)
    result = repo.get(1)
    assert result.words == "play football"


def test_get_not_found(session_fixture: Session, phrases_fixture):
    repo = PhraseRepository(session_fixture)
    result = repo.get(3)
    assert result is None
