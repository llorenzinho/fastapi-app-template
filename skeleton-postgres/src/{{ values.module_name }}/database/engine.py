from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from {{ values.module_name }}.config.database import DatabaseCfg


def create_db_engine(settings: DatabaseCfg) -> Engine:
    return create_engine(
        url=settings.database_url,
        echo=settings.echo_sql,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_pre_ping=True,
    )


def init_db(engine: Engine) -> None:
    SQLModel.metadata.create_all(engine)


def get_session_sync(engine: Engine) -> Session:
    with Session(engine) as session:
        return session
