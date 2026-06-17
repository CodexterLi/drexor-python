"""
对称加密工具

用于加密保存用户托管的 Polymarket API key / secret / passphrase。
基于 Fernet (AES-128-CBC + HMAC, 认证加密); 密钥由配置的密钥材料经 SHA-256 派生。

要点:
- 密钥材料来自配置 (POLYMARKET_ENC_KEY, 为空回退 SECRET_KEY), 不硬编码。
- 记录 encryption_key_version 以支持后续密钥轮换。
- 解密失败映射为稳定异常, 不向上泄露底层 InvalidToken 细节。
"""

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from app.config.settings import settings


class DecryptionError(Exception):
    """密文无法解密 (密钥不匹配或数据损坏)"""


def _derive_fernet_key(material: str) -> bytes:
    """由任意字符串密钥材料派生合法 Fernet 密钥 (32 字节 urlsafe base64)"""
    digest = hashlib.sha256(material.encode()).digest()
    return base64.urlsafe_b64encode(digest)


class CredentialCipher:
    """凭证密文加解密器"""

    def __init__(self, key_material: str | None = None, version: str | None = None):
        material = key_material or settings.POLYMARKET_ENC_KEY or settings.SECRET_KEY
        self._fernet = Fernet(_derive_fernet_key(material))
        self.version = version or settings.POLYMARKET_ENC_KEY_VERSION

    def encrypt(self, plaintext: str) -> str:
        """加密明文, 返回密文字符串"""
        return self._fernet.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext: str) -> str:
        """解密密文; 失败抛 DecryptionError"""
        try:
            return self._fernet.decrypt(ciphertext.encode()).decode()
        except InvalidToken as exc:
            raise DecryptionError("凭证解密失败") from exc
