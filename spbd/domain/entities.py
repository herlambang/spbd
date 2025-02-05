from sqlmodel import Field, Relationship, SQLModel


class BaseModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)


class User(BaseModel, table=True):
    __tablename__: str = "users"
    email: str
    audios: list["Audio"] = Relationship(back_populates="user")


class Phrase(BaseModel, table=True):
    __tablename__: str = "phrases"
    words: str
    audios: list["Audio"] = Relationship(back_populates="phrase")


class Audio(BaseModel, table=True):
    __tablename__: str = "audios"
    user_id: int = Field(default=None, foreign_key="users.id", nullable=False)
    phrase_id: int = Field(default=None, foreign_key="phrases.id", nullable=False)
    path: str

    user: User = Relationship(back_populates="audios")
    phrase: Phrase = Relationship(back_populates="audios")
