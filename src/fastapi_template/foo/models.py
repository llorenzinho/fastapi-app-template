from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Foo(SQLModel, table=True):
    __tablename__ = "foo"  # type: ignore

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)

    bar: str | None = Field(default=None, description="fake data")
