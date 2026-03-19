from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator


def strip_quotes(v: str) -> str:
    return v.strip("\"'")


def uuid(v: str) -> str:
    try:
        data = strip_quotes(v)
        UUID(data).is_safe
        return data
    except Exception:
        raise ValueError(f"Given data {v} is not uuid")


StringParam = Annotated[str, BeforeValidator(strip_quotes)]
UUIDParam = Annotated[str, BeforeValidator(uuid)]
