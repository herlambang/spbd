from sqlmodel import Field, Relationship, SQLModel


class BaseModel(SQLModel):
    id: int | None = Field(primary_key=True)


class User(BaseModel, table=True):
    __tablename__: str = "users"
    email: str
    user_audios: list["Audio"] = Relationship(back_populates="users")


class Phrase(BaseModel, table=True):
    __tablename__: str = "phrases"
    words: str
    phrase_audios: list["Audio"] = Relationship(back_populates="phrases")


class Audio(BaseModel, table=True):
    __tablename__: str = "audios"
    user_id: int = Field(default=None, foreign_key="users.id", primary_key=True)
    phrase_id: int = Field(default=None, foreign_key="phrases.id", primary_key=True)
    path: str

    users: User = Relationship(back_populates="user_audios")
    phrases: Phrase = Relationship(back_populates="phrase_audios")
