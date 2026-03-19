import jwt

from fastapi_template.config.jwt import JwtConfig


class JwtService:
    def __init__(self, config: JwtConfig) -> None:
        self.config = config

    def verify(self, key: str) -> str:
        payload = jwt.decode(  # type: ignore
            key, self.config.safe_verify_key, algorithms=[self.config.jwt_algorithm]
        )
        sub = payload.get("sub", None)
        if sub is None:
            raise jwt.InvalidTokenError("Sub is not")

        return sub
