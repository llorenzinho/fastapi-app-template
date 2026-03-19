from pydantic import BaseModel


class RedisCfg(BaseModel):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None

    @property
    def redis_url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"
