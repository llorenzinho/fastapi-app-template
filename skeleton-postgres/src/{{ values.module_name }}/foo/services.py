from {{ values.module_name }}.core.exceptions import NotFoundException
from {{ values.module_name }}.core.log import get_logger
from {{ values.module_name }}.foo.models import Foo
from {{ values.module_name }}.foo.repositories import FooRepo
from {{ values.module_name }}.foo.schemas import CreateFooSchema, FooSchema


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
