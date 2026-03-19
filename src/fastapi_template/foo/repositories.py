from sqlmodel import Session, select

from fastapi_template.core.log import get_logger
from fastapi_template.foo.models import Foo
from fastapi_template.foo.schemas import CreateFooSchema


class FooRepo:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.log = get_logger(FooRepo.__name__)

    def list_foo(self) -> list[Foo]:
        return list(self.session.exec(select(Foo)).all())

    def get_foo(self, id: str) -> Foo | None:
        return self.session.get(Foo, id)

    def create_foo(self, schema: CreateFooSchema) -> Foo:
        user = Foo(bar=schema.bar)

        self.session.add(user)
        self.session.flush()
        return user

    def delete_foo(self, id: str) -> Foo | None:
        foo = self.session.get(Foo, id)
        if not foo:
            return None

        self.session.delete(foo)
        return foo
