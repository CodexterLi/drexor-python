"""
钱包登录 Schema
"""

from pydantic import BaseModel, Field


class WalletNonceRequest(BaseModel):
    """钱包 Nonce 请求"""

    wallet_address: str = Field(..., min_length=42, max_length=42, description="EVM 钱包地址")


class WalletLoginRequest(BaseModel):
    """钱包登录请求"""

    wallet_address: str = Field(..., min_length=42, max_length=42, description="EVM 钱包地址")
    signature: str = Field(..., description="钱包对登录消息的签名")
    message: str = Field(..., description="服务端生成的待签名登录消息")


class WalletNonceResponse(BaseModel):
    """钱包 Nonce 响应"""

    nonce: str = Field(..., description="钱包登录随机数")
    message: str = Field(..., description="需要钱包签名的登录消息")


class WalletLoginResponse(BaseModel):
    """钱包登录响应"""

    user_id: int = Field(..., description="登录用户 ID")
    wallet_address: str = Field(..., description="已认证的钱包地址")
