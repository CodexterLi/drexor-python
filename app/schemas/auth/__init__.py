"""
认证相关 Schema
"""

from app.schemas.auth.api_key import (
    ApiKeyResponse,
    CreateApiKeyRequest,
    CreateApiKeyResponse,
)
from app.schemas.auth.login import LoginRequest, TokenResponse
from app.schemas.auth.totp import TOTPSetupResponse, TOTPVerifyRequest
from app.schemas.auth.user import UserCreate, UserResponse
from app.schemas.auth.wallet import (
    WalletLoginRequest,
    WalletLoginResponse,
    WalletNonceRequest,
    WalletNonceResponse,
)

__all__ = [
    "ApiKeyResponse",
    "CreateApiKeyRequest",
    "CreateApiKeyResponse",
    "LoginRequest",
    "TOTPSetupResponse",
    "TOTPVerifyRequest",
    "TokenResponse",
    "UserCreate",
    "UserResponse",
    "WalletLoginRequest",
    "WalletLoginResponse",
    "WalletNonceRequest",
    "WalletNonceResponse",
]
