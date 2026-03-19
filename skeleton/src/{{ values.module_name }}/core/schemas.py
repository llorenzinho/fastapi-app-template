import re

from pydantic import BaseModel, field_validator


class PasswordMixin(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        errors: list[str] = []

        if len(v.encode("utf-8")) > 72:
            errors.append("massimo 72 caratteri")
        if len(v) < 8:
            errors.append("almeno 8 caratteri")
        if not re.search(r"[A-Z]", v):
            errors.append("almeno una lettera maiuscola")
        if not re.search(r"[a-z]", v):
            errors.append("almeno una lettera minuscola")
        if not re.search(r"\d", v):
            errors.append("almeno un numero")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            errors.append("almeno un carattere speciale")

        if errors:
            raise ValueError(f"Password non valida: {', '.join(errors)}")

        return v
