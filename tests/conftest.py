# flake8: noqa

import os
from pathlib import Path

storage_dir = Path(__file__).parent / "storage"
os.environ["STORAGE_DIR"] = str(storage_dir)


import shutil

import pytest
from sqlmodel import Session, SQLModel, create_engine, delete
from sqlmodel.pool import StaticPool

from spbd.domain.entities import Audio, Phrase, User


def get_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def add_users(session_fixture: Session):
    session_fixture.add(User(email="abc@gmail.com", id=1))
    session_fixture.add(User(email="bcd@gmail.com", id=2))
    session_fixture.commit()


def add_phrases(session_fixture: Session):
    session_fixture.add(Phrase(id=1, words="play football"))
    session_fixture.add(Phrase(id=2, words="python code based"))
    session_fixture.commit()


def add_audios(session_fixture: Session):
    add_users(session_fixture)
    add_phrases(session_fixture)

    session_fixture.add(Audio(id=1, user_id=1, phrase_id=1, path=str(Path(__file__))))
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


@pytest.fixture()
def phrases_fixture(session_fixture: Session):
    add_phrases(session_fixture)


@pytest.fixture()
def audios_fixture(session_fixture: Session):
    add_audios(session_fixture)


@pytest.fixture()
def sample_file_fixture():
    return storage_dir / "sample.mp3"


@pytest.fixture(autouse=True)
def each_before_after(session_fixture: Session):

    yield

    models = [User, Phrase, Audio]

    for m in models:
        stm = delete(m)
        session_fixture.exec(stm)

    session_fixture.commit()


@pytest.fixture(autouse=True, scope="session")
def session_before_after():
    yield

    # clean up upload test folders
    shutil.rmtree(storage_dir / "audio")
    shutil.rmtree(storage_dir / "cached")
