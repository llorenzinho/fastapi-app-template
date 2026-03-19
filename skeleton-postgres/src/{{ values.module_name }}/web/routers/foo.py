from fastapi import APIRouter, status

from {{ values.module_name }}.foo.schemas import CreateFooSchema, FooSchema
{% if values.enable_redis %}
from {{ values.module_name }}.web.cache import cached, invalidate_cache
{% endif %}
from {{ values.module_name }}.web.deps import FooServiceDep
from {{ values.module_name }}.web.utils import UUIDParam

foo = APIRouter(prefix="/foo", tags=["foo"])


@foo.post("", status_code=status.HTTP_201_CREATED)
{% if values.enable_redis %}
@invalidate_cache("foo:list")
{% endif %}
def create(svc: FooServiceDep, sch: CreateFooSchema) -> FooSchema:
    return svc.create_foo(sch)


@foo.get(path="/{id:str}")
{% if values.enable_redis %}
@cached(key="foo:{id}", schema=FooSchema, ttl=300)
{% endif %}
def get_foo(foo: FooServiceDep, id: UUIDParam) -> FooSchema:
    return foo.get_foo_detail(id)


@foo.get(path="")
{% if values.enable_redis %}
@cached(key="foo:list", schema=list[FooSchema], ttl=300)
{% endif %}
def list_foo(foo: FooServiceDep) -> list[FooSchema]:
    return foo.list_foo()


@foo.delete("/{id:str}")
{% if values.enable_redis %}
@invalidate_cache("foo:{id}", "foo:list")
{% endif %}
def delete_foo(svc: FooServiceDep, id: UUIDParam) -> FooSchema:
    return svc.delete_foo(id)
