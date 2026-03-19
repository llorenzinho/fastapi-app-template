from pydantic import BaseModel


class CreateFooSchema(BaseModel):
    bar: str | None


class FooSchema(BaseModel):
    id: str
    bar: str | None = None
