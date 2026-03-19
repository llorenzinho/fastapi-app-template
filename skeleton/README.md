# {{ values.service_name }}

FastAPI microservice generated from the platform template.

## Stack

- **FastAPI** — web framework
- **Uvicorn** — ASGI server
{% if values.enable_postgres %}
- **SQLModel** — ORM (PostgreSQL)
{% endif %}
{% if values.enable_redis %}
- **Redis** — caching
{% endif %}

## Running locally

```bash
docker compose up --build
```

## Configuration

All configuration is driven by environment variables with the prefix `APP_`:

| Variable | Description |
|---|---|
| `APP_SERVER__HOST` | Server host (default: `0.0.0.0`) |
| `APP_SERVER__PORT` | Server port (default: `3000`) |
| `APP_LOG__LEVEL` | Log level (default: `INFO`) |
| `APP_JWT__VERIFY_KEY` | RSA public key for JWT verification |
{% if values.enable_postgres %}
| `APP_DB__USER` | PostgreSQL user |
| `APP_DB__PASSWORD` | PostgreSQL password |
| `APP_DB__HOST` | PostgreSQL host |
| `APP_DB__PORT` | PostgreSQL port |
| `APP_DB__DB` | PostgreSQL database name |
{% endif %}
{% if values.enable_redis %}
| `APP_REDIS__HOST` | Redis host |
| `APP_REDIS__PORT` | Redis port |
{% endif %}
