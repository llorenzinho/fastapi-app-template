import uvicorn

from fastapi_template.config.app import cfg
from fastapi_template.core.enums import LogLevel

if __name__ == "__main__":
    configs = cfg()
    uvicorn.run(
        "fastapi_template.web.asgi:app",
        host=configs.server.host,
        port=configs.server.port,
        reload=configs.log.level is LogLevel.DEBUG,
        forwarded_allow_ips="*",  # TODO: Manage from configs
        proxy_headers=True,  # TODO: Manage from configs
    )
