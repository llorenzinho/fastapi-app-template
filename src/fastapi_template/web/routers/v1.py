from fastapi import APIRouter

from fastapi_template.web.routers.foo import foo

v1 = APIRouter(prefix="/api/v1")

v1.include_router(foo)
