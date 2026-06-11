"""
公共接口响应 Schema
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """健康检查响应"""

    status: str = Field(..., description="服务健康状态")


class ApiInfoResponse(BaseModel):
    """服务信息响应"""

    name: str = Field(..., description="服务名称")
    version: str = Field(..., description="服务版本")
    description: str = Field(..., description="服务描述")
