import logging.config
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
{% if values.enable_postgres %}
from sqlmodel import select
{% endif %}

from {{ values.module_name }}.config.app import cfg
from {{ values.module_name }}.core import constants
from {{ values.module_name }}.core.exceptions import NotFoundException
{% if values.enable_postgres %}
from {{ values.module_name }}.database.engine import create_db_engine, init_db
{% endif %}
{% if values.enable_postgres or values.enable_redis %}
from {{ values.module_name }}.web.deps import (
    {% if values.enable_postgres %}
    SyncSessionDep,
    {% endif %}
    {% if values.enable_redis %}
    CacheServiceDep,
    {% endif %}
)
{% endif %}
from {{ values.module_name }}.web.exceptions import generic_exception_handler
from {{ values.module_name }}.web.exceptions import not_found_exception_handler  # type: ignore
from {{ values.module_name }}.web.middlewares.logging import RouterLoggingMiddleware
from {{ values.module_name }}.web.routers.v1 import v1

logging.config.dictConfig(cfg().log.uvicorn_log_config())


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    root_logger = logging.getLogger("root")
    root_logger.info("APP STARTING")
    root_logger.info(f"{'Running APP:'.ljust(18)} {constants.APP_NAME}")
    root_logger.info(f"{'Service Version:'.ljust(18)} {constants.APP_VERSION}")
    {% if values.enable_postgres %}
    init_db(create_db_engine(cfg().db))  # TODO: remove in prod
    {% endif %}
    yield
    root_logger.debug("APP STOPPED")


app = FastAPI(
    title=constants.APP_NAME,
    version=constants.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(RouterLoggingMiddleware)  # type: ignore


@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check(
    {% if values.enable_postgres %}
    session: SyncSessionDep,
    {% endif %}
    {% if values.enable_redis %}
    cache: CacheServiceDep,
    {% endif %}
):
    {% if values.enable_postgres or values.enable_redis %}
    statuses = {}
    {% if values.enable_postgres %}
    statuses["db"] = False
    try:
        session.exec(select(1))
        statuses["db"] = True
    except Exception:
        pass
    {% endif %}
    {% if values.enable_redis %}
    statuses["cache"] = False
    try:
        statuses["cache"] = cache.ping()
    except Exception:
        pass
    {% endif %}
    return JSONResponse(
        status_code=(
            status.HTTP_200_OK
            if all(statuses.values())
            else status.HTTP_503_SERVICE_UNAVAILABLE
        ),
        content={k: "OK" if v else "KO" for k, v in statuses.items()},
    )
    {% else %}
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "OK"})
    {% endif %}


app.include_router(v1)

app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)  # type: ignore
