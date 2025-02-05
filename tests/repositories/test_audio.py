from sqlmodel import Session

from spbd.repositories.audio import AudioRepository


def test_get(session_fixture: Session, audios_fixture):
    repo = AudioRepository(session_fixture)
    result = repo.get(1)

    assert result.id == 1
    assert result.user.id == 1
    assert result.phrase.id == 1


def test_get_not_found(session_fixture: Session, audios_fixture):
    repo = AudioRepository(session_fixture)
    result = repo.get(3)

    assert result is None


def test_find_by_user_phrase(session_fixture: Session, audios_fixture):
    repo = AudioRepository(session_fixture)

    result = repo.find_by_user_phrase(1, 1)
    assert result is not None

    result = repo.find_by_user_phrase(1, 2)
    assert result is None


def test_create(session_fixture: Session, audios_fixture):
    repo = AudioRepository(session_fixture)
    result = repo.create(1, 2)

    assert result is not None
    assert result.user.id == 1
    assert result.phrase.id == 2


def test_delete(session_fixture: Session, audios_fixture):
    repo = AudioRepository(session_fixture)
    repo.delete(1)

    assert repo.get(1) is None
