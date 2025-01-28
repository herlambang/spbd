"""
Add fixtures data for demo purpose.
"""

import sys
from pathlib import Path

from sqlmodel import Session, col, select

ROOT_PATH = str(Path(__file__).parents[1])
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

from spbd.domain.entities import Phrase, User  # noqa
from spbd.infra import db  # noqa


def fetch_ids(session: Session, cls):
    stm = select(cls).where(col(cls.id).in_([1, 2])).limit(2)
    result = session.exec(stm)
    return [row.id for row in result.all()]


def main():
    users = [(1, "abc@gmail.com"), (2, "bcd@gmail.com")]
    phrases = [(1, "play football"), (2, "I love python")]

    with Session(db.engine) as session:
        user_ids = fetch_ids(session, User)
        for user in users:
            if user[0] not in user_ids:
                session.add(User(id=user[0], email=user[1]))
                print(f"Add user {user[0]}")

        phrase_ids = fetch_ids(session, Phrase)
        for phrase in phrases:
            if phrase[0] not in phrase_ids:
                session.add(Phrase(id=phrase[0], words=phrase[1]))
                print(f"Add phrase {phrase[0]}")

        session.commit()


if __name__ == "__main__":
    main()
