import pytest
from sqlmodel import Session, SQLModel, create_engine, delete
from sqlmodel.pool import StaticPool

from spbd.domain.entities import User


def get_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def add_users(session_fixture: Session):
    session_fixture.add(User(email="abc@gmail.com", id=1))
    session_fixture.add(User(email="bcd@gmail.com", id=2))
    session_fixture.commit()


@pytest.fixture(scope="session")
def session_fixture():
    yield from get_session()


@pytest.fixture(scope="session")
def session_callable_fixture(session_fixture):
    def get():
        yield session_fixture

    return get


@pytest.fixture()
def users_fixture(session_fixture: Session):
    add_users(session_fixture)


@pytest.fixture(autouse=True)
def before_after(session_fixture: Session):

    yield

    models = [User]

    for m in models:
        stm = delete(m)
        session_fixture.exec(stm)

    session_fixture.commit()
