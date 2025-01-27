from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int | None = Field(primary_key=True)


class User(BaseModel, table=True):
    __tablename__: str = "users"
    email: str


class Phrase:
    id: int


class Audio:
    id: int
    user: User
    phrase: Phrase
    path: str
