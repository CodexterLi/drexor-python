"""
登录与令牌 Schema
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """登录请求"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="登录密码")
    totp_code: str | None = Field(None, description="TOTP 六位验证码，账号启用两步验证时必填")


class TokenResponse(BaseModel):
    """令牌响应"""

    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="访问令牌过期时间，单位秒")
