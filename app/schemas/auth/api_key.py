"""
API Key Schema
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateApiKeyRequest(BaseModel):
    """创建 API Key 请求"""

    name: str = Field(..., min_length=1, max_length=50, description="API Key 名称")
    expires_in: int | None = Field(None, description="过期时间，单位秒；不传则永不过期")


class CreateApiKeyResponse(BaseModel):
    """创建 API Key 响应（含明文 secret，仅返回一次）"""

    id: int = Field(..., description="API Key ID")
    name: str = Field(..., description="API Key 名称")
    key: str = Field(..., description="API Key 公钥标识")
    secret: str = Field(..., description="API Key Secret 明文，仅创建时返回一次")
    expires_at: datetime | None = Field(None, description="过期时间，空值表示永不过期")
    created_at: datetime = Field(..., description="创建时间")


class ApiKeyResponse(BaseModel):
    """API Key 列表项"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="API Key ID")
    name: str = Field(..., description="API Key 名称")
    key: str = Field(..., description="API Key 公钥标识")
    is_active: bool = Field(..., description="API Key 是否有效")
    expires_at: datetime | None = Field(None, description="过期时间，空值表示永不过期")
    last_used_at: datetime | None = Field(None, description="最后使用时间")
    created_at: datetime = Field(..., description="创建时间")
