from fastapi import APIRouter

{% if values.enable_postgres %}
from {{ values.module_name }}.web.routers.foo import foo
{% endif %}

v1 = APIRouter(prefix="/api/v1")

{% if values.enable_postgres %}
v1.include_router(foo)
{% endif %}
