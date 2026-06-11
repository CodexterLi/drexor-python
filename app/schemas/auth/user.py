"""
用户 Schema
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, EmailStr, Field

if TYPE_CHECKING:
    from app.models.user import User


class UserCreate(BaseModel):
    """用户创建请求"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名，3-50 个字符")
    email: EmailStr = Field(..., description="用户邮箱地址")
    password: str = Field(..., min_length=8, description="初始登录密码，至少 8 个字符")


class UserResponse(BaseModel):
    """用户信息响应"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="用户 ID")
    username: str = Field(..., description="用户名")
    email: str = Field(..., description="用户邮箱地址")
    is_active: bool = Field(..., description="用户是否启用")
    is_superuser: bool = Field(..., description="是否为超级管理员")
    totp_enabled: bool = Field(..., description="是否已启用 TOTP 两步验证")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    @classmethod
    def from_user(cls, user: "User") -> dict:
        """将用户对象转换为响应字典"""
        return cls.model_validate(user).model_dump()
