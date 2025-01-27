from sqlmodel import Session, create_engine

from spbd.core.config import settings

engine = create_engine(settings.db_url)


def get_session():
    with Session(engine) as session:
        yield session
