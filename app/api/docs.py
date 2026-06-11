"""
API 文档入口

保留 FastAPI 默认 Swagger UI (`/docs`)，额外提供 Scalar API Reference (`/scalar`)。
"""

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from starlette.responses import HTMLResponse

SCALAR_DOCS_PATH = "/scalar"


def register_api_docs(app: FastAPI) -> None:
    """注册额外的 API 文档入口。"""

    @app.get(SCALAR_DOCS_PATH, include_in_schema=False)
    async def scalar_html() -> HTMLResponse:
        return get_scalar_api_reference(
            openapi_url=app.openapi_url,
            title=f"{app.title} API Docs",
            telemetry=False,
        )
