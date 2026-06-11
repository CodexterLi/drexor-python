"""
TOTP 两步验证 Schema
"""

from pydantic import BaseModel, Field


class TOTPVerifyRequest(BaseModel):
    """TOTP 验证请求"""

    totp_code: str = Field(..., min_length=6, max_length=6, description="TOTP 六位验证码")


class TOTPSetupResponse(BaseModel):
    """TOTP 设置响应"""

    secret: str = Field(..., description="TOTP 明文密钥，仅用于初始化绑定")
    uri: str = Field(..., description="Authenticator 应用可识别的 otpauth URI")
