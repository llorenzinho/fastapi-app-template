from fastapi_template.core.exceptions import NotFoundException
from fastapi_template.core.log import get_logger
from fastapi_template.foo.models import Foo
from fastapi_template.foo.repositories import FooRepo
from fastapi_template.foo.schemas import CreateFooSchema, FooSchema


class FooService:
    def __init__(self, repo: FooRepo) -> None:
        self.repo = repo
        self.log = get_logger(FooService.__name__)

    def create_foo(self, schema: CreateFooSchema) -> FooSchema:
        foo = self.repo.create_foo(schema)
        return FooSchema(id=str(foo.id), bar=foo.bar)

    def get_foo_detail(self, id: str) -> FooSchema:
        foo = self.repo.get_foo(id)
        if not foo:
            raise NotFoundException(Foo, id)

        return FooSchema(id=str(foo.id), bar=foo.bar)

    def list_foo(self) -> list[FooSchema]:
        return [
            FooSchema(
                id=str(foo.id),
                bar=foo.bar,
            )
            for foo in self.repo.list_foo()
        ]

    def delete_foo(self, id: str) -> FooSchema:
        foo = self.repo.delete_foo(id)
        if not foo:
            raise NotFoundException(Foo, id)
        return FooSchema(id=str(foo.id), bar=foo.bar)
