"""
通用路由
"""

from fastapi import APIRouter

from app.core.responses import ok
from app.schemas.common import ApiInfoResponse, HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查"""
    return ok(data={"status": "healthy"})


@router.get("/info", response_model=ApiInfoResponse)
async def api_info():
    """获取 API 信息"""
    return ok(
        data={
            "name": "drexor-python",
            "version": "0.1.0",
            "description": "Drexor Python backend with authentication, database, Redis and WebSocket",
        }
    )
