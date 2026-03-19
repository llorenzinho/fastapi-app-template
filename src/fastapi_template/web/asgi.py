import logging.config
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from sqlmodel import select

from fastapi_template.config.app import cfg
from fastapi_template.core import constants
from fastapi_template.core.exceptions import NotFoundException
from fastapi_template.database.engine import create_db_engine, init_db
from fastapi_template.web.deps import CacheServiceDep, SyncSessionDep
from fastapi_template.web.exceptions import not_found_exception_handler  # type: ignore
from fastapi_template.web.exceptions import (
    generic_exception_handler,
)
from fastapi_template.web.middlewares.logging import RouterLoggingMiddleware
from fastapi_template.web.routers.v1 import v1

logging.config.dictConfig(cfg().log.uvicorn_log_config())


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    root_logger = logging.getLogger("root")
    root_logger.info("APP STARTING")
    root_logger.info(f"{'Running APP:'.ljust(18)} {constants.APP_NAME}")
    root_logger.info(f"{'Service Version:'.ljust(18)} {constants.APP_VERSION}")
    init_db(create_db_engine(cfg().db))  # TODO: remove in prod
    yield
    root_logger.debug("APP STOPPED")


app = FastAPI(
    title=constants.APP_NAME,
    version=constants.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(RouterLoggingMiddleware)  # type: ignore (this actually work)


@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check(session: SyncSessionDep, cache: CacheServiceDep):

    statuses = {"db": False, "cache": False}
    try:
        session.exec(select(1))
        statuses["db"] = True
    except Exception:
        pass

    try:
        statuses["cache"] = cache.ping()
    except Exception:
        pass

    return JSONResponse(
        status_code=(
            status.HTTP_200_OK
            if all(statuses.values())
            else status.HTTP_503_SERVICE_UNAVAILABLE
        ),
        content={k: "OK" if v else "KO" for k, v in statuses.items()},
    )


app.include_router(v1)

app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)  # type: ignore
