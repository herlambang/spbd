from spbd.repositories.phrase import PhraseRepository


def test_get(session_fixture, phrases_fixture):
    phrase_repo = PhraseRepository(session_fixture)
    phrase = phrase_repo.get(1)
    assert phrase is not None


def test_get_not_found(session_fixture):
    phrase_repo = PhraseRepository(session_fixture)
    phrase = phrase_repo.get(10)
    assert phrase is None
