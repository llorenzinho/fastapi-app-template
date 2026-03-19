from pydantic import BaseModel


class JwtConfig(BaseModel):
    verify_key: str
    jwt_algorithm: str = "RS256"

    @property
    def safe_verify_key(self) -> str:
        return self.verify_key.strip("\\n\\t\\r")
