from spbd.repositories.user import UserRepository


def test_get(session_fixture, users_fixture):
    user_repo = UserRepository(session_fixture)
    user = user_repo.get(1)
    assert user is not None


def test_get_not_found(session_fixture):
    user_repo = UserRepository(session_fixture)
    user = user_repo.get(10)
    assert user is None
