from fastapi import APIRouter, status

from fastapi_template.foo.schemas import CreateFooSchema, FooSchema
from fastapi_template.web.cache import cached, invalidate_cache
from fastapi_template.web.deps import FooServiceDep
from fastapi_template.web.utils import UUIDParam

foo = APIRouter(prefix="/foo", tags=["foo"])


@foo.post("", status_code=status.HTTP_201_CREATED)
@invalidate_cache("foo:list")
def create(svc: FooServiceDep, sch: CreateFooSchema) -> FooSchema:
    return svc.create_foo(sch)


@foo.get(path="/{id:str}")
@cached(key="foo:{id}", schema=FooSchema, ttl=300)
def get_foo(foo: FooServiceDep, id: UUIDParam) -> FooSchema:
    return foo.get_foo_detail(id)


@foo.get(path="")
@cached(key="foo:list", schema=list[FooSchema], ttl=300)
def list_foo(foo: FooServiceDep) -> list[FooSchema]:
    return foo.list_foo()


@foo.delete("/{id:str}")
@invalidate_cache("foo:{id}", "foo:list")
def delete_foo(svc: FooServiceDep, id: UUIDParam) -> FooSchema:
    return svc.delete_foo(id)
